from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, random

S = 2  # supersample
W, H = 1080 * S, 1350 * S
BG = (24, 17, 13)
BG2 = (38, 26, 19)
BONE = (239, 230, 214)
MUTED = (176, 160, 140)
COPPER = (201, 123, 69)
COPPER_D = (122, 62, 30)
COPPER_L = (240, 178, 120)
LIME = (143, 174, 58)

LORA = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
LORA_I = "/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf"
INTER = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
INTER_SB = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"


def font(path, size, var=None):
    f = ImageFont.truetype(path, size * S)
    if var:
        try:
            f.set_variation_by_name(var)
        except Exception:
            pass
    return f


def base():
    img = Image.new("RGB", (W, H), BG)
    # soft warm vignette glow
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W * 0.1, H * 0.15, W * 0.9, H * 0.85), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(260 * S))
    warm = Image.new("RGB", (W, H), BG2)
    img = Image.composite(warm, img, glow)
    # fine grain
    random.seed(7)
    d = ImageDraw.Draw(img)
    for _ in range(9000):
        x, y = random.randrange(W), random.randrange(H)
        c = random.choice([(32, 23, 18), (20, 14, 11)])
        d.point((x, y), fill=c)
    return img


def header(img, idx, total):
    d = ImageDraw.Draw(img)
    f = font(INTER_SB, 22)
    d.text((80 * S, 70 * S), "KONUŞAN KOKTEYLLER", font=f, fill=COPPER)
    t = f"{idx}/{total}"
    w = d.textlength(t, font=f)
    d.text((W - 80 * S - w, 70 * S), t, font=f, fill=MUTED)
    d.line((80 * S, 112 * S, W - 80 * S, 112 * S), fill=(70, 52, 40), width=2 * S)


def wrap(d, text, f, maxw):
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(" "), ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= maxw:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def text_block(img, x, y, text, f, fill, maxw, lh=1.35):
    d = ImageDraw.Draw(img)
    for line in wrap(d, text, f, maxw):
        d.text((x, y), line, font=f, fill=fill)
        y += int(f.size * lh)
    return y


# ---------- illustrations ----------
def copper_fill(w, h):
    g = Image.new("RGB", (w, h))
    gd = ImageDraw.Draw(g)
    for x in range(w):
        t = x / max(1, w - 1)
        # dark edges, bright highlight at ~30%
        k = math.exp(-((t - 0.3) ** 2) / 0.02) * 0.9 + math.exp(-((t - 0.75) ** 2) / 0.01) * 0.25
        edge = min(1, (1 - abs(t - 0.5) * 2) * 2.2)
        base = [COPPER_D[i] + (COPPER[i] - COPPER_D[i]) * edge for i in range(3)]
        col = tuple(int(base[i] + (COPPER_L[i] - base[i]) * min(1, k)) for i in range(3))
        gd.line((x, 0, x, h), fill=col)
    # hammered dimples
    random.seed(3)
    for _ in range(int(w * h / 900)):
        cx, cy = random.randrange(w), random.randrange(h)
        r = random.randint(4, 9) * S // 2 + 2
        px = g.getpixel((cx, cy))
        lighter = tuple(min(255, c + 22) for c in px)
        darker = tuple(max(0, c - 18) for c in px)
        gd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=darker)
        gd.ellipse((cx - r + 2, cy - r + 1, cx + r - 3, cy + r - 4), fill=lighter)
    return g.filter(ImageFilter.GaussianBlur(1.2 * S))


def lime_wheel(img, cx, cy, r, rot=0):
    d = ImageDraw.Draw(img)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(96, 128, 34))
    ri = r * 0.86
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), fill=(226, 232, 190))
    rp = r * 0.8
    d.ellipse((cx - rp, cy - rp, cx + rp, cy + rp), fill=(168, 196, 82))
    for i in range(9):
        a = rot + i * 2 * math.pi / 9
        d.line((cx, cy, cx + math.cos(a) * rp, cy + math.sin(a) * rp), fill=(226, 232, 190), width=max(2, int(r * 0.06)))
    d.ellipse((cx - r * 0.1, cy - r * 0.1, cx + r * 0.1, cy + r * 0.1), fill=(226, 232, 190))


