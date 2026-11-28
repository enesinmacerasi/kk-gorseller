"""Konuşan Kokteyller carousel renderer — final style (poster + taped napkin sketches)."""
import sys
import hybrid
from five import *

NAVY = (12, 32, 56)
RED = (171, 39, 34)
LOGO_CREAM = (230, 219, 206)
FIRA = "/usr/share/fonts/truetype/google-fonts/ofl/firasans/FiraSans-SemiBold.ttf"
LN = Image.open("/home/claude/carousel/logo_navy.png")
LR = Image.open("/home/claude/carousel/logo_red.png")


def wordmark(img, x, y, h, top_col, bot_col):
    """transparent logo, recolored: 'konuşan' = top_col, 'kokteyller' = bot_col"""
    w = int(LN.width * h / LN.height)
    n, r = LN.resize((w, h), Image.LANCZOS), LR.resize((w, h), Image.LANCZOS)
    img.paste(top_col, (int(x), int(y)), n)
    img.paste(bot_col, (int(x), int(y)), r)
    return w

PALETTES = {
    # 2 · Bordo: şarap kırmızısı zemin, krem yazı, mercan vurgular
    "bordo": dict(bg=(110, 28, 38), text=(246, 234, 214), emph="color", emph_text=(242, 160, 130),
                  num=(242, 160, 130), shadow=(50, 10, 14), logo=((246, 234, 214), (242, 160, 130))),
    # 3 · Kömür: siyaha yakın zemin, krem yazı, lime yeşili vurgular
    "komur": dict(bg=(28, 26, 24), text=(246, 234, 214), emph="color", emph_text=(150, 196, 70),
                  num=(150, 196, 70), shadow=(0, 0, 0), logo=((246, 234, 214), (150, 196, 70))),
}
TOTAL = 8
MX = 75 * S
INK = (34, 24, 20)
ORG = (196, 90, 42)
DARK_T = (30, 22, 18)


def gr(c, dv):
    return tuple(max(0, min(255, x + dv)) for x in c)


def logo(img, cx, cy, r):
    l = LOGO.resize((2 * r, 2 * r), Image.LANCZOS)
    sh = Image.new("L", img.size, 0)
    ImageDraw.Draw(sh).ellipse((cx - r + 6 * S, cy - r + 10 * S, cx + r + 6 * S, cy + r + 10 * S), fill=150)
    img.paste((0, 0, 0), mask=sh.filter(ImageFilter.GaussianBlur(10 * S)))
    img.paste(l, (cx - r, cy - r), l)


def bg(P, seed):
    img = Image.new("RGB", (W, H), P["bg"])
    grain(img, [gr(P["bg"], -7), gr(P["bg"], 7)], seed=seed)
    return img.convert("RGBA")


def header(img, P, idx, label=None):
    d = ImageDraw.Draw(img)
    lw = wordmark(img, MX, 58 * S, 88 * S, *P["logo"])
    f = F(BEBAS, 44)
    if label:
        d.text((MX + lw + 30 * S, 82 * S), label, font=f, fill=P["text"])
    t = f"{idx}/{TOTAL}"
    d.text((W - MX - d.textlength(t, font=f), 73 * S), t, font=f, fill=P["num"])


def words_line(d, P, x, y, s, f, emph):
    if emph and P["emph"] == "bar":
        w = d.textlength(s, font=f)
        asc = f.size
        d.rectangle((x - 10 * S, y + asc * 0.12, x + w + 10 * S, y + asc * 1.02), fill=P["bar"])
        d.text((x, y), s, font=f, fill=P["emph_text"])
    else:
        d.text((x, y), s, font=f, fill=P["emph_text"] if emph else P["text"])


def big_stack(img, P, lines, y, size, emph_idx, lh=0.98):
    d = ImageDraw.Draw(img)
    for i, wd in enumerate(lines):
        s = size; f = F(BEBAS, s)
        while d.textlength(wd, font=f) > W - 170 * S:
            s -= 4; f = F(BEBAS, s)
        words_line(d, P, MX, y, wd, f, i in emph_idx)
        y += int(f.size * lh)
    return y


def body(img, P, parts, y, size=56, lh=1.36):
    d = ImageDraw.Draw(img)
    f = F(FIRA, size)
    x, maxx = MX, W - MX
    sp = d.textlength(" ", font=f)
    for s, emph in parts:
        for w in s.split():
            ww = d.textlength(w, font=f)
            if x + ww > maxx:
                x = MX; y += int(size * lh * S)
            if emph and P["emph"] == "bar":
                d.rectangle((x - 6 * S, y + 4 * S, x + ww + 6 * S, y + size * 1.22 * S), fill=P["bar"])
            d.text((x, y), w, font=f, fill=P["emph_text"] if emph else P["text"])
            x += ww + sp
    return y + int(size * lh * S)


