import shutil, random, math
import kk
from kk import *
from styles import wobble, sk_rect, sk_ellipse

P = PALETTES["komur"]
INKC = kk.INK
pre = "NG"


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


random.seed(7)
# 1 cover
img = bg(P, 11)
big_stack(img, P, ["BEN,", "BOZULMUŞ BİR", "AMERICANO'YUM."], 110 * S, 175, {1, 2})
tmp = Image.new("RGBA", img.size, (0, 0, 0, 0))
kk.INK = P["text"]; INKC = P["text"]
rocks(tmp, 700 * S, 820 * S, 0.95)
img.alpha_composite(tmp)
INKC = kk.INK = (34, 24, 20)
wordmark(img, MX, H - 250 * S, 170 * S, *P["logo"])
d = ImageDraw.Draw(img)
d.text((MX, 1000 * S), "NEGRONI", font=F(BEBAS, 56), fill=P["text"])
d.text((MX, 1062 * S), "kaydır →", font=F(FIRA, 30), fill=P["num"])
save(img, f"{pre}_01.jpg")

pages = [
    ("PARÇA 1/3 · CAMPARI", lambda n, w, h: bottle(n, w // 2, h - 60 * S, 1.0, (190, 40, 40, 170)), -3,
     [("İlk parçam Campari.", 0), ("1860'ta Gaspare Campari adında bir likörcünün bitter tarifinden doğdu.", 0), ("O acı ama yakmayan kırmızı tat benim imzam.", 1)]),
    ("PARÇA 2/3 · TATLI VERMUT", lambda n, w, h: bottle(n, w // 2, h - 60 * S, 1.0, (120, 50, 30, 160)), 3,
     [("İkinci parçam tatlı vermut.", 0), ("1786'da Torino'da Antonio Benedetto Carpano şarabı otlar ve baharatlarla tatlandırdı.", 0), ("Campari'nin acısını o yumuşatıyor.", 1)]),
    ("PARÇA 3/3 · CİN", lambda n, w, h: bottle(n, w // 2, h - 60 * S, 1.0, (200, 215, 215, 120)), -2,
     [("Üçüncü parçam cin.", 0), ("Ama aslında burada olmamalıydı.", 1), ("Benden önce bu bardakta soda vardı ve adım Americano'ydu.", 0)]),
]
for i, (lab, fn, ang, parts) in enumerate(pages):
    img = bg(P, i + 12); header(img, P, i + 2, lab)
    card(img, P, fn, W // 2, 490 * S, 720 * S, 600 * S, ang)
    body(img, P, parts, 900 * S)
    save(img, f"{pre}_0{i + 2}.jpg")

img = bg(P, 15); header(img, P, 5)
big_stack(img, P, ["SODA GİTTİ,", "CİN GELDİ."], 190 * S, 120, {1})
card(img, P, lambda n, w, h: rocks(n, w // 2, 140 * S, 0.9, orange=False), W // 2, 690 * S, 600 * S, 470 * S, 3)
body(img, P, [("Rivayete göre 1919 civarı, Floransa.", 0), ("Kont Camillo Negroni her zamanki Americano'sunu istedi, ama bir şartla:", 0), ("soda yerine cin.", 1)], 980 * S, 50)
save(img, f"{pre}_05.jpg")

img = bg(P, 16); header(img, P, 6)
big_stack(img, P, ["ADIMI DA", "KONT VERDİ."], 190 * S, 120, {1})
card(img, P, lambda n, w, h: rocks(n, w // 2 - 20 * S, 150 * S, 0.9), W // 2, 690 * S, 600 * S, 470 * S, -3)
body(img, P, [("Barmen fark belli olsun diye limon yerine portakal koydu.", 0), ("Herkes kontun içkisine Negroni demeye başladı.", 1), ("Bir asır sonra hâlâ eşit ölçüde üç parçayım.", 0)], 980 * S, 48)
save(img, f"{pre}_06.jpg")

img = bg(P, 17); header(img, P, 7, "TARİF")


def recipe(n, w, h):
    d = ImageDraw.Draw(n)
    d.text((70 * S, 70 * S), "NEGRONI", font=F(BEBAS, 110), fill=DARK_T)
    d.text((70 * S, 190 * S), "MALZEMELER", font=F(BEBAS, 44), fill=ORG)
    y = 260 * S
    fn_ = F(FIRA, 50)
    for name in ["Cin", "Campari", "Tatlı vermut", "Portakal kabuğu", "Bol buz"]:
        wobble(d, sk_rect(72 * S, y + 16 * S, 104 * S, y + 48 * S, 4), DARK_T, 3 * S, closed=True, jitter=2, passes=1)
        d.text((140 * S, y), name, font=fn_, fill=DARK_T)
        d.line((70 * S, y + 74 * S, w - 70 * S, y + 74 * S), fill=(225, 218, 205), width=2 * S)
        y += 84 * S
    y += 6 * S
    d.text((70 * S, y), "BARMEN NOTU", font=F(BEBAS, 40), fill=ORG)
    d.text((70 * S, y + 46 * S), "Karıştır, asla çalkalama. Sonra portakal", font=F(BRUSH, 40), fill=DARK_T)
    d.text((70 * S, y + 92 * S), "kabuğunu bardağın üstünde sık, yağı insin.", font=F(BRUSH, 40), fill=DARK_T)
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
shutil.copy("KK_komur_08.jpg", f"{pre}_08.jpg")
print("ok")
