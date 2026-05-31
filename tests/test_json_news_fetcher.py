from datetime import datetime, timedelta

from src.fetchers import json_news_fetcher
from src.fetchers.json_news_fetcher import JSONNewsFetcher


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "featured": {
                "title": "Recent investment article",
                "slug": "/economy/recent-investment",
                "excerpt": "<p>Bangladesh investment summary</p>",
                "datetime": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            },
            "posts": [{
                "title": "Old article",
                "slug": "/economy/old",
                "datetime": (datetime.utcnow() - timedelta(hours=48)).isoformat(),
            }, {
                "title": "Global article",
                "slug": "/economy/global/global-article",
                "datetime": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
            }],
        }


def test_json_news_fetcher_reads_nested_paths_and_respects_hours(monkeypatch):
    monkeypatch.setattr(
        json_news_fetcher.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    results = JSONNewsFetcher().fetch({
        "name": "Example API",
        "url": "https://api.example.com/economy",
        "items_paths": ["featured", "posts"],
        "link_prefix": "https://example.com",
        "exclude_link_prefixes": ["/economy/global"],
        "prequalified": True,
    })

    assert [item["title"] for item in results] == ["Recent investment article"]
    assert results[0]["link"] == "https://example.com/economy/recent-investment"
    assert results[0]["summary"] == "Bangladesh investment summary"
    assert results[0]["prequalified"] is True
