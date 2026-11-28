import shutil, random, math
import kk
import hybrid
from kk import *
from styles import wobble, sk_rect, sk_ellipse

P = PALETTES["bordo"]
INKC = kk.INK
pre = "DQ"


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




def coupe(n, cx, top, k, fill=True, garnish=True):
    d = ImageDraw.Draw(n)
    s = S * k
    rim = 190 * s
    if fill:
        col = Image.new("RGBA", n.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(col)
        yy = top + 18 * s
        while yy < top + 120 * s:
            t = (yy - top) / (130 * s)
            hw = rim * math.sqrt(max(0, 1 - t * t)) - 12 * s
            cd.line((cx - hw, yy, cx + hw, yy + random.uniform(-4, 4) * S), fill=(225, 230, 170, 160), width=int(5 * s))
            yy += 6 * s
        n.alpha_composite(col)
    bowl = []
    for i in range(31):
        a = math.pi * i / 30
        bowl.append((cx - rim * math.cos(a), top + 130 * s * math.sin(a)))
    wobble(d, bowl, INKC, int(5 * s), passes=3, jitter=3)
    wobble(d, sk_ellipse(cx, top, rim, 16 * s, 40), INKC, int(4 * s), passes=2, jitter=2)
    wobble(d, [(cx - 7 * s, top + 128 * s), (cx - 7 * s, top + 320 * s)], INKC, int(5 * s), passes=2, jitter=2)
    wobble(d, [(cx + 7 * s, top + 128 * s), (cx + 7 * s, top + 320 * s)], INKC, int(5 * s), passes=2, jitter=2)
    wobble(d, sk_ellipse(cx, top + 330 * s, 110 * s, 16 * s, 40), INKC, int(5 * s), passes=2, jitter=2)
    if garnish:
        ox, oy, rr = cx + rim - 10 * s, top - 6 * s, 56 * s
        oc = Image.new("RGBA", n.size, (0, 0, 0, 0)); od = ImageDraw.Draw(oc)
        od.ellipse((ox - rr, oy - rr, ox + rr, oy + rr), fill=(150, 196, 70, 170))
        for i in range(10):
            a = i * 2 * math.pi / 10
            od.line((ox, oy, ox + math.cos(a) * rr * .85, oy + math.sin(a) * rr * .85), fill=(240, 240, 200, 220), width=int(5 * s))
        n.alpha_composite(oc)
        wobble(d, sk_ellipse(ox, oy, rr, rr, 40), INKC, int(4 * s), passes=2, jitter=2)


def syrup(n, cx, by, k):
    """sugar bowl + spoon"""
    d = ImageDraw.Draw(n)
    s = S * k
    col = Image.new("RGBA", n.size, (0, 0, 0, 0)); cd = ImageDraw.Draw(col)
    r = random.Random(9)
    for i in range(160):
        x = r.uniform(cx - 170 * s, cx + 170 * s); y = r.uniform(by - 230 * s, by - 190 * s)
        cd.rectangle((x - 4 * S, y - 4 * S, x + 4 * S, y + 4 * S), fill=(200, 190, 175, 230))
    n.alpha_composite(col)
    bowl = []
    for i in range(31):
        a = math.pi * i / 30
        bowl.append((cx - 200 * s * math.cos(a), by - 200 * s + 170 * s * math.sin(a)))
    wobble(d, bowl, INKC, int(6 * s), passes=3, jitter=3)
    wobble(d, sk_ellipse(cx, by - 200 * s, 200 * s, 22 * s, 40), INKC, int(4 * s), passes=2, jitter=2)
    wobble(d, [(cx + 60 * s, by - 210 * s), (cx + 210 * s, by - 380 * s)], INKC, int(6 * s), passes=2, jitter=2)
    wobble(d, sk_ellipse(cx + 40 * s, by - 195 * s, 36 * s, 20 * s, 30), INKC, int(4 * s), passes=2, jitter=2)


random.seed(17)
pages = [
    ("PARÇA 1/3 · BEYAZ ROM", lambda n, w, h: bottle(n, w // 2, h - 60 * S, 1.0, (225, 225, 215, 140)), -3,
     [("İlk parçam beyaz rom.", 0), ("Şeker kamışından geliyor.", 0), ("Hafif ve temiz bi rom, o yüzden en sade hâlimle bile parlıyorum.", 1)]),
    ("PARÇA 2/3 · LIME", lambda n, w, h: lime_wheel(n, w // 2 - 60 * S, h // 2, 1.0), 3,
     [("İkinci parçam lime.", 0), ("Romla yarışmıyor, onu uyandırıyor.", 0), ("Taze sık, şişedeki hazır sular bana yaramaz.", 1)]),
    ("PARÇA 3/3 · ŞEKER", lambda n, w, h: syrup(n, w // 2 - 40 * S, h - 70 * S, 1.0), -2,
     [("Üçüncü parçam şeker.", 0), ("Rom ile lime'ı barıştıran o.", 0), ("Şurubu evde yapmak kolay: eşit şeker ve su, karıştır, erit.", 1)]),
]
for i, (lab, fn, ang, parts) in enumerate(pages):
    img = bg(P, i + 52); header(img, P, i + 2, lab)
    card(img, P, fn, W // 2, 490 * S, 720 * S, 600 * S, ang)
    body(img, P, parts, 900 * S)
    save(img, f"{pre}_0{i + 2}.jpg")


def mine(n, w, h):
    d = ImageDraw.Draw(n)
    # pickaxe (left), coupe (right)
    wobble(d, [(90 * S, 390 * S), (230 * S, 160 * S)], INKC, 8 * S, passes=3, jitter=2)
    wobble(d, [(120 * S, 120 * S), (190 * S, 135 * S), (250 * S, 165 * S), (300 * S, 225 * S)], INKC, 9 * S, passes=3, jitter=2)
    r = random.Random(2)
    for i in range(14):
        x = r.uniform(70, 300) * S; y = r.uniform(400, 430) * S
        d.ellipse((x - 9 * S, y - 7 * S, x + 9 * S, y + 7 * S), fill=(120, 110, 100))
    coupe(n, w - 160 * S, 120 * S, 0.62, garnish=False)


img = bg(P, 55); header(img, P, 5)
big_stack(img, P, ["BİR MADEN,", "BİR MÜHENDİS."], 190 * S, 120, {1})
card(img, P, mine, W // 2, 690 * S, 600 * S, 470 * S, 3)
body(img, P, [("Rivayete göre 1898, Küba. Daiquirí'deki demir madeninde çalışan Amerikalı mühendis Jennings Cox beni ilk karıştıran oldu.", 0), ("Kasabanın adı bana kaldı.", 1)], 980 * S, 46)
save(img, f"{pre}_05.jpg")

img = bg(P, 56); header(img, P, 6)
big_stack(img, P, ["SONRA HAVANA'YA", "TAŞINDIM."], 190 * S, 120, {1})
card(img, P, lambda n, w, h: coupe(n, w // 2 - 20 * S, 110 * S, 0.85), W // 2, 690 * S, 600 * S, 470 * S, -3)
body(img, P, [("El Floridita'nın barmeni Constantino Ribalaigua beni buzla çırpıp donmuş bi hâle soktu.", 0), ("Barın müdavimlerinden biri: Hemingway.", 1)], 980 * S, 48)
save(img, f"{pre}_06.jpg")

img = bg(P, 57); header(img, P, 7, "TARİF")


def recipe(n, w, h):
    d = ImageDraw.Draw(n)
    d.text((70 * S, 70 * S), "DAIQUIRI", font=F(BEBAS, 110), fill=DARK_T)
    d.text((70 * S, 190 * S), "MALZEMELER", font=F(BEBAS, 44), fill=ORG)
    y = 260 * S
    fn_ = F(FIRA, 50)
    for name in ["Beyaz rom", "Taze lime suyu", "Şeker şurubu", "Buz (çalkalamak için)"]:
        wobble(d, sk_rect(72 * S, y + 16 * S, 104 * S, y + 48 * S, 4), DARK_T, 3 * S, closed=True, jitter=2, passes=1)
        d.text((140 * S, y), name, font=fn_, fill=DARK_T)
        d.line((70 * S, y + 74 * S, w - 70 * S, y + 74 * S), fill=(225, 218, 205), width=2 * S)
        y += 84 * S
    y += 30 * S
    d.text((70 * S, y), "BARMEN NOTU", font=F(BEBAS, 40), fill=ORG)
    d.text((70 * S, y + 46 * S), "Kadehi önceden buzlukta soğut. Buzsuz", font=F(BRUSH, 40), fill=DARK_T)
    d.text((70 * S, y + 92 * S), "servis edilirim, soğuk bardak beni soğuk tutar.", font=F(BRUSH, 40), fill=DARK_T)
    y += 180 * S
    fsd = F(BEBAS, 58)
    tw = d.textlength("SIRLARIN DEVAMI", font=fsd)
    tx = w - 70 * S - 110 * S - tw
    d.text((tx, y + 40 * S), "SIRLARIN DEVAMI", font=fsd, fill=ORG)
    ay = y + 72 * S; ax0 = w - 70 * S - 95 * S; ax1 = w - 75 * S
    wobble(d, [(ax0, ay), (ax1, ay)], ORG, 5 * S, jitter=2, passes=2)
    wobble(d, [(ax1 - 26 * S, ay - 20 * S), (ax1, ay), (ax1 - 26 * S, ay + 20 * S)], ORG, 5 * S, jitter=2, passes=2)
    kk.wordmark(n, w - 240 * S, 60 * S, 110 * S, DARK_T, ORG)


card(img, P, recipe, W // 2, 730 * S, 900 * S, 1080 * S, -1.5)
save(img, f"{pre}_07.jpg")
shutil.copy("KK_bordo_08.jpg", f"{pre}_08.jpg")
print("ok")
