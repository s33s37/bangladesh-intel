"""
孟加拉商业情报日报 - 数据采集调度器
插件化架构：自动根据配置中的 type 字段调用对应的抓取插件
"""
import time
import hashlib
import re
from datetime import datetime
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.newsapi_fetcher import NewsAPIFetcher
from src.fetchers.scraper_fetcher import WebScraperFetcher
from src.fetchers.api_fetcher import APIFetcher
from src.fetchers.browser_fetcher import BrowserFetcher
from src.fetchers.pdf_fetcher import PDFFetcher
from src.fetchers.social_fetcher import SocialFetcher
from src.config import SOURCES, SECTORS, SECTOR_KEYWORDS

# 插件注册中心：type -> Fetcher 类
FETCHER_REGISTRY = {
    "rss": RSSFetcher,
    "newsapi": NewsAPIFetcher,
    "scraper": WebScraperFetcher,
    "api": APIFetcher,
    "browser": BrowserFetcher,
    "pdf": PDFFetcher,
    "social": SocialFetcher,
}

ITEM_TYPE_BY_SOURCE = {
    "api": "indicator",
    "pdf": "policy_doc",
    "social": "social",
}

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "fbclid", "gclid", "mc_cid", "mc_eid",
}


def normalize_link(link):
    """Normalize links before deduplication."""
    if not link:
        return ""

    parsed = urlparse(link.strip())
    query = parse_qs(parsed.query, keep_blank_values=True)
    query = {k: v for k, v in query.items() if k not in TRACKING_PARAMS}
    normalized_query = urlencode(query, doseq=True)

    return urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower(),
        parsed.path.rstrip("/"),
        "",
        normalized_query,
        "",
    ))


def normalize_title(title):
    """Normalize titles enough to merge syndicated duplicates."""
    title = re.sub(r'\s+', ' ', title or "").strip().lower()
    title = re.sub(r'\s[-|]\s(?:the )?[\w\s.&]+$', '', title)
    return re.sub(r'[^\w\u4e00-\u9fff]', '', title)


def deduplicate_entries(entries):
    """Deduplicate by normalized link, then normalized title."""
    seen_links = set()
    seen_titles = set()
    unique_entries = []

    for entry in entries:
        title_key = normalize_title(entry.get("title", ""))[:60]
        link_key = normalize_link(entry.get("link", ""))

        if link_key:
            link_hash = hashlib.md5(link_key.encode("utf-8")).hexdigest()
            if link_hash in seen_links:
                continue
            seen_links.add(link_hash)

        if title_key:
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

        unique_entries.append(entry)

    return unique_entries


# 全局编译行业关键词正则（加速匹配）
_SECTOR_PATTERNS = None


def _build_sector_patterns():
    """将 SECTOR_KEYWORDS 编译为 (sector_name, compiled_regex) 列表"""
    global _SECTOR_PATTERNS
    if _SECTOR_PATTERNS is not None:
        return _SECTOR_PATTERNS
    patterns = []
    # 中文关键词：直接包含即可匹配
    cn_aliases = {
        "成衣纺织": ["成衣", "纺织", "服装", "面料", "制衣"],
        "基建": ["基建", "桥梁", "港口", "铁路", "公路", "隧道", "地铁"],
        "能源": ["能源", "电力", "天然气", "液化气", "电网", "发电"],
        "太阳能": ["太阳能", "光伏", "新能源"],
        "电动两轮车": ["电动自行车", "电动车", "电摩", "两轮车"],
        "电动汽车": ["电动汽车", "新能源汽车", "充电桩"],
        "制药": ["制药", "医药", "药品", "疫苗"],
        "ICT电商": ["电商", "互联网", "软件", "信息技术", "数字化", "科技"],
        "黄麻": ["黄麻"],
        "皮革": ["皮革", "制鞋"],
        "船舶拆解": ["拆船", "船舶回收"],
        "渔业": ["渔业", "水产", "海鲜", "养虾"],
        "农产品加工": ["农产品", "食品加工", "农业", "粮食"],
        "陶瓷": ["陶瓷", "瓷砖"],
        "家具": ["家具", "木材"],
        "轻工制造": ["轻工", "制造", "五金"],
        "造船": ["造船"],
        "医疗器械": ["医疗器械", "医疗设备"],
        "塑料": ["塑料", "包装"],
        "家电": ["家电", "电器"],
        "数字经济": ["数字经济", "人工智能", "区块链", "智慧城市"],
    }
    for sector in SECTORS:
        keywords = SECTOR_KEYWORDS.get(sector, [])
        # 加入中文别名
        extra = cn_aliases.get(sector, [])
        all_kw = list(set(keywords + extra))
        if all_kw:
            parts = []
            for kw in all_kw:
                escaped = re.escape(kw)
                # 英文短词（字母+数字）加 \b 单词边界，避免 "ai" 匹配 "rain"
                if re.match(r'^[a-zA-Z0-9]+$', kw):
                    parts.append(r'\b' + escaped + r'\b')
                else:
                    parts.append(escaped)
            pattern = re.compile('|'.join(parts), re.IGNORECASE)
            patterns.append((sector, pattern))
    _SECTOR_PATTERNS = patterns
    return patterns


