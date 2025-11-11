# scripts/deliver_case_study.py
from pathlib import Path
from typing import Optional, List, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, KeepTogether, Preformatted)

PORTFOLIO = Path("deliveries/portfolio")
PORTFOLIO.mkdir(parents=True, exist_ok=True)

BRAND = {
    "bg":       colors.Color(0.11, 0.08, 0.23),   # deep mauve (#1B153B)
    "primary":  colors.Color(0.64, 0.55, 0.81),   # lavender (#A38DCE)
    "accent":   colors.Color(0.76, 0.27, 0.39),   # rose (#C24464)
    "text":     colors.black,
    "gray":     colors.Color(0.96, 0.96, 0.98),
}

def _styles():
    base = getSampleStyleSheet()
    base["Normal"].fontSize = 10
    base["Normal"].leading = 14

    h1 = ParagraphStyle(
        "H1", parent=base["Heading1"],
        fontSize=20, leading=24, textColor=BRAND["primary"],
        spaceAfter=10, spaceBefore=6)
    h2 = ParagraphStyle(
        "H2", parent=base["Heading2"],
        fontSize=14, leading=18, textColor=BRAND["accent"],
        spaceBefore=12, spaceAfter=6)
    body = ParagraphStyle("Body", parent=base["Normal"])
    mono = ParagraphStyle("Code", parent=base["Code"], fontSize=9, leading=12)
    caption = ParagraphStyle("Caption", parent=base["Normal"], fontSize=8, textColor=colors.grey)
    return {"H1": h1, "H2": h2, "Body": body, "Code": mono, "Caption": caption}

STY = _styles()

def _title_page(title: str, subtitle: str, analyst: str, cover_img: Optional[Path]) -> List:
    flow = []
    # Optional cover image at top
    if cover_img and Path(cover_img).exists():
        img = Image(str(cover_img), width=14*cm, height=7.5*cm)
        flow += [img, Spacer(1, 0.6*cm)]

    flow += [
        Paragraph(title, STY["H1"]),
        Paragraph(subtitle, STY["H2"]),
        Spacer(1, 0.5*cm),
        Paragraph(f"<b>Analyst:</b> {analyst}", STY["Body"]),
        Spacer(1, 0.2*cm),
    ]
    flow.append(PageBreak())
    return flow

def _key_table(rows: List[Tuple[str, str]]) -> Table:
    tbl = Table([["Aspect", "Highlights"]] + rows, colWidths=[4.0*cm, 12.5*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BRAND["primary"]),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,0), "LEFT"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BRAND["gray"], colors.white]),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("GRID", (0,0), (-1,-1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    return tbl

def parse_markdown(md_path: Path):
    """Very light MD: first line starting with # is title; next heading (##) becomes section; the rest becomes body."""
    text = md_path.read_text(encoding="utf-8")
    lines = [ln.rstrip() for ln in text.splitlines()]
    title = ""
    sections = []  # list of (heading, body_text)

    buf, current = [], None
    for ln in lines:
        if ln.startswith("# "):
            title = ln[2:].strip()
        elif ln.startswith("## "):
            if current:
                sections.append((current, "\n".join(buf).strip()))
                buf = []
            current = ln[3:].strip()
        else:
            buf.append(ln)
    if current:
        sections.append((current, "\n".join(buf).strip()))

    return title or md_path.stem.replace("_", " ").title(), sections

def render_pdf(md_path: Path,
               analyst: str = "Arune R. — Market Intelligence & Competitor Research",
               cover_img: Optional[Path] = None,
               out_pdf: Optional[Path] = None) -> Path:
    md_path = Path(md_path)
    assert md_path.exists(), f"Markdown not found: {md_path}"
    title, sections = parse_markdown(md_path)

    if out_pdf is None:
        out_pdf = PORTFOLIO / (md_path.stem + ".pdf")

    doc = SimpleDocTemplate(str(out_pdf), pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    story = []
    # Title page
    story += _title_page(
        title=title,
        subtitle="Social Media Scheduling — Example Deliverable",
        analyst=analyst,
        cover_img=cover_img,
    )

    # Executive Summary (if present)
    # Look for a section that starts with "Executive Summary" or first section as summary
    if sections:
        h, b = sections[0]
        if "summary" in h.lower():
            story += [Paragraph("Executive Summary", STY["H2"]),
                      Paragraph(b.replace("\n", "<br/>"), STY["Body"]),
                      Spacer(1, 0.4*cm)]
            sections = sections[1:]

    # Key Highlights table (optional, derives from bullets like '- item: text')
    highlights = []
    if sections:
        # very light extraction: look for bullet lines " - Key: value"
        for h, b in sections:
            for ln in b.splitlines():
                if ":" in ln and ln.strip().startswith(("-", "*")):
                    k, v = ln.split(":", 1)
                    highlights.append((k.lstrip("-* ").strip(), v.strip()))
    if highlights:
        story += [Paragraph("Key Highlights", STY["H2"]),
                  _key_table(highlights[:8]), Spacer(1, 0.4*cm)]

    # Sections
    for h, b in sections:
        story += [KeepTogether([
            Paragraph(h, STY["H2"]),
            Paragraph(b.replace("\n", "<br/>"), STY["Body"]),
            Spacer(1, 0.3*cm),
        ])]

    # If the MD had code blocks or raw bullets you want to preserve exactly, append as Preformatted:
    # story += [Paragraph("Appendix (raw notes)", STY["H2"]),
    #           Preformatted(Path("data/raw/portfolio/seed.json").read_text(), STY["Code"])]

    doc.build(story)
    print(f"Saved PDF -> {out_pdf}")
    return out_pdf

if __name__ == "__main__":
    # Auto-render the three MD files you already generate
    cover = PORTFOLIO / "cover_competitor_brief.png"
    for md in sorted(PORTFOLIO.glob("*.md")):
        render_pdf(md, cover_img=cover)
