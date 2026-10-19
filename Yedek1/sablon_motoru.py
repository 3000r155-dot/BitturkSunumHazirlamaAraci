# sablon_motoru.py - BiTTuRK Sunum Hazırlama Aracı Şablon Motoru

# ayarlar.py içerisindeki havuz yapısı ve sizin belirttiğiniz birebir linkler
RESIM_HAVUZU = {
    # Dil Butonları (https)
    "orjinal": "https://bitturk.net",
    "cift": "https://bitturk.net",
    "dublaj": "https://bitturk.net",
    "altyazi": "https://bitturk.net",
    "3d": "https://bitturk.net",
    "anonim": "https://bitturk.net",
    
    # Şerit Görselleri (http)
    "dizidetaylari": "http://bitturk.net",
    "dizioyunculari": "http://bitturk.net",
    "dizikonusu": "http://bitturk.net",
    "fragman": "http://bitturk.net",
    "nfo": "http://bitturk.net",
    "keyifliseyirler": "http://bitturk.net",
    "kaynak": "http://bitturk.net",
    
    # Diğer Şerit Linkleriniz (Eksiksiz Sabit Tutulanlar)
    "filmdetaylari": "https://bitturk.net",
    "filmkonusu": "https://bitturk.net",
    "oyuncular": "https://bitturk.net",
    "oyuntanitim": "https://bitturk.net",
    "sistemgereksinimi": "https://bitturk.net",
    "bilgi": "https://bitturk.net",
    "programtanitim": "https://bitturk.net",
    "ekrangoruntusu": "https://ibb.co",
    "xxx": "https://ibb.co",
    "altin": "https://bitturk.net",
    "gumus": "https://bitturk.net",
    "parcalistesi": "https://bitturk.net",
    "keyiflidinlemeler": "https://bitturk.net",
    "x2sunum": "https://bitturk.net",
    "btrgkaynak": "https://bitturk.net"
}

def _dil_etiketleri_uret(medya_secenekleri):
    """Uygulamadaki Checkbutton durumlarına göre yan yana dil resimlerini basar."""
    dil_bbcode = ""
    if medya_secenekleri.get("orjinal") == "Evet": 
        dil_bbcode += f"[img]{RESIM_HAVUZU['orjinal']}[/img]"
    if medya_secenekleri.get("cift") == "Evet": 
        dil_bbcode += f"[img]{RESIM_HAVUZU['cift']}[/img]"
    if medya_secenekleri.get("dublaj") == "Evet": 
        dil_bbcode += f"[img]{RESIM_HAVUZU['dublaj']}[/img]"
    if medya_secenekleri.get("altyazi") == "Evet": 
        dil_bbcode += f"[img]{RESIM_HAVUZU['altyazi']}[/img]"
    if medya_secenekleri.get("3d") == "Evet": 
        dil_bbcode += f"[img]{RESIM_HAVUZU['3d']}[/img]"
    if medya_secenekleri.get("anonim") == "Evet": 
        dil_bbcode += f"[img]{RESIM_HAVUZU['anonim']}[/img]"
    
    if dil_bbcode:
        return f"[center]{dil_bbcode}[/center]\n"
    return ""

def film_sablonu(veri, medya_secenekleri):
    """Film sekmesi için BBCode taslağını oluşturur."""
    bbcode = f"[center][b]{veri.get('ad', '')}[/b][/center]\n"
    bbcode += _dil_etiketleri_uret(medya_secenekleri)
    
    if veri.get("afis"): 
        bbcode += f"[center][img]{veri['afis']}[/img][/center]\n"
    if veri.get("detay"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['filmdetaylari']}[/img][/center]\n[center][img]{veri['detay']}[/img][/center]\n"
    if veri.get("konu"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['filmkonusu']}[/img][/center]\n[center][b]{veri['konu']}[/b][/center]\n"
    if veri.get("oyuncu"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['oyuncular']}[/img][/center]\n[center][img]{veri['oyuncu']}[/img][/center]\n"
    if veri.get("fragman"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['fragman']}[/img][/center]\n[center][youtube]{veri['fragman']}[/youtube][/center]\n"
    if veri.get("info"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['nfo']}[/img][/center]\n[center][code]{veri['info']}[/code][/center]\n"
        
    bbcode += f"[center][img]{RESIM_HAVUZU['keyifliseyirler']}[/img][/center]"
    return bbcode

