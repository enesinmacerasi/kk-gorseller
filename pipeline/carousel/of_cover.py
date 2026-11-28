import shutil, random, math
import kk
from kk import *
from styles import wobble, sk_rect, sk_ellipse

P = PALETTES["bordo"]
INKC = kk.INK
pre = "OF"


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


def rocks(n, cx, top, k, orange=True, tint=(200, 120, 40, 160)):
    d = ImageDraw.Draw(n)
    w, h = 300 * S * k, 260 * S * k
    x0 = cx - w / 2
    col = Image.new("RGBA", n.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    for i in range(int(170 / 7)):
        yy = top + 80 * S * k + i * 7 * S * k
        cd.line((x0 + 14 * S * k, yy, x0 + w - 14 * S * k, yy + random.uniform(-5, 5) * S), fill=tint, width=int(6 * S * k))
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




def fit(d, s, size, maxw):
    f = F(BEBAS, size)
    while d.textlength(s, font=f) > maxw:
        size -= 4; f = F(BEBAS, size)
    return f


random.seed(7)
img = bg(P, 41)
tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
kk.INK = P["text"]; INKC = P["text"]
rocks(tmp, 500 * S, 800 * S, 1.2, orange=False)
img.alpha_composite(tmp)
d = ImageDraw.Draw(img)
# Angostura bottle tilted, dashing drops mid-air into the glass
bt = Image.new("RGBA", (200 * S, 360 * S), (0, 0, 0, 0)); bd = ImageDraw.Draw(bt)
bd.rounded_rectangle((30 * S, 120 * S, 170 * S, 350 * S), radius=26 * S, fill=(120, 40, 25, 255))
bd.rectangle((75 * S, 40 * S, 125 * S, 130 * S), fill=(120, 40, 25, 255))
bd.rectangle((70 * S, 10 * S, 130 * S, 50 * S), fill=(230, 200, 70, 255))
bd.rectangle((22 * S, 160 * S, 178 * S, 330 * S), fill=(246, 234, 214, 255))  # oversized paper label
wobble(bd, sk_rect(22 * S, 160 * S, 178 * S, 330 * S, 8), (28, 26, 24), 4 * S, closed=True, jitter=2, passes=2)
wobble(bd, sk_rect(30 * S, 120 * S, 170 * S, 350 * S, 8), P["text"], 5 * S, closed=True, jitter=2, passes=2)
bt = bt.resize((160 * S, 288 * S), Image.LANCZOS).rotate(135, expand=True, resample=Image.BICUBIC)
cx_, cy_ = bt.width / 2 - 85 * S, bt.height / 2 + 85 * S
img.alpha_composite(bt, (int(700 * S - cx_), int(735 * S - cy_)))
for (x, y, r) in [(680, 766, 10), (668, 792, 9)]:
    d.ellipse(((x - r) * S, (y - r * 1.4) * S, (x + r) * S, (y + r) * S), fill=(200, 60, 45))
for a in (-0.4, 0.1, 0.6):  # dash/shake strokes
    cx, cy = 850 * S, 635 * S
    wobble(d, [(cx + 10 * S * math.cos(a), cy + 30 * S * math.sin(a)), (cx + 55 * S * math.cos(a), cy + 55 * S * math.sin(a))], P["num"], 5 * S, jitter=1, passes=1)
# speech bubble, tail to the glass
bx0, by0, bx1, by1 = 70 * S, 175 * S, 1010 * S, 500 * S
d.rounded_rectangle((bx0, by0, bx1, by1), radius=60 * S, fill=P["text"])
d.polygon([(330 * S, by1 - 4 * S), (420 * S, 795 * S), (450 * S, by1 - 4 * S)], fill=P["text"])
wobble(d, [(330 * S, by1), (420 * S, 795 * S), (450 * S, by1)], (20, 18, 16), 5 * S, jitter=2, passes=2)
d.rounded_rectangle((bx0, by0, bx1, by1), radius=60 * S, outline=(20, 18, 16), width=6 * S)
d.line((336 * S, by1 - 3 * S, 444 * S, by1 - 3 * S), fill=P["text"], width=10 * S)
L1, L2 = "KOKTEYLİN İLK", "TARİFİ BENİM."
f1 = fit(d, L1, 130, 840 * S); f2 = fit(d, L2, 130, 840 * S)
f = f1 if f1.size < f2.size else f2
d.text((120 * S, 205 * S), L1, font=f, fill=(34, 24, 20))
d.text((120 * S, 345 * S), L2, font=f, fill=(170, 50, 50))
tag = "KONUŞAN KOKTEYL #5"; ft = F(BEBAS, 44)
d.text((W - MX - d.textlength(tag, font=ft), 110 * S), tag, font=ft, fill=P["num"])
wordmark(img, MX, H - 230 * S, 150 * S, *P["logo"])
fn = F(BEBAS, 72)
d.text((W - MX - d.textlength("OLD FASHIONED", font=fn), H - 210 * S), "OLD FASHIONED", font=fn, fill=P["text"])
fk = F(FIRA, 32)
d.text((W - MX - d.textlength("kaydır →", font=fk), H - 125 * S), "kaydır →", font=fk, fill=P["num"])
save(img, "OF_01.jpg"); print("ok")
