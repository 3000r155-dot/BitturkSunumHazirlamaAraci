# tasarim_elemanlari.py - PARÇA 1 (ÇEKİRDEK YAPI VE 3 GÖZELİ DÖNÜŞ MOTORU)

import customtkinter as ctk
import webbrowser
from tkinter import filedialog, messagebox
import os
import shutil
import re
from playwright.sync_api import sync_playwright
import ayarlar

try:
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
except Exception:
    pass

# Temizleme fonksiyonunun tüm sekmelerdeki bileşenleri görebilmesi için global listeler
TÜM_GİRDİLER = []
TÜM_ONAY_KUTULARI = []
TÜM_ONAY_ETİKETLERİ = []

def create_layout_structure(parent):
    # Sol panel girdileri ve bağımsız pencereli container'ları taşır (Genişlik mühürlü)
    sol_frame = ctk.CTkFrame(parent, width=320, fg_color="transparent")
    sol_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10)
    sol_frame.pack_propagate(False)

    # Sağ panel BBCode kutusunu ve tabandaki buton konteynerini taşır
    sag_frame = ctk.CTkFrame(parent, fg_color="transparent")
    sag_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # BBCode kutusunu tek başına şık ve bağımsız bir Visual Container içine alıyoruz
    bbcode_container = ctk.CTkFrame(sag_frame, border_width=1, border_color=["#D1D5DB", "#43474B"])
    # Alttaki buton kutusuyla tam eşit hizalanması için padx sıfırlandı
    bbcode_container.pack(side="top", fill="both", expand=True, pady=(0, 4), padx=0)
    
    lbl_bbcode_title = ctk.CTkLabel(bbcode_container, text="  📋 BBCode Çıktı Ekranı (Canlı Önizleme)", font=ctk.CTkFont(size=11, weight="bold"), text_color=["#4B5563", "#9CA3AF"])
    lbl_bbcode_title.pack(anchor="w", pady=(4, 1), padx=4)

    # BBCode kutusu container içine tam oturuyor, dikey alanı butonları sıkıştırmayacak şekilde dengeler
    txt_output = ctk.CTkTextbox(bbcode_container, font=ctk.CTkFont(family="Courier", size=12), fg_color="transparent")
    txt_output.pack(padx=6, pady=(1, 6), fill="both", expand=True)

    txt_output._textbox.tag_configure("center", justify="center")
    txt_output._textbox.tag_configure("serit_resim", foreground="#E41414")
    txt_output._textbox.tag_configure("dil_resim", foreground="#107C41")
    
    txt_output._textbox.tag_configure("bbcode_tag", foreground="#00BFFF", font=ctk.CTkFont(family="Courier", size=12, weight="bold"))
    txt_output._textbox.tag_configure("bbcode_url", foreground="#FF8C00", font=ctk.CTkFont(family="Courier", size=12))

    def bbcode_renklendir_tetikleyici(event=None):
        content = txt_output.get("1.0", "end")
        txt_output._textbox.tag_remove("bbcode_tag", "1.0", "end")
        txt_output._textbox.tag_remove("bbcode_url", "1.0", "end")
        
        for match in re.finditer(r'\[\/?[a-zA-Z0-9\=\#\s\:\/\.\-\_\?\&\=\%\+\,\;\!\@\^\*\(\)]+\]', content):
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            txt_output._textbox.tag_add("bbcode_tag", start_idx, end_idx)
            
        for match in re.finditer(r'https?://[^\s\[\]]+', content):
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            txt_output._textbox.tag_add("bbcode_url", start_idx, end_idx)

    def sarmalanmis_insert(index, text, *args):
        txt_output._textbox._original_insert(index, text, *args)
        bbcode_renklendir_tetikleyici()

    txt_output._textbox._original_insert = txt_output._textbox.insert
    txt_output._textbox.insert = sarmalanmis_insert
    
    txt_output.bind("<KeyRelease>", bbcode_renklendir_tetikleyici)
    txt_output.bbcode_renklendir = bbcode_renklendir_tetikleyici

    # HATANIN KÖKÜNÜ KESEN SATIR: main.py'nin beklediği 3. değişken (sag_frame) dışarı aktarılıyor!
    return sol_frame, txt_output, sag_frame
# tasarim_elemanlari.py - PARÇA 2 (YÜKLEME MOTORU SİSTEMİ)

