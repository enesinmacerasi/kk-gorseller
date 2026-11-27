from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, random

S = 2
W, H = 1080 * S, 1350 * S
FD = "/home/claude/fonts/"
SHRIK = FD + "shrikhand.ttf"
BEBAS = FD + "bebas-neue.ttf"
BRUSH = FD + "caveat-brush.ttf"
MONO_B = "/usr/share/fonts/truetype/google-fonts/ofl/anonymouspro/AnonymousPro-Bold.ttf"
HOOK = "Beni lezzet için değil, stok eritmek için icat ettiler."


def F(p, s):
    return ImageFont.truetype(p, int(s * S))


def wrap(d, text, f, maxw):
    out, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out


def save(img, name):
    img.convert("RGB").resize((1080, 1350), Image.LANCZOS).save(name, quality=95)


# =============== A: 1940s bar matchbook / riso print ===============
def style_a():
    PAPER = (241, 232, 214)
    ORANGE = (214, 92, 42)
    GREEN = (28, 74, 56)
    img = Image.new("RGB", (W, H), PAPER)
    random.seed(1)
    d = ImageDraw.Draw(img)
    for _ in range(60000):
        x, y = random.randrange(W), random.randrange(H)
        d.point((x, y), fill=random.choice([(230, 219, 198), (248, 241, 228), (226, 214, 192)]))

    def ink_layer(color, draw_fn, offset=(0, 0)):
        m = Image.new("L", (W, H), 0)
        draw_fn(ImageDraw.Draw(m), m)
        # riso texture: knock out random specks
        sp = Image.new("L", (W, H), 255)
        sd = ImageDraw.Draw(sp)
        for _ in range(26000):
            x, y = random.randrange(W), random.randrange(H)
            sd.point((x, y), fill=random.choice([0, 120]))
        m = ImageChops.multiply(m, sp)
        m = ImageChops.offset(m, *offset)
        lay = Image.new("RGB", (W, H), color)
        # multiply ink onto paper
        blended = ImageChops.multiply(img, lay)
        img.paste(blended, (0, 0), m)

    # frame like a matchbook cover
    def frame(d, m):
        d.rectangle((50 * S, 50 * S, W - 50 * S, H - 50 * S), outline=255, width=6 * S)
        d.rectangle((66 * S, 66 * S, W - 66 * S, H - 66 * S), outline=255, width=2 * S)
    ink_layer(GREEN, frame)

    # halftone mug (orange) + big sun circle behind
    def mug_half(d, m):
        cx, top = W // 2 - 40 * S, 640 * S
        bw, bh = 400 * S, 440 * S
        step = 16 * S
        for y in range(top, top + bh, step):
            for x in range(cx - bw // 2, cx + bw // 2, step):
                t = (x - (cx - bw // 2)) / bw
                shade = 0.35 + 0.65 * abs(t - 0.3) * 1.6
                r = step * 0.5 * min(1, shade)
                d.ellipse((x - r, y - r, x + r, y + r), fill=255)
        # rim + base solid
        d.rounded_rectangle((cx - bw // 2 - 14 * S, top - 30 * S, cx + bw // 2 + 14 * S, top + 10 * S), radius=14 * S, fill=255)
        d.rectangle((cx - bw // 2, top + bh - 20 * S, cx + bw // 2, top + bh), fill=255)
        # handle
        d.rounded_rectangle((cx + bw // 2 - 20 * S, top + 70 * S, cx + bw // 2 + 150 * S, top + 330 * S), radius=80 * S, outline=255, width=34 * S)
    ink_layer(ORANGE, mug_half)

    # green layer: lime, ice outlines, text (slightly misregistered)
    def green_stuff(d, m):
        cx, top = W // 2 - 40 * S, 640 * S
        lx, ly, r = cx + 130 * S, top - 80 * S, 90 * S
        d.ellipse((lx - r, ly - r, lx + r, ly + r), outline=255, width=12 * S)
        for i in range(8):
            a = i * math.pi / 4
            d.line((lx, ly, lx + math.cos(a) * r * 0.85, ly + math.sin(a) * r * 0.85), fill=255, width=6 * S)
        for (ox, oy, s) in [(-120, -70, 120), (-10, -90, 110)]:
            x, y = cx + ox * S, top + oy * S
            d.rounded_rectangle((x - s * S / 2, y - s * S / 2, x + s * S / 2, y + s * S / 2), radius=16 * S, outline=255, width=8 * S)
        # hook text
        f = F(SHRIK, 74)
        y = 140 * S
        for line in wrap(d, HOOK, f, W - 220 * S):
            tw = d.textlength(line, font=f)
            d.text(((W - tw) / 2, y), line, font=f, fill=255)
            y += 96 * S
        fb = F(BEBAS, 58)
        t = "MOSCOW MULE"
        d.text(((W - d.textlength(t, font=fb)) / 2, 1150 * S), t, font=fb, fill=255)
        fs = F(BEBAS, 34)
        t = "KONUŞAN KOKTEYLLER  ·  NO. 01"
        d.text(((W - d.textlength(t, font=fs)) / 2, 1225 * S), t, font=fs, fill=255)
    ink_layer(GREEN, green_stuff, offset=(4 * S, -3 * S))
    save(img, "A_kibrit.jpg")


# =============== B: bar napkin doodle ===============
def wobble(d, pts, fill, width, closed=False, jitter=3, passes=2):
    for p in range(passes):
        q = [(x + random.uniform(-jitter, jitter) * S, y + random.uniform(-jitter, jitter) * S) for x, y in pts]
        if closed:
            q.append(q[0])
        d.line(q, fill=fill, width=width, joint="curve")


def sk_rect(x0, y0, x1, y1, n=12):
    pts = []
    for i in range(n): pts.append((x0 + (x1 - x0) * i / n, y0))
    for i in range(n): pts.append((x1, y0 + (y1 - y0) * i / n))
    for i in range(n): pts.append((x1 - (x1 - x0) * i / n, y1))
    for i in range(n): pts.append((x0, y1 - (y1 - y0) * i / n))
    return pts


def sk_ellipse(cx, cy, rx, ry, n=60, a0=0, a1=2 * math.pi):
    return [(cx + math.cos(a0 + (a1 - a0) * i / n) * rx, cy + math.sin(a0 + (a1 - a0) * i / n) * ry) for i in range(n + 1)]


def style_b():
    random.seed(4)
    # dark bar-top wood
    img = Image.new("RGB", (W, H), (46, 30, 20))
    d = ImageDraw.Draw(img)
    for y in range(H):
        v = math.sin(y / (7 * S) + math.sin(y / (90 * S)) * 3) * 6 + math.sin(y / (2.3 * S)) * 3
        c = (int(52 + v), int(34 + v * 0.7), int(22 + v * 0.5))
        d.line((0, y, W, y), fill=c)
    img = img.filter(ImageFilter.GaussianBlur(0.6 * S))
    # napkin
    nw = 940 * S
    nap = Image.new("RGBA", (nw, nw), (250, 248, 243, 255))
    nd = ImageDraw.Draw(nap)
    # embossed border pattern
    for i in range(0, nw, 26 * S):
        for (x, y) in [(i, 34 * S), (i, nw - 34 * S), (34 * S, i), (nw - 34 * S, i)]:
            nd.ellipse((x - 5 * S, y - 5 * S, x + 5 * S, y + 5 * S), fill=(232, 229, 222))
    nd.rectangle((60 * S, 60 * S, nw - 60 * S, nw - 60 * S), outline=(236, 233, 226), width=3 * S)
    # fold lines
    nd.line((nw // 2, 0, nw // 2, nw), fill=(238, 235, 229), width=4 * S)
    nd.line((0, nw // 2, nw, nw // 2), fill=(238, 235, 229), width=4 * S)
    INK = (40, 28, 22)
    # copper ring stain
    st = Image.new("RGBA", nap.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    sd.ellipse((90 * S, nw - 300 * S, 330 * S, nw - 60 * S), outline=(170, 110, 60, 90), width=14 * S)
    st = st.filter(ImageFilter.GaussianBlur(4 * S))
    nap = Image.alpha_composite(nap, st)
    nd = ImageDraw.Draw(nap)
    # handwritten hook in a sketchy bubble
    f = F(BRUSH, 84)
    lines = wrap(nd, HOOK, f, nw - 260 * S)
    y = 120 * S
    for line in lines:
        nd.text((130 * S, y), line, font=f, fill=INK)
        y += 88 * S
    bx0, by0, bx1, by1 = 95 * S, 100 * S, nw - 95 * S, y + 30 * S
    wobble(nd, sk_ellipse((bx0 + bx1) / 2, (by0 + by1) / 2, (bx1 - bx0) / 2 + 20 * S, (by1 - by0) / 2 + 26 * S, 80, 0.15 * math.pi + math.pi / 2, 2 * math.pi + math.pi / 2), INK, 4 * S)
    tx = nw // 2 - 20 * S
    wobble(nd, [(tx - 30 * S, by1 + 18 * S), (tx + 10 * S, by1 + 110 * S), (tx + 50 * S, by1 + 14 * S)], INK, 4 * S)
    # sketch mug
    cx, top = nw // 2 - 40 * S, by1 + 160 * S
    bw, bh = 300 * S, 300 * S
    mug = [(cx - bw / 2, top), (cx + bw / 2, top), (cx + bw / 2 - 12 * S, top + bh), (cx - bw / 2 + 12 * S, top + bh)]
    pts = []
    for a, b in zip(mug, mug[1:] + mug[:1]):
        for i in range(10):
            pts.append((a[0] + (b[0] - a[0]) * i / 10, a[1] + (b[1] - a[1]) * i / 10))
    wobble(nd, pts, INK, 5 * S, closed=True, passes=3)
    wobble(nd, sk_rect(cx - bw / 2 - 14 * S, top - 24 * S, cx + bw / 2 + 14 * S, top + 6 * S), INK, 4 * S, closed=True)
    wobble(nd, sk_ellipse(cx + bw / 2 + 50 * S, top + 140 * S, 70 * S, 100 * S, 40, -math.pi / 2, math.pi / 2), INK, 6 * S, passes=3)
    # hatching shade on left
    for i in range(14):
        x = cx - bw / 2 + 20 * S + i * 9 * S
        wobble(nd, [(x, top + 30 * S), (x - 6 * S, top + bh - 20 * S)], INK, 2 * S, jitter=2, passes=1)
    # dents
    for _ in range(18):
        x = random.uniform(cx - 60 * S, cx + bw / 2 - 30 * S); y2 = random.uniform(top + 40 * S, top + bh - 40 * S)
        nd.arc((x, y2, x + 18 * S, y2 + 12 * S), 200, 340, fill=INK, width=2 * S)
    # lime + ice
    lx, ly = cx + 80 * S, top - 70 * S
    wobble(nd, sk_ellipse(lx, ly, 70 * S, 70 * S), INK, 4 * S, closed=False, passes=2)
    for i in range(6):
        a = i * math.pi / 3
        wobble(nd, [(lx, ly), (lx + math.cos(a) * 60 * S, ly + math.sin(a) * 60 * S)], INK, 3 * S, passes=1)
    wobble(nd, sk_rect(cx - 110 * S, top - 110 * S, cx - 10 * S, top - 10 * S), INK, 4 * S, closed=True)
    # copper marker splash on the mug (a quick colored-pencil fill)
    col = Image.new("RGBA", nap.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    for i in range(40):
        y2 = top + 10 * S + i * 7 * S
        cd.line((cx - bw / 2 + 10 * S + random.uniform(-6, 6) * S, y2, cx + bw / 2 - 18 * S + random.uniform(-10, 10) * S, y2 + random.uniform(-8, 8) * S), fill=(200, 110, 55, 140), width=7 * S)
    for i in range(16):
        a = i * 2 * math.pi / 16
        cd.line((lx, ly, lx + math.cos(a) * 62 * S, ly + math.sin(a) * 62 * S), fill=(130, 170, 60, 150), width=9 * S)
    nap = Image.alpha_composite(nap, col)
    nd = ImageDraw.Draw(nap)
    # signature
    fs = F(BRUSH, 46)
    nd.text((nw - 380 * S, nw - 130 * S), "— Moscow Mule", font=fs, fill=INK)
    nap = nap.rotate(-3, expand=True, resample=Image.BICUBIC)
    sh = Image.new("L", (W, H), 0)
    px, py = (W - nap.width) // 2, 220 * S
    ImageDraw.Draw(sh).rectangle((px + 30 * S, py + 40 * S, px + nap.width - 10 * S, py + nap.height + 10 * S), fill=200)
    sh = sh.filter(ImageFilter.GaussianBlur(30 * S))
    img.paste((10, 6, 4), mask=sh)
    img.paste(nap, (px, py), nap)
    d = ImageDraw.Draw(img)
    fl = F(BRUSH, 48)
    d.text((80 * S, 80 * S), "konuşan kokteyller", font=fl, fill=(232, 210, 180))
    t = "kaydır"
    tw = d.textlength(t, font=fl); ax = W - 80 * S
    d.text((ax - tw - 70 * S, H - 120 * S), t, font=fl, fill=(232, 210, 180))
    d.line((ax - 55 * S, H - 88 * S, ax, H - 88 * S), fill=(232, 210, 180), width=4 * S)
    d.line((ax - 18 * S, H - 102 * S, ax, H - 88 * S, ax - 18 * S, H - 74 * S), fill=(232, 210, 180), width=4 * S)
    save(img, "B_pecete.jpg")


# =============== C: big type poster ===============
def style_c():
    BG = (199, 92, 44)
    CREAM = (246, 234, 214)
    DARK = (30, 22, 18)
    LIMEC = (150, 196, 70)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    random.seed(9)
    for _ in range(40000):
        d.point((random.randrange(W), random.randrange(H)), fill=random.choice([(190, 86, 40), (206, 98, 50)]))
    # giant quote mark
    fq = F(SHRIK, 520)
    d.text((40 * S, -170 * S), "“", font=fq, fill=(176, 78, 36))
    # stacked big type
    words = ["BENİ LEZZET", "İÇİN DEĞİL,", "STOK ERİTMEK", "İÇİN İCAT", "ETTİLER."]
    y = 170 * S
    for i, wd in enumerate(words):
        size = 188
        f = F(BEBAS, size)
        while d.textlength(wd, font=f) > W - 150 * S:
            size -= 4; f = F(BEBAS, size)
        col = DARK if i in (2, 3) else CREAM
        d.text((75 * S, y), wd, font=f, fill=col)
        y += int(f.size * 0.95)
    # flat geometric mug cropped at bottom right
    cx, top = 760 * S, 1080 * S
    bw = 360 * S
    d.rounded_rectangle((cx + bw / 2 - 30 * S, top + 60 * S, cx + bw / 2 + 120 * S, top + 300 * S), radius=80 * S, outline=DARK, width=36 * S)
    d.polygon([(cx - bw / 2, top), (cx + bw / 2, top), (cx + bw / 2 - 14 * S, H + 50 * S), (cx - bw / 2 + 14 * S, H + 50 * S)], fill=DARK)
    d.rectangle((cx - bw / 2 - 16 * S, top - 30 * S, cx + bw / 2 + 16 * S, top + 8 * S), fill=DARK)
    d.ellipse((cx + 60 * S, top - 150 * S, cx + 230 * S, top + 20 * S), fill=LIMEC)
    d.ellipse((cx + 78 * S, top - 132 * S, cx + 212 * S, top + 2 * S), outline=CREAM, width=6 * S)
    fb = F(BEBAS, 46)
    d.text((75 * S, 1180 * S), "MOSCOW MULE", font=fb, fill=CREAM)
    fs = F(MONO_B, 26)
    d.text((75 * S, 1240 * S), "konuşan kokteyller · 01", font=fs, fill=DARK)
    save(img, "C_poster.jpg")


if __name__ == "__main__":
    style_a(); style_b(); style_c()

