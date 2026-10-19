# sablon_motoru.py - BiTTuRK Şablon Üretim Altyapısı
import re
from ayarlar import SERIT_URL_DEPOSU

def format_youtube_url(url):
    """Kullanıcıdan gelen youtube linklerini temiz watch?v= formatına çevirir."""
    if not url or not url.strip():
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    video_id = "dQw4w9WgXcQ"
    match = re.search(r'(?:v=|\/v\/|embed\/|youtu\.be\/|\/shorts\/|watch\?v=)([a-zA-Z0-9_-]{11})', url)
    if match:
        video_id = match.group(1)
    return f"https://www.youtube.com/watch?v={video_id}"

def build_media_language_icons(medya_secenekleri):
    """Seçilen seçeneklere göre dil ikonlarını yan yana dizen BBCode bloğu (başta)."""
    ikonlar = []
    if medya_secenekleri.get("cift") == "Evet":
        ikonlar.append(f"[img]{SERIT_URL_DEPOSU['dual']}[/img]")
    if medya_secenekleri.get("dublaj") == "Evet":
        ikonlar.append(f"[img]{SERIT_URL_DEPOSU['turkcedub']}[/img]")
    if medya_secenekleri.get("orjinal") == "Evet":
        ikonlar.append(f"[img]{SERIT_URL_DEPOSU['orjdub']}[/img]")
    if medya_secenekleri.get("altyazi") == "Evet":
        ikonlar.append(f"[img]{SERIT_URL_DEPOSU['altyazili']}[/img]")
    if ikonlar:
        return f"[center]{''.join(ikonlar)}[/center]\n"
    return ""

def build_extra_icons(medya_secenekleri):
    """Seçilen seçeneklere göre 3d ve anonimkaynak ikonlarını yan yana dizen BBCode bloğu (NFO'dan sonra)."""
    ikonlar = []
    if medya_secenekleri.get("3d") == "Evet":
        ikonlar.append(f"[img]{SERIT_URL_DEPOSU['3d']}[/img]")
    if medya_secenekleri.get("anonim") == "Evet":
        ikonlar.append(f"[img]{SERIT_URL_DEPOSU['anonimkaynak']}[/img]")
    if ikonlar:
        return f"[center]{''.join(ikonlar)}[/center]\n"
    return ""

def film_sablonu(veri, medya_secenekleri):
    """The WONDERfools düzenine tam uyumlu mühürlü Film BBCode motoru."""
    kod = []
    if veri.get("ad"):
        kod.append(f"[center]{veri['ad'].strip()}[/center]\n")
    kod.append(build_media_language_icons(medya_secenekleri))
    
    # 🚨 DÜZELTME: [center Pall] hatası tamamen temizlenip mühürlü [center] yapıldı 🚨
    if veri.get("afis"):
        kod.append(f"[center][img]{veri['afis'].strip()}[/img][/center]\n")
    
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['filmdetaylari']}[/img][/center]")
    if veri.get("detay"):
        kod.append(f"[center][img]{veri['detay'].strip()}[/img][/center]\n")
        
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['oyuncular']}[/img][/center]")
    if veri.get("oyuncu"):
        kod.append(f"[center][img]{veri['oyuncu'].strip()}[/img][/center]\n")
        
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['filmkonusu']}[/img][/center]")
    if veri.get("konu"):
        kod.append(f"[center][b]{veri['konu'].strip()}[/b][/center]\n")
        
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['fragman']}[/img][/center]")
    fragman_url = format_youtube_url(veri.get("fragman"))
    kod.append(f"[center][youtube]{fragman_url}[/youtube][/center]\n")
    
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['nfo']}[/img][/center]")
    if veri.get("info"):
        kod.append(f"[center][code]{veri['info'].strip()}[/code][/center]\n")
    else:
        kod.append("[center][code]Info Bilgileri NFO Sekmesindedir[/code][/center]\n")
    
    kod.append(build_extra_icons(medya_secenekleri))
        
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['keyifliseyirler']}[/img][/center]")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['kaynak']}[/img][/center]")
    return "".join(kod)