def dizi_sablonu(veri, medya_secenekleri):
    """Dizi sekmesi için BBCode taslağını oluşturur."""
    bbcode = f"[center][b]{veri.get('ad', '')}[/b][/center]\n"
    bbcode += _dil_etiketleri_uret(medya_secenekleri)
    
    if veri.get("afis"): 
        bbcode += f"[center][img]{veri['afis']}[/img][/center]\n"
    if veri.get("detay"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['dizidetaylari']}[/img][/center]\n[center][img]{veri['detay']}[/img][/center]\n"
    if veri.get("konu"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['dizikonusu']}[/img][/center]\n[center][b]{veri['konu']}[/b][/center]\n"
    if veri.get("oyuncu"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['dizioyunculari']}[/img][/center]\n[center][img]{veri['oyuncu']}[/img][/center]\n"
    if veri.get("fragman"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['fragman']}[/img][/center]\n[center][youtube]{veri['fragman']}[/youtube][/center]\n"
    if veri.get("info"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['nfo']}[/img][/center]\n[center][code]{veri['info']}[/code][/center]\n"
    if veri.get("kaynak_durum") == "Evet" and veri.get("kaynak_veri"):
        bbcode += f"[center][img]{RESIM_HAVUZU['kaynak']}[/img][/center]\n[center]{veri['kaynak_veri']}[/center]\n"
        
    bbcode += f"[center][img]{RESIM_HAVUZU['keyifliseyirler']}[/img][/center]"
    return bbcode

def muzik_sablonu(veri):
    """Müzik kategorisi için BBCode çıktısı üretir."""
    bbcode = f"[center][b]{veri.get('album', '')}[/b][/center]\n"
    if veri.get("afis"): 
        bbcode += f"[center][img]{veri['afis']}[/img][/center]\n"
    if veri.get("detay"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['bilgi']}[/img][/center]\n[center]{veri['detay']}[/center]\n"
    if veri.get("parca"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['parcalistesi']}[/img][/center]\n[center][code]{veri['parca']}[/code][/center]\n"
        
    bbcode += f"[center][img]{RESIM_HAVUZU['keyiflidinlemeler']}[/img][/center]"
    return bbcode

def oyun_sablonu(veri):
    """Oyun kategorisi için BBCode çıktısı üretir."""
    bbcode = f"[center][b]{veri.get('ad', '')}[/b][/center]\n"
    if veri.get("afis"): 
        bbcode += f"[center][img]{veri['afis']}[/img][/center]\n"
    if veri.get("tanitim"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['oyuntanitim']}[/img][/center]\n[center]{veri['tanitim']}[/center]\n"
    if veri.get("sistem"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['sistemgereksinimi']}[/img][/center]\n[center][b]{veri['sistem']}[/b][/center]\n"
    if veri.get("fragman"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['fragman']}[/img][/center]\n[center][youtube]{veri['fragman']}[/youtube][/center]\n"
    if veri.get("info"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['nfo']}[/img][/center]\n[center][code]{veri['info']}[/code][/center]\n"
        
    bbcode += f"[center][img]{RESIM_HAVUZU['keyifliseyirler']}[/img][/center]"
    return bbcode

def program_sablonu(veri):
    """Program/Diğer kategorisi için BBCode çıktısı üretir."""
    bbcode = f"[center][b]{veri.get('ad', '')}[/b][/center]\n"
    if veri.get("afis"): 
        bbcode += f"[center][img]{veri['afis']}[/img][/center]\n"
    if veri.get("tanitim"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['programtanitim']}[/img][/center]\n[center]{veri['tanitim']}[/center]\n"
    if veri.get("sistem"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['sistemgereksinimi']}[/img][/center]\n[center]{veri['sistem']}[/center]\n"
    if veri.get("info"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['nfo']}[/img][/center]\n[center][code]{veri['info']}[/code][/center]\n"
        
    bbcode += f"[center][img]{RESIM_HAVUZU['keyifliseyirler']}[/img]"
    return bbcode

# EKSİK OLAN VE HATAYA SEBEP VEREN FONKSİYON BURAYA EKLENDİ
def vip_sablonu(veri):
    """V.I.P Paylaşımlar için BBCode çıktısı üretir."""
    bbcode = f"[center][b][size=6][color=#FF0000]★ V.I.P ÖZEL PAYLAŞIM ★[/color][/size][/b][/center]\n\n"
    bbcode += f"[center][b][size=4][color=#FFFF00]{veri.get('ad', '')}[/color][/size][/b][/center]\n\n"
    if veri.get("ekran"): 
        bbcode += f"[center][img]{RESIM_HAVUZU['ekrangoruntusu']}[/img][/center]\n[center][img]{veri['ekran']}[/img][/center]\n"
        
    bbcode += f"[center][img]{RESIM_HAVUZU['keyifliseyirler']}[/img][/center]"
    return bbcode
