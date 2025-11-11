from pathlib import Path
from datetime import datetime, timezone, timedelta
import csv, json, re, time
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "utils" / "config.json").read_text())

LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)
CSV_PATH = LOGS / "reddit_jobs.csv"

HEADERS = {"User-Agent": "Mozilla/5.0 (Rouze/1.0)"}

def fetch_json(url: str):
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def scrape_sub(sub: str, limit: int):
    url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit}"
    try:
        data = fetch_json(url)
    except (URLError, HTTPError):
        return []

    items = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        items.append({
            "id": d.get("id"),
            "subreddit": sub,
            "title": (d.get("title") or "").strip(),
            "selftext": (d.get("selftext") or "").strip(),
            "author": d.get("author"),
            "permalink": "https://www.reddit.com" + d.get("permalink", ""),
            "created_utc": d.get("created_utc", 0),
            "url": d.get("url_overridden_by_dest") or ""
        })
    return items

def load_seen_ids():
    if not CSV_PATH.exists():
        return set()
    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        return {row["id"] for row in csv.DictReader(f)}

BUDGET_RE = re.compile(r'(?:(?:usd|\$)\s*|)\b(\d{1,4})(?:\s*-\s*\d{1,4})?\b', re.I)
EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
DISCORD_RE = re.compile(r'discord(?:app)?\.com\/users\/\d+|discord\s*:\s*[\w#]{2,}|@[\w]{2,}#\d{4}', re.I)
TG_RE = re.compile(r'(?:t\.me\/|telegram\.me\/|telegram\s*@)([\w_]{3,})', re.I)

def parse_budget(text: str):
    m = BUDGET_RE.search(text or "")
    return int(m.group(1)) if m else None

def detect_contacts(text: str):
    return {
        "email": (EMAIL_RE.search(text or "") or [None])[0],
        "discord": (DISCORD_RE.search(text or "") or [None])[0],
        "telegram": (TG_RE.search(text or "") or [None])[0]
    }

def detect_category(text: str):
    t = (text or "").lower()
    if any(k in t for k in ["logo","poster","banner","thumbnail","flyer","figma","canva","brand"]):
        return "design"
    if any(k in t for k in ["copy","bio","article","blog","about","caption","product description"]):
        return "writing"
    if any(k in t for k in ["data entry","excel","spreadsheet","csv","clean","format"]):
        return "data entry"
    return "general"

def allowed(text: str):
    t = (text or "").lower()
    if any(b.lower() in t for b in CFG["blacklist"]):
        return False
    if any(x in t for x in CFG["keywords"]["exclude"]):
        return False
    return True

def in_window(ts_utc: float):
    dt = datetime.fromtimestamp(ts_utc, tz=timezone.utc)
    return (datetime.now(timezone.utc) - dt) <= timedelta(hours=CFG["scan"]["recency_hours"])

def save_rows(rows):
    write_header = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "id","subreddit","title","selftext","author","permalink","created_iso",
            "category","budget_usd","email","discord","telegram"
        ])
        if write_header: w.writeheader()
        for r in rows:
            w.writerow(r)

def run():
    seen = load_seen_ids()
    collected = []
    for sub in CFG["scan"]["subreddits"]:
        posts = scrape_sub(sub, CFG["scan"]["limit_per_sub"])
        for p in posts:
            if p["id"] in seen: 
                continue
            if not in_window(p["created_utc"]): 
                continue
            body = f"{p['title']}\n{p['selftext']}"
            if not allowed(body): 
                continue
            cat = detect_category(body)
            budget = parse_budget(body)
            contacts = detect_contacts(body)
            created_iso = datetime.fromtimestamp(p["created_utc"], tz=timezone.utc).isoformat()
            collected.append({
                "id": p["id"],
                "subreddit": p["subreddit"],
                "title": p["title"],
                "selftext": p["selftext"],
                "author": p["author"],
                "permalink": p["permalink"],
                "created_iso": created_iso,
                "category": cat,
                "budget_usd": budget or "",
                "email": contacts["email"] or "",
                "discord": contacts["discord"] or "",
                "telegram": contacts["telegram"] or ""
            })
        time.sleep(0.9)  # be polite
    if collected:
        save_rows(collected)
    return collected

if __name__ == "__main__":
    out = run()
    print(f"New jobs saved: {len(out)}")