def mug(img, cx, cy, s):
    """copper moscow mule mug centered on cx, body top at cy"""
    bw, bh = int(300 * s), int(330 * s)
    x0, y0 = cx - bw // 2, cy
    # shadow
    sh = Image.new("L", img.size, 0)
    sd = ImageDraw.Draw(sh)
    sd.ellipse((x0 - 30 * s, y0 + bh - 30 * s, x0 + bw + 80 * s, y0 + bh + 40 * s), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(30 * s))
    img.paste((8, 5, 4), mask=sh)
    # handle
    d = ImageDraw.Draw(img)
    hx = x0 + bw - 20 * s
    d.rounded_rectangle((hx, y0 + 60 * s, hx + 120 * s, y0 + 250 * s), radius=int(70 * s), outline=COPPER_D, width=int(34 * s))
    d.rounded_rectangle((hx + 4 * s, y0 + 64 * s, hx + 116 * s, y0 + 246 * s), radius=int(66 * s), outline=COPPER, width=int(18 * s))
    # ice + lime above rim
    for (ox, oy, sz) in [(-80, -40, 90), (10, -60, 100), (70, -30, 80)]:
        ix, iy, isz = cx + ox * s, y0 + oy * s, sz * s
        d.rounded_rectangle((ix - isz / 2, iy - isz / 2, ix + isz / 2, iy + isz / 2), radius=int(14 * s), fill=(214, 222, 220))
        d.rounded_rectangle((ix - isz / 2 + 8 * s, iy - isz / 2 + 8 * s, ix, iy), radius=int(10 * s), fill=(240, 244, 242))
    lime_wheel(img, int(cx + 95 * s), int(y0 - 45 * s), int(70 * s), 0.3)
    # body (slightly tapered)
    mask = Image.new("L", (bw, bh), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(0, 0), (bw, 0), (bw - 12 * s, bh - 30 * s), (12 * s, bh - 30 * s)], fill=255)
    md.rounded_rectangle((12 * s, bh - 80 * s, bw - 12 * s, bh), radius=int(30 * s), fill=255)
    img.paste(copper_fill(bw, bh), (x0, y0), mask)
    # rim
    d.rounded_rectangle((x0 - 8 * s, y0 - 12 * s, x0 + bw + 8 * s, y0 + 22 * s), radius=int(14 * s), fill=COPPER_L)
    d.rounded_rectangle((x0 - 8 * s, y0 + 6 * s, x0 + bw + 8 * s, y0 + 22 * s), radius=int(8 * s), fill=COPPER)
    # base band
    d.rectangle((x0 + 14 * s, y0 + bh - 34 * s, x0 + bw - 14 * s, y0 + bh - 26 * s), fill=COPPER_D)


def bottle(img, cx, by, s):
    d = ImageDraw.Draw(img)
    w, h = int(170 * s), int(420 * s)
    x0, y0 = cx - w // 2, by - h
    glass = (120, 112, 104)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle((x0, y0 + 150 * s, x0 + w, by), radius=int(30 * s), fill=glass + (150,))
    ld.polygon([(x0 + 10 * s, y0 + 170 * s), (cx - 26 * s, y0 + 60 * s), (cx + 26 * s, y0 + 60 * s), (x0 + w - 10 * s, y0 + 170 * s)], fill=glass + (150,))
    ld.rectangle((cx - 26 * s, y0, cx + 26 * s, y0 + 70 * s), fill=glass + (150,))
    ld.rectangle((cx - 32 * s, y0 - 30 * s, cx + 32 * s, y0 + 10 * s), fill=COPPER_D + (255,))
    # liquid
    ld.rounded_rectangle((x0 + 14 * s, y0 + 210 * s, x0 + w - 14 * s, by - 14 * s), radius=int(22 * s), fill=(220, 222, 214, 90))
    # highlight
    ld.rounded_rectangle((x0 + 22 * s, y0 + 180 * s, x0 + 40 * s, by - 40 * s), radius=int(9 * s), fill=(255, 255, 255, 70))
    img.paste(layer, (0, 0), layer)
    # cobweb
    for i in range(5):
        d.line((x0 - 60 * s, y0 + 40 * s, x0 + 30 * s * i, y0 + 160 * s - i * 10 * s), fill=(90, 80, 70), width=S)


