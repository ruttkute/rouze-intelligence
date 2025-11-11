#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Google News RSS scraper for Rouze (Signal Miner).

- Fetches Google News RSS search results for one or more queries.
- Normalizes fields and writes to:
    1) SQLite: data/rouze_signals.sqlite (table: news_articles)
    2) JSONL:  data/raw/google_news/YYYY-MM-DD/<slug>-news.jsonl
- Safe to run repeatedly: uses UNIQUE(url) with INSERT OR IGNORE to avoid duplicates.

Requires:
    pip install feedparser requests python-dateutil

Usage examples:
    python -m scrapers.google_news_scraper --queries "upwork trends,fiverr reviews" --lang en --region US --limit 50
    python scrapers/google_news_scraper.py --queries "freelance research" --lang en --region US
"""

import argparse
import datetime as dt
import hashlib
import json
import logging
import os
import re
import sqlite3
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse, parse_qs, unquote, quote_plus

import feedparser
import requests
from dateutil import tz

# --------------------------- Config Defaults ---------------------------

DB_PATH = os.path.join("data", "rouze_signals.sqlite")
RAW_DIR = os.path.join("data", "raw", "google_news")
LOG_PATH = os.path.join("logs", "scrape.log")

DEFAULT_LANG = "en"   # 'hl' param (language UI)
DEFAULT_REGION = "US" # 'gl' + 'ceid' region
DEFAULT_LIMIT = 50
REQUEST_TIMEOUT = 15
REQUEST_PAUSE = (0.7, 1.5)  # seconds between requests (min, max)

# ----------------------------------------------------------------------

def ensure_dirs():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def setup_logger():
    ensure_dirs()
    logger = logging.getLogger("google_news_scraper")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    fh = logging.FileHandler(LOG_PATH)
    fh.setFormatter(fmt)
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

LOGGER = setup_logger()

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-") or "query"

def ts_iso(ts: Optional[time.struct_time]) -> str:
    if ts:
        try:
            dt_utc = dt.datetime(*ts[:6], tzinfo=tz.tzutc())
            return dt_utc.isoformat()
        except Exception:
            pass
    return dt.datetime.now(tz=tz.tzlocal()).isoformat()

def normalize_url(google_news_link: str) -> str:
    """
    Google News RSS entries often contain a Google redirect.
    Extract the original URL if present (?url=...), else return link.
    """
    try:
        parsed = urlparse(google_news_link)
        qs = parse_qs(parsed.query)
        if "url" in qs and qs["url"]:
            return unquote(qs["url"][0])
    except Exception:
        pass
    return google_news_link

def hash_id(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()

def build_rss_url(query: str, lang: str, region: str) -> str:
    # Google News RSS search endpoint
    # hl=<lang>-<REGION> UI language, gl=<REGION> geo, ceid=<REGION>:<lang>
    q = quote_plus(query)
    hl = f"{lang}-{region}"
    ceid = f"{region}:{lang}"
    return f"https://news.google.com/rss/search?q={q}&hl={hl}&gl={region}&ceid={ceid}"

def fetch_feed_raw(url: str) -> bytes:
    headers = {
        "User-Agent": "rouze-signal-miner/0.1 (GoogleNewsRSS) +https://github.com/",
        "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
    }
    resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.content

def parse_entries(content: bytes, query: str, lang: str, region: str) -> List[Dict]:
    feed = feedparser.parse(content)
    out: List[Dict] = []

    for e in feed.entries:
        link = normalize_url(e.get("link", "").strip())
        if not link:
            continue

        published_iso = ts_iso(e.get("published_parsed"))
        source = ""
        try:
            # Google News often gives source in e.source.title
            src = e.get("source")
            if isinstance(src, dict):
                source = src.get("title", "") or ""
            else:
                source = ""
        except Exception:
            source = ""

        summary = (e.get("summary") or "").strip()
        title = (e.get("title") or "").strip()

        record = {
            "article_id": hash_id(link),
            "title": title,
            "source": source,
            "url": link,
            "published_at": published_iso,
            "summary": summary,
            "query": query,
            "lang": lang,
            "region": region,
            "fetched_at": dt.datetime.now(tz=tz.tzlocal()).isoformat(),
            "raw_link": e.get("link", ""),
        }
        out.append(record)
    return out

# ----------------------------- Persistence ----------------------------

def init_db(conn: sqlite3.Connection):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS news_articles (
            article_id   TEXT PRIMARY KEY,
            title        TEXT,
            source       TEXT,
            url          TEXT UNIQUE,
            published_at TEXT,
            summary      TEXT,
            query        TEXT,
            lang         TEXT,
            region       TEXT,
            fetched_at   TEXT,
            raw_link     TEXT
        );
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_published ON news_articles(published_at);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_news_query ON news_articles(query);")
    conn.commit()

def upsert_articles(conn: sqlite3.Connection, articles: List[Dict]) -> int:
    if not articles:
        return 0
    cur = conn.cursor()
    inserted = 0
    for a in articles:
        try:
            cur.execute("""
                INSERT OR IGNORE INTO news_articles
                (article_id, title, source, url, published_at, summary, query, lang, region, fetched_at, raw_link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                a["article_id"], a["title"], a["source"], a["url"], a["published_at"], a["summary"],
                a["query"], a["lang"], a["region"], a["fetched_at"], a["raw_link"]
            ))
            if cur.rowcount == 1:
                inserted += 1
        except Exception as ex:
            LOGGER.warning("DB insert error for url=%s: %s", a.get("url"), ex)
    conn.commit()
    return inserted

