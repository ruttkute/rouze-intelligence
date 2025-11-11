import os, subprocess, sys, glob
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

def run_scraper():
    print("[run] scraping reddit hot…")
    py = sys.executable
    scraper = os.path.join(ROOT, "scrapers", "reddit_hot.py")
    subprocess.check_call([py, scraper])

def latest_csv():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "reddit_*_hot_*.csv")))
    return files[-1] if files else None

def run_analyzer(csv_path):
    # call rouze_agent/analyzer.py with the CSV path
    agent_root = os.path.abspath(os.path.join(ROOT, "..", "rouze_agent"))
    analyzer = os.path.join(agent_root, "analyzer.py")
    py = sys.executable
    print(f"[run] analyzing {csv_path} …")
    subprocess.check_call([py, analyzer, csv_path], cwd=agent_root)

if __name__ == "__main__":
    run_scraper()
    csv_path = latest_csv()
    if not csv_path:
        raise SystemExit("no CSV produced")
    run_analyzer(csv_path)
    print("[run] done.")
