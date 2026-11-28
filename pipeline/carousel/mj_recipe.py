import shutil
import kk
from kk import *
from styles import wobble, sk_rect

P = PALETTES["komur"]
img = bg(P, 77); header(img, P, 7, "TARİF")


def recipe(n, w, h):
    d = ImageDraw.Draw(n)
    d.text((70 * S, 70 * S), "MOJITO", font=F(BEBAS, 110), fill=DARK_T)
    d.text((70 * S, 190 * S), "MALZEMELER", font=F(BEBAS, 44), fill=ORG)
    y = 260 * S
    fn_ = F(FIRA, 50)
    for name in ["Beyaz rom", "Taze lime", "Şeker şurubu", "Taze nane", "Soda ve kırık buz"]:
        wobble(d, sk_rect(72 * S, y + 16 * S, 104 * S, y + 48 * S, 4), DARK_T, 3 * S, closed=True, jitter=2, passes=1)
        d.text((140 * S, y), name, font=fn_, fill=DARK_T)
        d.line((70 * S, y + 74 * S, w - 70 * S, y + 74 * S), fill=(225, 218, 205), width=2 * S)
        y += 84 * S
    y += 24 * S
    d.text((70 * S, y), "BARMEN NOTU", font=F(BEBAS, 40), fill=ORG)
    d.text((70 * S, y + 46 * S), "Naneyi bardağa atmadan avucunda bi kez", font=F(BRUSH, 40), fill=DARK_T)
    d.text((70 * S, y + 92 * S), "çırp. Kokusu açılır, yaprak acılaşmaz.", font=F(BRUSH, 40), fill=DARK_T)
    y += 160 * S
    fsd = F(BEBAS, 58)
    tw = d.textlength("SIRLARIN DEVAMI", font=fsd)
    tx = w - 70 * S - 110 * S - tw
    d.text((tx, y + 30 * S), "SIRLARIN DEVAMI", font=fsd, fill=ORG)
    ay = y + 62 * S; ax0 = w - 70 * S - 95 * S; ax1 = w - 75 * S
    wobble(d, [(ax0, ay), (ax1, ay)], ORG, 5 * S, jitter=2, passes=2)
    wobble(d, [(ax1 - 26 * S, ay - 20 * S), (ax1, ay), (ax1 - 26 * S, ay + 20 * S)], ORG, 5 * S, jitter=2, passes=2)
    kk.wordmark(n, w - 240 * S, 60 * S, 110 * S, DARK_T, ORG)


card(img, P, recipe, W // 2, 730 * S, 900 * S, 1080 * S, -1.5)
save(img, "MJ_07.jpg")
shutil.copy("KK_komur_08.jpg", "MJ_08.jpg")
print("ok")
