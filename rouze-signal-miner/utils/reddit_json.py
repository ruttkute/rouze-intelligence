#!/usr/bin/env python3
import time, requests, os, typing as t

UA = os.getenv("REDDIT_USER_AGENT", "rouze-signal-miner/0.1 by <username>")
BASE = "https://www.reddit.com"

def _get(url: str, params: dict) -> dict:
    backoff = 1.5
    for attempt in range(6):
        r = requests.get(url, headers={"User-Agent": UA}, params=params, timeout=30)
        # Small courtesy delay to stay friendly to Reddit
        if r.status_code == 429:           # rate limited
            time.sleep(backoff); backoff *= 1.8; continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Too many retries to Reddit JSON endpoint")

def fetch_subreddit(
    sub: str,
    where: t.Literal["hot","new","rising","top"]="hot",
    limit: int = 25,
    after: t.Optional[str] = None,
):
    """Returns (posts, next_after). limit<=100, after is fullname like 't3_abc123'."""
    url = f"{BASE}/r/{sub}/{where}.json"
    data = _get(url, {"limit": min(limit, 100), "after": after})

    posts = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        posts.append({
            "id": d.get("id"),
            "title": d.get("title"),
            "subreddit": d.get("subreddit"),
            "score": d.get("score"),
            "url": d.get("url"),
            "created_utc": d.get("created_utc"),
            "num_comments": d.get("num_comments"),
            "permalink": f"{BASE}{d.get('permalink')}",
        })
    return posts, data.get("data", {}).get("after")

if __name__ == "__main__":
    import sys, json
    sub = sys.argv[1] if len(sys.argv) > 1 else "test"
    posts, nxt = fetch_subreddit(sub, "hot", limit=25)
    print(json.dumps(posts, indent=2))
    print("next_after:", nxt)
