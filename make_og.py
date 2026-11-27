#!/usr/bin/env python3
"""OG(공유 미리보기) 이미지 생성 — 1200x630, 크리스마스×미스터리 다크 포레스트 톤."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, math

W, H = 1200, 630
SS = 2  # supersample
w, h = W * SS, H * SS

FOREST = (15, 35, 28)
FOREST_DEEP = (8, 19, 15)
FOREST_SOFT = (23, 53, 42)
BURGUNDY = (139, 30, 36)
GOLD = (212, 175, 55)
GOLD_SOFT = (231, 206, 134)
IVORY = (251, 247, 239)

# ---------- 배경: 세로 그라데이션 ----------
img = Image.new("RGB", (w, h), FOREST_DEEP)
d = ImageDraw.Draw(img)
for y in range(h):
    t = y / h
    # 위(밝은 포레스트) -> 아래(딥)
    e = t ** 0.9
    r = int(FOREST_SOFT[0] * (1 - e) + FOREST_DEEP[0] * e)
    g = int(FOREST_SOFT[1] * (1 - e) + FOREST_DEEP[1] * e)
    b = int(FOREST_SOFT[2] * (1 - e) + FOREST_DEEP[2] * e)
    d.line([(0, y), (w, y)], fill=(r, g, b))

# ---------- 금빛 글로우 (가운데 위) ----------
glow = Image.new("L", (w, h), 0)
gd = ImageDraw.Draw(glow)
cx, cy = w // 2, int(h * 0.10)
rad = int(w * 0.55)
for i in range(28, 0, -1):
    rr = int(rad * i / 28)
    a = int(26 * (1 - i / 28) ** 1.6)
    gd.ellipse([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2], fill=a)
glow = glow.filter(ImageFilter.GaussianBlur(60 * SS // 2))
img = Image.composite(Image.new("RGB", (w, h), GOLD), img, glow.point(lambda v: min(255, v * 2)))

# ---------- 버건디 글로우 (아래) ----------
glow2 = Image.new("L", (w, h), 0)
gd2 = ImageDraw.Draw(glow2)
cx2, cy2 = int(w * 0.5), int(h * 1.02)
rad2 = int(w * 0.60)
for i in range(28, 0, -1):
    rr = int(rad2 * i / 28)
    a = int(40 * (1 - i / 28) ** 1.5)
    gd2.ellipse([cx2 - rr, cy2 - rr // 2, cx2 + rr, cy2 + rr // 2], fill=a)
glow2 = glow2.filter(ImageFilter.GaussianBlur(80 * SS // 2))
img = Image.composite(Image.new("RGB", (w, h), BURGUNDY), img, glow2.point(lambda v: min(255, v * 2)))

# ---------- 눈 ----------
random.seed(1412)
snow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(snow)
for _ in range(210):
    x = random.uniform(0, w)
    y = random.uniform(0, h)
    r = random.uniform(0.7, 2.5) * SS
    a = int(random.uniform(38, 155))
    sd.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))
img = Image.alpha_composite(img.convert("RGBA"), snow)

d = ImageDraw.Draw(img)

# ---------- 금빛 프레임 ----------
def rect(inset, color, width):
    d.rectangle([inset, inset, w - inset, h - inset], outline=color, width=width)

rect(34 * SS, (212, 175, 55, 110), 1 * SS)
rect(44 * SS, (212, 175, 55, 40), 1 * SS)
# 모서리 다이아몬드
def diamond(cx, cy, s, color):
    d.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], outline=color, width=SS)

for px, py in [(34 * SS, 34 * SS), (w - 34 * SS, 34 * SS), (34 * SS, h - 34 * SS), (w - 34 * SS, h - 34 * SS)]:
    diamond(px, py, 7 * SS, (212, 175, 55, 160))

# ---------- 폰트 ----------
SERIF = "/usr/share/fonts/pickle-hwp/NotoSerifCJKkr-Regular.otf"
LSERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size * SS)

def draw_tracked(text, y, fnt, fill, tracking=0, anchor_center=True, stroke=0):
    """자간을 적용해 가운데 정렬로 그린다."""
    widths = []
    for ch in text:
        bb = d.textbbox((0, 0), ch, font=fnt, stroke_width=stroke)
        widths.append(bb[2] - bb[0] if ch != " " else fnt.size * 0.28)
    total = sum(widths) + tracking * (len(text) - 1)
    x = (w - total) / 2 if anchor_center else 0
    for ch, cw in zip(text, widths):
        if ch != " ":
            bb = d.textbbox((0, 0), ch, font=fnt, stroke_width=stroke)
            d.text((x - bb[0], y), ch, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=fill)
        x += cw + tracking
    return total

# ---------- 텍스트 ----------
eyebrow_font = font(LSERIF, 15)
draw_tracked("C H R I S T M A S   N I G H T   I N V I T A T I O N",
             int(96 * SS), font(LSERIF, 14), (231, 206, 134, 230), tracking=3 * SS)

# 장식선
line_y = int(140 * SS)
d.line([(w / 2 - 150 * SS, line_y), (w / 2 - 18 * SS, line_y)], fill=(212, 175, 55, 120), width=SS)
d.line([(w / 2 + 18 * SS, line_y), (w / 2 + 150 * SS, line_y)], fill=(212, 175, 55, 120), width=SS)
diamond(w / 2, line_y, 5 * SS, (231, 206, 134, 200))

title_font = font(SERIF, 58)
draw_tracked("머더미스터리", int(180 * SS), title_font, (251, 247, 239, 255), tracking=4 * SS, stroke=1 * SS)
draw_tracked("크리스마스 나잇", int(268 * SS), font(SERIF, 54), (231, 206, 134, 255), tracking=3 * SS, stroke=1 * SS)

# 구분 장식
dy = int(368 * SS)
d.line([(w / 2 - 90 * SS, dy), (w / 2 - 14 * SS, dy)], fill=(212, 175, 55, 90), width=SS)
d.line([(w / 2 + 14 * SS, dy), (w / 2 + 90 * SS, dy)], fill=(212, 175, 55, 90), width=SS)
diamond(w / 2, dy, 4 * SS, (212, 175, 55, 190))

draw_tracked("2026. 12. 12 SAT  ·  19:00", int(404 * SS), font(LSERIF, 30), (251, 247, 239, 225), tracking=3 * SS)
draw_tracked("12.12 SAT 19:00  —  12.13 SUN 06:00", int(452 * SS), font(LSERIF, 16), (251, 247, 239, 130), tracking=2 * SS)

venue_font = font(SERIF, 22)
draw_tracked("홍대 파티룸 ‘한 겨울, 사건의 집’", int(508 * SS), venue_font, (251, 247, 239, 175), tracking=1 * SS)

# ---------- 저장 ----------
out = img.convert("RGB").resize((W, H), Image.LANCZOS)
out.save("christmas-invite/og-image.png", "PNG", optimize=True)
print("saved", out.size)
