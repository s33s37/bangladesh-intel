"""
孟加拉商业情报日报 - 数据采集调度器
插件化架构：自动根据配置中的 type 字段调用对应的抓取插件
"""
import time
import hashlib
from datetime import datetime

from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.newsapi_fetcher import NewsAPIFetcher
from src.fetchers.scraper_fetcher import WebScraperFetcher
from src.fetchers.api_fetcher import APIFetcher
from src.fetchers.browser_fetcher import BrowserFetcher
from src.config import SOURCES

# 插件注册中心：type -> Fetcher 类
FETCHER_REGISTRY = {
    "rss": RSSFetcher,
    "newsapi": NewsAPIFetcher,
    "scraper": WebScraperFetcher,
    "api": APIFetcher,
    "browser": BrowserFetcher,
}


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
    scraper_count = len([s for s in sources if s.get("type") == "scraper"])
    print(f"[FETCH] 总数据源: {len(sources)} 个 (RSS:{rss_count} NewsAPI:{api_count} DataAPI:{api_data_count} Browser:{browser_count} Scraper:{scraper_count})")

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
            if entries:
                print(f"  [{i}/{len(sources)}] [{source_name}]: {len(entries)} 条")
            else:
                print(f"  [{i}/{len(sources)}] [{source_name}]: 0 条")
            all_entries.extend(entries)
        except Exception as e:
            print(f"  [{i}/{len(sources)}] [{source_name}] 异常: {str(e)[:60]}")

        # 礼貌延迟，避免触发限流
        time.sleep(0.3)

    # 去重：基于链接 MD5
    seen_links = set()
    unique_entries = []
    for e in all_entries:
        link_hash = hashlib.md5(e["link"].encode()).hexdigest()
        if link_hash not in seen_links:
            seen_links.add(link_hash)
            unique_entries.append(e)

    # 按时间倒序排列
    unique_entries.sort(key=lambda x: x.get("raw_date", datetime.utcnow()), reverse=True)
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
            entries.extend(e)
        time.sleep(0.5)

    # 去重
    seen = set()
    unique = []
    for e in entries:
        h = hashlib.md5(e["link"].encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(e)

    unique.sort(key=lambda x: x.get("raw_date", datetime.utcnow()), reverse=True)
    print(f"[TEST] 去重后: {len(unique)} 条")
    return unique


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
