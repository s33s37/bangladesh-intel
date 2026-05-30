from src.demo_data import get_demo_entries


def test_demo_entries_are_non_empty_and_structured():
    entries = get_demo_entries()

    assert len(entries) >= 3
    assert all(entry["title"] for entry in entries)
    assert any(entry.get("item_type") == "indicator" for entry in entries)
