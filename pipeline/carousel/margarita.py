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
# 1 cover
img = bg(P, 21)
big_stack(img, P, ["ADIM", "İSPANYOLCADA", "PAPATYA DEMEK."], 110 * S, 175, {1, 2})
tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
kk.INK = P["text"]; INKC = P["text"]
glass(tmp, 720 * S, 850 * S, 1.05)
img.alpha_composite(tmp)
INKC = kk.INK = (34, 24, 20)
wordmark(img, MX, H - 250 * S, 170 * S, *P["logo"])
d = ImageDraw.Draw(img)
d.text((MX, 1000 * S), "MARGARITA", font=F(BEBAS, 56), fill=P["text"])
d.text((MX, 1062 * S), "kaydır →", font=F(FIRA, 30), fill=P["num"])
save(img, f"{pre}_01.jpg")

pages = [
    ("PARÇA 1/3 · TEKİLA", lambda n, w, h: bottle(n, w // 2, h - 60 * S, 1.0, (225, 205, 150, 150)), -3,
     [("İlk parçam tekila.", 0), ("Meksika'da mavi agavdan yapılıyor.", 0), ("Tuzla ve limonla içilen o meşhur shot'ı bilirsin. Ben onun kokteyl hâliyim.", 1)]),
    ("PARÇA 2/3 · PORTAKAL LİKÖRÜ", lambda n, w, h: bottle(n, w // 2, h - 60 * S, 1.0, (235, 140, 50, 160)), 3,
     [("İkinci parçam portakal likörü.", 0), ("Triple sec ya da Cointreau.", 0), ("Tekilanın sertliğini o yumuşatıyor, tatlılığım ondan.", 1)]),
    ("PARÇA 3/3 · LIME", lambda n, w, h: lime_wheel(n, w // 2 - 60 * S, h // 2, 1.0), -2,
     [("Üçüncü parçam lime.", 0), ("Şişe limon suyu değil, taze sıkılmış lime.", 1), ("Ekşiliğim ve ferahlığım ondan.", 0)]),
]
for i, (lab, fn, ang, parts) in enumerate(pages):
    img = bg(P, i + 22); header(img, P, i + 2, lab)
    card(img, P, fn, W // 2, 490 * S, 720 * S, 600 * S, ang)
    body(img, P, parts, 900 * S)
    save(img, f"{pre}_0{i + 2}.jpg")

img = bg(P, 25); header(img, P, 5)
big_stack(img, P, ["PAPATYA", "AİLESİNDENİM."], 190 * S, 120, {1})
card(img, P, lambda n, w, h: glass(n, w // 2 - 20 * S, 110 * S, 0.85), W // 2, 690 * S, 600 * S, 470 * S, 3)
body(img, P, [("Eskiden \"Daisy\" yani papatya diye bi kokteyl ailesi vardı: bi ana içki, narenciye ve biraz tatlılık.", 0), ("Tekilayla yapılanına İspanyolcası dendi: Margarita.", 1)], 980 * S, 48)
save(img, f"{pre}_05.jpg")

img = bg(P, 26); header(img, P, 6)
big_stack(img, P, ["BABAM KİM,", "BİLEN YOK."], 190 * S, 120, {1})
def who(n, w, h):
    glass(n, w // 2 - 90 * S, 120 * S, 0.75, lime=False)
    dd = ImageDraw.Draw(n)
    for j, (x, y, sz) in enumerate([(w - 210 * S, 60 * S, 170), (w - 120 * S, 190 * S, 110), (w - 250 * S, 260 * S, 80)]):
        dd.text((x, y), "?", font=F(BEBAS, sz), fill=(196, 90, 42))
card(img, P, who, W // 2, 690 * S, 600 * S, 470 * S, -3)
body(img, P, [("1936'da Tijuana'da bi barmen \"yanlış şişeyi kaptım\" dedi ve tekilalı bi papatya doğdu.", 0), ("Bi de beni bi aktris için icat ettiğini söyleyen Carlos Herrera var. Rivayet çok.", 1)], 980 * S, 46)
save(img, f"{pre}_06.jpg")

img = bg(P, 27); header(img, P, 7, "TARİF")


def recipe(n, w, h):
    d = ImageDraw.Draw(n)
    d.text((70 * S, 70 * S), "MARGARITA", font=F(BEBAS, 110), fill=DARK_T)
    d.text((70 * S, 190 * S), "MALZEMELER", font=F(BEBAS, 44), fill=ORG)
    y = 260 * S
    fn_ = F(FIRA, 50)
    for name in ["Tekila", "Portakal likörü", "Taze lime suyu", "Bol buz", "Tuz (bardak kenarına)"]:
        wobble(d, sk_rect(72 * S, y + 16 * S, 104 * S, y + 48 * S, 4), DARK_T, 3 * S, closed=True, jitter=2, passes=1)
        d.text((140 * S, y), name, font=fn_, fill=DARK_T)
        d.line((70 * S, y + 74 * S, w - 70 * S, y + 74 * S), fill=(225, 218, 205), width=2 * S)
        y += 84 * S
    y += 6 * S
    d.text((70 * S, y), "BARMEN NOTU", font=F(BEBAS, 40), fill=ORG)
    d.text((70 * S, y + 46 * S), "Tuzu bardak kenarının sadece yarısına sür:", font=F(BRUSH, 40), fill=DARK_T)
    d.text((70 * S, y + 92 * S), "isteyen tuzlu, isteyen tuzsuz yudumlasın.", font=F(BRUSH, 40), fill=DARK_T)
    y += 156 * S
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
