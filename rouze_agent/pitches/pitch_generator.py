from pathlib import Path
from datetime import datetime
import textwrap, re

def tiny_plan(category: str):
    if category == "design":
        return ["2–3 quick concepts (invite/modern by default)", "1 round of refinements", "Final PNG + source if needed"]
    if category == "writing":
        return ["Outline first, then clean draft", "1 round of edits", "Final DOCX + plain text"]
    if category == "data entry":
        return ["Sample of 10 rows for QA", "Full pass with validation", "Neat Excel/CSV + brief notes"]
    return ["Fast draft", "Refinement", "Polished delivery"]

def humanify(s: str):
    s = s.replace("  ", " ")
    return re.sub(r'\n{3,}', '\n\n', s)

def pitch_variants(job: dict, qs: list):
    title = job.get("title","").strip()
    cat = job.get("category","general")
    link = job.get("permalink","")
    plan = tiny_plan(cat)

    base_open = f"Hey! I saw your post: “{title}”. I can take this on today and keep it clean, on-brand, and easy to approve."
    ask = "Before I start, a couple tiny checks:\n- " + "\n- ".join(qs[:3])

    v1 = f"""{base_open}

**Plan**
- {plan[0]}
- {plan[1]}
- {plan[2]}

**Why me**
Warm, precise, and quick. I mirror your tone and deliver files that slot right into your workflow.

If this feels right, send the details and I’ll begin. ({link})
"""
    v2 = f"""Hi! Loved the brief — here’s how I’d handle it fast without cutting corners.

**Approach**
• {plan[0]}
• {plan[1]}
• {plan[2]}

**Tiny clarifiers**
- {qs[0]}
- {qs[1]}
- {qs[2]}

Happy to start right away and keep updates short + visual. ({link})
"""
    v3 = f"""Hey there — quick pitch:

**You get**
1) {plan[0]}
2) {plan[1]}
3) {plan[2]}

**To confirm**
- {qs[0]}
- {qs[1]}
- {qs[2]}

I’ll keep it human, neat, and on-brand. Let’s go. ({link})
"""
    return [humanify(v1), humanify(v2), humanify(v3)]

def save_pitch_md(job: dict, analysis: dict, out_dir: Path):
    dt = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{dt}_{job.get('subreddit','reddit')}_{job.get('id','xxx')}_pitch.md"
    p = out_dir / name
    pitches = pitch_variants(job, analysis["questions"])
    body = f"""# Pitch — {job.get('title','(no title)')}

**Category:** {job.get('category','general')}  
**Budget (seen):** {job.get('budget_usd','')}  
**Link:** {job.get('permalink','')}

---

## Variant A
{pitches[0]}
---

## Variant B
{pitches[1]}
---

## Variant C
{pitches[2]}

---

**Rationale (short)**
Lead with clarity and speed. Offer 2–3 concepts or a sample first, then refine once. Delivery is tidy and ready to slot in.

"""
    p.write_text(body.strip(), encoding="utf-8")
    return p
