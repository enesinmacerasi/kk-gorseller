"""Daiquiri cover v2 – bolder: giant lime wheel backdrop, filled coupe, shaker mid-pour with splash."""
import math, random
from kk import *
from styles import wobble, sk_ellipse

P = PALETTES["komur"]
INK = (24, 20, 18)
CREAMC = P["text"]
LIME = (150, 196, 70)
LIME_L = (205, 228, 140)
LIME_D = (70, 110, 35)
LIQ = (222, 236, 170)
random.seed(4)

img = bg(P, 41)
d = ImageDraw.Draw(img)

# --- giant lime wheel behind everything (bleeds off right edge) ---
lw = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lw)
cx, cy, R = 760 * S, 930 * S, 400 * S
ld.ellipse((cx - R, cy - R, cx + R, cy + R), fill=LIME_D)
ld.ellipse((cx - R * .92, cy - R * .92, cx + R * .92, cy + R * .92), fill=(236, 236, 206))
n = 10
for i in range(n):
    a0 = i * 2 * math.pi / n + 0.06; a1 = (i + 1) * 2 * math.pi / n - 0.06
    pts = [(cx + 30 * S * math.cos((a0 + a1) / 2), cy + 30 * S * math.sin((a0 + a1) / 2))]
    pts += [(cx + R * .85 * math.cos(a0 + (a1 - a0) * j / 16), cy + R * .85 * math.sin(a0 + (a1 - a0) * j / 16)) for j in range(17)]
    ld.polygon(pts, fill=LIME)
    rr = random.Random(i)
    for _ in range(40):
        a = rr.uniform(a0 + .04, a1 - .04); r0 = rr.uniform(60 * S, R * .8); r1 = min(R * .83, r0 + rr.uniform(15, 50) * S)
        ld.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=LIME_L, width=int(rr.uniform(3, 7) * S))
lw.putalpha(lw.split()[3].point(lambda v: int(v * .9)))
img.alpha_composite(lw)

# --- coupe glass, big and filled ---
gx, top, k = 430 * S, 760 * S, 1.75
rim = 175 * S * k
bowl = [(gx - rim, top), (gx - 120 * S * k, top + 80 * S * k), (gx - 40 * S * k, top + 120 * S * k), (gx - 10 * S * k, top + 135 * S * k),
        (gx + 10 * S * k, top + 135 * S * k), (gx + 40 * S * k, top + 120 * S * k), (gx + 120 * S * k, top + 80 * S * k), (gx + rim, top)]
d.polygon(bowl, fill=LIQ)
# frost / bubbles in the drink
rr = random.Random(9)
for _ in range(60):
    x = rr.uniform(gx - rim * .8, gx + rim * .8); y = rr.uniform(top + 10 * S, top + 70 * S * k)
    r = rr.uniform(2, 6) * S
    d.ellipse((x - r, y - r, x + r, y + r), fill=(250, 252, 235))
d.ellipse((gx - rim, top - 22 * S * k, gx + rim, top + 22 * S * k), fill=(236, 246, 200), outline=CREAMC, width=8 * S)
stem_top = top + 135 * S * k
d.line((gx, stem_top, gx, stem_top + 260 * S), fill=CREAMC, width=12 * S)
d.ellipse((gx - 120 * S, stem_top + 250 * S, gx + 120 * S, stem_top + 285 * S), fill=CREAMC)
wobble(d, bowl, CREAMC, 8 * S, passes=2, jitter=2)
# highlight
d.line((gx - rim * .7, top + 30 * S, gx - rim * .45, top + 85 * S), fill=(255, 255, 250), width=10 * S)

