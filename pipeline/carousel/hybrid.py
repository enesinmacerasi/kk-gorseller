from five import *
import shutil

INK = (34, 24, 20)
ORG = (196, 90, 42)
TOTAL = 7


def page(idx, seed):
    img = napkin(W, H).convert("RGBA")
    random.seed(seed)
    d = ImageDraw.Draw(img)
    f = F(BRUSH, 40)
    d.text((110 * S, 95 * S), "konuşan kokteyller", font=f, fill=(150, 130, 110))
    t = f"{idx}/{TOTAL}"
    d.text((W - 110 * S - d.textlength(t, font=f), 95 * S), t, font=f, fill=(150, 130, 110))
    return img


def label(img, text, y=180):
    d = ImageDraw.Draw(img)
    f = F(BRUSH, 52)
    d.text((110 * S, y * S), text, font=f, fill=ORG)
    w = d.textlength(text, font=f)
    wobble(d, [(110 * S + i * w / 10, (y + 66) * S + math.sin(i * 1.3) * 3 * S) for i in range(11)], ORG, 4 * S, passes=1)


def say(img, text, y, size=66):
    d = ImageDraw.Draw(img)
    f = F(BRUSH, size)
    for line in wrap(d, text, f, W - 220 * S):
        d.text((110 * S, y), line, font=f, fill=INK)
        y += int(size * 1.12 * S)
    return y


def stain(img, cx, cy, r):
    st = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(st).ellipse((cx - r, cy - r, cx + r, cy + r), outline=(170, 110, 60, 80), width=14 * S)
    img.alpha_composite(st.filter(ImageFilter.GaussianBlur(4 * S)))


def sk_bottle(img, cx, by, k):
    d = ImageDraw.Draw(img)
    w, h = 170 * S * k, 430 * S * k
    x0, y0 = cx - w / 2, by - h
    col = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cd = ImageDraw.Draw(col)
    for i in range(30):
        yy = y0 + 200 * S * k + i * 7 * S * k
        cd.line((x0 + 14 * S * k, yy, x0 + w - 14 * S * k, yy + random.uniform(-6, 6) * S), fill=(150, 170, 175, 90), width=int(6 * S * k))
    img.alpha_composite(col)
    pts = [(x0, by), (x0, y0 + 170 * S * k), (cx - 28 * S * k, y0 + 70 * S * k), (cx - 28 * S * k, y0), (cx + 28 * S * k, y0), (cx + 28 * S * k, y0 + 70 * S * k), (x0 + w, y0 + 170 * S * k), (x0 + w, by)]
    pp = []
    for a, b in zip(pts, pts[1:] + pts[:1]):
        for i in range(8):
            pp.append((a[0] + (b[0] - a[0]) * i / 8, a[1] + (b[1] - a[1]) * i / 8))
    wobble(d, pp, INK, int(5 * S * k), closed=True, passes=3, jitter=3)
    wobble(d, sk_rect(cx - 34 * S * k, y0 - 40 * S * k, cx + 34 * S * k, y0 + 4 * S * k), INK, int(4 * S * k), closed=True)
    # "question mark" price tag: nobody buys
    wobble(d, sk_rect(x0 + w + 40 * S * k, y0 + 240 * S * k, x0 + w + 200 * S * k, y0 + 330 * S * k), ORG, int(4 * S * k), closed=True)
    wobble(d, [(x0 + w - 4 * S * k, y0 + 200 * S * k), (x0 + w + 40 * S * k, y0 + 270 * S * k)], ORG, int(3 * S * k))
    f = F(BRUSH, 56 * k)
    d.text((x0 + w + 95 * S * k, y0 + 245 * S * k), "?", font=f, fill=ORG)
    # cobweb
    for i in range(5):
        wobble(d, [(x0 - 80 * S * k, y0 + 30 * S * k), (x0 + i * 22 * S * k, y0 + 170 * S * k - i * 18 * S * k)], (120, 110, 100), max(2, int(2 * S * k)), passes=1)


def sk_crates(img, cx, by, k):
    d = ImageDraw.Draw(img)
    cw, ch = 280 * S * k, 160 * S * k
    for ox, oy in [(-cw / 2 - 12 * S * k, 0), (cw / 2 + 12 * S * k, 0), (0, -ch - 14 * S * k)]:
        x0, y0 = cx + ox - cw / 2, by + oy - ch
        for b in range(5):
            bx = x0 + 34 * S * k + b * 50 * S * k
            wobble(d, sk_rect(bx, y0 - 40 * S * k, bx + 24 * S * k, y0), INK, int(3 * S * k), closed=True, jitter=2)
        col = Image.new("RGBA", img.size, (0, 0, 0, 0))
        cd = ImageDraw.Draw(col)
        for i in range(int(ch / (8 * S * k))):
            yy = y0 + 6 * S * k + i * 8 * S * k
            cd.line((x0 + 6 * S * k, yy, x0 + cw - 6 * S * k, yy + random.uniform(-5, 5) * S), fill=(170, 120, 70, 110), width=int(6 * S * k))
        img.alpha_composite(col)
        d = ImageDraw.Draw(img)
        wobble(d, sk_rect(x0, y0, x0 + cw, y0 + ch), INK, int(5 * S * k), closed=True, passes=2)
        for j in (1, 2):
            wobble(d, [(x0, y0 + ch * j / 3), (x0 + cw, y0 + ch * j / 3)], INK, int(3 * S * k), passes=1)
    for _ in range(70):
        x = cx + random.uniform(-460, 460) * S * k; y = by + random.uniform(-520, 0) * S * k
        r = random.choice([2, 3]) * S
        d.ellipse((x - r, y - r, x + r, y + r), fill=(150, 130, 110))


