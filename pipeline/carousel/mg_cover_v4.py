import shutil, random, math
import kk
import hybrid
from kk import *
from styles import wobble, sk_rect, sk_ellipse

P = PALETTES["bordo"]
INKC = kk.INK
pre = "MG"


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



def glass(n, cx, top, k, lime=True):
    d = ImageDraw.Draw(n)
    s = S * k
    rim = 170 * s
    pts = [(cx - rim, top), (cx - 120 * s, top + 70 * s), (cx - 60 * s, top + 80 * s), (cx - 40 * s, top + 140 * s),
           (cx - 8 * s, top + 165 * s), (cx - 8 * s, top + 330 * s), (cx - 90 * s, top + 350 * s), (cx + 90 * s, top + 350 * s),
           (cx + 8 * s, top + 330 * s), (cx + 8 * s, top + 165 * s), (cx + 40 * s, top + 140 * s), (cx + 60 * s, top + 80 * s),
           (cx + 120 * s, top + 70 * s), (cx + rim, top)]
    col = Image.new("RGBA", n.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    for i in range(int(60 * k / 1.0) // 6 + 9):
        yy = top + 22 * s + i * 6 * s
        if yy > top + 72 * s: break
        hw = rim - (yy - top) * (rim - 120 * s) / (70 * s) - 10 * s
        cd.line((cx - hw, yy, cx + hw, yy + random.uniform(-4, 4) * S), fill=(205, 220, 120, 150), width=int(5 * s))
    n.alpha_composite(col)
    pp = []
    for a, b in zip(pts, pts[1:]):
        for i in range(6):
            pp.append((a[0] + (b[0] - a[0]) * i / 6, a[1] + (b[1] - a[1]) * i / 6))
    pp.append(pts[-1])
    wobble(d, pp, INKC, int(5 * s), passes=3, jitter=3)
    wobble(d, sk_ellipse(cx, top, rim, 16 * s, 40), INKC, int(4 * s), passes=2, jitter=2)
    r = random.Random(4)
    for i in range(70):  # salt on the rim
        a = r.uniform(math.pi * 0.05, math.pi * 0.95)
        x = cx - rim * math.cos(a); y = top - 16 * s * math.sin(a) + r.uniform(-6, 6) * S
        d.ellipse((x - 3 * S, y - 3 * S, x + 3 * S, y + 3 * S), fill=INKC)
    if lime:
        ox, oy, rr = cx + rim - 20 * s, top - 30 * s, 62 * s
        oc = Image.new("RGBA", n.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(oc)
        od.ellipse((ox - rr, oy - rr, ox + rr, oy + rr), fill=(150, 196, 70, 170))
        for i in range(10):
            a = i * 2 * math.pi / 10
            od.line((ox, oy, ox + math.cos(a) * rr * .85, oy + math.sin(a) * rr * .85), fill=(240, 240, 200, 220), width=int(5 * s))
        n.alpha_composite(oc)
        wobble(d, sk_ellipse(ox, oy, rr, rr, 40), INKC, int(4 * s), passes=2, jitter=2)


def lime_wheel(n, cx, cy, k):
    d = ImageDraw.Draw(n)
    rr = 170 * S * k
    oc = Image.new("RGBA", n.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(oc)
    od.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(150, 196, 70, 150))
    for i in range(10):
        a = i * 2 * math.pi / 10
        od.line((cx, cy, cx + math.cos(a) * rr * .86, cy + math.sin(a) * rr * .86), fill=(245, 240, 210, 230), width=int(9 * S * k))
    n.alpha_composite(oc)
    wobble(d, sk_ellipse(cx, cy, rr, rr, 60), INKC, int(6 * S * k), passes=3, jitter=3)
    wobble(d, sk_ellipse(cx, cy, rr * .86, rr * .86, 50), INKC, int(3 * S * k), passes=2, jitter=2)



random.seed(17)
img = bg(P, 21)
tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
kk.INK = P["text"]; INKC = P["text"]
glass(tmp, 520 * S, 800 * S, 1.45, lime=True)
img.alpha_composite(tmp)
d = ImageDraw.Draw(img)
# salt shaker mid-pour above the rim (tilted), grains falling
sh = Image.new("RGBA", (220 * S, 300 * S), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
sd.rounded_rectangle((40 * S, 70 * S, 180 * S, 280 * S), radius=30 * S, fill=(246, 234, 214, 255))
sd.rounded_rectangle((50 * S, 20 * S, 170 * S, 80 * S), radius=18 * S, fill=(180, 175, 170, 255))
for i in range(3):
    for j in range(2):
        sd.ellipse((80 * S + i * 28 * S, 36 * S + j * 20 * S, 88 * S + i * 28 * S, 44 * S + j * 20 * S), fill=(60, 50, 50, 255))
wobble(sd, sk_rect(40 * S, 70 * S, 180 * S, 280 * S, 10), (34, 24, 20), 5 * S, closed=True, jitter=2, passes=2)
sh = sh.rotate(140, expand=True, resample=Image.BICUBIC)
img.alpha_composite(sh, (int(720 * S), int(560 * S)))
r = random.Random(3)
for i in range(46):
    x = r.uniform(560, 760) * S; y = r.uniform(660, 790) * S
    rr = r.uniform(2.5, 5) * S
    d.rectangle((x - rr, y - rr, x + rr, y + rr), fill=(250, 246, 238))
# speech bubble
bx0, by0, bx1, by1 = 70 * S, 245 * S, 1010 * S, 520 * S
d.rounded_rectangle((bx0, by0, bx1, by1), radius=60 * S, fill=P["text"])
d.polygon([(330 * S, by1 - 4 * S), (400 * S, 760 * S), (450 * S, by1 - 4 * S)], fill=P["text"])
wobble(d, [(330 * S, by1), (400 * S, 760 * S), (450 * S, by1)], (34, 24, 20), 5 * S, jitter=2, passes=2)
d.rounded_rectangle((bx0, by0, bx1, by1), radius=60 * S, outline=(34, 24, 20), width=6 * S)
d.line((336 * S, by1 - 3 * S, 444 * S, by1 - 3 * S), fill=P["text"], width=10 * S)
L1, L2 = "BEN MARGARITA'YIM.", "BARMEN YANLIŞ ŞİŞEYİ KULLANDI."
sz = 140
while max(d.textlength(L1, font=F(BEBAS, sz)), d.textlength(L2, font=F(BEBAS, sz))) > 840 * S: sz -= 4
lh = int(sz * S * 1.02); y1 = int(372 * S - lh)
d.text((120 * S, y1), L1, font=F(BEBAS, sz), fill=(34, 24, 20))
d.text((120 * S, y1 + lh), L2, font=F(BEBAS, sz), fill=(170, 50, 50))
tag = "KONUŞAN KOKTEYL #3"; ft = F(BEBAS, 44)
d.text((W - MX - d.textlength(tag, font=ft), 110 * S), tag, font=ft, fill=P["num"])
wordmark(img, MX, H - 230 * S, 150 * S, *P["logo"])
fn = F(BEBAS, 72)
d.text((W - MX - d.textlength("MARGARITA", font=fn), H - 210 * S), "MARGARITA", font=fn, fill=P["text"])
fk = F(FIRA, 32)
d.text((W - MX - d.textlength("kaydır →", font=fk), H - 125 * S), "kaydır →", font=fk, fill=P["num"])
save(img, "MG_01_v4.jpg"); print("ok")