def tam_otomatik_imgbb_yukle(girdi_kutusu, update_callback):
    # Bilgisayardan yüklemek istediğiniz resmi bulmanız için standart Windows paneli açılır
    dosya_yolu = filedialog.askopenfilename(
        title="Yüklenecek Görseli Seçin",
        filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    
    if not dosya_yolu:
        return  # Seçim iptal edildiyse işlem yapma

    try:
        # Playwright görünmez (Headless) gerçek tarayıcı motoru başlatılıyor
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            
            # Sitedeki gereksiz kaynakları engelleyerek yükleme süresini en aza indiriyoruz
            def kaynak_filtresi(route):
                if route.request.resource_type in ["image", "stylesheet", "font", "media", "eventsource"]:
                    route.abort()
                else:
                    route.continue_()
            
            page.route("**/*", kaynak_filtresi)
            page.goto("https://imgbb.com", wait_until="domcontentloaded")
            
            page.wait_for_selector('li[data-action="top-bar-upload"]', timeout=10000)
            page.click('li[data-action="top-bar-upload"]')
            page.set_input_files('input[type="file"]', dosya_yolu)
            
            page.wait_for_selector('button[data-action="upload"]', state="visible", timeout=10000)
            page.click('button[data-action="upload"]')
            
            page.wait_for_selector('select[id="uploaded-embed-toggle"]', state="visible", timeout=20000)
            page.select_option('select[id="uploaded-embed-toggle"]', value="viewer-links")
            
            goruntuleyici_linki = page.locator('#uploaded-embed-code-0').input_value()
            browser.close()
            
            if goruntuleyici_linki and "ibb.co" in goruntuleyici_linki:
                if hasattr(girdi_kutusu, "delete"):
                    if isinstance(girdi_kutusu, ctk.CTkTextbox):
                        girdi_kutusu.delete("1.0", "end")
                        girdi_kutusu.insert("1.0", goruntuleyici_linki)
                    else:
                        girdi_kutusu.delete(0, 'end')
                        girdi_kutusu.insert(0, goruntuleyici_linki)
                
                girdi_kutusu.configure(fg_color="#A2E8A2", text_color="#000000")
                
                if update_callback:
                    update_callback()
            else:
                messagebox.showerror("Yükleme Hatası", "Resim yüklendi ancak Görüntüleyici Linki elementten ayıklanamadı.")
                
    except Exception as e:
        messagebox.showerror("Sistem Hatası", f"Otomatik yükleme motorunda tarayıcı hatası oluştu:\n{str(e)}")
# tasarim_elemanlari.py - PARÇA 3 (TAM GENİŞLİKTE EŞİT BOYUTLU BUTON KONTEYNERİ)

def ekle_alt_butonlar(app_instance, parent, txt_output, temizle_func, kaydet_func, yukle_func):
    # KESİN ÇÖZÜM: Genişliğin BBCode kutusuyla birebir aynı hizada olması için padx=0 yapıldı!
    # expand=False ve dikey pady=(4, 5) daraltması sayesinde "Siteye Git" butonu asla aşağıya taşmaz.
    buton_container = ctk.CTkFrame(parent, border_width=1, border_color=["#D1D5DB", "#43474B"])
    buton_container.pack(side="top", fill="x", pady=(4, 5), padx=0, expand=False)

    lbl_btn_title = ctk.CTkLabel(buton_container, text="  🛠️ Sunum İşlemleri & Taslak Yönetimi", font=ctk.CTkFont(size=11, weight="bold"), text_color=["#4B5563", "#9CA3AF"])
    lbl_btn_title.pack(anchor="w", pady=(4, 1), padx=4)

    btn_frame = ctk.CTkFrame(buton_container, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(2, 6), padx=6)
    
    def zincirleme_temizle():
        temizle_func()
        varsayilan_fg = ["#F9F9FA", "#343638"] if ctk.get_appearance_mode() == "Dark" else ["#F9F9FA", "#F9F9FA"]
        for girdi_obj in TÜM_GİRDİLER:
            try:
                girdi_obj.configure(fg_color=varsayilan_fg, text_color=["#000000", "#FFFFFF"])
            except Exception:
                pass
                
        for chk_obj in TÜM_ONAY_KUTULARI:
            try:
                chk_obj.configure(fg_color=["#3B8ED0", "#1F6AA5"], check_color=["#FFFFFF", "#FFFFFF"])
            except Exception:
                pass

        for lbl_obj in TÜM_ONAY_ETİKETLERİ:
            try:
                varsayilan_text = ["#000000", "#FFFFFF"]
                lbl_obj.configure(text_color=varsayilan_text)
            except Exception:
                pass
        
        if hasattr(txt_output, "bbcode_renklendir"):
            txt_output.bbcode_renklendir()

    def kopyala_panoya():
        app_instance.clipboard_clear()
        app_instance.clipboard_append(txt_output.get("1.0", "end-1c"))
        if hasattr(txt_output, "bbcode_renklendir"):
            txt_output.bbcode_renklendir()

    # KESİN DENGELİ BOYUT: fill="both" ve expand=True sayesinde 5 butonun genişliği de milimetrik olarak birbirine eşittir!
    ctk.CTkButton(btn_frame, text="🧹 Sunumu Temizle", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=zincirleme_temizle).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="📋 BBCode Kopyala", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=kopyala_panoya).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="💾 Taslağı Kaydet", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=kaydet_func).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="📂 Taslak Yükle", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=yukle_func).pack(side="left", fill="both", expand=True, padx=3)
    
    ctk.CTkButton(btn_frame, text="🌐 Siteye Git", font=ctk.CTkFont(size=11, weight="bold"), height=32, fg_color="green", 
                  command=lambda: webbrowser.open(ayarlar.MUHURLU_URL_DEPOLOSU["SITEYE_GIT"])).pack(side="left", fill="both", expand=True, padx=3)