# --- shaker mid-pour, top right ---
sh = Image.new("RGBA", (360 * S, 520 * S), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
sd.rounded_rectangle((60 * S, 150 * S, 300 * S, 500 * S), 40 * S, fill=(200, 205, 210))
sd.polygon([(80 * S, 150 * S), (120 * S, 60 * S), (240 * S, 60 * S), (280 * S, 150 * S)], fill=(175, 180, 186))
sd.rounded_rectangle((130 * S, 10 * S, 230 * S, 70 * S), 16 * S, fill=(150, 155, 160))
sd.rectangle((60 * S, 280 * S, 300 * S, 300 * S), fill=(150, 155, 160))
sd.line((110 * S, 180 * S, 110 * S, 470 * S), fill=(240, 242, 245), width=14 * S)
sh = sh.rotate(128, expand=True, resample=Image.BICUBIC)
img.alpha_composite(sh, (int(620 * S), int(420 * S)))
# pour stream into the glass
d.line([(700 * S, 640 * S), (665 * S, 690 * S), (630 * S, 760 * S)], fill=LIQ, width=20 * S, joint="curve")
# splash
for (x, y, r) in [(560, 735, 13), (520, 720, 9), (610, 715, 8), (500, 745, 7), (585, 690, 6), (470, 730, 5), (640, 745, 6)]:
    d.ellipse(((x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S), fill=LIQ)
# motion strokes (shaking)
for a in (-0.6, -0.1, 0.4):
    bx, by_ = 900 * S, 560 * S
    d.line((bx + 20 * S * math.cos(a), by_ + 20 * S * math.sin(a), bx + 75 * S * math.cos(a), by_ + 75 * S * math.sin(a)), fill=LIME, width=8 * S)

# --- speech bubble, slightly tilted with drop shadow ---
bub = Image.new("RGBA", (980 * S, 560 * S), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
bx0, by0, bx1, by1 = 20 * S, 20 * S, 950 * S, 420 * S
bd.rounded_rectangle((bx0, by0, bx1, by1), 60 * S, fill=CREAMC, outline=INK, width=7 * S)
bd.polygon([(250 * S, by1 - 6 * S), (330 * S, 540 * S), (380 * S, by1 - 6 * S)], fill=CREAMC)
bd.line([(250 * S, by1), (330 * S, 540 * S), (380 * S, by1)], fill=INK, width=7 * S)
bd.text((70 * S, 45 * S), "BEN DAIQUIRI.", font=F(BEBAS, 86), fill=(176, 64, 52))
f = F(BEBAS, 116)
bd.text((70 * S, 135 * S), "ADIMI BİR MADEN", font=f, fill=INK)
bd.text((70 * S, 268 * S), "KASABASINDAN ALDIM.", font=f, fill=(96, 140, 32))
shadow = Image.new("RGBA", bub.size, (0, 0, 0, 0))
shadow.paste((0, 0, 0, 150), (0, 0), bub)
shadow = shadow.filter(ImageFilter.GaussianBlur(14 * S)).rotate(-2, expand=True, resample=Image.BICUBIC)
bub = bub.rotate(-2, expand=True, resample=Image.BICUBIC)
img.alpha_composite(shadow, (int(60 * S), int(178 * S)))
img.alpha_composite(bub, (int(45 * S), int(160 * S)))

# --- tag, logo, name ---
d = ImageDraw.Draw(img)
tag = "KONUŞAN KOKTEYL #4"; ft = F(BEBAS, 44)
d.text((W - MX - d.textlength(tag, font=ft), 100 * S), tag, font=ft, fill=P["num"])
wordmark(img, MX, H - 200 * S, 140 * S, *P["logo"])
d.rounded_rectangle((W - MX - 300 * S, H - 205 * S, W - MX + 30 * S, H - 60 * S), 28 * S, fill=(28, 26, 24))
fn = F(BEBAS, 72)
d.text((W - MX - d.textlength("DAIQUIRI", font=fn), H - 190 * S), "DAIQUIRI", font=fn, fill=CREAMC)
fk = F(FIRA, 32)
d.text((W - MX - d.textlength("kaydır →", font=fk), H - 108 * S), "kaydır →", font=fk, fill=P["num"])
img.convert("RGB").resize((W // S, H // S), Image.LANCZOS).save("DQ_01_v2.jpg", quality=93)
print("ok")
