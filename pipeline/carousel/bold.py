"""Bold inner pages (2-6) – same attention format as the covers:
big headline, giant flat filled illustration over a colour disc that bleeds off the edge, short body text.
Usage: from bold import *; render_pages(pal, prefix, pages)  where pages = [dict(label, big, art, body)]"""
import math, random
from kk import *

INK = (34, 24, 20)

def disc(img, P, cx, cy, r, alpha=255, col=None):
    l = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    c = col or P["emph_text"]
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=c + (alpha,))
    img.alpha_composite(l)

def shadow_of(layer, blur=16, op=140, dx=14, dy=18):
    sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, op), (0, 0), layer)
    sh = sh.filter(ImageFilter.GaussianBlur(blur * S))
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (int(dx * S), int(dy * S)) if False else (0, 0))
    return sh

def place(img, layer, x, y, rot=0, shadow=True, maxw=640, maxh=520):
    if rot: layer = layer.rotate(rot, expand=True, resample=Image.BICUBIC)
    k = min(1.0, maxw * S / layer.width, maxh * S / layer.height)
    if k < 1: layer = layer.resize((int(layer.width * k), int(layer.height * k)), Image.LANCZOS)
    if shadow:
        sh = Image.new("RGBA", layer.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 130), (0, 0), layer)
        sh = sh.filter(ImageFilter.GaussianBlur(16 * S))
        img.alpha_composite(sh, (int(x - layer.width / 2 + 16 * S), int(y - layer.height / 2 + 22 * S)))
    img.alpha_composite(layer, (int(x - layer.width / 2), int(y - layer.height / 2)))

