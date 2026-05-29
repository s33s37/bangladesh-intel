"""
RSS 抓取插件
支持标准 RSS/Atom 源，自动清理 HTML 标签，处理时区
"""
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser as date_parser

from src.fetchers.base import BaseFetcher


class RSSFetcher(BaseFetcher):
    """RSS/Atom 源抓取器"""

    source_type = "rss"

    def fetch(self, config: dict, hours: int = 24) -> list:
        """抓取单个 RSS 源"""
        url = config.get("url", "")
        source_name = config.get("name", "Unknown RSS")
        entries = []

        try:
            feed = feedparser.parse(url, agent="BangladeshIntelBot/1.0")
            cutoff = datetime.utcnow() - timedelta(hours=72)

            for entry in feed.entries:
                published = (
                    entry.get("published")
                    or entry.get("updated")
                    or entry.get("pubDate")
                    or entry.get("date")
                    or ""
                )
                if not published:
                    pub_date = datetime.utcnow()
                else:
                    try:
                        pub_date = date_parser.parse(published)
                        if pub_date.tzinfo:
                            pub_date = pub_date.replace(tzinfo=None)
                    except Exception:
                        pub_date = datetime.utcnow()

                # 统一转换为 UTC 无时区时间进行比较
                compare_date = pub_date.replace(tzinfo=None) if pub_date.tzinfo else pub_date
                if compare_date >= cutoff:
                    summary = BeautifulSoup(
                        entry.get("summary", ""), "html.parser"
                    ).get_text(strip=True)
                    description = BeautifulSoup(
                        entry.get("description", ""), "html.parser"
                    ).get_text(strip=True)
                    content_val = ""
                    if (
                        entry.get("content")
                        and isinstance(entry.get("content"), list)
                        and len(entry.get("content")) > 0
                    ):
                        content_val = entry.get("content")[0].get("value", "")
                    text = max([summary, description, content_val], key=len)

                    entries.append({
                        "title": BeautifulSoup(
                            entry.get("title", ""), "html.parser"
                        ).get_text(strip=True),
                        "link": entry.get("link", ""),
                        "summary": text[:1500],
                        "source": source_name,
                        "pub_date": pub_date.strftime("%m-%d %H:%M"),
                        "raw_date": pub_date,
                    })
        except Exception as e:
            print(f"  [ERROR] [{source_name}] {str(e)[:60]}")

        return entries
