from styles import *

COPPER_BG = (199, 92, 44)
CREAM = (246, 234, 214)
DARK = (30, 22, 18)
GREEN_BG = (26, 62, 48)
LIMEC = (150, 196, 70)
NAPKIN = (250, 248, 243)


def grain(img, cols, n=40000, seed=9):
    random.seed(seed)
    d = ImageDraw.Draw(img)
    for _ in range(n):
        d.point((random.randrange(W), random.randrange(H)), fill=random.choice(cols))


def wood(img):
    d = ImageDraw.Draw(img)
    for y in range(H):
        v = math.sin(y / (7 * S) + math.sin(y / (90 * S)) * 3) * 6 + math.sin(y / (2.3 * S)) * 3
        d.line((0, y, W, y), fill=(int(52 + v), int(34 + v * 0.7), int(22 + v * 0.5)))


def napkin(nw, nh=None, fold=True):
    nh = nh or nw
    nap = Image.new("RGBA", (nw, nh), NAPKIN + (255,))
    nd = ImageDraw.Draw(nap)
    for i in range(0, max(nw, nh), 26 * S):
        for (x, y) in [(i, 34 * S), (i, nh - 34 * S), (34 * S, i), (nw - 34 * S, i)]:
            if x <= nw and y <= nh:
                nd.ellipse((x - 5 * S, y - 5 * S, x + 5 * S, y + 5 * S), fill=(232, 229, 222))
    nd.rectangle((60 * S, 60 * S, nw - 60 * S, nh - 60 * S), outline=(236, 233, 226), width=3 * S)
    if fold:
        nd.line((nw // 2, 0, nw // 2, nh), fill=(238, 235, 229), width=4 * S)
        nd.line((0, nh // 2, nw, nh // 2), fill=(238, 235, 229), width=4 * S)
    return nap


def sketch_mug(base, cx, top, k, ink, fill=(200, 110, 55, 140), lime=(130, 170, 60, 150), lw=5, seed=4):
    """hand-drawn copper mug on RGBA/RGB image `base`"""
    random.seed(seed)
    col = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    bw, bh = 300 * S * k, 300 * S * k
    lx, ly = cx + 80 * S * k, top - 70 * S * k
    if fill:
        for i in range(int(40)):
            y2 = top + 10 * S * k + i * 7 * S * k
            cd.line((cx - bw / 2 + 10 * S * k + random.uniform(-6, 6) * S * k, y2, cx + bw / 2 - 18 * S * k + random.uniform(-10, 10) * S * k, y2 + random.uniform(-8, 8) * S * k), fill=fill, width=int(7 * S * k))
    if lime:
        for i in range(16):
            a = i * 2 * math.pi / 16
            cd.line((lx, ly, lx + math.cos(a) * 62 * S * k, ly + math.sin(a) * 62 * S * k), fill=lime, width=int(9 * S * k))
    if base.mode == "RGBA":
        base.alpha_composite(col)
    else:
        base.paste(col, (0, 0), col)
    nd = ImageDraw.Draw(base)
    W5 = int(lw * S * k)
    mug = [(cx - bw / 2, top), (cx + bw / 2, top), (cx + bw / 2 - 12 * S * k, top + bh), (cx - bw / 2 + 12 * S * k, top + bh)]
    pts = []
    for a, b in zip(mug, mug[1:] + mug[:1]):
        for i in range(10):
            pts.append((a[0] + (b[0] - a[0]) * i / 10, a[1] + (b[1] - a[1]) * i / 10))
    wobble(nd, pts, ink, W5, closed=True, passes=3, jitter=3 * k)
    wobble(nd, sk_rect(cx - bw / 2 - 14 * S * k, top - 24 * S * k, cx + bw / 2 + 14 * S * k, top + 6 * S * k), ink, int(W5 * 0.8), closed=True, jitter=3 * k)
    wobble(nd, sk_ellipse(cx + bw / 2 + 50 * S * k, top + 140 * S * k, 70 * S * k, 100 * S * k, 40, -math.pi / 2, math.pi / 2), ink, int(W5 * 1.2), passes=3, jitter=3 * k)
    for i in range(14):
        x = cx - bw / 2 + 20 * S * k + i * 9 * S * k
        wobble(nd, [(x, top + 30 * S * k), (x - 6 * S * k, top + bh - 20 * S * k)], ink, max(2, int(2 * S * k)), jitter=2 * k, passes=1)
    for _ in range(18):
        x = random.uniform(cx - 60 * S * k, cx + bw / 2 - 30 * S * k); y2 = random.uniform(top + 40 * S * k, top + bh - 40 * S * k)
        nd.arc((x, y2, x + 18 * S * k, y2 + 12 * S * k), 200, 340, fill=ink, width=max(2, int(2 * S * k)))
    wobble(nd, sk_ellipse(lx, ly, 70 * S * k, 70 * S * k), ink, int(W5 * 0.8), passes=2, jitter=3 * k)
    for i in range(6):
        a = i * math.pi / 3
        wobble(nd, [(lx, ly), (lx + math.cos(a) * 60 * S * k, ly + math.sin(a) * 60 * S * k)], ink, int(W5 * 0.6), passes=1, jitter=3 * k)
    wobble(nd, sk_rect(cx - 110 * S * k, top - 110 * S * k, cx - 10 * S * k, top - 10 * S * k), ink, int(W5 * 0.8), closed=True, jitter=3 * k)


def stack(d, words, x, y, maxw, font_path, size, colors, lh=0.95):
    for i, wd in enumerate(words):
        s = size
        f = F(font_path, s)
        while d.textlength(wd, font=f) > maxw:
            s -= 4; f = F(font_path, s)
        d.text((x, y), wd, font=f, fill=colors[i % len(colors)] if isinstance(colors, list) else colors)
        y += int(f.size * lh)
    return y


def drop_shadow(img, box, blur=28, alpha=190):
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rectangle(box, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur * S))
    img.paste((10, 6, 4), mask=sh)


def tape(img, cx, cy, w, h, ang):
    t = Image.new("RGBA", (int(w), int(h)), (236, 228, 205, 170))
    td = ImageDraw.Draw(t)
    for x in range(0, int(w), 6 * S):
        td.line((x, 0, x, h), fill=(225, 216, 192, 120), width=S)
    t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
    img.paste(t, (int(cx - t.width / 2), int(cy - t.height / 2)), t)


WORDS = ["BENİ LEZZET", "İÇİN DEĞİL,", "STOK ERİTMEK", "İÇİN İCAT", "ETTİLER."]


# 1: napkin with big stamped poster type
def v1():
    img = Image.new("RGB", (W, H)); wood(img)
    nw, nh = 960 * S, 1180 * S
    nap = napkin(nw, nh)
    nd = ImageDraw.Draw(nap)
    INK = (40, 28, 22)
    y = stack(nd, WORDS, 90 * S, 90 * S, nw - 180 * S, BEBAS, 150, [INK, INK, (196, 90, 42), (196, 90, 42), INK], 0.96)
    sketch_mug(nap, nw // 2 + 150 * S, y + 110 * S, 0.72, INK)
    nd.text((90 * S, nh - 150 * S), "— Moscow Mule", font=F(BRUSH, 52), fill=INK)
    nap = nap.rotate(2, expand=True, resample=Image.BICUBIC)
    px, py = (W - nap.width) // 2, (H - nap.height) // 2 + 20 * S
    drop_shadow(img, (px + 30 * S, py + 40 * S, px + nap.width - 10 * S, py + nap.height + 10 * S))
    img.paste(nap, (px, py), nap)
    save(img, "P1_pecete_poster.jpg")


# 2: copper poster, cream hand-sketched mug
def v2():
    img = Image.new("RGB", (W, H), COPPER_BG)
    grain(img, [(190, 86, 40), (206, 98, 50)])
    d = ImageDraw.Draw(img)
    y = stack(d, WORDS, 75 * S, 90 * S, W - 150 * S, BEBAS, 165, [CREAM, CREAM, DARK, DARK, CREAM], 0.95)
    sketch_mug(img, 720 * S, 1040 * S, 0.75, CREAM, fill=None, lime=(150, 196, 70, 230), lw=6)
    d.text((75 * S, 1240 * S), "— Moscow Mule", font=F(BRUSH, 56), fill=CREAM)
    save(img, "P2_poster_cizim.jpg")


# 3: full-bleed napkin close-up, marker handwriting
def v3():
    nap = napkin(W, H)
    img = nap.convert("RGBA")
    d = ImageDraw.Draw(img)
    INK = (34, 24, 20)
    f = F(BRUSH, 120)
    y = 130 * S
    for line in wrap(d, HOOK, f, W - 220 * S):
        d.text((110 * S, y), line, font=f, fill=INK)
        y += 120 * S
    # underline "stok eritmek" style scribble
    wobble(d, [(110 * S + i * 40 * S, y + 10 * S + math.sin(i) * 6 * S) for i in range(16)], (196, 90, 42), 8 * S, passes=2)
    sketch_mug(img, W // 2 - 60 * S, y + 300 * S, 1.25, INK)
    st = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(st).ellipse((W - 420 * S, H - 470 * S, W - 90 * S, H - 140 * S), outline=(170, 110, 60, 90), width=16 * S)
    st = st.filter(ImageFilter.GaussianBlur(4 * S))
    img.alpha_composite(st)
    d = ImageDraw.Draw(img)
    d.text((110 * S, H - 170 * S), "konuşan kokteyller", font=F(BRUSH, 50), fill=(150, 130, 110))
    save(img, "P3_pecete_yakin.jpg")


# 4: bottle-green poster + taped napkin sketch
def v4():
    img = Image.new("RGB", (W, H), GREEN_BG)
    grain(img, [(22, 56, 43), (32, 70, 54)])
    d = ImageDraw.Draw(img)
    stack(d, WORDS[:3], 75 * S, 110 * S, W - 150 * S, BEBAS, 160, [CREAM, CREAM, (222, 120, 64)], 0.95)
    d.text((75 * S, 110 * S + int(160 * S * 0.95) * 3 + 10 * S), "İÇİN İCAT ETTİLER.", font=F(BEBAS, 110), fill=(222, 120, 64))
    nw = 480 * S
    nap = napkin(nw)
    sketch_mug(nap, nw // 2 - 30 * S, 190 * S, 0.75, (40, 28, 22))
    ImageDraw.Draw(nap).text((60 * S, nw - 120 * S), "— Moscow Mule", font=F(BRUSH, 44), fill=(40, 28, 22))
    nap = nap.rotate(-6, expand=True, resample=Image.BICUBIC)
    px, py = W - nap.width - 50 * S, H - nap.height - 40 * S
    drop_shadow(img, (px + 30 * S, py + 30 * S, px + nap.width, py + nap.height), 24)
    img.paste(nap, (px, py), nap)
    tape(img, px + nap.width / 2, py + 20 * S, 220 * S, 60 * S, 4)
    d.text((75 * S, H - 120 * S), "konuşan kokteyller · 01", font=F(MONO_B, 28), fill=CREAM)
    save(img, "P4_yesil_kolaj.jpg")


# 5: cream paper, rubber-stamp poster type + small napkin
def v5():
    PAPER = (241, 232, 214)
    img = Image.new("RGB", (W, H), PAPER)
    grain(img, [(230, 219, 198), (248, 241, 228)], 60000)
    stamp = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(stamp)
    stack(sd, WORDS, 75 * S, 100 * S, W - 150 * S, BEBAS, 150, 255, 0.95)
    sp = Image.new("L", (W, H), 255)
    spd = ImageDraw.Draw(sp)
    random.seed(2)
    for _ in range(90000):
        x, y = random.randrange(W), random.randrange(H)
        spd.point((x, y), fill=random.choice([0, 0, 90]))
    stamp = ImageChops.multiply(stamp, sp.filter(ImageFilter.GaussianBlur(0.8)))
    img.paste((196, 86, 40), (0, 0), stamp)
    nw = 400 * S
    nap = napkin(nw)
    sketch_mug(nap, nw // 2 - 25 * S, 160 * S, 0.62, (40, 28, 22))
    nap = nap.rotate(5, expand=True, resample=Image.BICUBIC)
    px, py = 80 * S, H - nap.height - 50 * S
    drop_shadow(img, (px + 20 * S, py + 30 * S, px + nap.width, py + nap.height), 20, 120)
    img.paste(nap, (px, py), nap)
    d = ImageDraw.Draw(img)
    d.text((W - 470 * S, H - 230 * S), "— Moscow Mule", font=F(BRUSH, 64), fill=(40, 28, 22))
    d.text((W - 470 * S, H - 140 * S), "konuşan kokteyller · 01", font=F(MONO_B, 26), fill=(120, 100, 80))
    save(img, "P5_muhur.jpg")


v1(); v2(); v3(); v4(); v5()
print("ok")
