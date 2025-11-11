import json
import sqlite3
from pathlib import Path
from typing import Dict, Any, Iterable

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source TEXT NOT NULL,
  url TEXT UNIQUE,
  author TEXT,
  title TEXT,
  content TEXT,
  upvotes INTEGER,
  comments_count INTEGER,
  created_utc INTEGER,
  scraped_at TEXT,
  extra_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_signals_source ON signals(source);
CREATE INDEX IF NOT EXISTS idx_signals_created ON signals(created_utc);
"""

def get_conn(sqlite_path: str) -> sqlite3.Connection:
    Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(sqlite_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.executescript(SCHEMA)
    return conn

def insert_records(conn: sqlite3.Connection, records: Iterable[Dict[str, Any]]) -> int:
    rows = [
        (
            r.get("source"),
            r.get("url"),
            r.get("author"),
            r.get("title"),
            r.get("content"),
            r.get("upvotes"),
            r.get("comments_count"),
            r.get("created_utc"),
            r.get("scraped_at"),
            json.dumps(r.get("extra", {}), ensure_ascii=False),
        )
        for r in records
    ]
    cur = conn.executemany(
        """INSERT OR IGNORE INTO signals(
            source, url, author, title, content, upvotes, comments_count,
            created_utc, scraped_at, extra_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
        rows
    )
    conn.commit()
    return cur.rowcount
