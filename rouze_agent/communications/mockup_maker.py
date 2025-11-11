# utils/mockup_maker.py
import json3
from pathlib import Path
from datetime import datetime
import textwrap
from PIL import Image, ImageDraw, ImageFont

# ---------- Load style packs ----------
ROOT = Path(__file__).resolve().parents[1]
STYLES_PATH = ROOT / "utils" / "style_packs.json"
STYLES = json.loads(STYLES_PATH.read_text())

# ---------- Helpers ----------
def _load_font(name="Helvetica", size=48):
    """
    Try to load a named system font, otherwise fall back to Pillow default.
    You can later replace this to load a font file from utils/fonts/.
    """
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()

def _text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont):
    """
    Pillow 10+: use textbbox (textsize is removed).
    Returns (width, height).
    """
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]

# ---------- Main ----------
def quick_banner(out_dir, title, subtitle="", style="invite_modern", size=(1080, 1080)):
    """
    Generate a banner PNG based on a style pack.
    - out_dir: output folder
    - title: main line
    - subtitle: smaller line below title (optional)
    - style: key in style_packs.json
    - size: (W, H) in pixels
    Returns: path to the saved PNG
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # style lookup with safe fallback
    cfg = STYLES.get(style) or STYLES.get("invite_modern")
    if not cfg:
        raise KeyError(f"Style '{style}' not found and 'invite_modern' missing.")

    W, H = size

    # Support both "bg" and "background" keys
    bg = cfg.get("bg") or cfg.get("background") or "#111111"
    ink = cfg.get("ink", "#ffffff")
    accent = cfg.get("accent", "#888888")
    font_name = cfg.get("font", "Helvetica")

    img = Image.new("RGB", (W, H), bg)
    draw = ImageDraw.Draw(img)

    # Fonts (scale with width)
    title_font = _load_font(font_name, int(W * 0.08))
    sub_font = _load_font(font_name, int(W * 0.035))

    # Wrap title nicely
    wrap_width = 18 if W <= 1080 else 24
    lines = textwrap.wrap(title, width=wrap_width) or [title]

    # Draw title centered
    y = H // 3
    for line in lines:
        tw, th = _text_size(draw, line, title_font)
        draw.text(((W - tw) / 2, y), line, font=title_font, fill=ink)
        y += th + 10

    # Subtitle
    if subtitle:
        tw, th = _text_size(draw, subtitle, sub_font)
        draw.text(((W - tw) / 2, y + 20), subtitle, font=sub_font, fill=accent)

    # Save
    safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title.strip())
    out_path = out_dir / f"{safe_title}_{style}.png"
    img.save(out_path)
    return str(out_path)
