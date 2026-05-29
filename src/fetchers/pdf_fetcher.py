"""
PDF/文档解析插件
从孟加拉政府公报、SRO、政策文件中提取结构化情报
支持直接解析 PDF 文件和抓取 PDF 列表页
"""
import os
import re
import io
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse

import requests

from src.fetchers.base import BaseFetcher


class PDFFetcher(BaseFetcher):
    """
    PDF 文档解析抓取器

    支持两种模式：
    1. single_pdf: 直接抓取单个 PDF 文件并解析
    2. list_page: 先抓取 PDF 列表页，再逐个下载解析

    config 参数：
        mode: "single_pdf" | "list_page"
        url: PDF 文件 URL 或列表页 URL
        pdf_link_selector: 列表页中定位 PDF 链接的 CSS 选择器（list_page 模式）
        pdf_link_prefix: PDF 链接补全前缀（可选）
        title_pattern: 从 PDF 文件名或链接文本提取标题的正则（可选）
        max_pdfs: 最多下载解析的 PDF 数量（默认 5）
    """

    source_type = "pdf"

    # 站点预配置
    SITE_PRESETS = {
        "nbr_sro": {
            "name": "NBR - SRO法规",
            "mode": "list_page",
            "url": "https://nbr.gov.bd/sro/eng",
            "pdf_link_selector": "a[href$='.pdf'], a[href*='.pdf?'], a[href*='download']",
            "pdf_link_prefix": "https://nbr.gov.bd",
            "title_pattern": r"SRO[-\s]*(\d+)",
            "max_pdfs": 5,
        },
        "bangladesh_gazette": {
            "name": "Bangladesh Gazette",
            "mode": "list_page",
            "url": "https://www.dpp.gov.bd/upload/",
            "pdf_link_selector": "a[href$='.pdf'], a[href*='.pdf?']",
            "pdf_link_prefix": "",
            "title_pattern": r"(Gazette|Notification|SRO)[-\s]*(\d+)",
            "max_pdfs": 5,
        },
        "bb_policy": {
            "name": "Bangladesh Bank - 政策",
            "mode": "list_page",
            "url": "https://www.bb.org.bd/en/index.php/publication/",
            "pdf_link_selector": "a[href$='.pdf'], a[href*='.pdf?']",
            "pdf_link_prefix": "https://www.bb.org.bd",
            "title_pattern": r"(Policy|Circular|Guideline|Notice|Order)[-\s]*(\d+)",
            "max_pdfs": 5,
        },
        "mof_budget": {
            "name": "财政部 - 预算文件",
            "mode": "list_page",
            "url": "https://mof.gov.bd/en/budget/",
            "pdf_link_selector": "a[href$='.pdf'], a[href*='.pdf?']",
            "pdf_link_prefix": "https://mof.gov.bd",
            "title_pattern": r"(Budget|Report|Statement)[-\s]*(\d+)",
            "max_pdfs": 5,
        },
    }

    # PDF 内容中高价值关键词（命中即提高优先级）
    KEY_TERMS = [
        "SRO", "tariff", "duty", "tax", "exemption", "ban", "restriction",
        "import", "export", "quota", "license", "policy", "regulation",
        "incentive", "subsidy", "investment", "foreign", "joint venture",
        "customs", "bonded", "drawback", "crisis", "shortage",
        "infrastructure", "tender", "bid", "project", "development",
    ]

    def __init__(self):
        self.pdfplumber_available = False
        self._check_deps()

    def _check_deps(self):
        """检查 pdfplumber 是否安装"""
        try:
            import pdfplumber
            self.pdfplumber_available = True
        except ImportError:
            self.pdfplumber_available = False

    def fetch(self, config: dict, hours: int = 24) -> list:
        """抓取并解析 PDF 文档"""
        if not self.pdfplumber_available:
            print(f"  [SKIP] [PDF] pdfplumber 未安装，请执行: pip install pdfplumber")
            return []

        site = config.get("site", "")
        mode = config.get("mode", "single_pdf")
        source_name = config.get("name", "PDFFetcher")

        # 使用站点预设
        if site and site in self.SITE_PRESETS:
            preset = self.SITE_PRESETS[site].copy()
            preset.update({k: v for k, v in config.items() if k != "site" and v})
            config = preset
            mode = config.get("mode", mode)
            source_name = config.get("name", source_name)

        if mode == "single_pdf":
            return self._fetch_single_pdf(config, source_name)
        elif mode == "list_page":
            return self._fetch_list_page(config, source_name, hours)
        else:
            print(f"  [ERROR] [PDF] 未知 mode: {mode}")
            return []

    # ==================== 单 PDF 文件模式 ====================

    def _fetch_single_pdf(self, config: dict, source_name: str) -> list:
        """直接下载并解析单个 PDF"""
        url = config.get("url", "")
        if not url:
            return []

        print(f"  [PDF] 正在下载: {url}")
        text = self._download_and_extract(url)

        if not text:
            return []

        entries = self._text_to_entries(text, url, source_name)
        print(f"  [OK] [PDF] {source_name}: {len(entries)} 条")
        return entries

    # ==================== 列表页模式 ====================

    def _fetch_list_page(self, config: dict, source_name: str, hours: int) -> list:
        """先抓取 PDF 列表页，再逐个下载解析"""
        url = config.get("url", "")
        link_selector = config.get("pdf_link_selector", "a[href$='.pdf']")
        link_prefix = config.get("pdf_link_prefix", "")
        max_pdfs = config.get("max_pdfs", 5)

        if not url:
            return []

        print(f"  [PDF] 扫描列表页: {url}")

        try:
            resp = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                timeout=30,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [ERROR] [PDF] 列表页请求失败: {str(e)[:60]}")
            return []

        # 提取 PDF 链接
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        pdf_links = []

        for a_tag in soup.select(link_selector):
            href = a_tag.get("href", "").strip()
            if not href:
                continue
            if not href.startswith(("http://", "https://")):
                href = urljoin(link_prefix if link_prefix else url, href)
            title = a_tag.get_text(strip=True) or self._extract_title_from_url(href)
            pdf_links.append({"title": title, "url": href})

        # 去重
        seen = set()
        unique_links = []
        for link in pdf_links:
            if link["url"] not in seen:
                seen.add(link["url"])
                unique_links.append(link)

        if not unique_links:
            print(f"  [WARN] [PDF] 未找到 PDF 链接")
            return []

        print(f"  [PDF] 找到 {len(unique_links)} 个 PDF，开始解析 (最多 {max_pdfs} 个)...")

        all_entries = []
        for i, link in enumerate(unique_links[:max_pdfs]):
            print(f"  [PDF] [{i+1}/{min(max_pdfs, len(unique_links))}] {link['title'][:50]}...")
            text = self._download_and_extract(link["url"])
            if text:
                entries = self._text_to_entries(text, link["url"], source_name, link["title"])
                all_entries.extend(entries)

        if all_entries:
            print(f"  [OK] [PDF] {source_name}: 共 {len(all_entries)} 条")
        else:
            print(f"  [WARN] [PDF] {source_name}: 未解析到内容")

        return all_entries

    # ==================== PDF 解析核心 ====================

    def _download_and_extract(self, url: str) -> str:
        """下载 PDF 并提取文本内容"""
        import pdfplumber

        try:
            resp = requests.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "application/pdf,application/x-pdf,*/*",
                },
                timeout=60,
            )
            resp.raise_for_status()

            pdf_file = io.BytesIO(resp.content)
            text_parts = []

            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages[:20]:  # 最多解析 20 页
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text.strip())

            return "\n".join(text_parts)

        except requests.RequestException as e:
            print(f"  [ERROR] [PDF] 下载失败 {url}: {str(e)[:60]}")
        except Exception as e:
            print(f"  [ERROR] [PDF] 解析失败 {url}: {str(e)[:60]}")

        return ""

    def _text_to_entries(self, text: str, source_url: str, source_name: str,
                         doc_title: str = "") -> list:
        """将 PDF 文本拆分为结构化情报条目"""
        entries = []
        now = datetime.utcnow()

        # 提取文档标题（第一行或文件名）
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if not lines:
            return []

        pdf_title = doc_title or self._extract_title_from_url(source_url) or lines[0][:100]

        # 提取日期
        doc_date = now
        date_match = re.search(
            r'(\d{1,2})\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*(\d{4})'
            r'|(\d{4})[年/\-](\d{1,2})[月/\-](\d{1,2})[日]?'
            r'|(\d{1,2})[/](\d{1,2})[/](\d{4})',
            text, re.IGNORECASE
        )
        if date_match:
            groups = date_match.groups()
            try:
                if groups[0] and groups[1] and groups[2]:
                    months = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
                              "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
                    doc_date = datetime(int(groups[2]), months.get(groups[1].lower()[:3], 1), int(groups[0]))
                elif groups[3] and groups[4] and groups[5]:
                    doc_date = datetime(int(groups[3]), int(groups[4]), int(groups[5]))
                elif groups[6] and groups[7] and groups[8]:
                    doc_date = datetime(int(groups[8]), int(groups[6]), int(groups[7]))
            except (ValueError, KeyError):
                pass

        # 检测文档类型
        doc_type = "政府公告"
        if any(kw in text.lower() for kw in ["sro", "statutory regulatory"]):
            doc_type = "SRO法规"
        elif any(kw in text.lower() for kw in ["gazette", "gazete"]):
            doc_type = "官方公报"
        elif any(kw in text.lower() for kw in ["budget", "fiscal"]):
            doc_type = "预算文件"
        elif any(kw in text.lower() for kw in ["circular", "notification"]):
            doc_type = "通知"
        elif any(kw in text.lower() for kw in ["policy", "strategy", "plan"]):
            doc_type = "政策文件"
        elif any(kw in text.lower() for kw in ["tender", "bid", "eoi"]):
            doc_type = "招标公告"

        # 提取关键段落（含高价值关键词的段落）
        key_paragraphs = []
        for line in lines:
            if len(line) < 20:
                continue
            line_lower = line.lower()
            matched_terms = [kw for kw in self.KEY_TERMS if kw.lower() in line_lower]
            if matched_terms:
                key_paragraphs.append({
                    "text": line[:300],
                    "terms": matched_terms,
                    "score": len(matched_terms),
                })

        # 按关键词匹配度排序，取最重要的 3 条
        key_paragraphs.sort(key=lambda x: -x["score"])

        # 构建主条目
        summary_parts = []
        if doc_type:
            summary_parts.append(f"[{doc_type}]")

        if key_paragraphs:
            summary_parts.append(key_paragraphs[0]["text"][:200])

        if not summary_parts:
            # 取文档前几行作为摘要
            content_lines = [l for l in lines if len(l) > 30][:3]
            summary_parts.extend(content_lines)

        summary = " | ".join(summary_parts)

        # 提取关键实体
        entities = self._extract_entities(text)

        # 判断影响/重要性
        importance = self._judge_importance(text, key_paragraphs)

        main_entry = {
            "title": f"[{doc_type}] {pdf_title[:100]}",
            "link": source_url,
            "summary": summary[:500],
            "source": source_name,
            "pub_date": doc_date.strftime("%m-%d %H:%M"),
            "raw_date": doc_date,
        }
        entries.append(main_entry)

        # 如果有多个关键段落，为每个高价值段落生成独立条目
        seen_texts = set()
        for para in key_paragraphs[1:4]:  # 最多额外 3 条
            para_text = para["text"][:150]
            if para_text in seen_texts:
                continue
            seen_texts.add(para_text)

            sub_entry = {
                "title": f"[{doc_type}·要点] {'/'.join(para['terms'][:3])}",
                "link": source_url,
                "summary": para_text[:300],
                "source": source_name,
                "pub_date": doc_date.strftime("%m-%d %H:%M"),
                "raw_date": doc_date,
            }
            entries.append(sub_entry)

        return entries

    def _extract_title_from_url(self, url: str) -> str:
        """从 URL 中提取可读的文件名"""
        parsed = urlparse(url)
        path = parsed.path
        filename = path.split("/")[-1] if path else ""
        # 移除扩展名和 URL 编码
        name = re.sub(r'\.pdf$', '', filename, flags=re.IGNORECASE)
        name = re.sub(r'%20|_|\+', ' ', name)
        return name[:100]

    def _extract_entities(self, text: str) -> list:
        """从文本中提取关键实体"""
        entities = []

        # 金额（美元/塔卡）
        amounts = re.findall(r'[\$TkBDT]?\s*[\d,]+(?:\.\d+)?\s*(?:million|billion|crore|lakh|USD|BDT|Tk)?', text)
        entities.extend([a.strip()[:30] for a in amounts[:5]])

        # 机构名
        orgs = re.findall(r'(?:Ministry|Department|Bangladesh|National|Directorate)\s+of\s+[\w\s]+', text)
        entities.extend([o.strip()[:30] for o in orgs[:3]])

        # SRO 编号
        sros = re.findall(r'SRO\s*[:\-]?\s*\d+[\d/\.]*', text, re.IGNORECASE)
        entities.extend([s.strip() for s in sros[:3]])

        return list(set(entities))[:10]

    def _judge_importance(self, text: str, key_paragraphs: list) -> str:
        """判断文档重要性"""
        high_signals = ["effective immediately", "with immediate effect", "ban", "prohibit",
                        "emergency", "crisis", "urgent", "mandatory", "compulsory"]
        text_lower = text.lower()
        high_count = sum(1 for s in high_signals if s in text_lower)

        if high_count >= 2 or len(key_paragraphs) >= 5:
            return "高"
        elif high_count >= 1 or len(key_paragraphs) >= 2:
            return "中"
        return "低"
