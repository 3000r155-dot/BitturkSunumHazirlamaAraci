# ayarlar.py - MÜHÜRLÜ HAVUZ, REGEX VE DLL İKON TANIMLAMALARI

MUHURLU_URL_DEPOLOSU = {
    "SITEYE_GIT": "https://bitturk.net/?p=torrents&action=upload&pid=21",
    "orjinal": "https://bitturk.net/images/orjdub.png",
    "cift": "https://bitturk.net/images/dual.png",
    "dublaj": "https://bitturk.net/images/turkcedub.png",
    "altyazi": "https://bitturk.net/images/altyazili.png",
    "3d": "https://bitturk.net/images/3d.png",
    "anonim": "https://bitturk.net/images/anonimkaynak.png"
}

DIL_PATTERNLER = [
    r"\[img\]https://bitturk\.net/images/orjdub\.png\[/img\]",
    r"\[img\]https://bitturk\.net/images/dual\.png\[/img\]",
    r"\[img\]https://bitturk\.net/images/turkcedub\.png\[/img\]",
    r"\[img\]https://bitturk\.net/images/altyazili\.png\[/img\]",
    r"\[img\]https://bitturk\.net/images/3d\.png\[/img\]",
    r"\[img\]https://bitturk\.net/images/anonimkaynak\.png\[/img\]"
]

SERIT_PATTERNLER = [
    r"\[img\]http://bitturk\.net/images/dizidetaylari\.png\[/img\]",
    r"\[img\]http://bitturk\.net/images/dizioyunculari\.png\[/img\]",
    r"\[img\]http://bitturk\.net/images/dizikonusu\.png\[/img\]",
    r"\[img\]http://bitturk\.net/images/fragman\.png\[/img\]",
    r"\[img\]http://bitturk\.net/images/nfo\.png\[/img\]",
    r"\[img\]http://bitturk\.net/images/keyifliseyirler\.png\[/img\]",
    r"\[img\]http://bitturk\.net/images/kaynak\.png\[/img\]"
]

# --- DLL VE MODERN İKON YAPILANDIRMASI ---
# Varsayılan olarak Windows'un kendi zengin imageres.dll dosyasını veya kendi üreteceğiniz 'CustomIcons.dll' dosyasını bağlayabilirsiniz.
DLL_YOLU = "imageres.dll" 

IKON_INDEKSLERI = {
    "temizle": 84,     # Çöp kutusu veya temizlik ikonu indeksi
    "kopyala": 22,     # Pano / Kopyalama ikonu indeksi
    "kaydet": 28,      # Disk / Kaydetme ikonu indeksi
    "yukle": 3,        # Klasör / Açma ikonu indeksi
    "site": 142,       # Dünya / İnternet ikonu indeksi
    "karanlik": 121,   # Ay / Gece modu ikonu indeksi
    "aydinlik": 122    # Güneş / Gündüz modu ikonu indeksi
}
