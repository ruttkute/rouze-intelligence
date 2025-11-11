import os, sys, json, re, textwrap
from datetime import datetime
from pathlib import Path

# local imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.style_mimic import get_client_profile, analyze_style, update_style, log_convo, slugify

OUT_DIR = Path("pitches/replies")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_last_payload():
    p = Path("logs/last_run.json")
    return json.loads(p.read_text()) if p.exists() else {}

def detect_intent(msg: str):
    m = msg.lower()
    intents = set()
    if any(k in m for k in ["competitor", "competition", "compare", "benchmark"]):
        intents.add("competitors")
    if any(k in m for k in ["price", "budget", "cost", "$"]):
        intents.add("pricing")
    if any(k in m for k in ["timeline", "how fast", "deadline", "turnaround", "48h"]):
        intents.add("timeline")
    if any(k in m for k in ["sample", "example", "portfolio", "work sample", "case study"]):
        intents.add("samples")
    if any(k in m for k in ["scope", "deliverable", "what do i get", "what will i get"]):
        intents.add("scope")
    if any(k in m for k in ["nda", "confidential", "privacy", "private"]):
        intents.add("nda")
    if any(k in m for k in ["revision", "edit", "changes"]):
        intents.add("revisions")
    if any(k in m for k in ["call", "zoom", "meet"]):
        intents.add("call")
    return intents or {"general"}

def wrap(lines, bullets=False):
    if bullets:
        return "\n".join(f"- {l}" for l in lines)
    return "\n\n".join(textwrap.fill(l, width=96) for l in lines)

def tone_headers(style):
    greeting = style.get("greeting") or "Hi"
    signoff  = style.get("signoff") or "Best"
    return greeting, signoff

def build_sections(intents, style, payload):
    prefers_bullets = style.get("prefers_bullets", False)
    rows = (payload.get("payload", {}) or {}).get("reddit_rows", 0)
    reviews_rows = (payload.get("payload", {}) or {}).get("reviews_rows", 0)
    topics = (payload.get("payload", {}) or {}).get("reddit_topics", [])[:3]
    cons = (payload.get("payload", {}) or {}).get("review_cons", [])[:3]
    brief = payload.get("brief", "Rouze_Insight_Brief_Sample.md")

    sections = []

    if "scope" in intents or "general" in intents:
        sections.append(wrap([
            "Here’s what I deliver in the 48-hour Insight Brief:",
            "• Market & customer research focused on your beauty niche.",
            "• 3–5 key findings (customer pain points, trends, competitor signals).",
            "• Short evidence (review quotes, community chatter).",
            "• A clear “So what / Now what” section with 3 actions."
        ], bullets=False if prefers_bullets else False))

    if "competitors" in intents:
        sections.append(wrap([
            "Competitor coverage (MVP): top 3–5 brands in your space, their standout claims, pricing cues, and one thing to copy or counter next."
        ], bullets=False))

    if "timeline" in intents:
        sections.append(wrap([
            "Turnaround: 48 hours from ‘GO’. Day 1 = data collection, Day 2 = synthesis + brief. If you’d like a 24-hour rush, I can do that for an extra $25."
        ]))

    if "pricing" in intents:
        sections.append(wrap([
            "Starter project: $75 for a 2-page Insight Brief.",
            "Optional add-ons:",
            "• Extra SKUs or competitors (+$25 each).",
            "• Follow-up working session to apply insights (+$40 / 30 mins)."
        ], bullets=True if prefers_bullets else False))

    if "samples" in intents:
        sections.append(wrap([
            f"Recent scan covered {rows} community posts and {reviews_rows} buyer reviews.",
            f"I’ve attached a sample format: {os.path.basename(brief)}."
        ]))

    if "nda" in intents:
        sections.append(wrap([
            "I’m happy to sign your NDA. I only use public data and keep client materials private. I can work inside a shared drive if you prefer."
        ]))

    if "revisions" in intents:
        sections.append(wrap([
            "One tight revision is included (clarifications or small tweaks). Bigger scope changes usually mean new data, which we can price simply."
        ]))

    if "call" in intents:
        sections.append(wrap([
            "If a quick call helps, I can do a 10-minute kickoff to confirm products/competitors and success criteria."
        ]))

    # proof / personalization footer
    if topics or cons:
        sections.append(wrap([
            f"From this week’s signals: topics trending = {', '.join(topics) or '—'};",
            f"top buyer frictions = {', '.join(cons) or '—'}.",
            "I’ll adapt the brief to your exact SKUs and competitor set."
        ]))

    return "\n\n".join(sections)

def generate_reply(client_name: str, client_message: str):
    profile = get_client_profile(client_name)
    # blend stored style with fresh read (people change tone)
    fresh = analyze_style(client_message)
    style = fresh
    update_style(client_name, style)

    intents = detect_intent(client_message)
    payload = load_last_payload()

    greeting, signoff = tone_headers(style)
    opener = f"{greeting} {client_name}," if client_name.strip() else f"{greeting},"
    body = build_sections(intents, style, payload)
    closer = "If this works, reply “GO” and I’ll lock the 48-hour window." if "concise" in style.get("tones", []) else \
             "If this fits, reply “GO” and I’ll confirm timing and start immediately."

    msg = f"""{opener}

{body}

{closer}
{signoff},
Arune (Rouze)
"""
    return msg, style, intents

def main():
    if len(sys.argv) < 3:
        print('usage: python pitches/reply_generator.py "<Client Name>" /path/to/client_message.txt')
        sys.exit(1)

    client = sys.argv[1]
    path = Path(sys.argv[2])
    text = path.read_text(encoding="utf-8")

    msg, style, intents = generate_reply(client, text)

    ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out = OUT_DIR / f"{slugify(client)}_{ts}.md"
    out.write_text(msg, encoding="utf-8")

    log_convo(client, "client_msg", text)
    log_convo(client, "reply_draft", msg)

    print(f"[reply] tones={style.get('tones')} intents={sorted(list(intents))} -> {out}")

if __name__ == "__main__":
    main()
