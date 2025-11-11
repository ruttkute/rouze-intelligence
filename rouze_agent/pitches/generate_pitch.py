import os, sys, json, textwrap
from datetime import datetime
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.style_mimic import analyze_style, update_style, log_convo, slugify

PITCH_DIR = Path("pitches/generated")
PITCH_DIR.mkdir(parents=True, exist_ok=True)

def load_last_payload():
    logp = Path("logs/last_run.json")
    if not logp.exists():
        return None
    return json.loads(logp.read_text())

def style_wrap(lines, prefers_bullets):
    if prefers_bullets:
        return "\n".join([f"- {l}" for l in lines])
    else:
        return "\n".join([textwrap.fill(l, width=100) for l in lines])

def build_pitch(client_name, job_text, payload):
    style = analyze_style(job_text)
    update_style(client_name, style)
    greeting = style["greeting"]
    signoff = style["signoff"]
    tones = style["tones"]
    prefers_bullets = style["prefers_bullets"]

    # pull insights from last_run (safe defaults)
    topics = (payload or {}).get("payload", {}).get("reddit_topics", []) if payload else []
    cons = (payload or {}).get("payload", {}).get("review_cons", []) if payload else []
    rows = (payload or {}).get("payload", {}).get("reddit_rows", 0) if payload else 0
    reviews_rows = (payload or {}).get("payload", {}).get("reviews_rows", 0) if payload else 0
    brief_path = (payload or {}).get("brief", "Rouze_Insight_Brief_Sample.md")

    # messaging knobs
    title = "Market & Customer Research for Beauty Brands (48h Insight Brief)"
    if "formal" in tones:
        title = "Beauty Market & Customer Research — 48-Hour Executive Insight Brief"
    if "concise" in tones:
        title = "48h Insight Brief: Beauty Market & Customer Research"

    opener = f"{greeting} {client_name}," if client_name.strip() else f"{greeting},"
    one_liner = "I help beauty brands make faster, smarter decisions with focused market and customer research."

    body_points = [
        "Customer insights: what real buyers praise & complain about in recent product reviews (Amazon/Sephora).",
        "Market signals: what beauty communities are buzzing about right now (Reddit/TikTok).",
        "Competitor scan: standout claims, angles, and pricing that matter."
    ]

    proof = f"Last scan covered {rows} community posts and {reviews_rows} recent reviews; sample brief: {os.path.basename(brief_path)}."
    offer = "You’ll get a 2-page Insight Brief in 48h (starter: $75) with 3–5 findings and a clear “So what / Now what” section."
    close = "If helpful, reply “GO” and I’ll start today."

    # adapt tone
    if "warm" in tones:
        one_liner = "I translate real customer voices and live market chatter into clear, useful decisions for your team."
    if "technical" in tones:
        body_points[1] = "Market signals: community data (Reddit) with light sentiment/theme analysis."

    msg = f"""Title: {title}

{opener}

{one_liner}

{style_wrap(body_points, prefers_bullets)}

{proof}
{offer}

{close}
{signoff},
Arune (Rouze)
"""
    return msg, style

def main():
    if len(sys.argv) < 3:
        print("usage: python pitches/generate_pitch.py '<Client Name>' /path/to/job_post.txt")
        sys.exit(1)

    client_name = sys.argv[1]
    job_path = sys.argv[2]
    job_text = Path(job_path).read_text(encoding="utf-8")

    payload = load_last_payload()
    msg, style = build_pitch(client_name, job_text, payload)

    # save
    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out = PITCH_DIR / f"{slugify(client_name)}_{ts}.md"
    out.write_text(msg, encoding="utf-8")

    # log conversation
    log_convo(client_name, "client_post", job_text)
    log_convo(client_name, "pitch_draft", msg)

    print(f"[pitch] style={style['tones']} bullets={style['prefers_bullets']} -> {out}")

if __name__ == "__main__":
    main()
