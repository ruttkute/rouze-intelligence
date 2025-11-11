import os, sys, json, re
from datetime import datetime
import pandas as pd

# ---------- utils ----------
def ensure_dirs():
    for d in ["deliveries", "pitches", "logs", "data"]:
        os.makedirs(d, exist_ok=True)

def load_reddit_csv(path):
    df = pd.read_csv(path)
    df["text"] = (df["title"].fillna("") + " " + df["selftext"].fillna("")).str.strip()
    df = df[df["text"].str.len()>0].copy()
    df["source"] = "reddit"
    return df

def load_amazon_csv(paths):
    frames = []
    for p in paths:
        if p and os.path.exists(p):
            frames.append(pd.read_csv(p))
    if not frames:
        return pd.DataFrame(columns=["text","rating","asin","source"])
    df = pd.concat(frames, ignore_index=True)
    df["text"] = df["text"].fillna("").astype(str).str.strip()
    df = df[df["text"].str.len()>0].copy()
    # coerce rating
    with pd.option_context('mode.chained_assignment', None):
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df["source"] = "amazon"
    return df

def simple_sentiment(df):
    pos = {"good","great","love","glow","smooth","clear","fast","soft","best","works","improve","help","amazing"}
    neg = {"bad","hate","fail","irritate","burn","breakout","breakouts","rash","sticky","greasy","pill","peel","leak","smell","headache","expensive"}
    def score(t):
        t=t.lower()
        return sum(w in t for w in pos) - sum(w in t for w in neg)
    df["sent_score"] = df["text"].astype(str).map(score)
    return df

def top_words(texts, n=8, extra_stop=None):
    STOP = set(("the a an to of and for with on in by from is are was were be being been you your they them we us our it this that those these very just more have has had into out over under than will would could should might can".split()))
    if extra_stop: STOP |= set(extra_stop)
    words=[]
    for t in texts:
        words += re.findall(r"[a-zA-Z]{4,}", str(t).lower())
    words = [w for w in words if w not in STOP]
    return pd.Series(words).value_counts().head(n)

def review_drivers(df, topn=5):
    # Pros/cons by rating + simple keyword frequency
    pros = df[df["rating"]>=4.0] if "rating" in df else df.head(0)
    cons = df[df["rating"]<=2.0] if "rating" in df else df.head(0)
    pros_kw = top_words(pros["text"].tolist(), n=topn, extra_stop={"skin","face","time","product"})
    cons_kw = top_words(cons["text"].tolist(), n=topn, extra_stop={"skin","face","time","product"})
    return pros_kw.index.tolist(), cons_kw.index.tolist()

def business_implications(reddit_df, reviews_df):
    bullets=[]
    # Reddit summary
    r_avg = float(reddit_df["sent_score"].mean()) if not reddit_df.empty else 0.0
    r_topics = top_words(reddit_df["text"].tolist(), n=6).index.tolist() if not reddit_df.empty else []
    bullets.append(f"Community buzz favors **{('positive' if r_avg>0 else 'neutral/negative')}** sentiment; hot topics: {', '.join(r_topics[:4])}.")

    if not reviews_df.empty:
        pros, cons = review_drivers(reviews_df, topn=5)
        nrev = int(reviews_df.shape[0])
        avg_rating = float(reviews_df["rating"].mean()) if "rating" in reviews_df else None
        bullets.append(f"Reviews reality (n={nrev}, avg rating={avg_rating:.2f}): pros = {', '.join(pros[:3])}; cons = {', '.join(cons[:3])}.")
        # Cross-signal
        cross=[]
        if any("sticky" in c for c in cons) or any("greasy" in c for c in cons):
            cross.append("Buzz wants ‘glass skin’, but reviews flag **stickiness/greasy feel** → position ‘glass finish, zero stickiness’.")
        if any("fragrance" in c for c in cons) or any("smell" in c for c in cons):
            cross.append("Complaints about **fragrance** → offer fragrance-free variant or message ‘no added fragrance’.")
        if any("pump" in c or "leak" in c for c in cons):
            cross.append("Packaging pain (**pump/leaks**) → fix cap/pump and add ‘leak-proof’ to PDP.")
        if cross:
            bullets += cross
    else:
        bullets.append("No review data yet → add 1–2 SKUs to validate community buzz against buyer truth.")

    return r_avg, r_topics, bullets

