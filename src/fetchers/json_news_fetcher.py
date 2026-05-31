"""Fetcher for public JSON news endpoints."""

from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from src.fetchers.base import BaseFetcher


class JSONNewsFetcher(BaseFetcher):
    """Fetch news articles from a configurable public JSON endpoint."""

    source_type = "json_news"

    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    def fetch(self, config: dict, hours: int = 24) -> list:
        url = config.get("url", "")
        source_name = config.get("name", "JSON News")

        try:
            response = requests.get(url, headers=self.DEFAULT_HEADERS, timeout=30)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            print(f"  [ERROR] [{source_name}] {str(exc)[:80]}")
            return []

        cutoff = datetime.utcnow() - timedelta(hours=hours)
        entries = []
        seen_links = set()
        for item in self._extract_items(data, config.get("items_paths", [""])):
            title = self._clean_html(item.get(config.get("title_field", "title"), ""))
            raw_link = item.get(config.get("link_field", "slug"), "")
            if any(
                raw_link.startswith(prefix)
                for prefix in config.get("exclude_link_prefixes", [])
            ):
                continue
            link = urljoin(
                config.get("link_prefix", url),
                raw_link,
            )
            if not title or not link or link in seen_links:
                continue

            pub_date, date_unverified = self._parse_date(
                item.get(config.get("date_field", "datetime"), "")
            )
            if pub_date < cutoff:
                continue

            seen_links.add(link)
            entries.append({
                "title": title,
                "link": link,
                "summary": self._clean_html(
                    item.get(config.get("summary_field", "excerpt"), "")
                )[:1500],
                "source": source_name,
                "pub_date": pub_date.strftime("%m-%d %H:%M"),
                "raw_date": pub_date,
                "date_unverified": date_unverified,
                "prequalified": config.get("prequalified", False),
            })

        return entries[: config.get("max_items", 20)]

    @staticmethod
    def _extract_items(data, paths):
        items = []
        for path in paths:
            value = data
            for part in filter(None, path.split(".")):
                if not isinstance(value, dict):
                    value = None
                    break
                value = value.get(part)

            if isinstance(value, list):
                items.extend(item for item in value if isinstance(item, dict))
            elif isinstance(value, dict):
                items.append(value)
        return items

    @staticmethod
    def _clean_html(value):
        return BeautifulSoup(value or "", "html.parser").get_text(strip=True)

    @staticmethod
    def _parse_date(value):
        if not value:
            return datetime.utcnow(), True
        try:
            parsed = date_parser.parse(value)
            if parsed.tzinfo:
                parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
            return parsed, False
        except Exception:
            return datetime.utcnow(), True