def write_jsonl(articles: List[Dict], query: str) -> str:
    if not articles:
        return ""
    day_dir = os.path.join(RAW_DIR, dt.date.today().isoformat())
    os.makedirs(day_dir, exist_ok=True)
    path = os.path.join(day_dir, f"{slugify(query)}-news.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        for a in articles:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    return path

# ------------------------------- Runner --------------------------------

def scrape_queries(queries: List[str], lang: str, region: str, limit: int) -> None:
    LOGGER.info("Starting Google News scrape | queries=%s | lang=%s | region=%s | limit=%d",
                queries, lang, region, limit)

    # DB ready
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    total_added = 0
    for i, q in enumerate(queries, start=1):
        q = q.strip()
        if not q:
            continue

        try:
            url = build_rss_url(q, lang, region)
            LOGGER.info("(%d/%d) Fetch: %s", i, len(queries), url)
            raw = fetch_feed_raw(url)
            articles = parse_entries(raw, q, lang, region)

            if limit and len(articles) > limit:
                articles = articles[:limit]

            # persist
            jsonl_path = write_jsonl(articles, q)
            added = upsert_articles(conn, articles)
            total_added += added

            LOGGER.info("Saved %d items (new=%d) for query='%s' to %s",
                        len(articles), added, q, jsonl_path or "(skipped jsonl)")
        except requests.HTTPError as http_err:
            LOGGER.error("HTTP error for query='%s': %s", q, http_err)
        except Exception as ex:
            LOGGER.exception("Unhandled error for query='%s': %s", q, ex)

        # polite pause
        sleep_min, sleep_max = REQUEST_PAUSE
        time.sleep(sleep_min + (sleep_max - sleep_min) * 0.5)

    conn.close()
    LOGGER.info("Done. Total newly inserted rows: %d", total_added)

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Rouze Google News RSS scraper")
    ap.add_argument("--queries", type=str, required=True,
                    help="Comma-separated queries. Example: 'upwork trends,fiverr reviews'")
    ap.add_argument("--lang", type=str, default=DEFAULT_LANG, help="Language code (e.g., en)")
    ap.add_argument("--region", type=str, default=DEFAULT_REGION, help="Region code (e.g., US)")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Max items per query")
    return ap.parse_args()

def main():
    args = parse_args()
    queries = [q for q in (args.queries.split(",") if args.queries else []) if q.strip()]
    if not queries:
        LOGGER.error("No queries provided.")
        return
    scrape_queries(queries, args.lang, args.region, args.limit)

if __name__ == "__main__":
    main()