def write_brief(payload):
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out = os.path.join("deliveries", f"Rouze_Beauty_Insight_Brief_{ts}.md")
    content = f"""# Beauty E-Commerce Insight Brief — MVP

## Executive Summary
- Community buzz (Reddit) sentiment avg: {payload['reddit_avg']:.2f}; hot topics: {", ".join(payload['reddit_topics'][:4])}
- Reviews reality: {payload['reviews_summary']}
- **Now:** 3 quick actions at the end.

## Signal Map — Reddit Buzz
- Sources: {payload['reddit_src']}
- Posts analyzed: {payload['reddit_rows']}
- Top topics: {", ".join(payload['reddit_topics'])}
- Sentiment (rough): {payload['reddit_avg']:.2f}

## Review Reality — Amazon
- Files: {", ".join(payload['amazon_files']) if payload['amazon_files'] else "—"}
- Reviews analyzed: {payload['reviews_rows']}
- Pros (top): {", ".join(payload['review_pros'][:5]) if payload['review_pros'] else "—"}
- Cons (top): {", ".join(payload['review_cons'][:5]) if payload['review_cons'] else "—"}

## Cross-Signal Insights (Buzz ≠ Buyer Truth)
""" + "\n".join([f"- {b}" for b in payload["bullets"]]) + """

## Now What — 3 Fast Actions (7–14 days)
1) PDP copy: Lead with one buzz topic + one review-based friction remover (e.g., “glass finish, zero stickiness”).
2) Creative test: UGC hook addressing #1 con (e.g., “No fragrance headache”); A/B on landing + ads.
3) Quick fix: Packaging/claim tweak if applicable (e.g., leak-proof pump) and measure refund rate shift.

*Metrics to watch:* PDP CTR change, review sentiment tilt, refund/return reasons.
"""
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    return out

def write_pitch(payload, brief_path):
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out = os.path.join("pitches", f"Beauty_Pitch_{ts}.md")
    hooks = ", ".join(payload["reddit_topics"][:3])
    body = f"""Subject: Fast beauty insights from real buyers & communities (48h)

Hi — I combine **community buzz** (Reddit) with **buyer truth** (recent Amazon reviews) to spot what to say and fix next.

What I’m seeing now: {hooks} drive conversation, while reviews flag top frictions like {", ".join(payload["review_cons"][:2]) if payload["review_cons"] else "packaging/fragrance"}.

I’ll deliver a 2-page **Signal Snapshot** in 48h for **$75**:
- scrape 2–3 relevant subs + 1–2 of your SKUs’ reviews
- distill themes & friction drivers
- give you “so what / now what” actions (copy, creative, quick fixes)

Sample brief generated today: {os.path.basename(brief_path)}
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
        raise SystemExit("usage: python analyzer.py /path/to/reddit_*.csv [/path/to/amazon_*.csv ...]")

    # inputs
    reddit_csv = sys.argv[1]
    amazon_csvs = sys.argv[2:]

    r_df = load_reddit_csv(reddit_csv)
    r_df = simple_sentiment(r_df)
    a_df = load_amazon_csv(amazon_csvs)

    r_avg, r_topics, bullets = business_implications(r_df, a_df)

    # reviews summary
    if not a_df.empty:
        pros, cons = review_drivers(a_df, topn=5)
        reviews_summary = f"n={int(a_df.shape[0])}, avg rating={a_df['rating'].mean():.2f}"
    else:
        pros, cons = [], []
        reviews_summary = "no SKU reviews included yet"

    payload = {
        "reddit_src": os.path.basename(reddit_csv),
        "reddit_rows": int(r_df.shape[0]),
        "reddit_avg": float(r_avg),
        "reddit_topics": r_topics,
        "amazon_files": [os.path.basename(x) for x in amazon_csvs],
        "reviews_rows": int(a_df.shape[0]),
        "review_pros": pros,
        "review_cons": cons,
        "reviews_summary": reviews_summary,
        "bullets": bullets
    }

    brief = write_brief(payload)
    pitch = write_pitch(payload, brief)

    log_path = os.path.join("logs", "last_run.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({"inputs": [reddit_csv] + amazon_csvs, "brief": brief, "pitch": pitch, "payload": payload}, f, indent=2)

    print(f"[agent] brief -> {brief}")
    print(f"[agent] pitch -> {pitch}")
