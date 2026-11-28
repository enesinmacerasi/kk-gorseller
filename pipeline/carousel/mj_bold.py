from mj_art import *
P = PALETTES["komur"]
LIMEC = (150, 196, 70); CREAMD = (236, 226, 200); CORAL = (242, 140, 110)
pages = [
    (2, "PARÇA 1/3 · BEYAZ ROM", ["İLK PARÇAM:", "BEYAZ ROM."], art_bottle((236, 238, 228), glass=(205, 216, 210), label="RON BLANCO"), (540, 715), -8, (690, 715), CORAL,
     [("Hafif bi rom seç.", 0), ("Ağır bi rom naneyi bastırır, ben ferahlığımı kaybederim.", 1)]),
    (3, "PARÇA 2/3 · NANE", ["İKİNCİ PARÇAM:", "TAZE NANE."], art_mint(), (560, 715), 6, (620, 715), CREAMD,
     [("İmzam bu.", 0), ("Naneyi ezme, hafifçe bastır. Ezilen nane acılaşır.", 1)]),
    (4, "PARÇA 3/3 · LIME, ŞEKER, SODA", ["ÜÇÜNCÜ PARÇAM:", "LIME, ŞEKER, SODA."], art_wheel((70, 110, 35), (150, 196, 70), (205, 228, 140)), (580, 715), 12, (640, 715), CREAMD,
     [("Lime ile şeker beni dengeler, soda hafifletir.", 0), ("Sodayı en son ekle ki gazı kaçmasın.", 1)]),
    (5, None, ["ÖNCE", "İLAÇTIM."], art_ship(), (540, 715), -3, (720, 715), LIMEC,
     [("Rivayete göre 1500'lerin sonu, Küba. Korsan Francis Drake'in tayfası hastalanınca, şeker kamışından yapılan sert bi içkiye nane, lime ve şeker kattılar.", 0), ("Adı El Draque'ydı.", 1)]),
    (6, None, ["ADIMI KİMSE", "TAM BİLMİYOR."], art_word(), (540, 715), -4, (700, 715), CORAL,
     [("Kimi Afrika kökenli 'mojo' kelimesinden diyor, kimi İspanyolca 'mojadito', yani 'biraz ıslak'.", 0), ("Beni dünyaya Havana'nın barları tanıttı.", 1)]),
]
for i, (idx, lab, big, art, axy, rot, dxy, dc, parts) in enumerate(pages):
    img = bold_page(P, idx, lab, big, art, axy, rot, dxy, parts, 70 + i, dc)
    save(img, f"MJB_0{idx}.jpg")
print("ok")
