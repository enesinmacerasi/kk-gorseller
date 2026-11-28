from bold import *
P = PALETTES["bordo"]
CREAMD = (240, 226, 200); CORAL = (242, 160, 130)
pages = [
    (2, "PARÇA 1/3 · VİSKİ", ["İLK PARÇAM:", "VİSKİ."], art_bottle((196, 112, 40), glass=(230, 214, 190), label="WHISKEY"), (540, 715), -8, (690, 715), CREAMD,
     [("Bourbon da olur, rye da.", 0), ("Sade bi kokteylim, viskinin tadını saklayacak yerim yok.", 1)]),
    (3, "PARÇA 2/3 · ŞEKER", ["İKİNCİ PARÇAM:", "ŞEKER."], art_sugar(), (560, 715), 0, (680, 715), CORAL,
     [("Klasik usulde bi küp şeker bardağın dibinde eritilir.", 0), ("Viskinin sert köşelerini o yuvarlıyor.", 1)]),
    (4, "PARÇA 3/3 · ANGOSTURA", ["ÜÇÜNCÜ PARÇAM:", "ANGOSTURA."], art_bottle((120, 40, 25), glass=(150, 70, 50), label="BITTER", h=560, cap=(230, 180, 40), round_=False), (540, 715), 6, (690, 715), CREAMD,
     [("1824'te Venezuela'da Dr. Siegert onu mide ilacı olarak yaptı.", 0), ("Bugün birkaç damlası beni toparlıyor.", 1)]),
    (5, None, ["ADIMDAN ÖNCE", "TARİFİM VARDI."], art_newspaper("1806", "COCK-TAIL"), (520, 715), -5, (720, 715), CORAL,
     [("1806'da New York'ta bi gazete \"kokteyl\"i tanımladı: içki, şeker, su ve bitter.", 0), ("Yani tam olarak beni.", 1)]),
    (6, None, ["ESKİ USUL,", "LÜTFEN."], art_rocks((196, 112, 40), k=1.05, peel=True), (520, 715), -3, (700, 715), CREAMD,
     [("1800'lerin ikinci yarısında barmenler bana likör, absent falan eklemeye başladı.", 0), ("Sade hâlimi özleyenler \"eski usul\" istedi: Old Fashioned.", 1)]),
]
for i, (idx, lab, big, art, axy, rot, dxy, dc, parts) in enumerate(pages):
    img = bold_page(P, idx, lab, big, art, axy, rot, dxy, parts, 70 + i, dc)
    save(img, f"OFB_0{idx}.jpg")
print("ok")
