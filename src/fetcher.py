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
from src.config import SOURCES

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

    # 按时间倒序排列
    unique_entries.sort(key=lambda x: x.get("raw_date", datetime.utcnow()), reverse=True)

    # 限制最大条目数（防止报告过于臃肿）
    max_items = 80
    if len(unique_entries) > max_items:
        print(f"[FETCH] 超过上限{max_items}条，截取最新{max_items}条")
        unique_entries = unique_entries[:max_items]

    print(f"[FETCH] 去重后总计: {len(unique_entries)} 条")
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
