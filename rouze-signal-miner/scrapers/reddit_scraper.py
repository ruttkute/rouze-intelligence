from utils.reddit_json import fetch_subreddit
# from utils.db import upsert_posts  # (if you have a DB layer)

def run(subs: list[str], per_sub_limit=100):
    for sub in subs:
        got = 0
        after = None
        while got < per_sub_limit:
            batch, after = fetch_subreddit(sub, "hot", limit=min(100, per_sub_limit-got), after=after)
            if not batch: break
            # upsert_posts(batch)  # plug into your DB if needed
            for p in batch: print(p["title"])  # or whatever you need
            got += len(batch)
            time.sleep(1.2)  # be polite
            if not after: break

if __name__ == "__main__":
    run(["test", "worldnews"], per_sub_limit=150)
