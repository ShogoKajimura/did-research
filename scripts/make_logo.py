#!/usr/bin/env python3
"""
Re-render the BS-lab title-figure PDF at high zoom, replace the white
background with transparency, and recolor the grey strokes to accent-deep
so the logo blends with the site's sage palette.

Source PDF must be downloaded (materialized) before running.
"""
import os
import fitz
from PIL import Image

SRC = "/Users/shogo/Dropbox/a6_KIT/BS研究室/ロゴ/スライドタイトル図.pdf"
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

ACCENT_DEEP = (0x16, 0x4b, 0x53)  # #164b53

# Render at 10x zoom => ~720 DPI for crispness at any size
doc = fitz.open(SRC)
page = doc[0]
zoom = 10
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat, alpha=True)
img = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
print(f"rendered: {img.size}")

# Trim transparent margin so the logo packs tight in any container
bbox = img.getbbox()
img = img.crop(bbox)
print(f"trimmed: {img.size}")

# Walk pixels: turn the white-ish bg transparent, recolor the grey strokes
W, H = img.size
px = img.load()
ar, ag, ab = ACCENT_DEEP
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        # White-ish background -> transparent
        if r > 240 and g > 240 and b > 240:
            px[x, y] = (0, 0, 0, 0)
            continue
        # Grey strokes (R≈G≈B, any luminance < 240) -> solid accent_deep
        # Use original luminance as alpha modulator so anti-aliased edges stay smooth.
        mx, mn = max(r, g, b), min(r, g, b)
        if mx - mn < 20:
            luminance = (r + g + b) / 3
            # darker pixel -> higher alpha; light grey -> proportionally lower alpha
            mod = max(0, (240 - luminance) / 240)
            new_a = int(a * (0.55 + 0.45 * mod))  # keep mid-grey ~70-80% alpha
            px[x, y] = (ar, ag, ab, new_a)

# Downscale slightly for file size while keeping retina-friendly
max_w = 1600
if img.size[0] > max_w:
    new_h = int(img.size[1] * max_w / img.size[0])
    img = img.resize((max_w, new_h), Image.LANCZOS)
    print(f"downscaled: {img.size}")

img.save(OUT, "PNG", optimize=True)
print(f"saved: {OUT}  ({os.path.getsize(OUT)} bytes)")
