# ayarlar.py - BiTTuRK Sunum Hazırlama Aracı Merkezi Ayar Havuzu

MUHURLU_URL_DEPOLOSU = {
    "SITEYE_GIT": "https://bitturk.net",
    "YUKLEME_SAYFASI": "https://bitturk.net/?p=torrents&action=upload&pid=21"
}

# Gönderdiğiniz tam listeye göre güncellenmiş BiTTuRK Şerit ve İkon URL Deposu
SERIT_URL_DEPOSU = {
    "turkcedub": "https://bitturk.net/images/turkcedub.png",
    "altyazili": "https://bitturk.net/images/altyazili.png",
    "orjdub": "https://bitturk.net/images/orjdub.png",
    "dual": "https://bitturk.net/images/dual.png",
    "3d": "https://bitturk.net/images/3d.png",
    "anonimkaynak": "https://bitturk.net/images/anonimkaynak.png",
    "dizioyunculari": "https://bitturk.net/images/dizioyunculari.png",
    "oyuncular": "https://bitturk.net/images/oyuncular.png",
    "filmdetaylari": "https://bitturk.net/images/filmdetaylari.png",
    "dizidetaylari": "https://bitturk.net/images/dizidetaylari.png",
    "dizikonusu": "https://bitturk.net/images/dizikonusu.png",
    "filmkonusu": "https://bitturk.net/images/filmkonusu.png",
    "fragman": "https://bitturk.net/images/fragman.png",
    "nfo": "https://bitturk.net/images/nfo.png",
    "oyuntanitim": "https://bitturk.net/images/oyuntanitim.png",
    "sistemgereksinimi": "https://bitturk.net/images/sistemgereksinimi.png",
    "bilgi": "https://bitturk.net/images/bilgi.png",
    "programtanitim": "https://bitturk.net/images/programtanitim.png",
    "keyifliseyirler": "https://bitturk.net/images/keyifliseyirler.png",
    "ekrangoruntusu": "https://image.ibb.co/m0ecs8/ekrangoruntusu.png",
    "xxx": "https://image.ibb.co/mu17s8/xxx.png",
    "altin": "https://bitturk.net/images/altin.png",
    "gumus": "https://bitturk.net/images/gumus.png",
    "parcalistesi": "https://bitturk.net/images/parcalistesi.png",
    "keyiflidinlemeler": "https://bitturk.net/images/keyiflidinlemeler.png",
    "x2sunum": "https://bitturk.net/images/x2sunum.png",
    "kaynak": "https://bitturk.net/images/kaynak.png",
    "btrgkaynak": "https://bitturk.net/images/btrgkaynak.png"
}

# Canlı metin renklendiricinin dil ve şerit ikon linklerini yakalamasını sağlayan düzenli ifadeler
DIL_PATTERNLER = [
    r'https?://bitturk\.net/images/(?:dual|turkcedub|orjdub|altyazili|3d|anonimkaynak)\.png'
]

SERIT_PATTERNLER = [
    r'https?://(?:bitturk\.net/images|image\.ibb\.co)/[^\s\[\]]+\.png'
]
