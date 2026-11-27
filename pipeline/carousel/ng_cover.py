import shutil, random, math
import kk
from kk import *
from styles import wobble, sk_rect, sk_ellipse

P = PALETTES["komur"]
INKC = kk.INK
pre = "NG"


def bottle(n, cx, by, k, tint, label_col=None):
    d = ImageDraw.Draw(n)
    w, h = 150 * S * k, 400 * S * k
    x0, y0 = cx - w / 2, by - h
    col = Image.new("RGBA", n.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    for i in range(int(200 * k / 1.0) // 7):
        yy = y0 + 190 * S * k + i * 7 * S * k
        if yy > by - 10 * S * k: break
        cd.line((x0 + 12 * S * k, yy, x0 + w - 12 * S * k, yy + random.uniform(-5, 5) * S), fill=tint, width=int(6 * S * k))
    n.alpha_composite(col)
    pts = [(x0, by), (x0, y0 + 160 * S * k), (cx - 24 * S * k, y0 + 70 * S * k), (cx - 24 * S * k, y0), (cx + 24 * S * k, y0), (cx + 24 * S * k, y0 + 70 * S * k), (x0 + w, y0 + 160 * S * k), (x0 + w, by)]
    pp = []
    for a, b in zip(pts, pts[1:] + pts[:1]):
        for i in range(8):
            pp.append((a[0] + (b[0] - a[0]) * i / 8, a[1] + (b[1] - a[1]) * i / 8))
    wobble(d, pp, INKC, int(5 * S * k), closed=True, passes=3, jitter=3)
    wobble(d, sk_rect(cx - 30 * S * k, y0 - 36 * S * k, cx + 30 * S * k, y0 + 4 * S * k), INKC, int(4 * S * k), closed=True)
    # blank label
    wobble(d, sk_rect(x0 + 18 * S * k, y0 + 200 * S * k, x0 + w - 18 * S * k, y0 + 290 * S * k), INKC, int(3 * S * k), closed=True, passes=2)


def rocks(n, cx, top, k, orange=True):
    d = ImageDraw.Draw(n)
    w, h = 300 * S * k, 260 * S * k
    x0 = cx - w / 2
    col = Image.new("RGBA", n.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    for i in range(int(170 / 7)):
        yy = top + 80 * S * k + i * 7 * S * k
        cd.line((x0 + 14 * S * k, yy, x0 + w - 14 * S * k, yy + random.uniform(-5, 5) * S), fill=(176, 40, 40, 150), width=int(6 * S * k))
    n.alpha_composite(col)
    wobble(d, [(x0, top), (x0 + 8 * S * k, top + h), (x0 + w - 8 * S * k, top + h), (x0 + w, top)], INKC, int(6 * S * k), passes=3, jitter=3)
    wobble(d, sk_ellipse(cx, top, w / 2, 18 * S * k, 40), INKC, int(4 * S * k), passes=2, jitter=2)
    wobble(d, sk_rect(x0 + 70 * S * k, top + 40 * S * k, x0 + 210 * S * k, top + 180 * S * k, 6), INKC, int(4 * S * k), closed=True, passes=2)
    if orange:
        ox, oy, r = x0 + w - 30 * S * k, top - 10 * S * k, 70 * S * k
        oc = Image.new("RGBA", n.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(oc)
        for i in range(14):
            a = i * 2 * math.pi / 14
            od.line((ox, oy, ox + math.cos(a) * r * .9, oy + math.sin(a) * r * .9), fill=(230, 140, 50, 200), width=int(9 * S * k))
        n.alpha_composite(oc)
        wobble(d, sk_ellipse(ox, oy, r, r, 40), INKC, int(4 * S * k), passes=2, jitter=2)



random.seed(7)
img = bg(P, 11)
# big glass, drawn in cream
tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
kk.INK = P["text"]; INKC = P["text"]
rocks(tmp, 560 * S, 745 * S, 1.38, orange=False)
img.alpha_composite(tmp)
d = ImageDraw.Draw(img)
# orange peel being twisted above the glass + spray (mid-action)
px, py = 790 * S, 630 * S
peel = [(px - 90 * S, py + 20 * S), (px - 40 * S, py - 30 * S), (px + 20 * S, py - 40 * S), (px + 80 * S, py - 10 * S), (px + 95 * S, py + 30 * S)]
oc = Image.new("RGBA", img.size, (0, 0, 0, 0)); od = ImageDraw.Draw(oc)
od.line(peel, fill=(232, 130, 40, 255), width=34 * S, joint="curve")
img.alpha_composite(oc)
wobble(d, peel, P["text"], 5 * S, jitter=2, passes=2)
for i, (dx, dy, r) in enumerate([(-40, 70, 9), (-5, 95, 7), (30, 80, 8), (-70, 110, 6), (10, 130, 5), (55, 115, 6), (-30, 150, 4), (40, 160, 4)]):
    d.ellipse((px + dx * S - r * S, py + dy * S - r * S, px + dx * S + r * S, py + dy * S + r * S), fill=(240, 160, 70))
for a in (-0.5, 0, 0.5):  # motion strokes = twisting
    cx, cy = px + 130 * S, py - 10 * S
    wobble(d, [(cx + 10 * S * math.cos(a), cy + 30 * S * math.sin(a)), (cx + 55 * S * math.cos(a), cy + 55 * S * math.sin(a))], P["num"], 5 * S, jitter=1, passes=1)
# speech bubble with tail to the glass
bx0, by0, bx1, by1 = 70 * S, 200 * S, 1010 * S, 560 * S
bub = sk_rect(bx0, by0, bx1, by1, 24)
d.rounded_rectangle((bx0, by0, bx1, by1), radius=60 * S, fill=P["text"])
tail = [(430 * S, by1 - 4 * S), (520 * S, 730 * S), (560 * S, by1 - 4 * S)]
d.polygon(tail, fill=P["text"])
wobble(d, [(430 * S, by1), (520 * S, 730 * S), (560 * S, by1)], (20, 18, 16), 5 * S, jitter=2, passes=2)
d.rounded_rectangle((bx0, by0, bx1, by1), radius=60 * S, outline=(20, 18, 16), width=6 * S)
d.line((436 * S, by1 - 3 * S, 554 * S, by1 - 3 * S), fill=P["text"], width=10 * S)
f = F(BEBAS, 150)
d.text((120 * S, 240 * S), "BEN BOZULMUŞ", font=f, fill=(28, 26, 24))
d.text((120 * S, 390 * S), "BİR AMERICANO'YUM.", font=F(BEBAS, 132), fill=(110, 150, 40))
# series tag + name
tag = "KONUŞAN KOKTEYL #2"
ft = F(BEBAS, 44)
tw = d.textlength(tag, font=ft)
d.text((W - MX - tw, 110 * S), tag, font=ft, fill=P["num"])
wordmark(img, MX, H - 230 * S, 150 * S, *P["logo"])
d.text((W - MX - d.textlength("NEGRONI", font=F(BEBAS, 72)), H - 210 * S), "NEGRONI", font=F(BEBAS, 72), fill=P["text"])
d.text((W - MX - d.textlength("kaydır →", font=F(FIRA, 32)), H - 125 * S), "kaydır →", font=F(FIRA, 32), fill=P["num"])
save(img, "NG_01_new.jpg")
print("ok")
