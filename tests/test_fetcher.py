from datetime import datetime, timedelta

import src.fetcher as fetcher_module
from src.fetcher import deduplicate_entries, is_relevant_article
from src.fetchers import rss_fetcher
from src.fetchers.rss_fetcher import RSSFetcher


class FakeFeed:
    def __init__(self, entries, bozo=False, bozo_exception=""):
        self.entries = entries
        self.bozo = bozo
        self.bozo_exception = bozo_exception


class FakeResponse:
    def __init__(self, content=b"<rss />", url="https://example.com/feed"):
        self.content = content
        self.url = url
        self.status_code = 200
        self.headers = {"Content-Type": "application/rss+xml"}

    def raise_for_status(self):
        return None


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


def test_relevance_filter_keeps_prequalified_entries():
    assert is_relevant_article({
        "title": "Curated economy bulletin",
        "summary": "Verified category endpoint",
        "prequalified": True,
    })


def test_relevance_filter_drops_road_accident_and_sports_keyword_collisions():
    assert not is_relevant_article({
        "title": "Man killed in Chandpur road accident",
        "summary": "",
    })
    assert not is_relevant_article({
        "title": "Ronaldo's final bid for World Cup glory",
        "summary": "",
    })
    assert not is_relevant_article({
        "title": "Measles: Death toll rises with five more deaths",
        "summary": "",
    })
    assert not is_relevant_article({
        "title": "Illegal entry case - The Business Standard",
        "summary": "Illegal entry case - The Business Standard",
        "source": "Google News - Bangladesh",
    })


def test_relevance_filter_keeps_general_business_signals():
    assert is_relevant_article({
        "title": "ADB intends to provide $5b over five years",
        "summary": "The investment package will support Bangladesh.",
    })
    assert is_relevant_article({
        "title": "Crop losses and debt trouble northern farmers",
        "summary": "",
    })


def test_rss_fetcher_respects_hours(monkeypatch):
    now = datetime.utcnow()
    recent = now - timedelta(hours=2)
    old = now - timedelta(hours=30)

    def fake_parse(content):
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
    monkeypatch.setattr(rss_fetcher.requests, "get", lambda *args, **kwargs: FakeResponse())

    fetcher = RSSFetcher()
    results = fetcher.fetch({"url": "https://example.com/feed", "name": "Test"}, hours=24)

    assert [item["title"] for item in results] == ["Recent item"]
    assert fetcher.last_health["status"] == "ok"
    assert fetcher.last_health["feed_entries"] == 2
    assert fetcher.last_health["recent_entries"] == 1


def test_rss_fetcher_records_empty_feed_health(monkeypatch):
    monkeypatch.setattr(rss_fetcher.feedparser, "parse", lambda content: FakeFeed([]))
    monkeypatch.setattr(rss_fetcher.requests, "get", lambda *args, **kwargs: FakeResponse())

    fetcher = RSSFetcher()
    assert fetcher.fetch({"url": "https://example.com/feed", "name": "Empty"}) == []
    assert fetcher.last_health["status"] == "empty_feed"
    assert fetcher.last_health["http_status"] == 200


def test_fetch_all_sources_uses_rss_web_fallback_and_saves_health(monkeypatch):
    saved = {}

    class FakeRSSFetcher:
        def __init__(self):
            self.last_health = {
                "name": "Test RSS",
                "status": "empty_feed",
                "fallback_used": False,
                "fallback_count": 0,
            }

        def fetch(self, config, hours):
            return []

    class FakeScraperFetcher:
        def fetch(self, config, hours):
            return [{
                "title": "Bangladesh solar investment",
                "link": "https://example.com/solar",
                "summary": "Solar energy project",
                "raw_date": datetime.utcnow(),
            }]

    monkeypatch.setattr(fetcher_module, "SOURCES", [{
        "type": "rss",
        "name": "Test RSS",
        "url": "https://example.com/feed",
        "fallback_scraper": {
            "url": "https://example.com/news",
            "item_selector": "a",
        },
    }])
    monkeypatch.setitem(fetcher_module.FETCHER_REGISTRY, "rss", FakeRSSFetcher)
    monkeypatch.setattr(fetcher_module, "WebScraperFetcher", FakeScraperFetcher)
    monkeypatch.setattr(fetcher_module.time, "sleep", lambda seconds: None)
    monkeypatch.setattr(
        fetcher_module,
        "save_daily_json",
        lambda kind, items: saved.update({"kind": kind, "items": items}),
    )

    results = fetcher_module.fetch_all_sources()

    assert results[0]["source_type"] == "scraper_fallback"
    assert saved["kind"] == "source_health"
    assert saved["items"][0]["fallback_used"] is True
    assert saved["items"][0]["fallback_count"] == 1
