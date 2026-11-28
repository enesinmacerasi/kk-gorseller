"""Mojito flat illustrations for bold pages + cover."""
import math, random
from bold import *

MINT = (88, 170, 96); MINT_L = (150, 210, 140); MINT_D = (40, 104, 56)
CREAM = (246, 234, 214)


def leaf_poly(cx, cy, L, Wd, ang):
    pts = []
    for i in range(25):
        t = i / 24
        x = -L / 2 + L * t; y = -Wd * math.sin(math.pi * t) ** 0.85
        pts.append((x, y))
    for i in range(24, -1, -1):
        t = i / 24
        x = -L / 2 + L * t; y = Wd * math.sin(math.pi * t) ** 0.85
        pts.append((x, y))
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def draw_leaf(d, cx, cy, L, Wd, ang, col=MINT, vein=MINT_L):
    d.polygon(leaf_poly(cx, cy, L, Wd, ang), fill=col)
    ca, sa = math.cos(ang), math.sin(ang)
    d.line((cx - L * .45 * ca, cy - L * .45 * sa, cx + L * .45 * ca, cy + L * .45 * sa), fill=vein, width=max(2, int(L / 60)))
    for k in (-.25, 0, .25):
        bx, by = cx + L * k * ca, cy + L * k * sa
        for sgn in (-1, 1):
            a2 = ang + sgn * 0.9
            d.line((bx, by, bx + Wd * .7 * math.cos(a2) + L * .08 * ca, by + Wd * .7 * math.sin(a2) + L * .08 * sa), fill=vein, width=max(2, int(L / 90)))


