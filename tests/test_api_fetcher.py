from src.fetchers.api_fetcher import APIFetcher


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return [
            {"page": 1},
            [
                {"date": "2024", "value": None},
                {"date": "2023", "value": 5.12},
                {"date": "2022", "value": 4.5},
            ],
        ]


class FakeBOMResponse:
    content = (
        b'\xef\xbb\xbf[{"currency":"USD","buy":"120","sell":"121",'
        b'"date":"2026-05-31"}]'
    )

    def raise_for_status(self):
        return None


class FakeHTMLResponse:
    content = b"""
        <div class="exchange">
          <div class="display_table">
            <div><div>Currency</div><div>Highest</div><div>Lowest</div><div>WAR</div></div>
            <div><div>USD</div><div>122.75</div><div>122.50</div><div>122.60</div></div>
          </div>
          <p class="last_update">Last update: 24th May, 2026</p>
        </div>
    """

    def raise_for_status(self):
        return None


def test_worldbank_returns_latest_non_empty_indicator(monkeypatch):
    def fake_get(url, headers=None, timeout=None):
        return FakeResponse()

    monkeypatch.setattr("src.fetchers.api_fetcher.requests.get", fake_get)

    results = APIFetcher().fetch({
        "type": "api",
        "name": "WorldBank - GDP Growth",
        "api_type": "worldbank",
        "indicator": "NY.GDP.MKTP.KD.ZG",
        "country": "BD",
    })

    assert len(results) == 1
    assert "(2023)" in results[0]["title"]
    assert results[0]["item_type"] == "indicator"


def test_bangladesh_bank_accepts_utf8_bom_json(monkeypatch):
    monkeypatch.setattr(
        "src.fetchers.api_fetcher.requests.get",
        lambda *args, **kwargs: FakeBOMResponse(),
    )

    results = APIFetcher().fetch({
        "type": "api",
        "name": "Bangladesh Bank - Exchange Rate",
        "api_type": "bangladesh_bank",
    })

    assert len(results) == 1
    assert "USD" in results[0]["title"]


def test_bangladesh_bank_parses_official_html_card(monkeypatch):
    monkeypatch.setattr(
        "src.fetchers.api_fetcher.requests.get",
        lambda *args, **kwargs: FakeHTMLResponse(),
    )

    results = APIFetcher().fetch({
        "type": "api",
        "name": "Bangladesh Bank - Exchange Rate",
        "api_type": "bangladesh_bank",
    })

    assert len(results) == 1
    assert "USD/BDT" in results[0]["title"]
    assert "WAR 122.60" in results[0]["summary"]
