"""Run a focused RSS source health check without generating a report."""

import argparse

from src.config import RSS_SOURCES
from src.fetchers.rss_fetcher import RSSFetcher
from src.storage import save_daily_json


def run_health_check(hours=24, include_google=False, include_disabled=False):
    sources = [
        source
        for source in RSS_SOURCES
        if (include_disabled or source.get("enabled", True))
        and (include_google or not source.get("name", "").startswith("Google News"))
    ]
    health_items = []

    print(f"[RSS HEALTH] Checking {len(sources)} sources")
    for index, source in enumerate(sources, 1):
        fetcher = RSSFetcher()
        fetcher.fetch(source, hours=hours)
        health = fetcher.last_health
        health_items.append(health)
        print(
            f"  [{index}/{len(sources)}] [{health['name']}] "
            f"{health['status']} HTTP:{health['http_status']} "
            f"feed:{health['feed_entries']} recent:{health['recent_entries']}"
        )

    save_daily_json("source_health", health_items)
    return health_items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument(
        "--include-google",
        action="store_true",
        help="Include Google News keyword feeds in addition to media feeds.",
    )
    parser.add_argument(
        "--include-disabled",
        action="store_true",
        help="Recheck sources disabled after earlier failures.",
    )
    args = parser.parse_args()
    run_health_check(
        hours=args.hours,
        include_google=args.include_google,
        include_disabled=args.include_disabled,
    )


if __name__ == "__main__":
    main()
