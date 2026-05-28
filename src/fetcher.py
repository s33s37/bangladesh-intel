"""
孟加拉商业情报日报 - 数据采集模块
负责从所有配置源抓取过去24小时的新闻
"""

import feedparser
import requests
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import time
import hashlib


# 所有RSS源配置（从config导入）
from src.config import (
    GENERAL_RSS,
    OFFICIAL_SOURCES,
    TEXTILE_SOURCES,
    INFRA_SOURCES,
    ENERGY_SOURCES,
    SOLAR_SOURCES,
    EV_SOURCES,
    PHARMA_SOURCES,
    ICT_SOURCES,
    SHIPBREAKING_SOURCES,
    FISHERY_SOURCES,
    TRADITIONAL_SOURCES,
    TENDER_SOURCES,
    CHINA_SOURCES,
    GOOGLE_ALERTS_RSS,
)


def build_source_list():
    """
    构建完整的源列表，统一格式
    """
    all_sources = []
    
    # 1. 通用媒体RSS（已经是正确格式）
    all_sources.extend(GENERAL_RSS)
    
    # 2. 其他分类源（需要提取url和name）
    category_sources = [
        ("官方机构", OFFICIAL_SOURCES),
        ("成衣纺织", TEXTILE_SOURCES),
        ("基建", INFRA_SOURCES),
        ("能源", ENERGY_SOURCES),
        ("太阳能", SOLAR_SOURCES),
        ("电动两轮车", EV_SOURCES),
        ("制药", PHARMA_SOURCES),
        ("ICT电商", ICT_SOURCES),
        ("船舶拆解", SHIPBREAKING_SOURCES),
        ("渔业", FISHERY_SOURCES),
        ("传统产业", TRADITIONAL_SOURCES),
        ("招标平台", TENDER_SOURCES),
        ("中国视角", CHINA_SOURCES),
    ]
    
    for category_name, source_list in category_sources:
        for src in source_list:
            if isinstance(src, dict) and "url" in src:
                all_sources.append({
                    "name": f"{src.get('name', 'Unknown')} ({category_name})",
                    "url": src["url"]
                })
    
    # 3. Google Alerts RSS
    for url in GOOGLE_ALERTS_RSS:
        if url and url.strip():
            all_sources.append({
                "name": "Google Alert",
                "url": url.strip()
            })
    
    return all_sources


def fetch_rss(url, source_name, hours=24):
    """
    抓取单个RSS源，只返回过去N小时内的条目
    """
    entries = []
    try:
        feed = feedparser.parse(url, agent="BangladeshIntelBot/1.0")
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        for entry in feed.entries:
            published = entry.get('published', entry.get('updated', entry.get('pubDate', '')))
            if not published:
                continue
            
            try:
                pub_date = date_parser.parse(published)
                if pub_date.tzinfo:
                    pub_date = pub_date.replace(tzinfo=None)
            except Exception:
                continue
            
            if pub_date >= cutoff:
                summary = entry.get('summary', '')
                description = entry.get('description', '')
                content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                text = max([summary, description, content], key=len)
                
                entries.append({
                    "title": entry.get('title', '').strip(),
                    "link": entry.get('link', ''),
                    "summary": text[:1500],
                    "source": source_name,
                    "pub_date": pub_date.strftime("%m-%d %H:%M"),
                    "raw_date": pub_date,
                })
    except Exception as e:
        print(f"[ERROR] RSS fetch failed [{source_name}]: {str(e)[:80]}")
    
    return entries


def fetch_all_sources(hours=24):
    """
    采集所有配置源的新闻
    """
    all_entries = []
    sources = build_source_list()
    
    print(f"[FETCH] Total sources: {len(sources)}")
    
    for i, src in enumerate(sources, 1):
        entries = fetch_rss(src["url"], src["name"], hours)
        if entries:
            print(f"  [{i}/{len(sources)}] {src['name']}: {len(entries)} entries")
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
    
    # 按时间倒序
    unique_entries.sort(key=lambda x: x["raw_date"], reverse=True)
    
    print(f"[FETCH] Total unique entries: {len(unique_entries)} from {len(sources)} sources")
    return unique_entries


def fetch_for_test():
    """
    测试模式：只抓前3个通用源
    """
    print("[TEST MODE] Fetching limited sources...")
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
    print(f"\n--- Sources breakdown ---")
    source_counts = {}
    for r in results:
        src = r["source"]
        source_counts[src] = source_counts.get(src, 0) + 1
    
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"  {src}: {count}")
    
    print(f"\nTotal: {len(results)} entries")
