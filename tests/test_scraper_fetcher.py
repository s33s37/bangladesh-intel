from src.fetchers import scraper_fetcher
from src.fetchers.scraper_fetcher import WebScraperFetcher


class FakeResponse:
    text = """
        <div class="article">
          <h2>Bangladesh solar investment expands</h2>
          <a class="overlay" href="/business/solar-investment"></a>
        </div>
    """
    encoding = "utf-8"

    def raise_for_status(self):
        return None


def test_scraper_fetcher_supports_relative_title_and_link_selectors(monkeypatch):
    monkeypatch.setattr(
        scraper_fetcher.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    results = WebScraperFetcher().fetch({
        "name": "Example",
        "url": "https://example.com/",
        "item_selector": ".article",
        "title_selector": "h2",
        "link_selector": "a.overlay",
        "link_prefix": "https://example.com",
    })

    assert results[0]["title"] == "Bangladesh solar investment expands"
    assert results[0]["link"] == "https://example.com/business/solar-investment"
