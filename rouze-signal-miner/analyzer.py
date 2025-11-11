import os, sys, json
from datetime import datetime
import pandas as pd

# ---------- utils ----------
def ensure_dirs():
    for d in ["deliveries", "pitches", "logs", "data"]:
        os.makedirs(d, exist_ok=True)

def load_csv(path):
    df = pd.read_csv(path)
    # basic cleaning
    df["text"] = (df["title"].fillna("") + " " + df["selftext"].fillna("")).str.strip()
    df = df[df["text"].str.len()>0].copy()
    return df

def simple_sentiment(df):
    # ultra-light lexicon (no heavy installs)
    pos = set(["good","great","love","win","help","amazing","awesome","profit","clear","easy","fast","best"])
    neg = set(["bad","hate","fail","risk","slow","low","hard","bug","issue","problem","confused","expensive"])
    def score(t):
        t=t.lower()
        s = sum(w in t for w in pos) - sum(w in t for w in neg)
        return s
    df["sent_score"] = df["text"].astype(str).map(score)
    return df

def extract_topics(df, top_n=8):
    # crude keyword frequency (MVP)
    import re
    STOP = set(("the a an to of and for with on in by from is are was were be being been i you they we he she it or as at this that those these".split()))
    words = []
    for t in df["text"].tolist():
        words += [w for w in re.findall(r"[a-zA-Z]{4,}", str(t).lower()) if w not in STOP]
    s = pd.Series(words).value_counts().head(top_n)
    return s.index.tolist()

def business_implications(df):
    # transform observations into "so what?"
    avg = df["sent_score"].mean()
    vol = int(df.shape[0])
    topk = extract_topics(df, top_n=6)
    bullets = []
    if avg < 0:
        bullets.append("Market mood skews negative → pitch **problem-solving** and **clarity**.")
    else:
        bullets.append("Market mood is neutral/positive → pitch **speed** and **leverage** themes.")
    bullets.append(f"Volume: {vol} recent posts scanned → real demand exists right now.")
    bullets.append(f"Hot topics people mention: {', '.join(topk)}.")
    bullets.append("Lead magnet idea: a 2-page **signal brief** from Reddit hot threads for the client’s niche.")
    bullets.append("Offer: scrape → analyze → 2-page brief in 48h, starter price $75.")
    return bullets

def write_brief(insights, src_csv):
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out = os.path.join("deliveries", f"Rouze_Insight_Brief_{ts}.md")
    df_info = f"- Source CSV: `{os.path.basename(src_csv)}`\n- Rows analyzed: {insights['rows']}\n"
    content = f"""# Rouze Insight Brief — MVP

## Executive Summary
This brief turns **raw Reddit signals** into actionable insights for client acquisition and offer design.

{df_info}

## Key Findings
- Average sentiment score: {insights['avg_sent']:.2f}
- Top topics: {", ".join(insights['topics'])}

## So What? (Business Implications)
""" + "\n".join([f"- {b}" for b in insights["bullets"]]) + """

## Now What? (Recommended Next Steps)
1) Use these topics to frame outreach hooks.
2) Offer a $75 “signal snapshot” (48h) to start relationships.
3) Collect testimonials, then scale to weekly dashboards/retainers.
"""
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    return out

def write_pitch(insights, brief_path):
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out = os.path.join("pitches", f"Pitch_{ts}.md")
    hooks = ", ".join(insights["topics"][:3])
    body = f"""Subject: I turn raw Reddit signals into quick wins for your niche

Hi — I analyze **real, unfiltered conversations** and distill them into a 2-page brief you can act on immediately.

**What I just observed:** {hooks} are trending in your space; sentiment average = {insights['avg_sent']:.2f} across {insights['rows']} fresh posts.

**Offer:** I’ll deliver a 2-page **Signal Snapshot** in 48h for **$75**:
- scrape relevant threads
- extract themes + sentiment
- give you “so what / now what” actions

Here’s a sample brief I just generated: {os.path.basename(brief_path)}

If useful, reply “GO” and I’ll start today.
— Arune (Rouze)
"""
    with open(out, "w", encoding="utf-8") as f:
        f.write(body)
    return out

# ---------- main ----------
if __name__ == "__main__":
    ensure_dirs()
    if len(sys.argv) < 2:
        raise SystemExit("usage: python analyzer.py /path/to/reddit_*.csv")

    src_csv = sys.argv[1]
    df = load_csv(src_csv)
    df = simple_sentiment(df)
    avg = float(df["sent_score"].mean())
    topics = extract_topics(df, top_n=6)
    bullets = business_implications(df)

    insights = {
        "rows": int(df.shape[0]),
        "avg_sent": avg,
        "topics": topics,
        "bullets": bullets
    }

    brief = write_brief(insights, src_csv)
    pitch = write_pitch(insights, brief)

    log_path = os.path.join("logs", "last_run.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "source_csv": src_csv,
            "brief": brief,
            "pitch": pitch,
            "insights": insights
        }, f, indent=2)

    print(f"[agent] brief -> {brief}")
    print(f"[agent] pitch -> {pitch}")
