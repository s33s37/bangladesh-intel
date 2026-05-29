"""
孟加拉商业情报日报 - 数据采集模块
"""

import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import time
import hashlib

from src.config import GENERAL_RSS, GOOGLE_NEWS_RSS, GOOGLE_ALERTS_RSS


def fetch_rss(url, source_name, hours=24):
    """
    抓取单个RSS源，只返回过去N小时内的条目
    """
    entries = []
    try:
        feed = feedparser.parse(url, agent="BangladeshIntelBot/1.0")
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        for entry in feed.entries:
            # 尝试多种时间字段
            published = (entry.get('published') or 
                        entry.get('updated') or 
                        entry.get('pubDate') or 
                        entry.get('date') or
                        '')
            if not published:
                # 没有时间戳，但保留条目（给AI处理）
                pub_date = datetime.utcnow()
            else:
                try:
                    pub_date = date_parser.parse(published)
                    if pub_date.tzinfo:
                        pub_date = pub_date.replace(tzinfo=None)
                except Exception:
                    # 解析失败，用当前时间
                    pub_date = datetime.utcnow()
            
            # 放宽时间限制：保留过去72小时的内容（避免时区问题）
            # 统一转换为 UTC 无时区时间进行比较
            cutoff = datetime.utcnow() - timedelta(hours=72)
            compare_date = pub_date.replace(tzinfo=None) if pub_date.tzinfo else pub_date
            if compare_date >= cutoff:
                summary = BeautifulSoup(entry.get('summary', ''), "html.parser").get_text(strip=True)
                description = BeautifulSoup(entry.get('description', ''), "html.parser").get_text(strip=True)
                content_val = ''
                if entry.get('content') and isinstance(entry.get('content'), list) and len(entry.get('content')) > 0:
                    content_val = entry.get('content')[0].get('value', '')
                text = max([summary, description, content_val], key=len)
                
                entries.append({
                    "title": BeautifulSoup(entry.get('title', ''), "html.parser").get_text(strip=True),
                    "link": entry.get('link', ''),
                    "summary": text[:1500],
                    "source": source_name,
                    "pub_date": pub_date.strftime("%m-%d %H:%M"),
                    "raw_date": pub_date,
                })
    except Exception as e:
        print(f"[ERROR] [{source_name}] {str(e)[:60]}")
    
    return entries


def fetch_all_sources(hours=24):
    """
    采集所有配置源的新闻
    """
    all_entries = []
    
    # 合并所有源
    sources = GENERAL_RSS.copy()
    sources.extend(GOOGLE_NEWS_RSS)
    
    for url in GOOGLE_ALERTS_RSS:
        if url and url.strip():
            sources.append({"name": "Google Alert", "url": url.strip()})
    
    print(f"[FETCH] Total sources: {len(sources)}")
    
    for i, src in enumerate(sources, 1):
        entries = fetch_rss(src["url"], src["name"], hours)
        if entries:
            print(f"  [{i}/{len(sources)}] {src['name']}: {len(entries)} entries")
        else:
            print(f"  [{i}/{len(sources)}] {src['name']}: 0 entries")
        all_entries.extend(entries)
        time.sleep(0.3)
    
    # 去重
    seen_links = set()
    unique_entries = []
    for e in all_entries:
        link_hash = hashlib.md5(e["link"].encode()).hexdigest()
        if link_hash not in seen_links:
            seen_links.add(link_hash)
            unique_entries.append(e)
    
    unique_entries.sort(key=lambda x: x["raw_date"], reverse=True)
    print(f"[FETCH] Total unique entries: {len(unique_entries)}")
    return unique_entries


def fetch_for_test():
    """
    测试模式：只抓前3个通用源
    """
    print("[TEST MODE] Fetching first 3 sources...")
    entries = []
    for src in GENERAL_RSS[:3]:
        e = fetch_rss(src["url"], src["name"], hours=48)
        if e:
            entries.extend(e)
        time.sleep(0.5)
    
    seen = set()
    unique = []
    for e in entries:
        h = hashlib.md5(e["link"].encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(e)
    
    unique.sort(key=lambda x: x["raw_date"], reverse=True)
    print(f"[TEST] Fetched {len(unique)} unique entries")
    return unique


if __name__ == "__main__":
    results = fetch_all_sources(hours=24)
    source_counts = {}
    for r in results:
        src = r["source"]
        source_counts[src] = source_counts.get(src, 0) + 1
    
    print(f"\n--- Top sources ---")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {src}: {count}")
    print(f"\nTotal: {len(results)} entries")