# tasarim_elemanlari.py - PARÇA 4 (BAĞIMSIZ VISUAL CONTAINER GİRDİLERİ VE KUSURSUZ DİKEY HİZALAMA)

def ekle_girdi(parent, label_text, is_textbox=False, height=60, has_upload=False, ornek="", update_callback=None):
    emoji_haritasi = {
        "Film Adı": "🎬 Film Adı", "Dizi Adı": "📺 Dizi Adı", "Albüm Adı": "🎵 Albüm Adı", "Adı": "📦 Eser Adı", "Sunum Adı": "⭐ Özel Başlık",
        "Afiş (Resim Linki)": "🖼️ Afiş (Resim Linki)", "Detay (Resim Linki)": "🔍 Detay (Resim Linki)", "Oyuncular (Resim Linki)": "👥 Oyuncular (Resim Linki)",
        "Konu": "📝 Konu Açıklaması", "Tanıtım": "📖 Tanıtım ve Özet", "Detay": "📊 Teknik Detaylar", "Parça Listesi": "📜 Parça Listesi",
        "Fragman (Youtube Linki)": "🎥 Fragman (Youtube Linki)", "Minumum Sistem": "💻 Sistem Gereksinimleri", "NFO / Info": "ℹ️ NFO / Info Bilgisi",
        "info": "ℹ️ NFO / Info Bilgisi", "Ekran Görüntüsü (Resim Linki)": "📸 Ekran Görüntüsü"
    }
    
    # Her bir başlık ve textbox için tamamen bağımsız bir şık Visual Container (Group Box)
    tekli_container = ctk.CTkFrame(parent, border_width=1, border_color=["#E5E7EB", "#374151"], fg_color="transparent")
    tekli_container.pack(fill="x", pady=3, padx=2)
    
    gosterilecek_baslik = emoji_haritasi.get(label_text, label_text)
    lbl = ctk.CTkLabel(tekli_container, text=f" {gosterilecek_baslik}", font=ctk.CTkFont(size=11, weight="bold"), anchor="w")
    lbl.pack(fill="x", pady=(3, 1), padx=4)
    
    varsayilan_fg = ["#F9F9FA", "#343638"] if ctk.get_appearance_mode() == "Dark" else ["#F9F9FA", "#F9F9FA"]

    def girdi_renk_guncelle(girdi_obj):
        try:
            veri = girdi_obj.get("1.0", "end-1c") if is_textbox else girdi_obj.get()
            if len(veri.strip()) > 0 and veri.strip() != ornek:
                girdi_obj.configure(fg_color="#A2E8A2", text_color="#000000")
            else:
                girdi_obj.configure(fg_color=varsayilan_fg, text_color=["#000000", "#FFFFFF"])
        except Exception:
            pass

    def sarmalanmis_callback(event=None, girdi_obj=None):
        if girdi_obj:
            girdi_renk_guncelle(girdi_obj)
        if update_callback:
            update_callback()
        try:
            parent.master.master.txt_output.bbcode_renklendir()
        except Exception:
            pass

    # KESİN DİKEY HİZALAMA: Afiş alanı iç dolgusu (padx=6) ile diğer tüm kutularla milimetrik eşitlendi
    if is_textbox:
        girdi = ctk.CTkTextbox(tekli_container, height=height, font=ctk.CTkFont(size=11))
        girdi.pack(fill="x", pady=(1, 4), padx=6)
    else:
        if has_upload:
            f = ctk.CTkFrame(tekli_container, fg_color="transparent")
            f.pack(fill="x", pady=(1, 4), padx=6)
            girdi = ctk.CTkEntry(f, placeholder_text=ornek, font=ctk.CTkFont(size=11))
            girdi.pack(side="left", fill="x", expand=True, padx=(0, 4))
            btn_yukle = ctk.CTkButton(f, text="📤 Yükle", width=50, height=24, font=ctk.CTkFont(size=10, weight="bold"), command=lambda: tam_otomatik_imgbb_yukle(girdi, lambda: sarmalanmis_callback(None, girdi)))
            btn_yukle.pack(side="right")
        else:
            girdi = ctk.CTkEntry(tekli_container, placeholder_text=ornek, font=ctk.CTkFont(size=11))
            girdi.pack(fill="x", pady=(1, 4), padx=6)

    def odak_kaybi_kontrolu(event):
        try:
            veri = girdi.get("1.0", "end-1c") if is_textbox else girdi.get()
            if not veri.strip():
                if is_textbox:
                    girdi.delete("1.0", "end")
                    girdi.insert("1.0", ornek)
                    girdi.configure(text_color="gray")
                girdi.configure(fg_color=varsayilan_fg)
        except Exception:
            pass

    girdi.bind("<FocusOut>", odak_kaybi_kontrolu)
    girdi.bind("<KeyRelease>", lambda event: sarmalanmis_callback(event, girdi))
    girdi.orijinal_ornek = ornek
    TÜM_GİRDİLER.append(girdi)
    return girdi

