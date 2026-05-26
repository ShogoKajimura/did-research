#!/usr/bin/env python3
"""
OGP image (1200x630) for social-share preview.
Matches the site's Twin Streams palette.
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ---- output ----
W, H = 1200, 630
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "og.png")

# ---- palette ----
BG = (0xee, 0xf5, 0xf3)
BG_STRONG = (0xdc, 0xea, 0xe7)
INK = (0x10, 0x23, 0x2a)
INK_SOFT = (0x54, 0x69, 0x70)
ACCENT = (0x2f, 0x6f, 0x73)
ACCENT_DEEP = (0x16, 0x4b, 0x53)
ACCENT_SOFT = (0xb8, 0xd8, 0xd4)
IRIS = (0x73, 0x7b, 0x9f)

# ---- fonts ----
# Use macOS YuGothic OTFs (PIL handles OTF fine for raster)
FONT_REG = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/ee89e7987a76cc8cfdff36c96bd7bc77655b343e.asset/AssetData/YuGothic-Medium.otf"
FONT_BOLD = "/System/Library/AssetsV2/com_apple_MobileAsset_Font8/b7a6a6575a699e801915b73b9e1e75c74a3404ce.asset/AssetData/YuGothic-Bold.otf"
FONT_HIRA = "/System/Library/Fonts/Hiragino Sans GB.ttc"
font_fallback = FONT_HIRA  # fallback

def load(path, size, bold=False):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype(font_fallback, size)

f_title = load(FONT_BOLD, 124, bold=True)
f_subtitle = load(FONT_BOLD, 42, bold=True)
f_lab = load(FONT_REG, 32)
f_meta = load(FONT_REG, 26)
f_url = load(FONT_BOLD, 24, bold=True)

# ---- canvas ----
img = Image.new("RGB", (W, H), BG)
draw = ImageDraw.Draw(img)

# soft gradient: vertical linear from #f7fbfa to bg-strong
for y in range(H):
    t = y / H
    r = int(0xf7 + (BG_STRONG[0] - 0xf7) * t)
    g = int(0xfb + (BG_STRONG[1] - 0xfb) * t)
    b = int(0xfa + (BG_STRONG[2] - 0xfa) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# accent radial blobs (approximate with concentric circles)
def soft_circle(cx, cy, r_max, color, alpha_peak=70):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    steps = 36
    for i in range(steps, 0, -1):
        a = int(alpha_peak * (i / steps) ** 2)
        r = r_max * (i / steps)
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    img.alpha_composite(overlay) if img.mode == "RGBA" else img.paste(
        Image.alpha_composite(img.convert("RGBA"), overlay), (0, 0)
    )

# Convert to RGBA for blob compositing
img = img.convert("RGBA")
draw = ImageDraw.Draw(img)

def blob(cx, cy, r_max, color, alpha_peak=80):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    steps = 28
    for i in range(steps, 0, -1):
        a = int(alpha_peak * (i / steps) ** 2.4)
        r = int(r_max * (i / steps))
        od.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    img.alpha_composite(overlay)

blob(150, 80, 360, ACCENT_SOFT, 110)
blob(1080, 60, 280, IRIS, 70)

draw = ImageDraw.Draw(img)

# ---- logo (brain) ----
logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")
    # Recolor near-grey pixels to accent_deep for brand cohesion
    # Skip recolor for simplicity; just resize and paste
    lw = 280
    aspect = logo.height / logo.width
    lh = int(lw * aspect)
    logo_resized = logo.resize((lw, lh), Image.LANCZOS)
    img.paste(logo_resized, (60, 64), logo_resized)

# ---- main title ----
title = "「私」の謎に迫る"
# Draw title at center-left, large
title_y = 220
draw.text((60, title_y), title, font=f_title, fill=INK)

# ---- subtitle (English) ----
subtitle = "Brain Science Lab · DID neuroimaging"
draw.text((64, title_y + 145), subtitle, font=f_subtitle, fill=ACCENT_DEEP)

# ---- meta line ----
meta = "解離性同一症の脳機能研究／参加者募集中"
draw.text((64, title_y + 210), meta, font=f_meta, fill=INK_SOFT)

# ---- bottom URL bar ----
bar_h = 84
bar_y = H - bar_h
# accent-deep gradient
for y in range(bar_y, H):
    t = (y - bar_y) / bar_h
    r = int(ACCENT[0] + (ACCENT_DEEP[0] - ACCENT[0]) * t)
    g = int(ACCENT[1] + (ACCENT_DEEP[1] - ACCENT[1]) * t)
    b = int(ACCENT[2] + (ACCENT_DEEP[2] - ACCENT[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# URL text
draw.text((60, bar_y + 28), "shogokajimura.github.io/did-research", font=f_url, fill=(0xfa, 0xf8, 0xf3))
# Right-side affiliation tag (sized to fit before W)
tag = "京大 / KIT / 立正大 共同研究"
tw = draw.textlength(tag, font=f_meta)
draw.text((W - tw - 60, bar_y + 30), tag, font=f_meta, fill=(0xfa, 0xf8, 0xf3))

# Save
img = img.convert("RGB")
img.save(OUT, "PNG", optimize=True)
print(f"saved: {OUT}  ({W}x{H})")
