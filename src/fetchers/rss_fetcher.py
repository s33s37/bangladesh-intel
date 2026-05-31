"""RSS/Atom feed fetcher with per-source health diagnostics."""

from datetime import datetime, timedelta, timezone

import feedparser
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from src.fetchers.base import BaseFetcher


class RSSFetcher(BaseFetcher):
    """Fetch RSS/Atom entries and expose diagnostics for the latest run."""

    source_type = "rss"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "BangladeshIntelBot/1.0 "
            "(+https://github.com/s33s37/bangladesh-intel)"
        ),
        "Accept": (
            "application/rss+xml,application/atom+xml,"
            "application/xml,text/xml,*/*;q=0.8"
        ),
    }

    def __init__(self):
        self.last_health = {}

    def fetch(self, config: dict, hours: int = 24) -> list:
        """Fetch one configured RSS source."""
        url = config.get("url", "")
        source_name = config.get("name", "Unknown RSS")
        entries = []
        self.last_health = {
            "type": "rss",
            "name": source_name,
            "url": url,
            "final_url": "",
            "status": "pending",
            "http_status": None,
            "content_type": "",
            "feed_entries": 0,
            "recent_entries": 0,
            "latest_published": "",
            "bozo": False,
            "bozo_exception": "",
            "error": "",
            "fallback_used": False,
            "fallback_count": 0,
        }

        try:
            response = requests.get(
                url,
                headers=self.DEFAULT_HEADERS,
                timeout=config.get("timeout", 30),
                allow_redirects=True,
            )
            self.last_health.update({
                "final_url": response.url,
                "http_status": response.status_code,
                "content_type": response.headers.get("Content-Type", ""),
            })
            response.raise_for_status()

            feed = feedparser.parse(response.content)
            feed_entries = list(getattr(feed, "entries", []))
            self.last_health["feed_entries"] = len(feed_entries)
            self.last_health["bozo"] = bool(getattr(feed, "bozo", False))
            self.last_health["bozo_exception"] = str(
                getattr(feed, "bozo_exception", "")
            )[:300]

            cutoff = datetime.utcnow() - timedelta(hours=hours)
            latest_published = None
            for entry in feed_entries:
                published = (
                    entry.get("published")
                    or entry.get("updated")
                    or entry.get("pubDate")
                    or entry.get("date")
                    or ""
                )
                pub_date, date_unverified = self._parse_date(published)
                if not date_unverified:
                    latest_published = max(latest_published or pub_date, pub_date)

                if pub_date < cutoff:
                    continue

                summary = self._clean_html(entry.get("summary", ""))
                description = self._clean_html(entry.get("description", ""))
                content_val = ""
                content = entry.get("content")
                if content and isinstance(content, list):
                    content_val = self._clean_html(content[0].get("value", ""))
                text = max([summary, description, content_val], key=len)

                entries.append({
                    "title": self._clean_html(entry.get("title", "")),
                    "link": entry.get("link", ""),
                    "summary": text[:1500],
                    "source": source_name,
                    "pub_date": pub_date.strftime("%m-%d %H:%M"),
                    "raw_date": pub_date,
                    "date_unverified": date_unverified,
                })

            self.last_health["recent_entries"] = len(entries)
            if latest_published:
                self.last_health["latest_published"] = latest_published.isoformat()

            if self.last_health["bozo"] and not feed_entries:
                self.last_health["status"] = "parse_error"
            elif not feed_entries:
                self.last_health["status"] = "empty_feed"
            elif not entries:
                self.last_health["status"] = "empty_recent"
            elif self.last_health["bozo"]:
                self.last_health["status"] = "parse_warning"
            else:
                self.last_health["status"] = "ok"
        except requests.HTTPError as exc:
            self._record_error("http_error", source_name, exc)
        except requests.RequestException as exc:
            self._record_error("request_error", source_name, exc)
        except Exception as exc:
            self._record_error("fetch_error", source_name, exc)

        return entries

    def _record_error(self, status, source_name, exc):
        self.last_health["status"] = status
        self.last_health["error"] = str(exc)[:300]
        print(f"  [ERROR] [{source_name}] {str(exc)[:60]}")

    @staticmethod
    def _clean_html(value):
        return BeautifulSoup(value or "", "html.parser").get_text(strip=True)

    @staticmethod
    def _parse_date(published):
        if not published:
            return datetime.utcnow(), True

        try:
            pub_date = date_parser.parse(published)
            if pub_date.tzinfo:
                pub_date = pub_date.astimezone(timezone.utc).replace(tzinfo=None)
            return pub_date, False
        except Exception:
            return datetime.utcnow(), True
