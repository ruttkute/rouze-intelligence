import os, time, csv, requests
from datetime import datetime
from urllib.parse import quote

USER_AGENT = "RouzeSignalMiner/0.1 (contact: research@rouze.local)"
HEADERS = {"User-Agent": USER_AGENT}

def fetch_subreddit_hot(subreddit: str, limit: int = 100):
    # Reddit public JSON (no API key). Respect rate limits.
    url = f"https://www.reddit.com/r/{quote(subreddit)}/hot.json?limit={min(limit,100)}"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()["data"]["children"]
    rows = []
    for item in data:
        p = item["data"]
        rows.append({
            "id": p.get("id",""),
            "subreddit": p.get("subreddit",""),
            "title": p.get("title","").replace("\n"," ").strip(),
            "selftext": (p.get("selftext","") or "").replace("\n"," ").strip(),
            "score": p.get("score",0),
            "num_comments": p.get("num_comments",0),
            "created_utc": int(p.get("created_utc",0)),
            "permalink": f"https://www.reddit.com{p.get('permalink','')}"
        })
    return rows

def save_csv(rows, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def run(subreddits):
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    for sub in subreddits:
        rows = fetch_subreddit_hot(sub, limit=100)
        out = os.path.join("data", f"reddit_{sub}_hot_{ts}.csv")
        if rows:
            save_csv(rows, out)
            print(f"[miner] saved {len(rows)} rows -> {out}")
        time.sleep(1)  # polite

if __name__ == "__main__":
    # pick signals that are relevant to landing first freelance data jobs
    run(["freelance", "forhire", "hireawriter"])