def ekle_medya_onay_kutulari(parent, update_callback=None):
    # Seçenekler grubu için ana Visual Container / Group Box
    group_box = ctk.CTkFrame(parent, border_width=1, border_color=["#D1D5DB", "#43474B"])
    group_box.pack(fill="x", pady=5, padx=2)
    
    lbl_group_title = ctk.CTkLabel(group_box, text="  ⚙️ Medya Seçenekleri & Dil Ayarları", font=ctk.CTkFont(size=11, weight="bold"), text_color=["#4B5563", "#9CA3AF"])
    lbl_group_title.pack(anchor="w", pady=(4, 2), padx=2)

    chk_frame1 = ctk.CTkFrame(group_box, fg_color="transparent")
    chk_frame1.pack(fill="x", pady=2, padx=6)
    chk_frame2 = ctk.CTkFrame(group_box, fg_color="transparent")
    chk_frame2.pack(fill="x", pady=(2, 6), padx=6)
    
    vars = {
        "orjinal": ctk.StringVar(value="Hayır"), "cift": ctk.StringVar(value="Hayır"),
        "dublaj": ctk.StringVar(value="Hayır"), "altyazi": ctk.StringVar(value="Hayır"),
        "anonim": ctk.StringVar(value="Hayır"), "3d": ctk.StringVar(value="Hayır")
    }
    
    def chk_renk_guncelle(lbl_obj, str_var):
        if str_var.get() == "Evet":
            lbl_obj.configure(text_color="#107C41")
        else:
            lbl_obj.configure(text_color=["#000000", "#FFFFFF"])

    def on_check_click(lbl_obj, str_var):
        chk_renk_guncelle(lbl_obj, str_var)
        if update_callback:
            update_callback()
        try:
            parent.master.master.txt_output.bbcode_renklendir()
        except Exception:
            pass

    # Sütun kaymalarını sıfırlayan 'width=95' sabit matris düzeni
    # 1. SATIR
    item_f1 = ctk.CTkFrame(chk_frame1, width=95, height=26, fg_color="transparent")
    item_f1.pack(side="left", padx=1, anchor="w")
    item_f1.pack_propagate(False)
    chk_orjinal = ctk.CTkCheckBox(item_f1, text="", width=18, variable=vars["orjinal"], onvalue="Evet", offvalue="Hayır")
    lbl_orjinal = ctk.CTkLabel(item_f1, text="🌐 Orijinal", font=ctk.CTkFont(size=10))
    chk_orjinal.configure(command=lambda: on_check_click(lbl_orjinal, vars["orjinal"]))
    chk_orjinal.pack(side="left", anchor="w"); lbl_orjinal.pack(side="left", padx=2, anchor="w")
    TÜM_ONAY_KUTULARI.append(chk_orjinal); TÜM_ONAY_ETİKETLERİ.append(lbl_orjinal)

    item_f2 = ctk.CTkFrame(chk_frame1, width=95, height=26, fg_color="transparent")
    item_f2.pack(side="left", padx=1, anchor="w")
    item_f2.pack_propagate(False)
    chk_cift = ctk.CTkCheckBox(item_f2, text="", width=18, variable=vars["cift"], onvalue="Evet", offvalue="Hayır")
    lbl_cift = ctk.CTkLabel(item_f2, text="🔄 Çift Dil", font=ctk.CTkFont(size=10))
    chk_cift.configure(command=lambda: on_check_click(lbl_cift, vars["cift"]))
    chk_cift.pack(side="left", anchor="w"); lbl_cift.pack(side="left", padx=2, anchor="w")
    TÜM_ONAY_KUTULARI.append(chk_cift); TÜM_ONAY_ETİKETLERİ.append(lbl_cift)

    item_f3 = ctk.CTkFrame(chk_frame1, width=95, height=26, fg_color="transparent")
    item_f3.pack(side="left", padx=1, anchor="w")
    item_f3.pack_propagate(False)
    chk_dublaj = ctk.CTkCheckBox(item_f3, text="", width=18, variable=vars["dublaj"], onvalue="Evet", offvalue="Hayır")
    lbl_dublaj = ctk.CTkLabel(item_f3, text="🇹🇷 Dublaj", font=ctk.CTkFont(size=10))
    chk_dublaj.configure(command=lambda: on_check_click(lbl_dublaj, vars["dublaj"]))
    chk_dublaj.pack(side="left", anchor="w"); lbl_dublaj.pack(side="left", padx=2, anchor="w")
    TÜM_ONAY_KUTULARI.append(chk_dublaj); TÜM_ONAY_ETİKETLERİ.append(lbl_dublaj)
    
    # 2. SATIR
    item_f4 = ctk.CTkFrame(chk_frame2, width=95, height=26, fg_color="transparent")
    item_f4.pack(side="left", padx=1, anchor="w")
    item_f4.pack_propagate(False)
    chk_altyazi = ctk.CTkCheckBox(item_f4, text="", width=18, variable=vars["altyazi"], onvalue="Evet", offvalue="Hayır")
    lbl_altyazi = ctk.CTkLabel(item_f4, text="📝 Altyazı", font=ctk.CTkFont(size=10))
    chk_altyazi.configure(command=lambda: on_check_click(lbl_altyazi, vars["altyazi"]))
    chk_altyazi.pack(side="left", anchor="w"); lbl_altyazi.pack(side="left", padx=2, anchor="w")
    TÜM_ONAY_KUTULARI.append(chk_altyazi); TÜM_ONAY_ETİKETLERİ.append(lbl_altyazi)

    item_f5 = ctk.CTkFrame(chk_frame2, width=95, height=26, fg_color="transparent")
    item_f5.pack(side="left", padx=1, anchor="w")
    item_f5.pack_propagate(False)
    chk_anonim = ctk.CTkCheckBox(item_f5, text="", width=18, variable=vars["anonim"], onvalue="Evet", offvalue="Hayır")
    lbl_anonim = ctk.CTkLabel(item_f5, text="👤 Anonim", font=ctk.CTkFont(size=10))
    chk_anonim.configure(command=lambda: on_check_click(lbl_anonim, vars["anonim"]))
    chk_anonim.pack(side="left", anchor="w"); lbl_anonim.pack(side="left", padx=2, anchor="w")
    TÜM_ONAY_KUTULARI.append(chk_anonim); TÜM_ONAY_ETİKETLERİ.append(lbl_anonim)
    
    item_f6 = ctk.CTkFrame(chk_frame2, width=95, height=26, fg_color="transparent")
    item_f6.pack(side="left", padx=1, anchor="w")
    item_f6.pack_propagate(False)
    chk_3d = ctk.CTkCheckBox(item_f6, text="", width=18, variable=vars["3d"], onvalue="Evet", offvalue="Hayır")
    lbl_3d = ctk.CTkLabel(item_f6, text="🕶️ 3D", font=ctk.CTkFont(size=10))
    chk_3d.configure(command=lambda: on_check_click(lbl_3d, vars["3d"]))
    chk_3d.pack(side="left", anchor="w"); lbl_3d.pack(side="left", padx=2, anchor="w")
    TÜM_ONAY_KUTULARI.append(chk_3d); TÜM_ONAY_ETİKETLERİ.append(lbl_3d)
    
    return vars