def sk_polaroid(img, cx, cy, k):
    d = ImageDraw.Draw(img)
    pw, ph = 480 * S * k, 570 * S * k
    x0, y0 = cx - pw / 2, cy - ph / 2
    wobble(d, sk_rect(x0, y0, x0 + pw, y0 + ph), INK, int(5 * S * k), closed=True, passes=2)
    wobble(d, sk_rect(x0 + 34 * S * k, y0 + 34 * S * k, x0 + pw - 34 * S * k, y0 + pw - 34 * S * k), INK, int(4 * S * k), closed=True)
    sketch_mug(img, cx - 20 * S * k, y0 + 210 * S * k, 0.6 * k, INK)
    d = ImageDraw.Draw(img)
    # flash lines
    for a in (-0.5, -0.1, 0.3):
        wobble(d, [(x0 + pw + 30 * S * k, y0 + 40 * S * k), (x0 + pw + 30 * S * k + math.cos(a) * 90 * S * k, y0 + 40 * S * k + math.sin(a) * 90 * S * k)], ORG, int(5 * S * k), passes=1)


# 1 cover = P2
shutil.copy("P2_poster_cizim.jpg", "H_01.jpg")

# 2
img = page(2, 2); label(img, "parça 1/3 · votka")
sk_bottle(img, W // 2 - 80 * S, 800 * S, 1.05)
say(img, "İlk parçam votka. 1940'larda Amerika'da kimse votka içmiyordu. John Martin, Smirnoff'u almıştı ama şişeler rafta kalıyordu.", 880 * S)
save(img, "H_02.jpg")

# 3
img = page(3, 3); label(img, "parça 2/3 · zencefil birası")
sk_crates(img, W // 2, 780 * S, 0.95)
say(img, "İkinci parçam zencefil birası. Cock 'n' Bull barının sahibi Jack Morgan kendi birasını yaptırdı. Kasalar bodrumda toz tutuyordu.", 880 * S)
save(img, "H_03.jpg")

# 4
img = page(4, 4); label(img, "parça 3/3 · bakır kupa")
sketch_mug(img, W // 2 - 60 * S, 480 * S, 1.0, INK, seed=8)
stain(img, W - 250 * S, 560 * S, 130 * S)
say(img, "Kupamın nereden geldiği hâlâ tartışmalı. Üç ayrı rivayet var. Birinde satamadığı bakır kupalarla bi kadın bara giriyor.", 880 * S)
save(img, "H_04.jpg")

# 5
img = page(5, 5)
d = ImageDraw.Draw(img)
f = F(BRUSH, 60)
x = 110 * S
for part, c in [("votka", INK), (" + ", ORG), ("zencefil birası", INK), (" + ", ORG), ("kupa", INK)]:
    d.text((x, 185 * S), part, font=f, fill=c); x += d.textlength(part, font=f)
wobble(d, sk_ellipse(W // 2 - 20 * S, 222 * S, 490 * S, 80 * S), ORG, 4 * S)
sketch_mug(img, W // 2 - 60 * S, 470 * S, 1.0, INK, seed=11)
say(img, "Üç batık ürünü bi bardağa koydular, üstüne biraz lime sıktılar. Adımı da Moscow Mule koydular.", 900 * S)
save(img, "H_05.jpg")

# 6
img = page(6, 6)
sk_polaroid(img, W // 2 - 20 * S, 500 * S, 1.0)
say(img, "Beni ünlü yapan tadım değil, bi fotoğraf makinesiydi. Martin elinde Polaroid'le bar bar gezdi. Barmeni benimle çekti, bi kopyasını ona bıraktı, diğerini sonraki bara gösterdi.", 860 * S, 58)
save(img, "H_06.jpg")

# 7 recipe on napkin
img = page(7, 7)
d = ImageDraw.Draw(img)
d.text((110 * S, 170 * S), "Moscow Mule", font=F(BRUSH, 120), fill=INK)
wobble(d, [(110 * S + i * 60 * S, 305 * S + math.sin(i) * 5 * S) for i in range(11)], ORG, 7 * S, passes=2)
y = 370 * S
fa, fn = F(BRUSH, 70), F(BRUSH, 64)
for amt, name in [("4,5 cl", "votka"), ("1 cl", "taze lime suyu"), ("12 cl", "zencefil birası"), ("bol", "buz"), ("1", "lime dilimi")]:
    wobble(d, sk_rect(115 * S, y + 22 * S, 145 * S, y + 52 * S, 4), INK, 3 * S, closed=True, jitter=2, passes=1)
    d.text((180 * S, y), amt, font=fa, fill=ORG)
    d.text((440 * S, y + 4 * S), name, font=fn, fill=INK)
    y += 86 * S
y += 20 * S
y = say(img, "Kupayı ağzına kadar buzla doldur. Votkayı ve lime suyunu ekle, üstüne zencefil birasını dök. Kaşıkla bi kez kaldır, yeter.", y, 52)
y += 75 * S
d = ImageDraw.Draw(img)
note = "Barmen notu: Ginger ale değil, ginger beer. Farkı yapan o acılık."
fnn = F(BRUSH, 54)
lines = wrap(d, note, fnn, W - 330 * S)
for i, line in enumerate(lines):
    d.text((160 * S, y + i * 62 * S), line, font=fnn, fill=ORG)
hh = len(lines) * 62 * S
wobble(d, sk_ellipse(W // 2, y + hh / 2, W / 2 - 80 * S, hh / 2 + 50 * S, 80, 0.2, 2 * math.pi + 0.5), ORG, 4 * S)
stain(img, W - 230 * S, 520 * S, 150 * S)
save(img, "H_07.jpg")
print("ok")