# ---------------- flat illustrations (return RGBA layers) ----------------
def art_bottle(liquid, glass=(225, 232, 228), label="", label_col=(246, 234, 214), h=640, cap=(60, 40, 30), round_=False):
    w = int(h * (0.5 if round_ else 0.36)) * S; H_ = h * S
    L = Image.new("RGBA", (w + 40 * S, H_ + 40 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cx = L.width / 2; top = 20 * S
    neck_w = w * .28
    body_top = top + H_ * (.45 if round_ else .32)
    d.rectangle((cx - neck_w / 2, top + 40 * S, cx + neck_w / 2, body_top + 20 * S), fill=glass)
    d.rounded_rectangle((cx - neck_w / 2 - 6 * S, top, cx + neck_w / 2 + 6 * S, top + 60 * S), 10 * S, fill=cap)
    if round_:
        d.ellipse((cx - w / 2, body_top - 40 * S, cx + w / 2, top + H_), fill=glass)
        d.ellipse((cx - w / 2 + 16 * S, body_top + H_ * .12, cx + w / 2 - 16 * S, top + H_ - 16 * S), fill=liquid)
    else:
        d.polygon([(cx - neck_w / 2, body_top), (cx - w / 2, body_top + 90 * S), (cx + w / 2, body_top + 90 * S), (cx + neck_w / 2, body_top)], fill=glass)
        d.rounded_rectangle((cx - w / 2, body_top + 80 * S, cx + w / 2, top + H_), 40 * S, fill=glass)
        d.rounded_rectangle((cx - w / 2 + 16 * S, body_top + 150 * S, cx + w / 2 - 16 * S, top + H_ - 16 * S), 30 * S, fill=liquid)
    lh = H_ * .26; ly = top + H_ * .58
    d.rounded_rectangle((cx - w / 2 + 22 * S, ly, cx + w / 2 - 22 * S, ly + lh), 14 * S, fill=label_col)
    if label:
        f = F(BEBAS, int(lh / S * .36))
        while d.textlength(label, font=f) > w - 70 * S: f = F(BEBAS, f.size // S - 4)
        tw = d.textlength(label, font=f)
        d.text((cx - tw / 2, ly + lh * .26), label, font=f, fill=INK)
    d.line((cx - w / 2 + 40 * S, body_top + 120 * S, cx - w / 2 + 40 * S, top + H_ - 60 * S), fill=(255, 255, 255, 170), width=14 * S)
    return L

def art_wheel(rind, flesh, flesh_l, pith=(242, 238, 214), r=330, seg=10, seed=1):
    R = r * S; L = Image.new("RGBA", (2 * R + 20 * S, 2 * R + 20 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    c = L.width / 2
    d.ellipse((c - R, c - R, c + R, c + R), fill=rind)
    d.ellipse((c - R * .92, c - R * .92, c + R * .92, c + R * .92), fill=pith)
    for i in range(seg):
        a0 = i * 2 * math.pi / seg + .06; a1 = (i + 1) * 2 * math.pi / seg - .06
        pts = [(c + 26 * S * math.cos((a0 + a1) / 2), c + 26 * S * math.sin((a0 + a1) / 2))]
        pts += [(c + R * .85 * math.cos(a0 + (a1 - a0) * j / 16), c + R * .85 * math.sin(a0 + (a1 - a0) * j / 16)) for j in range(17)]
        d.polygon(pts, fill=flesh)
        rr = random.Random(seed * 50 + i)
        for _ in range(34):
            a = rr.uniform(a0 + .04, a1 - .04); r0 = rr.uniform(50 * S, R * .8); r1 = min(R * .83, r0 + rr.uniform(14, 44) * S)
            d.line((c + r0 * math.cos(a), c + r0 * math.sin(a), c + r1 * math.cos(a), c + r1 * math.sin(a)), fill=flesh_l, width=int(rr.uniform(3, 7) * S))
    return L

def art_sugar(n=3, size=200):
    s = size * S; L = Image.new("RGBA", (int(s * 2.6), int(s * 2.2)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    spots = [(s * .9, s * 1.25), (s * 1.75, s * 1.35), (s * 1.3, s * .55)][:n]
    for (x, y) in spots:
        top = [(x, y - s * .35), (x + s * .5, y - s * .1), (x, y + s * .15), (x - s * .5, y - s * .1)]
        d.polygon(top, fill=(255, 253, 248))
        d.polygon([(x - s * .5, y - s * .1), (x, y + s * .15), (x, y + s * .75), (x - s * .5, y + s * .5)], fill=(226, 220, 208))
        d.polygon([(x + s * .5, y - s * .1), (x, y + s * .15), (x, y + s * .75), (x + s * .5, y + s * .5)], fill=(205, 198, 186))
        rr = random.Random(int(x))
        for _ in range(40):
            px = x + rr.uniform(-s * .45, s * .45); py = y + rr.uniform(-s * .1, s * .6)
            d.point((px, py), fill=(250, 248, 240))
    return L

def art_coupe(liquid, k=1.0, frozen=False, garnish=None):
    s = S * k; L = Image.new("RGBA", (int(760 * s), int(760 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cx, top, rim = L.width / 2, 120 * s, 330 * s
    bowl = [(cx - rim, top), (cx - 230 * s, top + 140 * s), (cx - 80 * s, top + 200 * s), (cx - 16 * s, top + 215 * s),
            (cx + 16 * s, top + 215 * s), (cx + 80 * s, top + 200 * s), (cx + 230 * s, top + 140 * s), (cx + rim, top)]
    d.polygon(bowl, fill=liquid)
    d.ellipse((cx - rim, top - 36 * s, cx + rim, top + 36 * s), fill=tuple(min(255, c + 25) for c in liquid))
    if frozen:  # slushy dome
        d.ellipse((cx - rim * .9, top - 120 * s, cx + rim * .9, top + 40 * s), fill=tuple(min(255, c + 35) for c in liquid))
        rr = random.Random(3)
        for _ in range(140):
            x = rr.uniform(cx - rim * .8, cx + rim * .8); y = rr.uniform(top - 100 * s, top + 20 * s)
            d.ellipse((x - 5 * s, y - 5 * s, x + 5 * s, y + 5 * s), fill=(255, 255, 250))
    d.line(bowl, fill=(246, 234, 214), width=int(9 * s))
    d.rectangle((cx - 12 * s, top + 210 * s, cx + 12 * s, top + 520 * s), fill=(246, 234, 214))
    d.ellipse((cx - 170 * s, top + 505 * s, cx + 170 * s, top + 550 * s), fill=(246, 234, 214))
    d.line((cx - rim * .7, top + 40 * s, cx - rim * .45, top + 120 * s), fill=(255, 255, 255), width=int(12 * s))
    if garnish == "lime":
        g = art_wheel((70, 110, 35), (150, 196, 70), (205, 228, 140), r=int(95 * k), seg=8, seed=9)
        L.alpha_composite(g, (int(cx + rim - g.width * .55), int(top - g.height * .6)))
    return L

def art_rocks(liquid, k=1.0, cube=True, peel=False):
    s = S * k; L = Image.new("RGBA", (int(700 * s), int(640 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, x1, top, bot = 70 * s, 630 * s, 110 * s, 600 * s
    lt = top + 130 * s
    d.polygon([(x0 + 14 * s, lt), (x0 + 28 * s, bot - 34 * s), (x1 - 28 * s, bot - 34 * s), (x1 - 14 * s, lt)], fill=liquid)
    d.ellipse((x0 + 14 * s, lt - 24 * s, x1 - 14 * s, lt + 24 * s), fill=tuple(min(255, c + 24) for c in liquid))
    if cube:
        cb = [(250 * s, lt - 90 * s), (500 * s, lt - 110 * s), (530 * s, lt + 150 * s), (280 * s, lt + 170 * s)]
        d.polygon(cb, fill=(240, 222, 202)); d.line(cb + [cb[0]], fill=(255, 250, 244), width=int(6 * s))
    if peel:
        d.rounded_rectangle((420 * s, 40 * s, 640 * s, 110 * s), int(34 * s), fill=(255, 166, 50), outline=(246, 234, 214), width=int(8 * s))
    d.rectangle((x0 + 28 * s, bot - 38 * s, x1 - 28 * s, bot), fill=(240, 228, 210))
    d.line([(x0, top), (x0 + 28 * s, bot), (x1 - 28 * s, bot), (x1, top)], fill=(246, 234, 214), width=int(11 * s))
    d.ellipse((x0, top - 28 * s, x1, top + 28 * s), outline=(246, 234, 214), width=int(9 * s))
    d.line((x0 + 60 * s, top + 70 * s, x0 + 80 * s, top + 330 * s), fill=(255, 250, 240), width=int(12 * s))
    return L

def art_mine():
    L = Image.new("RGBA", (900 * S, 700 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    # mine cart full of ore
    d.polygon([(150 * S, 330 * S), (750 * S, 330 * S), (690 * S, 560 * S), (210 * S, 560 * S)], fill=(150, 96, 60))
    d.rectangle((150 * S, 330 * S, 750 * S, 370 * S), fill=(110, 70, 44))
    rr = random.Random(2)
    for _ in range(26):
        x = rr.uniform(190, 710) * S; y = rr.uniform(250, 340) * S; r = rr.uniform(26, 50) * S
        d.ellipse((x - r, y - r * .8, x + r, y + r * .8), fill=rr.choice([(90, 80, 74), (120, 108, 98), (70, 62, 58)]))
    for x in (290, 610):
        d.ellipse(((x - 62) * S, 520 * S, (x + 62) * S, 644 * S), fill=(46, 40, 38)); d.ellipse(((x - 20) * S, 562 * S, (x + 20) * S, 602 * S), fill=(200, 190, 180))
    d.rectangle((60 * S, 650 * S, 840 * S, 668 * S), fill=(120, 90, 60))
    # pickaxe leaning
    d.line((640 * S, 40 * S, 800 * S, 330 * S), fill=(150, 100, 60), width=26 * S)
    d.arc((520 * S, 0, 820 * S, 160 * S), 190, 350, fill=(200, 205, 210), width=36 * S)
    return L

def art_newspaper(year="1806", head="COCK-TAIL"):
    L = Image.new("RGBA", (760 * S, 820 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle((40 * S, 40 * S, 720 * S, 780 * S), fill=(242, 234, 214))
    d.rectangle((40 * S, 40 * S, 720 * S, 780 * S), outline=INK, width=6 * S)
    f = F(BEBAS, 92); tw = d.textlength("THE BALANCE", font=f)
    d.text((380 * S - tw / 2, 70 * S), "THE BALANCE", font=f, fill=INK)
    d.line((80 * S, 190 * S, 680 * S, 190 * S), fill=INK, width=6 * S)
    f2 = F(BEBAS, 150); tw = d.textlength(year, font=f2)
    d.text((380 * S - tw / 2, 205 * S), year, font=f2, fill=(170, 50, 50))
    f3 = F(BEBAS, 70); tw = d.textlength(head, font=f3)
    d.rectangle((380 * S - tw / 2 - 20 * S, 395 * S, 380 * S + tw / 2 + 20 * S, 480 * S), fill=(255, 200, 90))
    d.text((380 * S - tw / 2, 400 * S), head, font=f3, fill=INK)
    for i in range(7):
        y = (520 + i * 34) * S
        d.line((80 * S, y, (680 if i % 3 else 520) * S, y), fill=(120, 110, 100), width=10 * S)
    return L

# ---------------- page renderer ----------------
def bold_page(P, idx, label, big, art, art_xy, art_rot, disc_xy, body_parts, seed, disc_col=None):
    img = bg(P, seed)
    header(img, P, idx, label)
    disc(img, P, disc_xy[0] * S, disc_xy[1] * S, 285 * S, 255, disc_col)
    place(img, art, art_xy[0] * S, art_xy[1] * S, art_rot)
    d = ImageDraw.Draw(img)
    f = F(BEBAS, 132)
    for i, ln in enumerate(big):
        while d.textlength(ln, font=f) > 930 * S: f = F(BEBAS, f.size // S - 6)
    for i, ln in enumerate(big):
        d.text((MX, (150 + i * 128) * S), ln, font=f, fill=P["emph_text"] if i == len(big) - 1 else P["text"])
    body(img, P, body_parts, 1010 * S, 46)
    return img
