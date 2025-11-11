import os, re, json, hashlib
from datetime import datetime
from pathlib import Path

CLIENT_DIR = Path("pitches/clients")
CLIENT_DIR.mkdir(parents=True, exist_ok=True)

def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower()).strip("-")
    if not s:
        s = hashlib.md5(name.encode("utf-8")).hexdigest()[:8]
    return s

def analyze_style(text: str) -> dict:
    # basic features
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [s for s in sentences if s]
    words = re.findall(r"\b\w+\b", text)
    avg_sent_len = (sum(len(s.split()) for s in sentences) / max(1, len(sentences)))
    exclam = text.count("!")
    qmarks = text.count("?")
    emojis = len(re.findall(r"[\U0001F300-\U0001FAFF]", text))
    bullets = len(re.findall(r"(^|\n)\s*[-•*]\s+", text))
    caps_ratio = sum(1 for c in text if c.isupper()) / max(1, sum(1 for c in text if c.isalpha()))
    url_count = len(re.findall(r"https?://", text))
    first_person = len(re.findall(r"\bI\b|\bwe\b|\bour\b", text, flags=re.I))
    jargon_hits = len(re.findall(r"\bmarket research|competitor|insights?|kpi|roi|funnel|positioning|benchmark|sentiment\b", text, re.I))

    # label rules (simple, effective)
    tone = []
    if avg_sent_len <= 14 and bullets >= 1:
        tone.append("concise")
    if avg_sent_len > 20 or jargon_hits >= 2:
        tone.append("formal")
    if emojis or exclam >= 2:
        tone.append("warm")
    if caps_ratio > 0.12 or exclam >= 3:
        tone.append("salesy")
    if url_count > 0 or "api" in text.lower():
        tone.append("technical")
    if not tone:
        tone = ["neutral"]

    # preferred structure
    prefers_bullets = bullets > 0 or avg_sent_len < 18
    greeting = "Hi" if "warm" in tone or "concise" in tone else "Hello"
    signoff = "Best" if "formal" in tone else "Cheers" if "warm" in tone else "Thanks"

    return {
        "avg_sentence_len": round(avg_sent_len, 2),
        "exclam": exclam,
        "qmarks": qmarks,
        "emojis": emojis,
        "bullets": bullets,
        "caps_ratio": round(caps_ratio, 3),
        "url_count": url_count,
        "first_person": first_person,
        "jargon_hits": jargon_hits,
        "tones": tone,
        "prefers_bullets": prefers_bullets,
        "greeting": greeting,
        "signoff": signoff,
    }

def get_client_profile(client_name: str) -> dict:
    cid = slugify(client_name)
    fp = CLIENT_DIR / cid / "profile.json"
    if fp.exists():
        return json.loads(fp.read_text())
    return {"client_id": cid, "name": client_name, "history": [], "style": None}

def save_client_profile(profile: dict):
    cid = profile["client_id"]
    pdir = CLIENT_DIR / cid
    pdir.mkdir(parents=True, exist_ok=True)
    (pdir / "profile.json").write_text(json.dumps(profile, indent=2))

def log_convo(client_name: str, role: str, text: str):
    profile = get_client_profile(client_name)
    entry = {"ts": datetime.utcnow().isoformat(), "role": role, "text": text}
    profile["history"].append(entry)
    save_client_profile(profile)

def update_style(client_name: str, style_dict: dict):
    profile = get_client_profile(client_name)
    profile["style"] = style_dict
    save_client_profile(profile)
    return profile
