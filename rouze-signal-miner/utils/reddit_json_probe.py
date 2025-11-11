#!/usr/bin/env python3
import os, time, json, sys, requests

UA = os.getenv("REDDIT_USER_AGENT", "macos:rouze-signal-miner:v0.1 (by /u/Even_Regular_2938)")
BASE = "https://www.reddit.com"

def fetch(sub, where="hot", limit=25):
    url = f"{BASE}/r/{sub}/{where}.json?limit={limit}"
    r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    if r.status_code == 429:
        # simple backoff if rate limited
        time.sleep(2)
        r = requests.get(url, headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    data = r.json()
    out = []
    for c in data.get("data", {}).get("children", []):
        d = c.get("data", {})
        out.append({
            "id": d.get("id"),
            "title": d.get("title"),
            "subreddit": d.get("subreddit"),
            "score": d.get("score"),
            "url": d.get("url"),
            "created_utc": d.get("created_utc"),
            "num_comments": d.get("num_comments"),
            "permalink": f'{BASE}{d.get("permalink")}',
        })
    return out

if __name__ == "__main__":
    sub = sys.argv[1] if len(sys.argv) > 1 else "test"
    posts = fetch(sub, "hot", limit=5)
    print(json.dumps(posts, indent=2))
