# RSS Operations

The daily scheduler skips sources marked with `"enabled": false` in
`src/config.py`. Disabled sources remain configured for manual review.

Check active media RSS sources:

```bash
python -m src.rss_health --hours 48
```

Recheck disabled media RSS sources manually:

```bash
python -m src.rss_health --hours 48 --include-disabled
```

Include the Google News keyword feeds when needed:

```bash
python -m src.rss_health --hours 48 --include-google
```

Each check writes `data/source_health_YYYY-MM-DD.json`.