def dizi_sablonu(veri, medya_secenekleri):
    kod = []
    if veri.get("ad"): kod.append(f"[center]{veri['ad'].strip()}[/center]\n")
    kod.append(build_media_language_icons(medya_secenekleri))
    if veri.get("afis"): kod.append(f"[center][img]{veri['afis'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['dizidetaylari']}[/img][/center]")
    if veri.get("detay"): kod.append(f"[center][img]{veri['detay'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['dizioyunculari']}[/img][/center]")
    if veri.get("oyuncu"): kod.append(f"[center][img]{veri['oyuncu'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['dizikonusu']}[/img][/center]")
    if veri.get("konu"): kod.append(f"[center][b]{veri['konu'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['fragman']}[/img][/center]")
    fragman_url = format_youtube_url(veri.get("fragman"))
    kod.append(f"[center][youtube]{fragman_url}[/youtube][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['nfo']}[/img][/center]")
    if veri.get("info"): kod.append(f"[center][code]{veri['info'].strip()}[/code][/center]\n")
    else: kod.append("[center][code]Info Bilgileri NFO Sekmesindedir[/code][/center]\n")
    kod.append(build_extra_icons(medya_secenekleri))
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['keyifliseyirler']}[/img][/center]")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['kaynak']}[/img][/center]")
    return "".join(kod)

def muzik_sablonu(veri):
    kod = []
    if veri.get("album"): kod.append(f"[center]{veri['album'].strip()}[/center]\n")
    if veri.get("afis"): kod.append(f"[center][img]{veri['afis'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['filmdetaylari']}[/img][/center]")
    if veri.get("detay"): kod.append(f"[center][b]{veri['detay'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['parcalistesi']}[/img][/center]")
    if veri.get("parca"): kod.append(f"[center][b]{veri['parca'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['keyiflidinlemeler']}[/img][/center]")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['kaynak']}[/img][/center]")
    return "".join(kod)

def oyun_sablonu(veri):
    kod = []
    if veri.get("ad"): kod.append(f"[center]{veri['ad'].strip()}[/center]\n")
    if veri.get("afis"): kod.append(f"[center][img]{veri['afis'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['oyuntanitim']}[/img][/center]")
    if veri.get("tanitim"): kod.append(f"[center][b]{veri['tanitim'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['fragman']}[/img][/center]")
    fragman_url = format_youtube_url(veri.get("fragman"))
    kod.append(f"[center][youtube]{fragman_url}[/youtube][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['sistemgereksinimi']}[/img][/center]")
    if veri.get("sistem"): kod.append(f"[center][b]{veri['sistem'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['nfo']}[/img][/center]")
    if veri.get("info"): kod.append(f"[center][code]{veri['info'].strip()}[/code][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['keyifliseyirler']}[/img][/center]")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['kaynak']}[/img][/center]")
    return "".join(kod)

def program_sablonu(veri):
    kod = []
    if veri.get("ad"): kod.append(f"[center]{veri['ad'].strip()}[/center]\n")
    if veri.get("afis"): kod.append(f"[center][img]{veri['afis'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['programtanitim']}[/img][/center]")
    if veri.get("tanitim"): kod.append(f"[center][b]{veri['tanitim'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['fragman']}[/img][/center]")
    fragman_url = format_youtube_url(veri.get("fragman"))
    kod.append(f"[center][youtube]{fragman_url}[/youtube][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['sistemgereksinimi']}[/img][/center]")
    if veri.get("sistem"): kod.append(f"[center][b]{veri['sistem'].strip()}[/b][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['nfo']}[/img][/center]")
    if veri.get("info"): kod.append(f"[center][code]{veri['info'].strip()}[/code][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['keyifliseyirler']}[/img][/center]")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['kaynak']}[/img][/center]")
    return "".join(kod)

def vip_sablonu(veri):
    kod = []
    if veri.get("ad"): kod.append(f"[center]{veri['ad'].strip()}[/center]\n")
    if veri.get("ekran"): kod.append(f"[center][img]{veri['ekran'].strip()}[/img][/center]\n")
    kod.append(f"[center][img]{SERIT_URL_DEPOSU['keyifliseyirler']}[/img][/center]")
    return "".join(kod)
