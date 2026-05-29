"""
Headless 浏览器抓取插件
使用 Playwright 突破 Cloudflare 等 JS 挑战防护
适用于孟加拉政府网站（gov.bd 域名）等 requests 无法直接抓取的站点

依赖安装：playwright install chromium
"""
import os
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin

from src.fetchers.base import BaseFetcher


class BrowserFetcher(BaseFetcher):
    """
    Headless 浏览器抓取器
    通过 Playwright 启动 Chromium，绕过 Cloudflare 等 JS 挑战

    config 参数：
        url: 目标页面 URL
        item_selector: 每条新闻的容器 CSS 选择器
        title_selector: 标题选择器（相对于 item_selector）
        link_selector: 链接选择器（相对于 item_selector）
        summary_selector: 摘要选择器（可选）
        date_selector: 日期选择器（可选）
        wait_selector: 等待页面加载完成的选择器（可选）
        scroll: 是否滚动页面加载更多内容（默认 true）
        timeout: 页面加载超时时间（毫秒，默认 60000）
    """

    source_type = "browser"

    # 站点预配置：针对已知目标网站优化
    SITE_PRESETS = {
        "beza": {
            "url": "https://www.beza.gov.bd/",
            "item_selector": ".news-item, .post-item, .listing-item, article",
            "title_selector": "h2 a, h3 a, .title a, .post-title a",
            "link_selector": "a[href]",
            "summary_selector": ".description, .summary, p",
            "date_selector": ".date, .post-date, time",
            "wait_selector": "body.ready, #content, main",
            "scroll": True,
        },
        "nbr": {
            "url": "https://www.nbr.gov.bd/",
            "item_selector": ".news-item, .notice-item, .content-item, article, .single-item",
            "title_selector": "h2 a, h3 a, .title a, a strong",
            "link_selector": "a[href]",
            "summary_selector": ".description, p",
            "date_selector": ".date, time",
            "wait_selector": "#content, main, .main-content",
            "scroll": False,
        },
        "bida": {
            "url": "https://www.bida.gov.bd/",
            "item_selector": ".views-row, .news-item, article, .node",
            "title_selector": ".views-field-title a, h2 a, h3 a, .title a",
            "link_selector": "a[href]",
            "summary_selector": ".views-field-body p, .summary",
            "date_selector": ".views-field-created, .date, time",
            "wait_selector": ".content, main, #page",
            "scroll": True,
        },
        "bb": {
            "url": "https://www.bb.org.bd/",
            "item_selector": ".notice, .news, .listing-item, tr, .item",
            "title_selector": "a, td a, .title a",
            "link_selector": "a[href]",
            "summary_selector": "",
            "date_selector": ".date, td.date, time, td:first-child",
            "wait_selector": "body, #content, .content",
            "scroll": False,
        },
    }

    # 判断 Cloudflare 挑战页面的关键词
    CLOUDFLARE_KEYWORDS = [
        "Just a moment...",
        "Checking your browser",
        "Performing security verification",
        "Verifying you are human",
        "cloudflare",
        "__cf_chl_tk",
    ]

    def __init__(self):
        self.playwright_available = False
        self._check_playwright()

    def _check_playwright(self):
        """检查 Playwright 是否安装"""
        try:
            import playwright
            self.playwright_available = True
        except ImportError:
            self.playwright_available = False

    def fetch(self, config: dict, hours: int = 24) -> list:
        """使用 Headless 浏览器抓取页面"""
        if not self.playwright_available:
            print(f"  [SKIP] [Browser] playwright 未安装，请执行: pip install playwright && playwright install chromium")
            return []

        site = config.get("site", "")
        url = config.get("url", "")
        source_name = config.get("name", "BrowserFetcher")

        # 如果指定了 site 预设，使用预设配置并覆盖自定义项
        if site and site in self.SITE_PRESETS:
            preset = self.SITE_PRESETS[site].copy()
            preset.update({k: v for k, v in config.items() if k != "site" and v})
            config = preset
            url = config.get("url", url) or preset["url"]

        if not url:
            print(f"  [ERROR] [Browser] 未指定 url 或 site")
            return []

        try:
            return self._fetch_with_playwright(config, hours, source_name)
        except Exception as e:
            print(f"  [ERROR] [Browser] {source_name}: {str(e)[:80]}")
            return []

    def _fetch_with_playwright(self, config: dict, hours: int, source_name: str) -> list:
        """启动 Playwright 抓取页面"""
        from playwright.sync_api import sync_playwright

        url = config["url"]
        item_selector = config.get("item_selector", "a[href]")
        title_selector = config.get("title_selector", "")
        link_selector = config.get("link_selector", "a[href]")
        summary_selector = config.get("summary_selector", "")
        date_selector = config.get("date_selector", "")
        wait_selector = config.get("wait_selector", "")
        should_scroll = config.get("scroll", True)
        timeout = config.get("timeout", 60000)

        entries = []

        with sync_playwright() as p:
            # 启动浏览器（stealth 模式）
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                ],
            )

            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/142.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1920, "height": 1080},
                locale="en-US",
                timezone_id="Asia/Dhaka",
            )

            # 注入 stealth 脚本：隐藏自动化特征
            context.add_init_script("""
                // 隐藏 webdriver 特征
                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                // 模拟正常浏览器插件
                Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
                // 模拟正常语言列表
                Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en', 'bn'] });
                // 覆盖 chrome 对象
                window.chrome = { runtime: {} };
            """)

            page = context.new_page()

            try:
                # 导航到目标页面
                print(f"  [Browser] 正在加载 {url} ...")
                page.goto(url, wait_until="domcontentloaded", timeout=timeout)

                # 等待页面稳定
                page.wait_for_timeout(3000)

                # 检查是否触发了 Cloudflare 挑战
                page_title = page.title()
                is_cloudflare = any(kw.lower() in page_title.lower() for kw in self.CLOUDFLARE_KEYWORDS)

                if is_cloudflare:
                    # 等待 Cloudflare 挑战完成（最多 30 秒）
                    print(f"  [Browser] 检测到 Cloudflare 挑战，等待通过...")
                    try:
                        page.wait_for_timeout(5000)
                        for _ in range(25):  # 最多等 25 秒
                            page.wait_for_timeout(1000)
                            new_title = page.title()
                            if not any(kw.lower() in new_title.lower() for kw in self.CLOUDFLARE_KEYWORDS):
                                print(f"  [Browser] Cloudflare 挑战通过")
                                is_cloudflare = False
                                break
                    except Exception:
                        pass

                if is_cloudflare:
                    print(f"  [WARN] [Browser] {source_name}: Cloudflare 挑战未通过，可能无数据")
                    # 继续尝试，部分站点可能仍有内容

                # 等待内容选择器出现
                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=15000)
                    except Exception:
                        pass

                # 滚动加载更多内容
                if should_scroll:
                    for _ in range(3):
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        page.wait_for_timeout(1500)

                # 提取文章条目
                items = page.query_selector_all(item_selector)
                print(f"  [Browser] 找到 {len(items)} 条候选内容")

                now = datetime.utcnow()
                for item in items[:20]:  # 最多取 20 条
                    try:
                        entry = self._extract_entry(
                            page, item, title_selector, link_selector,
                            summary_selector, date_selector, url, source_name, now
                        )
                        if entry:
                            entries.append(entry)
                    except Exception:
                        continue

            except Exception as e:
                print(f"  [ERROR] [Browser] 页面处理异常: {str(e)[:60]}")

            finally:
                browser.close()

        if entries:
            print(f"  [OK] [Browser] {source_name}: {len(entries)} 条")
        else:
            print(f"  [WARN] [Browser] {source_name}: 0 条（可能被 Cloudflare 拦截）")

        return entries

    def _extract_entry(self, page, item, title_sel, link_sel, summary_sel, date_sel,
                       base_url, source_name, now):
        """从页面元素中提取单条新闻"""
        title_el = None
        link_el = None

        # 提取标题
        if title_sel:
            title_el = item.query_selector(title_sel)
        if not title_el:
            # 尝试查找任何 a 标签
            title_el = item.query_selector("a")

        if not title_el:
            return None

        title = title_el.inner_text().strip()
        if not title or len(title) < 5:
            return None

        # 提取链接
        if link_sel:
            link_el = item.query_selector(link_sel)
        if not link_el:
            link_el = title_el if title_el.get_attribute("href") else item.query_selector("a[href]")

        href = ""
        if link_el:
            href = link_el.get_attribute("href") or ""
            if href and not href.startswith(("http://", "https://")):
                href = urljoin(base_url, href)

        # 提取摘要
        summary = ""
        if summary_sel:
            sum_el = item.query_selector(summary_sel)
            if sum_el:
                summary = sum_el.inner_text().strip()[:300]

        # 提取日期
        pub_date = now
        if date_sel:
            date_el = item.query_selector(date_sel)
            if date_el:
                date_text = date_el.inner_text().strip()
                parsed = self._parse_date(date_text)
                if parsed:
                    pub_date = parsed

        return {
            "title": title[:200],
            "link": href[:500],
            "summary": summary[:500],
            "source": source_name,
            "pub_date": pub_date.strftime("%m-%d %H:%M"),
            "raw_date": pub_date,
        }

    def _parse_date(self, date_str: str) -> datetime | None:
        """尝试解析多种日期格式"""
        now = datetime.utcnow()
        date_str = re.sub(r'\s+', ' ', date_str.strip())

        patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',
            r'(\d{2})/(\d{2})/(\d{4})',
            r'(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{4})',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})',
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{1,2})月(\d{1,2})日',
        ]

        months = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
        }

        for pattern in patterns:
            m = re.search(pattern, date_str, re.IGNORECASE)
            if m:
                try:
                    groups = m.groups()
                    if len(groups) == 3:
                        if groups[1].isdigit():
                            y, mo, d = int(groups[0]), int(groups[1]), int(groups[2])
                        else:
                            mo = months.get(groups[1].lower()[:3], 1)
                            d, y = int(groups[0]), int(groups[2])
                        return datetime(y, mo, d)
                    elif len(groups) == 2:
                        mo, d = int(groups[0]), int(groups[1])
                        return datetime(now.year, mo, d)
                except (ValueError, KeyError):
                    continue

        return None
