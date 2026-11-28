"""Old Fashioned cover v2 (bordo template) – giant orange wheel backdrop, filled rocks glass with big cube,
orange peel being expressed (spray), tilted shadowed speech bubble starting with "BEN <NAME>."."""
import math, random
from kk import *

P = PALETTES["bordo"]
INK = (34, 24, 20)
CREAMC = P["text"]
OR = (236, 140, 50)
OR_L = (250, 190, 110)
OR_D = (190, 90, 30)
AMBER = (196, 112, 40)
random.seed(5)

img = bg(P, 51)
d = ImageDraw.Draw(img)

# --- giant orange wheel behind (bleeds off right edge) ---
lw = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lw)
cx, cy, R = 770 * S, 940 * S, 400 * S
ld.ellipse((cx - R, cy - R, cx + R, cy + R), fill=OR_D)
ld.ellipse((cx - R * .92, cy - R * .92, cx + R * .92, cy + R * .92), fill=(248, 232, 200))
n = 11
for i in range(n):
    a0 = i * 2 * math.pi / n + 0.06; a1 = (i + 1) * 2 * math.pi / n - 0.06
    pts = [(cx + 30 * S * math.cos((a0 + a1) / 2), cy + 30 * S * math.sin((a0 + a1) / 2))]
    pts += [(cx + R * .85 * math.cos(a0 + (a1 - a0) * j / 16), cy + R * .85 * math.sin(a0 + (a1 - a0) * j / 16)) for j in range(17)]
    ld.polygon(pts, fill=OR)
    rr = random.Random(i)
    for _ in range(40):
        a = rr.uniform(a0 + .04, a1 - .04); r0 = rr.uniform(60 * S, R * .8); r1 = min(R * .83, r0 + rr.uniform(15, 50) * S)
        ld.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=OR_L, width=int(rr.uniform(3, 7) * S))
img.alpha_composite(lw)

# --- rocks glass, big, filled amber with a big cube ---
gx, top = 420 * S, 720 * S
gw, gh = 520 * S, 430 * S
x0, x1 = gx - gw / 2, gx + gw / 2
liq_top = top + 120 * S
d.polygon([(x0 + 14 * S, liq_top), (x0 + 26 * S, top + gh - 30 * S), (x1 - 26 * S, top + gh - 30 * S), (x1 - 14 * S, liq_top)], fill=AMBER)
d.ellipse((x0 + 14 * S, liq_top - 22 * S, x1 - 14 * S, liq_top + 22 * S), fill=(220, 140, 60))
# big ice cube
cube = [(gx - 150 * S, liq_top - 80 * S), (gx + 110 * S, liq_top - 100 * S), (gx + 140 * S, liq_top + 150 * S), (gx - 120 * S, liq_top + 170 * S)]
d.polygon(cube, fill=(240, 220, 200))
d.line(cube + [cube[0]], fill=(255, 250, 245), width=6 * S)
d.line((gx - 110 * S, liq_top - 50 * S, gx - 60 * S, liq_top + 110 * S), fill=(255, 255, 252), width=10 * S)
# thick glass base + walls
d.rectangle((x0 + 26 * S, top + gh - 34 * S, x1 - 26 * S, top + gh), fill=(240, 228, 210))
d.line([(x0, top), (x0 + 26 * S, top + gh), (x1 - 26 * S, top + gh), (x1, top)], fill=CREAMC, width=10 * S)
d.ellipse((x0, top - 26 * S, x1, top + 26 * S), outline=CREAMC, width=8 * S)
d.line((x0 + 50 * S, top + 60 * S, x0 + 70 * S, top + 300 * S), fill=(255, 250, 240), width=10 * S)

