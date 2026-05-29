from datetime import datetime, timedelta

from src.fetcher import deduplicate_entries
from src.fetchers import rss_fetcher
from src.fetchers.rss_fetcher import RSSFetcher


class FakeFeed:
    def __init__(self, entries):
        self.entries = entries


def test_deduplicate_entries_normalizes_tracking_params_and_titles():
    entries = [
        {
            "title": "Bangladesh exports rise - Reuters",
            "link": "https://example.com/story?utm_source=newsletter",
        },
        {
            "title": "Bangladesh exports rise",
            "link": "https://example.com/story",
        },
    ]

    assert len(deduplicate_entries(entries)) == 1


def test_rss_fetcher_respects_hours(monkeypatch):
    now = datetime.utcnow()
    recent = now - timedelta(hours=2)
    old = now - timedelta(hours=30)

    def fake_parse(url, agent=None):
        return FakeFeed([
            {
                "title": "Recent item",
                "link": "https://example.com/recent",
                "summary": "recent summary",
                "published": recent.isoformat(),
            },
            {
                "title": "Old item",
                "link": "https://example.com/old",
                "summary": "old summary",
                "published": old.isoformat(),
            },
        ])

    monkeypatch.setattr(rss_fetcher.feedparser, "parse", fake_parse)

    results = RSSFetcher().fetch({"url": "https://example.com/feed", "name": "Test"}, hours=24)

    assert [item["title"] for item in results] == ["Recent item"]
