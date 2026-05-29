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