def is_relevant_article(entry):
    """
    关键词预过滤：检查文章标题+摘要是否命中至少一个行业关键词。
    命中率极低的文章（杂讯）直接丢弃，不进 AI 分析以节约成本。
    """
    text = f"{entry.get('title', '')} {entry.get('summary', '')}"
    if len(text.strip()) < 10:
        return False

    patterns = _build_sector_patterns()
    for sector, pattern in patterns:
        if pattern.search(text):
            return True

    # API 结构化数据（世界银行等）总是保留
    if entry.get("item_type") == "indicator":
        return True

    return False


def fetch_all_sources(hours=24):
    """
    采集所有配置源的新闻
    根据每个 source 的 type 字段自动选择对应插件
    """
    all_entries = []
    sources = SOURCES

    rss_count = len([s for s in sources if s.get("type", "rss") == "rss"])
    api_count = len([s for s in sources if s.get("type") == "newsapi"])
    api_data_count = len([s for s in sources if s.get("type") == "api"])
    browser_count = len([s for s in sources if s.get("type") == "browser"])
    pdf_count = len([s for s in sources if s.get("type") == "pdf"])
    social_count = len([s for s in sources if s.get("type") == "social"])
    scraper_count = len([s for s in sources if s.get("type") == "scraper"])
    print(f"[FETCH] 总数据源: {len(sources)} 个 (RSS:{rss_count} NewsAPI:{api_count} DataAPI:{api_data_count} Browser:{browser_count} PDF:{pdf_count} Social:{social_count} Scraper:{scraper_count})")

    for i, src in enumerate(sources, 1):
        source_type = src.get("type", "rss")
        source_name = src.get("name", "Unknown")
        fetcher_class = FETCHER_REGISTRY.get(source_type)

        if not fetcher_class:
            print(f"  [{i}/{len(sources)}] [{source_name}] 未知类型 '{source_type}'，跳过")
            continue

        fetcher = fetcher_class()
        try:
            entries = fetcher.fetch(src, hours)
            for entry in entries:
                entry.setdefault("item_type", ITEM_TYPE_BY_SOURCE.get(source_type, "news"))
                entry.setdefault("source_type", source_type)
            if entries:
                print(f"  [{i}/{len(sources)}] [{source_name}]: {len(entries)} 条")
            else:
                print(f"  [{i}/{len(sources)}] [{source_name}]: 0 条")
            all_entries.extend(entries)
        except Exception as e:
            print(f"  [{i}/{len(sources)}] [{source_name}] 异常: {str(e)[:60]}")

        # 礼貌延迟，避免触发限流
        time.sleep(0.3)

    unique_entries = deduplicate_entries(all_entries)

    # 行业关键词预过滤：丢弃不相关的杂讯
    before_filter = len(unique_entries)
    unique_entries = [e for e in unique_entries if is_relevant_article(e)]
    filtered = before_filter - len(unique_entries)
    if filtered:
        print(f"[FETCH] 行业关键词过滤: 丢弃 {filtered} 条不相关新闻")

    # 按时间倒序排列
    unique_entries.sort(key=lambda x: x.get("raw_date", datetime.utcnow()), reverse=True)

    # 限制最大条目数（防止报告过于臃肿）
    max_items = 80
    if len(unique_entries) > max_items:
        print(f"[FETCH] 超过上限{max_items}条，截取最新{max_items}条")
        unique_entries = unique_entries[:max_items]

    print(f"[FETCH] 去重+过滤后总计: {len(unique_entries)} 条")
    return unique_entries


def fetch_for_test():
    """
    测试模式：只抓取前 3 个 RSS 源
    """
    print("[TEST MODE] 抓取前 3 个 RSS 源...")
    rss_sources = [s for s in SOURCES if s.get("type", "rss") == "rss"][:3]
    fetcher = RSSFetcher()
    entries = []
    for src in rss_sources:
        e = fetcher.fetch(src, hours=48)
        if e:
            for entry in e:
                entry.setdefault("item_type", "news")
                entry.setdefault("source_type", "rss")
            entries.extend(e)
        time.sleep(0.5)

    unique = deduplicate_entries(entries)

    unique.sort(key=lambda x: x.get("raw_date", datetime.utcnow()), reverse=True)
    print(f"[TEST] 去重后: {len(unique)} 条")
    return unique[:40]


if __name__ == "__main__":
    results = fetch_all_sources(hours=24)
    source_counts = {}
    for r in results:
        src = r["source"]
        source_counts[src] = source_counts.get(src, 0) + 1

    print(f"\n--- 来源 Top10 ---")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {src}: {count}")
    print(f"\n总计: {len(results)} 条")