def art_mint(n=5):
    L_ = Image.new("RGBA", (760 * S, 700 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L_)
    d.line((380 * S, 680 * S, 380 * S, 120 * S), fill=MINT_D, width=18 * S)
    specs = [(250, 520, 300, 120, 2.6), (510, 500, 300, 120, 0.5), (240, 330, 280, 110, 2.8), (520, 310, 280, 110, 0.35), (380, 140, 240, 100, -1.57)]
    for (x, y, l, w, a) in specs[:n]:
        draw_leaf(d, x * S, y * S, l * S, w * S / 2, a)
    return L_


def art_highball(liquid=(214, 236, 196), k=1.0, straw=True):
    s = S * k; L_ = Image.new("RGBA", (int(560 * s), int(900 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(L_)
    x0, x1, top, bot = 100 * s, 460 * s, 160 * s, 860 * s
    lt = top + 70 * s
    d.rectangle((x0 + 12 * s, lt, x1 - 12 * s, bot - 30 * s), fill=liquid)
    rr = random.Random(7)
    # ice cubes
    for (cx, cy) in [(200, 320), (340, 300), (260, 460), (370, 520), (190, 600), (320, 680)]:
        a = rr.uniform(-.4, .4); r = 62 * s
        pts = [(cx * s + r * math.cos(a + i * math.pi / 2), cy * s + r * math.sin(a + i * math.pi / 2)) for i in range(4)]
        d.polygon(pts, fill=(236, 246, 232)); d.line(pts + [pts[0]], fill=(255, 255, 255), width=int(5 * s))
    # mint leaves inside
    for (cx, cy, a) in [(180, 720, .6), (360, 760, 2.4), (250, 560, -.4), (330, 410, 2.9)]:
        draw_leaf(d, cx * s, cy * s, 140 * s, 30 * s, a)
    # bubbles
    for _ in range(50):
        x = rr.uniform(x0 + 30 * s, x1 - 30 * s); y = rr.uniform(lt + 20 * s, bot - 50 * s); r = rr.uniform(3, 7) * s
        d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 255, 255), width=int(2 * s))
    if straw:
        d.line((330 * s, 20 * s, 290 * s, 700 * s), fill=(242, 140, 110), width=int(26 * s))
        d.line((330 * s, 20 * s, 318 * s, 220 * s), fill=(242, 140, 110), width=int(26 * s))
    # mint sprig on top
    for (cx, cy, a) in [(170, 150, -2.3), (240, 110, -1.7), (130, 210, 3.0)]:
        draw_leaf(d, cx * s, cy * s, 150 * s, 34 * s, a)
    # lime wedge on rim
    w = art_wheel((70, 110, 35), (150, 196, 70), (205, 228, 140), r=int(80 * k), seg=8, seed=3)
    w = w.crop((0, 0, w.width, w.height // 2 + 4 * S))
    L_.alpha_composite(w.rotate(-20, expand=True), (int(370 * s), int(95 * s)))
    d = ImageDraw.Draw(L_)
    d.line([(x0, top), (x0 + 12 * s, bot), (x1 - 12 * s, bot), (x1, top)], fill=CREAM, width=int(11 * s))
    d.rectangle((x0 + 12 * s, bot - 34 * s, x1 - 12 * s, bot), fill=(240, 228, 210))
    d.ellipse((x0, top - 22 * s, x1, top + 22 * s), outline=CREAM, width=int(8 * s))
    d.line((x0 + 40 * s, top + 60 * s, x0 + 52 * s, bot - 120 * s), fill=(255, 255, 250), width=int(12 * s))
    return L_


def art_ship():
    L_ = Image.new("RGBA", (900 * S, 760 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L_)
    # hull
    d.polygon([(90 * S, 470 * S), (810 * S, 470 * S), (720 * S, 620 * S), (180 * S, 620 * S)], fill=(120, 74, 44))
    d.rectangle((90 * S, 455 * S, 810 * S, 485 * S), fill=(86, 52, 32))
    for x in (260, 400, 540, 680):
        d.ellipse(((x - 16) * S, 520 * S, (x + 16) * S, 552 * S), fill=(40, 28, 22))
    # masts + sails
    for (mx, h, sw) in [(330, 400, 200), (580, 360, 180)]:
        d.rectangle(((mx - 9) * S, (470 - h) * S, (mx + 9) * S, 470 * S), fill=(86, 52, 32))
        d.polygon([((mx - sw / 2) * S, (470 - h + 40) * S), ((mx + sw / 2) * S, (470 - h + 40) * S), ((mx + sw / 2 - 20) * S, (470 - h / 2) * S), ((mx - sw / 2 + 20) * S, (470 - h / 2) * S)], fill=CREAM)
        d.polygon([((mx - sw / 2 - 10) * S, (470 - h / 2 + 15) * S), ((mx + sw / 2 + 10) * S, (470 - h / 2 + 15) * S), ((mx + sw / 2 - 10) * S, 440 * S), ((mx - sw / 2 + 10) * S, 440 * S)], fill=(236, 226, 200))
    # flag
    d.polygon([(339 * S, 70 * S), (440 * S, 95 * S), (339 * S, 120 * S)], fill=(40, 34, 30))
    # waves
    for i, y in enumerate((640, 690)):
        pts = [(x * S, (y + 18 * math.sin(x / 45 + i)) * S) for x in range(40, 861, 10)]
        d.line(pts, fill=(120, 170, 170), width=16 * S)
    # mint leaf floating near (medicine)
    draw_leaf(d, 790 * S, 260 * S, 170 * S, 38 * S, -0.6)
    return L_


def art_word():
    """'MOJO?' tag card for the name page."""
    L_ = Image.new("RGBA", (760 * S, 640 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L_)
    d.rounded_rectangle((60 * S, 80 * S, 700 * S, 560 * S), 40 * S, fill=(242, 234, 214), outline=INK, width=6 * S)
    d.ellipse((610 * S, 120 * S, 660 * S, 170 * S), fill=(34, 24, 20))
    f = F(BEBAS, 170)
    for i, (w, c) in enumerate([("MOJO?", (170, 50, 50)), ("MOJADITO?", MINT_D)]):
        ff = f
        while d.textlength(w, font=ff) > 560 * S: ff = F(BEBAS, ff.size // S - 6)
        tw = d.textlength(w, font=ff)
        d.text((380 * S - tw / 2, (150 + i * 190) * S), w, font=ff, fill=c)
    return L_
