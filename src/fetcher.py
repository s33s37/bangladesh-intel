"""
孟加拉商业情报日报 - 数据采集模块
负责从RSS和网页抓取过去24小时的新闻
"""

import feedparser
import requests
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import time
import hashlib
from src.config import GENERAL_RSS, GOOGLE_ALERTS_RSS


def fetch_rss(url, source_name, hours=24):
    """
    抓取单个RSS源，只返回过去N小时内的条目
    """
    entries = []
    try:
        # 设置User-Agent避免被封
        feed = feedparser.parse(url, agent="BangladeshIntelBot/1.0")
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        
        for entry in feed.entries:
            # 提取发布时间
            published = entry.get('published', entry.get('updated', entry.get('pubDate', '')))
            if not published:
                continue
            
            try:
                pub_date = date_parser.parse(published)
                if pub_date.tzinfo:
                    pub_date = pub_date.replace(tzinfo=None)
            except Exception:
                continue
            
            # 只保留 cutoff 之后的条目
            if pub_date >= cutoff:
                # 提取摘要（不同RSS字段名不同）
                summary = entry.get('summary', '')
                description = entry.get('description', '')
                content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                
                # 优先使用最长的文本作为内容
                text = max([summary, description, content], key=len)
                
                entries.append({
                    "title": entry.get('title', '').strip(),
                    "link": entry.get('link', ''),
                    "summary": text[:1500],  # 限制长度，避免超长
                    "source": source_name,
                    "pub_date": pub_date.strftime("%m-%d %H:%M"),
                    "raw_date": pub_date,
                })
    except Exception as e:
        print(f"[ERROR] RSS fetch failed [{source_name}]: {str(e)[:80]}")
    
    return entries


def fetch_web_page(url, source_name):
    """
    简单网页抓取（备用，用于无RSS的源）
    注意：这个版本较基础，复杂网页需要后续升级
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0"
        }
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return [{
                "title": f"Web page from {source_name}",
                "link": url,
                "summary": resp.text[:2000],
                "source": source_name,
                "pub_date": datetime.utcnow().strftime("%m-%d %H:%M"),
                "raw_date": datetime.utcnow(),
            }]
    except Exception as e:
        print(f"[ERROR] Web fetch failed [{source_name}]: {str(e)[:80]}")
    return []


def fetch_all_sources(hours=24):
    """
    采集所有配置源的新闻
    """
    all_entries = []
    
    # 1. 抓取通用媒体RSS
    print("[FETCH] General media RSS sources...")
    for src in GENERAL_RSS:
        entries = fetch_rss(src["url"], src["name"], hours)
        all_entries.extend(entries)
        if entries:
            print(f"  + {src['name']}: {len(entries)} entries")
        time.sleep(0.5)  # 礼貌延迟
    
    # 2. 抓取Google Alerts RSS
    print("[FETCH] Google Alerts RSS sources...")
    for url in GOOGLE_ALERTS_RSS:
        if url.strip():
            entries = fetch_rss(url, "Google Alert", hours)
            all_entries.extend(entries)
            if entries:
                print(f"  + Google Alert: {len(entries)} entries")
            time.sleep(0.5)
    
    # 3. 去重：按链接去重
    seen_links = set()
    unique_entries = []
    for e in all_entries:
        link_hash = hashlib.md5(e["link"].encode()).hexdigest()
        if link_hash not in seen_links:
            seen_links.add(link_hash)
            unique_entries.append(e)
    
    # 4. 按时间倒序排列
    unique_entries.sort(key=lambda x: x["raw_date"], reverse=True)
    
    print(f"[FETCH] Total unique entries: {len(unique_entries)}")
    return unique_entries


def fetch_for_test():
    """
    测试用：只抓取少量数据，快速验证
    """
    print("[TEST MODE] Fetching limited sources...")
    entries = []
    # 只抓前2个通用源
    for src in GENERAL_RSS[:2]:
        e = fetch_rss(src["url"], src["name"], hours=48)
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
    
    unique.sort(key=lambda x: x["raw_date"], reverse=True)
    print(f"[TEST] Fetched {len(unique)} unique entries")
    return unique


if __name__ == "__main__":
    # 本地测试运行
    results = fetch_all_sources(hours=24)
    print(f"\n--- Sample (first 3) ---")
    for r in results[:3]:
        print(f"[{r['source']}] {r['title'][:60]}...")
        print(f"  Date: {r['pub_date']} | Link: {r['link'][:80]}")
        print()
