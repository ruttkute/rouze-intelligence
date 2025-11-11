#!/usr/bin/env python3
from pathlib import Path
from datetime import date
from weasyprint import HTML, CSS
import re, markdown
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "templates"
OUT = ROOT / "deliveries" / "portfolio"
OUT.mkdir(parents=True, exist_ok=True)

env = Environment(loader=FileSystemLoader(str(TPL)))
tpl = env.get_template("base_report.html")

def split_sections(md_text: str):
    """Return (summary_md, highlights_rows, body_md) from a Rouze-style MD."""
    # Executive Summary = first '## ' Executive Summary (or first lines)
    summary_md = ""
    highlights = []
    body_md = md_text

    # try to capture explicit summary block
    m = re.search(r"^##\s*Executive Summary.*?$([\s\S]+?)(?=^##\s|\Z)", md_text, re.M)
    if m: summary_md = m.group(1).strip()

    # Key Highlights block as table or bullets after '## Key Highlights'
    mh = re.search(r"^##\s*Key Highlights.*?$([\s\S]+?)(?=^##\s|\Z)", md_text, re.M)
    if mh:
        lines = [ln.strip("-• ").strip() for ln in mh.group(1).splitlines() if ln.strip()]
        # accept "Aspect: text" or "Aspect — text"
        for ln in lines:
            if ":" in ln:
                a, b = ln.split(":", 1)
            elif "—" in ln:
                a, b = ln.split("—", 1)
            else:
                a, b = "Note", ln
            highlights.append({"aspect": a.strip(), "text": b.strip()})

    return summary_md, highlights, md_text

def md_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=["extra", "sane_lists"])

def infer_title(md_text: str, fallback: str) -> str:
    for ln in md_text.splitlines():
        if ln.startswith("# "): return ln[2:].strip()
    return fallback

def render_one(md_path: Path, analyst="Arune R."):
    text = md_path.read_text(encoding="utf-8")
    title = infer_title(text, md_path.stem.replace("_", " ").title())
    subtitle = "Example Deliverable"

    summary_md, highlights, body_md = split_sections(text)

    # 1) Render HTML from the Jinja template
    html = tpl.render(
        title=title,
        subtitle=subtitle,
        analyst=analyst,
        date=date.today().isoformat(),
        summary_html=md_to_html(summary_md) if summary_md else "",
        highlights=highlights,
        body_html=md_to_html(body_md),
        css_path=(TPL / "style.css").as_uri(),
        footer="Rouze Portfolio",
    )

    # 2) (optional) write the HTML next to the PDF for inspection
    out_html = OUT / (md_path.stem + ".html")
    out_pdf  = OUT / (md_path.stem + ".pdf")
    out_html.write_text(html, encoding="utf-8")

    # 3) WeasyPrint: HTML -> PDF (make CSS paths resolve relative to /templates)
    HTML(string=html, base_url=str(TPL)).write_pdf(
        str(out_pdf),
        stylesheets=[CSS(filename=str(TPL / "style.css"))],
    )
    print("Saved PDF →", out_pdf)

def main():
    md_dir = ROOT / "deliveries" / "portfolio"
    # render all .md files that exist (your 01_, 02_, 03_…)
    md_files = sorted(md_dir.glob("*.md"))
    if not md_files:
        print("No MD files in", md_dir)
        return
    for md in md_files:
        render_one(md)

if __name__ == "__main__":
    main()
