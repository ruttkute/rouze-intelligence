# scripts/make_cover.py
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("deliveries/portfolio"); OUT.mkdir(parents=True, exist_ok=True)

# Canvas + brand
W, H = 1600, 900
bg = (29, 21, 65)        # deep mauve
title = (162, 139, 207)  # lavender
accent = (195, 68, 100)  # rose

im = Image.new("RGB", (W, H), bg)
d = ImageDraw.Draw(im)

# Text
t1 = "Competitor Research Brief"
t2 = "Social Media Scheduling (Example)"

# Fonts (fallback safe)
try:
    f1 = ImageFont.truetype("Arial.ttf", 72)
    f2 = ImageFont.truetype("Arial.ttf", 44)
except Exception:
    f1 = ImageFont.load_default()
    f2 = ImageFont.load_default()

def text_size(draw, text, font):
    left, top, right, bottom = draw.textbbox((0,0), text, font=font)
    return right - left, bottom - top

# Measure with textbbox
w1, h1 = text_size(d, t1, f1)
w2, h2 = text_size(d, t2, f2)

# Positions
y1 = 340
y2 = y1 + h1 + 40

# Draw
d.text(((W - w1)//2, y1), t1, fill=title, font=f1)
d.text(((W - w2)//2, y2), t2, fill=accent, font=f2)

out = OUT / "cover_competitor_brief.png"
im.save(out)
print("Saved:", out)
