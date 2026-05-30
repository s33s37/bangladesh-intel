import src.processor as processor


def test_processor_import_and_model_name_without_keys(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(processor, "_read_optional_key", lambda path: "")
    processor.client = None
    processor.MODEL_NAME = None

    assert processor.get_model_name() == "unconfigured"


def test_indicator_entries_do_not_call_ai(monkeypatch):
    def fail_if_called(*args, **kwargs):
        raise AssertionError("AI analysis should not be called for indicators")

    monkeypatch.setattr(processor, "analyze_one", fail_if_called)

    result = processor.batch_analyze([
        {
            "title": "[世行数据] GDP",
            "summary": "孟加拉GDP增长率为 5.12%（2023年）",
            "source": "WorldBank",
            "link": "https://example.com",
            "pub_date": "2023-12-31 00:00",
            "item_type": "indicator",
        }
    ])

    assert result[0]["intel_type"] == "市场数据"
    assert result[0]["item_type"] == "indicator"


def test_news_entries_fallback_when_ai_is_unconfigured(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(processor, "_read_optional_key", lambda path: "")
    processor.client = None
    processor.MODEL_NAME = None

    result = processor.analyze_one(
        "Bangladesh garment exports face new tariff pressure",
        "Exporters warned that duty changes may affect RMG shipments.",
        "Test Source",
    )

    assert result["sector"] == "成衣纺织"
    assert result["intel_type"] == "政策变动"
    assert result["summary_cn"].startswith("来源消息：")
    assert result["reason"] == "无AI密钥"


def test_red_flag_keyword_uses_word_boundaries(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(processor, "_read_optional_key", lambda path: "")
    processor.client = None
    processor.MODEL_NAME = None

    result = processor.analyze_one(
        "Bangladesh solar investment reaches financial close",
        "The project secured funding and grid connection support.",
        "Test Source",
    )

    assert result["red_flag"] is False


def test_fallback_prefers_specific_title_sector(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(processor, "_read_optional_key", lambda path: "")
    processor.client = None
    processor.MODEL_NAME = None

    result = processor.analyze_one(
        "Chinese-backed solar park reaches financial close in Bangladesh",
        "A 100MW power project reached investment close with local grid support.",
        "Test Source",
    )

    assert result["sector"] == "太阳能"