def card(img, P, draw_fn, cx, cy, w, h, ang):
    nap = napkin(w, h, fold=False)
    draw_fn(nap, w, h)
    nap = nap.rotate(ang, expand=True, resample=Image.BICUBIC)
    px, py = int(cx - nap.width / 2), int(cy - nap.height / 2)
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rectangle((px + 24 * S, py + 30 * S, px + nap.width, py + nap.height + 6 * S), fill=180)
    img.paste(P["shadow"] + (255,), mask=sh.filter(ImageFilter.GaussianBlur(22 * S)))
    img.alpha_composite(nap, (px, py))
    tape(img, cx, py + 22 * S, 220 * S, 58 * S, -ang + 3)


def render(pal, prefix):
    PP = lambda i: PALETTES[pal]
    P = PP(1)
    hybrid.INK = INK
    hybrid.ORG = ORG

    # 1 cover
    img = bg(P, 1)
    y = big_stack(img, P, ["BENİ LEZZET", "İÇİN DEĞİL,", "STOK ERİTMEK", "İÇİN İCAT", "ETTİLER."], 90 * S, 165, {2, 3})
    sketch_mug(img, 730 * S, 1040 * S, 0.75, P["text"], fill=None, lime=(150, 196, 70, 230), lw=6)
    lw = wordmark(img, MX, H - 250 * S, 170 * S, *P["logo"])
    d = ImageDraw.Draw(img)
    d.text((MX, 1000 * S - 0), "MOSCOW MULE", font=F(BEBAS, 56), fill=P["text"])
    d.text((MX, 1062 * S), "kaydır →", font=F(FIRA, 30), fill=P["num"])
    save(img, f"{prefix}_01.jpg")

    # 2-4 parts
    pages = [
        ("PARÇA 1/3 · VOTKA", lambda n, w, h: hybrid.sk_bottle(n, w // 2 - 70 * S, h - 70 * S, 0.95), -3,
         [("İlk parçam votka.", 0), ("1940'larda Amerika'da kimse votka içmiyordu.", 1), ("John Martin, Smirnoff'u almıştı ama şişeler rafta kalıyordu.", 0)]),
        ("PARÇA 2/3 · ZENCEFİL BİRASI", lambda n, w, h: hybrid.sk_crates(n, w // 2, h - 60 * S, 0.78), 3,
         [("İkinci parçam zencefil birası. Cock 'n' Bull barının sahibi Jack Morgan kendi birasını yaptırdı.", 0), ("Kasalar bodrumda toz tutuyordu.", 1)]),
        ("PARÇA 3/3 · BAKIR KUPA", lambda n, w, h: sketch_mug(n, w // 2 - 50 * S, 190 * S, 0.95, INK, seed=8), -2,
         [("Kupamın nereden geldiği", 0), ("hâlâ tartışmalı.", 1), ("Üç ayrı rivayet var. Birinde satamadığı bakır kupalarla bi kadın bara giriyor.", 0)]),
    ]
    for i, (lab, fn, ang, parts) in enumerate(pages):
        P = PP(i + 2)
        img = bg(P, i + 2); header(img, P, i + 2, lab)
        card(img, P, fn, W // 2, 490 * S, 720 * S, 600 * S, ang)
        body(img, P, parts, 900 * S)
        save(img, f"{prefix}_0{i + 2}.jpg")

    # 5
    P = PP(5)
    img = bg(P, 5); header(img, P, 5)
    big_stack(img, P, ["VOTKA + ZENCEFİL", "BİRASI + KUPA"], 190 * S, 120, {1})
    card(img, P, lambda n, w, h: sketch_mug(n, w // 2 - 50 * S, 170 * S, 0.85, INK, seed=11), W // 2, 710 * S, 600 * S, 470 * S, 3)
    body(img, P, [("Üç batık ürünü bi bardağa koydular, üstüne biraz lime sıktılar.", 0), ("Adımı da Moscow Mule koydular.", 1)], 1000 * S)
    save(img, f"{prefix}_05.jpg")

    # 6
    P = PP(6)
    img = bg(P, 6); header(img, P, 6)
    big_stack(img, P, ["BENİ ÜNLÜ YAPAN", "BİR FOTOĞRAFTI."], 190 * S, 120, {1})
    card(img, P, lambda n, w, h: hybrid.sk_polaroid(n, w // 2 - 20 * S, h // 2, 0.75), W // 2, 720 * S, 600 * S, 500 * S, -3)
    body(img, P, [("Martin elinde Polaroid'le bar bar gezdi. Barmeni benimle çekti, bi kopyasını ona bıraktı,", 0), ("diğerini sonraki bara gösterdi.", 1)], 1010 * S, 50)
    save(img, f"{prefix}_06.jpg")

    # 7 recipe
    P = PP(7)
    img = bg(P, 7); header(img, P, 7, "TARİF")

    def recipe(n, w, h):
        d = ImageDraw.Draw(n)
        d.text((70 * S, 70 * S), "MOSCOW MULE", font=F(BEBAS, 110), fill=DARK_T)
        d.text((70 * S, 190 * S), "MALZEMELER", font=F(BEBAS, 44), fill=ORG)
        y = 260 * S
        fn = F(FIRA, 50)
        for name in ["Votka", "Taze lime suyu", "Zencefil birası", "Bol buz", "Lime dilimi"]:
            wobble(d, sk_rect(72 * S, y + 16 * S, 104 * S, y + 48 * S, 4), DARK_T, 3 * S, closed=True, jitter=2, passes=1)
            d.text((140 * S, y), name, font=fn, fill=DARK_T)
            d.line((70 * S, y + 74 * S, w - 70 * S, y + 74 * S), fill=(225, 218, 205), width=2 * S)
            y += 84 * S
        y += 6 * S
        d.text((70 * S, y), "BARMEN NOTU", font=F(BEBAS, 40), fill=ORG)
        d.text((70 * S, y + 46 * S), "Ginger ale değil, ginger beer kullan. Ale tatlı", font=F(BRUSH, 40), fill=DARK_T)
        d.text((70 * S, y + 92 * S), "ve yumuşak kalır; acı zencefil vuruşu beer'de.", font=F(BRUSH, 40), fill=DARK_T)
        y += 156 * S
        fsd = F(BEBAS, 58)
        tw = d.textlength("SIRLARIN DEVAMI", font=fsd)
        tx = w - 70 * S - 110 * S - tw
        d.text((tx, y + 40 * S), "SIRLARIN DEVAMI", font=fsd, fill=ORG)
        ay = y + 72 * S; ax0 = w - 70 * S - 95 * S; ax1 = w - 75 * S
        wobble(d, [(ax0, ay), (ax1, ay)], ORG, 5 * S, jitter=2, passes=2)
        wobble(d, [(ax1 - 26 * S, ay - 20 * S), (ax1, ay), (ax1 - 26 * S, ay + 20 * S)], ORG, 5 * S, jitter=2, passes=2)
        wordmark(n, w - 240 * S, 60 * S, 110 * S, DARK_T, ORG)

    card(img, P, recipe, W // 2, 730 * S, 900 * S, 1080 * S, -1.5)
    save(img, f"{prefix}_07.jpg")

    # 8 books / coming soon
    P = PP(8)
    img = bg(P, 8); header(img, P, 8)
    big_stack(img, P, ["E-KİTAPLARIN LİNKİ", "PROFİL AÇIKLAMASINDA"], 150 * S, 104, {1})

    def mkbook(path, w_, spine):
        cv = Image.open(path).convert("RGBA")
        h_ = int(cv.height * w_ / cv.width)
        book = Image.new("RGBA", (w_ + 22 * S, h_), (0, 0, 0, 0))
        ImageDraw.Draw(book).rectangle((0, 0, 22 * S, h_), fill=spine)
        book.alpha_composite(cv.resize((w_, h_), Image.LANCZOS), (22 * S, 0))
        return book

    b1 = mkbook("/home/claude/book/assets/cover_klasik.png", 370 * S, (70, 14, 22)).rotate(-5, expand=True, resample=Image.BICUBIC)
    b2 = mkbook("/home/claude/book/assets/cover_evde.png", 370 * S, (8, 8, 10)).rotate(4, expand=True, resample=Image.BICUBIC)
    for bk, bx, by in ((b2, 500 * S, 490 * S), (b1, 80 * S, 460 * S)):
        sh = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sh).rectangle((bx + 26 * S, by + 36 * S, bx + bk.width, by + bk.height + 8 * S), fill=190)
        img.paste(P["shadow"] + (255,), mask=sh.filter(ImageFilter.GaussianBlur(24 * S)))
        img.alpha_composite(bk, (bx, by))

    # launch discount sticker
    R = 128 * S
    st = Image.new("RGBA", (2 * R + 20 * S, 2 * R + 20 * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(st)
    c = st.width / 2
    sd.ellipse((c - R, c - R, c + R, c + R), fill=P["emph_text"])
    sd.ellipse((c - R + 12 * S, c - R + 12 * S, c + R - 12 * S, c + R - 12 * S), outline=(34, 24, 20), width=4 * S)
    for txt, fs, yy in (("LANSMANA ÖZEL", 30, -72), ("%20", 104, -42), ("İNDİRİM", 38, 56)):
        f_ = F(BEBAS, fs)
        tw = sd.textlength(txt, font=f_)
        sd.text((c - tw / 2, c + yy * S), txt, font=f_, fill=(34, 24, 20))
    st = st.rotate(12, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(st, (int(W - st.width - 10 * S), int(850 * S)))
    body(img, P, [("Ölçüler, yapılış, bar sırları ve evde kokteyl rehberi:", 0), ("shopier.com/konusankokteyller", 1)], 1150 * S, 48)
    save(img, f"{prefix}_08.jpg")


if __name__ == "__main__":
    for pal in sys.argv[1:] or ["komur", "bordo"]:
        render(pal, f"KK_{pal}")
    print("ok")