# --- orange peel being expressed above the glass (mid-action) ---
px, py = 780 * S, 690 * S
peel = Image.new("RGBA", (420 * S, 200 * S), (0, 0, 0, 0)); pd = ImageDraw.Draw(peel)
pd.rounded_rectangle((20 * S, 50 * S, 400 * S, 150 * S), 50 * S, fill=(255, 166, 50))
pd.rounded_rectangle((20 * S, 50 * S, 400 * S, 150 * S), 50 * S, outline=(248, 236, 214), width=12 * S)
pd.rounded_rectangle((14 * S, 44 * S, 406 * S, 156 * S), 56 * S, outline=INK, width=6 * S)
for i in range(18):
    x = 50 * S + i * 19 * S
    pd.ellipse((x, 90 * S, x + 7 * S, 97 * S), fill=OR_D)
peel = peel.rotate(18, expand=True, resample=Image.BICUBIC)
img.alpha_composite(peel, (int(px - 120 * S), int(py - 140 * S)))
# spray of oils falling into the glass
rr = random.Random(3)
for _ in range(22):
    x = rr.uniform(520, 760) * S; y = rr.uniform(650, 730) * S; r = rr.uniform(4, 10) * S
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 200, 110))
for a in (-0.5, 0, 0.5):  # twist strokes
    bx, by_ = 940 * S, 540 * S
    d.line((bx + 20 * S * math.cos(a), by_ + 20 * S * math.sin(a), bx + 75 * S * math.cos(a), by_ + 75 * S * math.sin(a)), fill=P["emph_text"], width=8 * S)

# --- tilted speech bubble with drop shadow ---
bub = Image.new("RGBA", (980 * S, 560 * S), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
bx0, by0, bx1, by1 = 20 * S, 20 * S, 950 * S, 420 * S
bd.rounded_rectangle((bx0, by0, bx1, by1), 60 * S, fill=CREAMC, outline=INK, width=7 * S)
bd.polygon([(250 * S, by1 - 6 * S), (330 * S, 540 * S), (380 * S, by1 - 6 * S)], fill=CREAMC)
bd.line([(250 * S, by1), (330 * S, 540 * S), (380 * S, by1)], fill=INK, width=7 * S)
bd.text((70 * S, 45 * S), "BEN OLD FASHIONED.", font=F(BEBAS, 86), fill=(150, 90, 30))
f = F(BEBAS, 130)
bd.text((70 * S, 135 * S), "KOKTEYLİN", font=f, fill=INK)
bd.text((70 * S, 268 * S), "ATASI BENİM.", font=f, fill=(170, 50, 50))
shadow = Image.new("RGBA", bub.size, (0, 0, 0, 0))
shadow.paste((0, 0, 0, 150), (0, 0), bub)
shadow = shadow.filter(ImageFilter.GaussianBlur(14 * S)).rotate(2, expand=True, resample=Image.BICUBIC)
bub = bub.rotate(2, expand=True, resample=Image.BICUBIC)
img.alpha_composite(shadow, (int(60 * S), int(178 * S)))
img.alpha_composite(bub, (int(45 * S), int(160 * S)))

# --- tag, logo, name (name on a dark pill so it reads over the backdrop) ---
d = ImageDraw.Draw(img)
tag = "KONUŞAN KOKTEYL #5"; ft = F(BEBAS, 44)
d.text((W - MX - d.textlength(tag, font=ft), 100 * S), tag, font=ft, fill=P["num"])
wordmark(img, MX, H - 200 * S, 140 * S, *P["logo"])
fn = F(BEBAS, 72); name = "OLD FASHIONED"
nw = d.textlength(name, font=fn)
d.rounded_rectangle((W - MX - nw - 40 * S, H - 205 * S, W - MX + 30 * S, H - 60 * S), 28 * S, fill=P["bg"])
d.text((W - MX - nw, H - 190 * S), name, font=fn, fill=CREAMC)
fk = F(FIRA, 32)
d.text((W - MX - d.textlength("kaydır →", font=fk), H - 108 * S), "kaydır →", font=fk, fill=P["num"])
img.convert("RGB").resize((W // S, H // S), Image.LANCZOS).save("OF_01_v2.jpg", quality=93)
print("ok")