def crates(img, cx, by, s):
    d = ImageDraw.Draw(img)
    cw, ch = int(260 * s), int(150 * s)
    wood, wood_d = (110, 72, 44), (70, 44, 26)
    pos = [(-cw // 2 - 10 * s, 0), (cw // 2 + 10 * s, 0), (0, -ch - 10 * s)]
    for ox, oy in pos:
        x0 = cx + ox - cw // 2
        y0 = by + oy - ch
        # bottle caps peeking
        for k in range(5):
            bx = x0 + 30 * s + k * 50 * s
            d.rectangle((bx, y0 - 34 * s, bx + 26 * s, y0), fill=(92, 64, 40))
            d.rectangle((bx - 3 * s, y0 - 44 * s, bx + 29 * s, y0 - 32 * s), fill=COPPER_D)
        d.rectangle((x0, y0, x0 + cw, y0 + ch), fill=wood)
        for k in range(3):
            yy = y0 + k * ch // 3
            d.line((x0, yy, x0 + cw, yy), fill=wood_d, width=4 * S)
        d.rectangle((x0, y0, x0 + cw, y0 + ch), outline=wood_d, width=6 * S)
    # dust
    random.seed(11)
    for _ in range(260):
        x = cx + random.randint(-420, 420) * s
        y = by + random.randint(-480, 10) * s
        r = random.choice([1, 1, 2]) * S
        d.ellipse((x - r, y - r, x + r, y + r), fill=(150, 130, 110))


def polaroid(img, cx, cy, s, angle):
    pw, ph = int(520 * s), int(620 * s)
    p = Image.new("RGBA", (pw, ph), BONE + (255,))
    pd = ImageDraw.Draw(p)
    pd.rectangle((36 * s, 36 * s, pw - 36 * s, pw - 36 * s), fill=(44, 32, 26))
    inner = Image.new("RGB", (pw, ph), (44, 32, 26))
    # little bar scene: mug + bottle
    tmp = Image.new("RGB", (pw, ph), (52, 38, 30))
    bottle(tmp, int(pw * 0.32), int(pw * 0.86), 0.62 * s / S * S / s * s if False else 0.62 * s)
    mug(tmp, int(pw * 0.6), int(pw * 0.5), 0.6 * s)
    m = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(m).rectangle((36 * s, 36 * s, pw - 36 * s, pw - 36 * s), fill=255)
    p.paste(tmp, (0, 0), m)
    # warm faded photo tint
    tint = Image.new("RGBA", (pw, ph), (230, 190, 140, 40))
    p = Image.alpha_composite(p, Image.composite(tint, Image.new("RGBA", (pw, ph), (0, 0, 0, 0)), m))
    p = p.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).rectangle((cx - p.width // 2 + 20 * s, cy - p.height // 2 + 30 * s, cx + p.width // 2 + 20 * s, cy + p.height // 2 + 30 * s), fill=170)
    sh = sh.filter(ImageFilter.GaussianBlur(28 * s))
    img.paste((6, 4, 3), mask=sh)
    img.paste(p, (cx - p.width // 2, cy - p.height // 2), p)


def number_tag(img, x, y, n, label):
    d = ImageDraw.Draw(img)
    fa = font(ANTON, 150)
    d.text((x, y), n, font=fa, fill=COPPER)
    nw = d.textlength(n, font=fa)
    fl = font(INTER_SB, 30)
    d.text((x + nw + 28 * S, y + 72 * S), label.upper(), font=fl, fill=BONE)


def finish(img, name):
    img.resize((1080, 1350), Image.LANCZOS).save(name, quality=95)


TOTAL = 7
MX = 80 * S
TW = W - 2 * MX
body = font(INTER, 40)
body_i = font(LORA_I, 44, "Italic")

# 1 cover
img = base(); header(img, 1, TOTAL)
d = ImageDraw.Draw(img)
fh = font(LORA, 92, "SemiBold")
y = text_block(img, MX, 190 * S, "Kimsenin istemediği üç şey,", fh, BONE, TW, 1.12)
y = text_block(img, MX, y, "bi kokteyl oldu.", font(LORA_I, 92, "SemiBold Italic"), COPPER_L, TW, 1.12)
mug(img, W // 2 - 50 * S, 700 * S, 1.38 * S)
fs = font(INTER_SB, 30)
d.text((MX, 1230 * S), "MOSCOW MULE", font=fs, fill=COPPER)
t = "kaydır  →"
d.text((W - MX - d.textlength(t, font=fs), 1230 * S), t, font=fs, fill=MUTED)
finish(img, "01.jpg")

# 2 vodka
img = base(); header(img, 2, TOTAL)
number_tag(img, MX, 170 * S, "1", "Satılmayan votka")
bottle(img, W // 2, 1000 * S, 1.25 * S)
text_block(img, MX, 1040 * S, "1940'larda Amerikalılar votka içmiyordu. John Martin, Smirnoff'un haklarını almıştı ama şişeler rafta kalıyordu.", body, BONE, TW)
finish(img, "02.jpg")

# 3 ginger beer
img = base(); header(img, 3, TOTAL)
number_tag(img, MX, 170 * S, "2", "Satılmayan zencefil birası")
crates(img, W // 2, 960 * S, 1.2 * S)
text_block(img, MX, 1040 * S, "Los Angeles'ta Cock 'n' Bull barının sahibi Jack Morgan kendi zencefil birasını yaptırdı. Kasalar bodrumda toz topluyordu.", body, BONE, TW)
finish(img, "03.jpg")

# 4 copper mug
img = base(); header(img, 4, TOTAL)
number_tag(img, MX, 170 * S, "3", "Bakır kupa")
mug(img, W // 2 - 50 * S, 560 * S, 1.2 * S)
text_block(img, MX, 1040 * S, "Kupanın nereden geldiği hâlâ tartışmalı. Üç ayrı rivayet var, birinde elinde satamadığı bakır kupalarla bi kadın bara giriyor.", body, BONE, TW)
finish(img, "04.jpg")

# 5 together
img = base(); header(img, 5, TOTAL)
d = ImageDraw.Draw(img)
fh2 = font(LORA, 78, "SemiBold")
y = text_block(img, MX, 200 * S, "Üç batık ürün", fh2, BONE, TW, 1.1)
text_block(img, MX, y, "aynı bardakta buluştu.", font(LORA_I, 78, "SemiBold Italic"), COPPER_L, TW, 1.1)
# three icons → mug
lime_wheel(img, W // 2 - 250 * S, 640 * S, 70 * S, 0.2)
lime_wheel(img, W // 2 + 250 * S, 640 * S, 70 * S, 1.1)
mug(img, W // 2 - 50 * S, 640 * S, 0.95 * S)
text_block(img, MX, 1060 * S, "Votka, zencefil birası, biraz lime. Bakır kupaya koydular, adını Moscow Mule koydular.", body, BONE, TW)
finish(img, "05.jpg")

# 6 polaroid marketing
img = base(); header(img, 6, TOTAL)
fh3 = font(LORA, 70, "SemiBold")
y = text_block(img, MX, 180 * S, "Asıl deha bardakta değil,", fh3, BONE, TW, 1.1)
text_block(img, MX, y, "fotoğraftaydı.", font(LORA_I, 70, "SemiBold Italic"), COPPER_L, TW, 1.1)
polaroid(img, W // 2, 680 * S, 0.95 * S, -5)
text_block(img, MX, 1030 * S, "Martin elinde Polaroid'le bar bar gezdi. Barmeni kupa ve şişeyle çekti, bi kopyasını ona bıraktı, diğerini bi sonraki bara gösterdi. İnternetten önce viral.", body, BONE, TW)
finish(img, "06.jpg")

# 7 recipe card
img = Image.new("RGB", (W, H), BONE)
d = ImageDraw.Draw(img)
random.seed(5)
for _ in range(14000):
    d.point((random.randrange(W), random.randrange(H)), fill=random.choice([(228, 218, 200), (245, 238, 225)]))
d.text((MX, 70 * S), "KONUŞAN KOKTEYLLER", font=font(INTER_SB, 22), fill=COPPER_D)
t = f"{TOTAL}/{TOTAL}"; f22 = font(INTER_SB, 22)
d.text((W - MX - d.textlength(t, font=f22), 70 * S), t, font=f22, fill=(140, 120, 100))
d.line((MX, 112 * S, W - MX, 112 * S), fill=(200, 185, 160), width=2 * S)
d.text((MX, 160 * S), "TARİF", font=font(INTER_SB, 30), fill=COPPER_D)
d.text((MX, 200 * S), "Moscow Mule", font=font(LORA, 104, "SemiBold"), fill=(40, 28, 20))
ing = [("4,5 cl", "votka"), ("1 cl", "taze lime suyu"), ("12 cl", "zencefil birası"), ("bol", "buz"), ("1", "lime dilimi (süs)")]
y = 380 * S
fa = font(ANTON, 58); fi = font(INTER, 42)
for amt, name in ing:
    d.text((MX, y), amt, font=fa, fill=COPPER_D)
    d.text((MX + 230 * S, y + 14 * S), name, font=fi, fill=(40, 28, 20))
    d.line((MX, y + 84 * S, W - MX, y + 84 * S), fill=(214, 200, 176), width=2 * S)
    y += 100 * S
y += 30 * S
y = text_block(img, MX, y, "Bakır kupayı ağzına kadar buzla doldur. Votkayı ve lime suyunu ekle, üstüne zencefil birasını dök. Kaşıkla bi kez kaldır, yeter.", font(INTER, 36), (40, 28, 20), TW)
y += 30 * S
d.rounded_rectangle((MX, y, W - MX, y + 150 * S), radius=24 * S, fill=(40, 28, 20))
d.text((MX + 40 * S, y + 28 * S), "BARMEN NOTU", font=font(INTER_SB, 24), fill=COPPER_L)
text_block(img, MX + 40 * S, y + 68 * S, "Ginger ale değil, ginger beer. Farkı yapan o acılık.", font(LORA_I, 34, "Italic"), BONE, TW - 80 * S)
finish(img, "07.jpg")
print("ok")
