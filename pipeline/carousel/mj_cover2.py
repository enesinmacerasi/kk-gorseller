"""Mojito cover – giant mint leaves backdrop, big highball, tilted bubble."""
import math, random
from mj_art import *

P = PALETTES["komur"]
INKC = (24, 20, 18)
CREAMC = P["text"]

img = bg(P, 61)
# giant mint leaves behind (bleed off right)
lw = Image.new("RGBA", img.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lw)
for (x, y, l, w, a, c) in [(820, 760, 760, 300, -0.9, MINT_D), (900, 1080, 700, 280, 0.5, MINT), (640, 1180, 560, 220, 2.6, MINT_D)]:
    draw_leaf(ld, x * S, y * S, l * S, w * S / 2, a, col=c, vein=MINT_L)
lw.putalpha(lw.split()[3].point(lambda v: int(v * .88)))
img.alpha_composite(lw)

# big highball
hb = art_highball(k=1.0)
hb = hb.rotate(-4, expand=True, resample=Image.BICUBIC)
place(img, hb, 520 * S, 905 * S, 0, shadow=True, maxw=460, maxh=600)

# extra floating leaves for motion
d = ImageDraw.Draw(img)
for (x, y, a) in [(820, 640, -0.4), (900, 560, 0.8), (760, 520, 2.2)]:
    draw_leaf(d, x * S, y * S, 120 * S, 28 * S, a)

# speech bubble
bub = Image.new("RGBA", (980 * S, 560 * S), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
bx0, by0, bx1, by1 = 20 * S, 20 * S, 950 * S, 420 * S
bd.rounded_rectangle((bx0, by0, bx1, by1), 60 * S, fill=CREAMC, outline=INKC, width=7 * S)
bd.polygon([(250 * S, by1 - 6 * S), (330 * S, 540 * S), (380 * S, by1 - 6 * S)], fill=CREAMC)
bd.line([(250 * S, by1), (330 * S, 540 * S), (380 * S, by1)], fill=INKC, width=7 * S)
bd.text((70 * S, 45 * S), "BEN MOJITO.", font=F(BEBAS, 86), fill=(176, 64, 52))
f = F(BEBAS, 128)
bd.text((70 * S, 135 * S), "BİR KORSANIN", font=f, fill=INKC)
bd.text((70 * S, 268 * S), "İLACIYDIM.", font=f, fill=MINT_D)
shadow = Image.new("RGBA", bub.size, (0, 0, 0, 0))
shadow.paste((0, 0, 0, 150), (0, 0), bub)
shadow = shadow.filter(ImageFilter.GaussianBlur(14 * S)).rotate(2, expand=True, resample=Image.BICUBIC)
bub = bub.rotate(2, expand=True, resample=Image.BICUBIC)
img.alpha_composite(shadow, (int(60 * S), int(178 * S)))
img.alpha_composite(bub, (int(45 * S), int(150 * S)))

d = ImageDraw.Draw(img)
tag = "KONUŞAN KOKTEYL #6"; ft = F(BEBAS, 44)
d.text((W - MX - d.textlength(tag, font=ft), 100 * S), tag, font=ft, fill=P["num"])
wordmark(img, MX, H - 200 * S, 140 * S, *P["logo"])
d.rounded_rectangle((W - MX - 300 * S, H - 205 * S, W - MX + 30 * S, H - 60 * S), 28 * S, fill=(28, 26, 24))
fn = F(BEBAS, 72)
d.text((W - MX - d.textlength("MOJITO", font=fn), H - 190 * S), "MOJITO", font=fn, fill=CREAMC)
fk = F(FIRA, 32)
d.text((W - MX - d.textlength("kaydır →", font=fk), H - 108 * S), "kaydır →", font=fk, fill=P["num"])
img.convert("RGB").resize((W // S, H // S), Image.LANCZOS).save("MJ_01.jpg", quality=93)
print("ok")
