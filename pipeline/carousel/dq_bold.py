from bold import *
P = PALETTES["komur"]
LIMEC = (150, 196, 70); CREAMD = (236, 226, 200); CORAL = (242, 140, 110)
pages = [
    (2, "PARÇA 1/3 · BEYAZ ROM", ["İLK PARÇAM:", "BEYAZ ROM."], art_bottle((236, 238, 228), glass=(205, 216, 210), label="RON BLANCO"), (540, 715), -8, (690, 715), LIMEC,
     [("Şeker kamışından geliyor.", 0), ("Hafif ve temiz bi rom, o yüzden en sade hâlimle bile parlıyorum.", 1)]),
    (3, "PARÇA 2/3 · LIME", ["İKİNCİ PARÇAM:", "LIME."], art_wheel((70, 110, 35), (150, 196, 70), (205, 228, 140)), (580, 715), 12, (600, 715), CREAMD,
     [("Romla yarışmıyor, onu uyandırıyor.", 0), ("Taze sık, şişedeki hazır sular bana yaramaz.", 1)]),
    (4, "PARÇA 3/3 · ŞEKER", ["ÜÇÜNCÜ PARÇAM:", "ŞEKER."], art_sugar(), (560, 715), 0, (680, 715), LIMEC,
     [("Rom ile lime'ı barıştıran o.", 0), ("Şurubu evde yapmak kolay: eşit şeker ve su, karıştır, erit.", 1)]),
    (5, None, ["BİR MADEN,", "BİR MÜHENDİS."], art_mine(), (540, 715), -3, (720, 715), LIMEC,
     [("Rivayete göre 1898, Küba. Daiquirí'deki demir madeninde çalışan Amerikalı mühendis Jennings Cox beni ilk karıştıran oldu.", 0), ("Kasabanın adı bana kaldı.", 1)]),
    (6, None, ["SONRA HAVANA'YA", "TAŞINDIM."], art_coupe((222, 236, 170), k=1.05, frozen=True, garnish="lime"), (520, 715), -4, (700, 715), CORAL,
     [("El Floridita'nın barmeni Constantino Ribalaigua beni buzla çırpıp donmuş bi hâle soktu.", 0), ("Barın müdavimlerinden biri: Hemingway.", 1)]),
]
for i, (idx, lab, big, art, axy, rot, dxy, dc, parts) in enumerate(pages):
    img = bold_page(P, idx, lab, big, art, axy, rot, dxy, parts, 60 + i, dc)
    save(img, f"DQB_0{idx}.jpg")
print("ok")
