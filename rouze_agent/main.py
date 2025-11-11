from pathlib import Path
import json, csv

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
PITCHES = ROOT / "pitches"
PITCHES.mkdir(exist_ok=True)

from scrapers.reddit_scraper import run as scrape_reddit
from analyzer import analyze
from pitches.pitch_generator import save_pitch_md

CFG = json.loads((ROOT / "utils" / "config.json").read_text())

def read_latest_rows(max_rows=400):
    path = LOGS / "reddit_jobs.csv"
    if not path.exists(): return []
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    # newest last in our appends; keep tail
    return rows[-max_rows:]

def choose_top(rows, k=5):
    enriched = []
    for r in rows:
        a = analyze(r)
        enriched.append((a["score"], r, a))
    enriched.sort(reverse=True, key=lambda x: x[0])
    return enriched[:k]

def main():
    print("🔎 Scanning Reddit…")
    new_jobs = scrape_reddit()
    print(f"Found {len(new_jobs)} new potential gigs.")
    rows = read_latest_rows()
    top = choose_top(rows, k=5)

    created = []
    for score, job, a in top:
        p = save_pitch_md(job, a, PITCHES)
        created.append((p.name, score, job.get("title","")))

    print("\n✅ Pitches created (top 5):")
    for name, sc, title in created:
        print(f"  [{sc:>3}] {name} — {title[:60]}")

    print("\nNext steps (manual):")
    print("1) Open the pitch .md you like and copy Variant A/B/C.")
    print("2) Post as a reply/DM or email (use contact found).")
    print("3) If client replies, switch to clarifying questions from the pitch.")
    print("4) After delivery, drop files in /deliveries and log what was accepted in /logs/accepted.txt.")

# --- Optional: auto-mockup for top design job ---
try:
    from utils.mockup_maker import quick_banner
    from utils.packager import make_delivery

    for score, job, _ in top:
        if job.get("category") == "design":
            title = (job.get("title") or "Design Concept").strip()
            out_png = quick_banner(
                "deliveries/preview_" + job.get("id", "design"),
                title,
                "invite/modern"
            )
            folder, zipf = make_delivery(
                "preview_" + job.get("id", "design"),
                [out_png],
                f"Here’s a clean preview mockup based on your brief:\n- {title}\nKept it light, modern, easy to approve."
            )
            print(f"\n🖼  Preview mockup created: {out_png}")
            print(f"📦 Delivery ZIP: {zipf}")
            break
except Exception as e:
    print(f"\n(mockup skipped) {e}")

if __name__ == "__main__":
    main()

