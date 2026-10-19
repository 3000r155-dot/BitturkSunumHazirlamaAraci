import customtkinter as ctk
import webbrowser
from tkinter import filedialog, messagebox
import json
import re
from playwright.sync_api import sync_playwright
import ayarlar
import requests
from PIL import Image, ImageTk
import io
import threading
from concurrent.futures import ThreadPoolExecutor
import app_icons

# 🚨 KESİN KİLİT: Orijinal kararlı listeniz parantezleri kapatılarak mühürlenmiştir! 🚨
TÜM_GİRDİLER = []
TÜM_ONAY_KUTULARI = []
TÜM_ONAY_ETİKETLERİ = []
ANA_YÜKLEME_GÖSTERGESI = None
ANALOG_PROGRESS_BAR = None
BBCODE_RENKLANDIRME_TIMER = None
ANA_PENCERE_REF = None

def create_layout_structure(parent):
    global ANA_YÜKLEME_GÖSTERGESI, ANALOG_PROGRESS_BAR, ANA_PENCERE_REF
    ANA_PENCERE_REF = parent.winfo_toplevel()
    # --- SOL PANEL: FORM GİRİŞ ALANI ---
    sol_frame = ctk.CTkFrame(parent, width=350, fg_color="transparent")
    sol_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10)
    sol_frame.pack_propagate(False)

    # --- SAĞ PANEL: SAF BBCODE ÇIKTI ALANI ---
    sag_frame = ctk.CTkFrame(parent, fg_color="transparent")
    sag_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    bbcode_container = ctk.CTkFrame(sag_frame, border_width=1, border_color=["#D1D5DB", "#43474B"])
    bbcode_container.pack(fill="both", expand=True, pady=(0, 4))
    
    lbl_bbcode_title = ctk.CTkLabel(bbcode_container, text="Üretilen Saf BBCode Çıktısı", image=app_icons.get_icon("output", 17), compound="left", font=ctk.CTkFont(size=12, weight="bold"), text_color=["#4B5563", "#9CA3AF"])
    lbl_bbcode_title.pack(anchor="w", pady=(6, 2), padx=6)
    txt_output = ctk.CTkTextbox(bbcode_container, font=ctk.CTkFont(family="Courier", size=13), fg_color="transparent")
    txt_output.pack(padx=8, pady=(2, 8), fill="both", expand=True)

    # ANA EKRANDA %100 EN ÜSTTE BELİRECEK HAREKETLİ PANEL GÖSTERGESİ
    ANA_YÜKLEME_GÖSTERGESI = ctk.CTkFrame(ANA_PENCERE_REF, fg_color=["#EAEAEA", "#1E1E1E"], corner_radius=10, border_width=2, border_color="#1F6AA5")
    
    lbl_ana_load = ctk.CTkLabel(ANA_YÜKLEME_GÖSTERGESI, text="Görsel Sunucuya Yükleniyor...", image=app_icons.get_icon("loading", 18), compound="left", font=ctk.CTkFont(size=13, weight="bold"))
    lbl_ana_load.pack(padx=40, pady=(20, 10))
    
    ANALOG_PROGRESS_BAR = ctk.CTkProgressBar(ANA_YÜKLEME_GÖSTERGESI, width=220, mode="indefinite", progress_color="#1F6AA5")
    ANALOG_PROGRESS_BAR.pack(padx=40, pady=(0, 20))

    txt_output._textbox.tag_configure("center", justify="center")
    # 🚨 MODERN RENK PALETİ: Daha göz alıcı ve profesyonel renkler 🚨
    txt_output._textbox.tag_configure("serit_resim", foreground="#FF6B35", font=ctk.CTkFont(family="Courier", size=13, weight="bold"))
    txt_output._textbox.tag_configure("dil_resim", foreground="#00C853")
    txt_output._textbox.tag_configure("bbcode_tag", foreground="#7C3AED", font=ctk.CTkFont(family="Courier", size=13, weight="bold"))
    txt_output._textbox.tag_configure("bbcode_url", foreground="#0891B2", font=ctk.CTkFont(family="Courier", size=13))
    txt_output._textbox.tag_configure("bbcode_bold", foreground="#DC2626", font=ctk.CTkFont(family="Courier", size=13, weight="bold"))
    txt_output._textbox.tag_configure("bbcode_italic", foreground="#9333EA", font=ctk.CTkFont(family="Courier", size=13, slant="italic"))
    def bbcode_renklendir_tetikleyici(event=None):
        global BBCODE_RENKLANDIRME_TIMER
        if BBCODE_RENKLANDIRME_TIMER is not None:
            try:
                ANA_PENCERE_REF.after_cancel(BBCODE_RENKLANDIRME_TIMER)
            except:
                pass
        
        def delayed_renklendir():
            global BBCODE_RENKLANDIRME_TIMER
            BBCODE_RENKLANDIRME_TIMER = None
            content = txt_output.get("1.0", "end-1c")
            txt_output._textbox.tag_remove("bbcode_tag", "1.0", "end")
            txt_output._textbox.tag_remove("bbcode_url", "1.0", "end")
            txt_output._textbox.tag_remove("serit_resim", "1.0", "end")
            txt_output._textbox.tag_remove("bbcode_bold", "1.0", "end")
            txt_output._textbox.tag_remove("bbcode_italic", "1.0", "end")
            
            # BBCode etiketleri
            for match in re.finditer(r'\[\/?[a-zA-Z0-9\=\#\s\:\/\.\-\_\?\&\=\%\+\,\;\!\@\^\*\(\)]+\]', content):
                txt_output._textbox.tag_add("bbcode_tag", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
                
            # URL'ler
            for match in re.finditer(r'https?://[^\s\[\]]+', content):
                txt_output._textbox.tag_add("bbcode_url", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

            # Resim etiketleri
            for match in re.finditer(r'\[img\]https?://[^\s\[\]]+\[/img\]', content, re.IGNORECASE):
                txt_output._textbox.tag_add("serit_resim", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            
            # Bold etiketleri
            for match in re.finditer(r'\[b\].*?\[/b\]', content, re.IGNORECASE):
                txt_output._textbox.tag_add("bbcode_bold", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            
            # Italic etiketleri
            for match in re.finditer(r'\[i\].*?\[/i\]', content, re.IGNORECASE):
                txt_output._textbox.tag_add("bbcode_italic", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
        
        BBCODE_RENKLANDIRME_TIMER = ANA_PENCERE_REF.after(150, delayed_renklendir)

    def sarmalanmis_insert(index, text, *args):
        txt_output._textbox._original_insert(index, text, *args)
        bbcode_renklendir_tetikleyici()
    txt_output._textbox._original_insert = txt_output._textbox.insert
    txt_output._textbox.insert = sarmalanmis_insert
    txt_output.bind("<KeyRelease>", bbcode_renklendir_tetikleyici)
    txt_output.bbcode_renklendir = bbcode_renklendir_tetikleyici
    
    return sol_frame, txt_output, sag_frame

def tam_otomatik_imgbb_yukle_worker(girdi_kutusu, update_callback, dosya_yolu):
    """Playwright otomasyon mekanizması üzerinden saf kaynak ayıklayan arka plan işçisi."""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["image", "stylesheet", "font", "media"] else route.continue_())
            page.goto("https://imgbb.com", wait_until="domcontentloaded")
            page.wait_for_selector('li[data-action="top-bar-upload"]', timeout=10000)
            page.click('li[data-action="top-bar-upload"]')
            page.set_input_files('input[type="file"]', dosya_yolu)
            page.wait_for_selector('button[data-action="upload"]', state="visible", timeout=10000)
            page.click('button[data-action="upload"]')
            page.wait_for_selector('select[id="uploaded-embed-toggle"]', state="visible", timeout=20000)
            page.select_option('select[id="uploaded-embed-toggle"]', value="viewer-links")
            link = page.locator('#uploaded-embed-code-0').input_value()
            browser.close()
            
            # 🚨 DÜZELTME: KUTUNUN İÇİNE ARTIK [img] DEĞİL SADECE SAF WEB LİNKİ BASILARAK KISIRDÖNGÜ KIRILDI 🚨
            if link and "ibb.co" in link:
                def arayüze_yaz():
                    if isinstance(girdi_kutusu, ctk.CTkTextbox):
                        girdi_kutusu.delete("1.0", "end")
                        girdi_kutusu.insert("1.0", link.strip())
                    else:
                        girdi_kutusu.delete(0, 'end')
                        girdi_kutusu.insert(0, link.strip())
                    if hasattr(girdi_kutusu, "renk_tazeleyici"): girdi_kutusu.renk_tazeleyici()
                    if update_callback: update_callback()
                if ANA_YÜKLEME_GÖSTERGESI:
                    ANA_YÜKLEME_GÖSTERGESI.after(10, arayüze_yaz)
    except Exception as e:
        if ANA_YÜKLEME_GÖSTERGESI:
            ANA_YÜKLEME_GÖSTERGESI.after(10, lambda: messagebox.showerror("Hata", f"Otomatik yükleme motorunda hata oluştu:\n{str(e)}"))
    finally:
        if ANA_YÜKLEME_GÖSTERGESI:
            def paneli_kapat():
                if ANALOG_PROGRESS_BAR: ANALOG_PROGRESS_BAR.stop()
                ANA_YÜKLEME_GÖSTERGESI.place_forget()
            ANA_YÜKLEME_GÖSTERGESI.after(10, paneli_kapat)

def tam_otomatik_imgbb_yukle(girdi_kutusu, update_callback):
    """Ana ekran üzerinde kilitleri çözen asenkron tetikleyici."""
    dosya_yolu = filedialog.askopenfilename(title="Yüklenecek Görseli Seçin", filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if not dosya_yolu: return
    
    if ANA_YÜKLEME_GÖSTERGESI:
        ANA_YÜKLEME_GÖSTERGESI.place(relx=0.5, rely=0.5, anchor="center")
        ANA_YÜKLEME_GÖSTERGESI.lift()
        if ANALOG_PROGRESS_BAR: ANALOG_PROGRESS_BAR.start()
        ANA_YÜKLEME_GÖSTERGESI.update()
        
    threading.Thread(target=tam_otomatik_imgbb_yukle_worker, args=(girdi_kutusu, update_callback, dosya_yolu), daemon=True).start()

def ekle_alt_butonlar(app_instance, parent, txt_output, temizle_func, kaydet_func, yukle_func):
    buton_container = ctk.CTkFrame(parent, border_width=1, border_color=["#D1D5DB", "#43474B"])
    buton_container.pack(side="top", fill="x", pady=(4, 5), padx=0, expand=False)
    lbl_btn_title = ctk.CTkLabel(buton_container, text="Sunum İşlemleri & Taslak Yönetimi", image=app_icons.get_icon("tools", 16), compound="left", font=ctk.CTkFont(size=11, weight="bold"), text_color=["#4B5563", "#9CA3AF"])
    lbl_btn_title.pack(anchor="w", pady=(4, 1), padx=4)
    btn_frame = ctk.CTkFrame(buton_container, fg_color="transparent")
    btn_frame.pack(fill="x", pady=(2, 6), padx=6)
    
    def zincirleme_temizle():
        temizle_func()
        varsayilan_fg = ["#F9F9FA", "#343638"] if ctk.get_appearance_mode() == "Dark" else ["#F9F9FA", "#F9F9FA"]
        for girdi_obj in TÜM_GİRDİLER:
            try: girdi_obj.configure(fg_color=varsayilan_fg, text_color=["#000000", "#FFFFFF"])
            except Exception: pass
        for chk_obj in TÜM_ONAY_KUTULARI:
            try: chk_obj.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            except Exception: pass
        if hasattr(txt_output, "bbcode_renklendir"): txt_output.bbcode_renklendir()

    def kopyala_panoya():
        app_instance.clipboard_clear()
        app_instance.clipboard_append(txt_output.get("1.0", "end-1c"))

    actions = [
        ("Temizle", "clear", zincirleme_temizle),
        ("Kopyala", "copy", kopyala_panoya),
        ("Kaydet", "save", kaydet_func),
        ("Yükle", "load", yukle_func),
        ("Yükleme Sayfasına Git", "upload", lambda: webbrowser.open(ayarlar.MUHURLU_URL_DEPOLOSU["YUKLEME_SAYFASI"])),
    ]
    for text, icon_name, command in actions:
        button = ctk.CTkButton(
            btn_frame,
            text=text,
            image=app_icons.get_icon(icon_name, 16),
            compound="left",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=32,
            command=command,
            fg_color="green" if text == "Yükleme Sayfasına Git" else None,
        )
        button.pack(side="left", fill="both", expand=True, padx=2)

def ekle_girdi(parent, label_text, is_textbox=False, height=60, has_upload=False, ornek="", update_callback=None):
    tekli_container = ctk.CTkFrame(parent, border_width=1, border_color=["#E5E7EB", "#374151"], fg_color="transparent")
    tekli_container.pack(fill="x", pady=3, padx=2)
    icon_by_label = (
        ("Afiş", "poster"), ("Ekran", "screenshot"), ("Detay", "details"), ("Oyuncu", "cast"),
        ("Konu", "synopsis"), ("Tanıtım", "promo"), ("Fragman", "play"), ("Albüm", "album"),
        ("Parça", "music"), ("Sistem", "settings"), ("NFO", "document"), ("Info", "document"),
        ("Sunum", "film"), ("Film", "film"), ("Dizi", "series"), ("Oyun", "game"),
        ("Adı", "title"),
    )
    icon_name = next((name for keyword, name in icon_by_label if keyword.casefold() in label_text.casefold()), "edit")
    lbl = ctk.CTkLabel(tekli_container, text=label_text, image=app_icons.get_icon(icon_name, 15), compound="left", font=ctk.CTkFont(size=11, weight="bold"), anchor="w")
    lbl.pack(fill="x", pady=(3, 1), padx=4)
    varsayilan_fg = ["#F9F9FA", "#343638"] if ctk.get_appearance_mode() == "Dark" else ["#F9F9FA", "#F9F9FA"]

    def girdi_renk_guncelle(girdi_obj):
        try:
            veri = girdi_obj.get("1.0", "end-1c") if is_textbox else girdi_obj.get()
            if len(veri.strip()) > 0 and veri.strip() != ornek.strip():
                girdi_obj.configure(fg_color="#A2E8A2", text_color="#000000")
            else:
                girdi_obj.configure(fg_color=varsayilan_fg, text_color=["#000000", "#FFFFFF"])
        except Exception: pass

    def sarmalanmis_callback(event=None, girdi_obj=None):
        if girdi_obj: girdi_renk_guncelle(girdi_obj)
        if update_callback: update_callback()

    if is_textbox:
        girdi = ctk.CTkTextbox(tekli_container, height=height, font=ctk.CTkFont(size=11))
        girdi.pack(fill="x", pady=(1, 4), padx=6)
    else:
        if has_upload:
            f = ctk.CTkFrame(tekli_container, fg_color="transparent")
            f.pack(fill="x", pady=(1, 4), padx=6)
            girdi = ctk.CTkEntry(f, placeholder_text=ornek, font=ctk.CTkFont(size=11))
            girdi.pack(side="left", fill="x", expand=True, padx=(0, 4))
            btn = ctk.CTkButton(f, text="Yükle", image=app_icons.get_icon("upload", 14), compound="left", width=76, height=24, command=lambda: tam_otomatik_imgbb_yukle(girdi, lambda: sarmalanmis_callback(None, girdi)))
            btn.pack(side="right")
        else:
            girdi = ctk.CTkEntry(tekli_container, placeholder_text=ornek, font=ctk.CTkFont(size=11))
            girdi.pack(fill="x", pady=(1, 4), padx=6)

    girdi.bind("<KeyRelease>", lambda event: sarmalanmis_callback(event, girdi))
    girdi.renk_tazeleyici = lambda: girdi_renk_guncelle(girdi)
    TÜM_GİRDİLER.append(girdi)
    return girdi

def ekle_medya_onay_kutulari(parent, update_callback=None):
    group_box = ctk.CTkFrame(parent, border_width=1, border_color=["#D1D5DB", "#43474B"])
    group_box.pack(fill="x", pady=5, padx=2)
    f1 = ctk.CTkFrame(group_box, fg_color="transparent"); f1.pack(fill="x", pady=2, padx=6)
    f2 = ctk.CTkFrame(group_box, fg_color="transparent"); f2.pack(fill="x", pady=(2, 6), padx=6)
    vars = {"orjinal": ctk.StringVar(value="Hayır"), "cift": ctk.StringVar(value="Hayır"), "dublaj": ctk.StringVar(value="Hayır"), "altyazi": ctk.StringVar(value="Hayır"), "anonim": ctk.StringVar(value="Hayır"), "3d": ctk.StringVar(value="Hayır")}
    def on_check_click(l_o, s_v): l_o.configure(text_color="#107C41" if s_v.get() == "Evet" else ["#000000", "#FFFFFF"]); update_callback() if update_callback else None

    for idx, (k, l, icon_name) in enumerate([("orjinal", "Orijinal", "website"), ("cift", "Çift Dil", "dual_audio"), ("dublaj", "Dublaj", "turkish_flag")]):
        item = ctk.CTkFrame(f1, width=95, height=26, fg_color="transparent"); item.pack(side="left", padx=1); item.pack_propagate(False)
        chk = ctk.CTkCheckBox(item, text="", width=18, variable=vars[k], onvalue="Evet", offvalue="Hayır")
        lbl = ctk.CTkLabel(item, text=l, image=app_icons.get_icon(icon_name, 13), compound="left", font=ctk.CTkFont(size=10))
        chk.configure(command=lambda c=chk, _l=lbl, v=vars[k]: on_check_click(_l, v))
        chk.pack(side="left"); lbl.pack(side="left", padx=2); TÜM_ONAY_KUTULARI.append(chk)
    for idx, (k, l, icon_name) in enumerate([("altyazi", "Altyazı", "synopsis"), ("anonim", "Anonim", "anonymous"), ("3d", "3D", "3d")]):
        item = ctk.CTkFrame(f2, width=95, height=26, fg_color="transparent"); item.pack(side="left", padx=1); item.pack_propagate(False)
        chk = ctk.CTkCheckBox(item, text="", width=18, variable=vars[k], onvalue="Evet", offvalue="Hayır")
        lbl = ctk.CTkLabel(item, text=l, image=app_icons.get_icon(icon_name, 13), compound="left", font=ctk.CTkFont(size=10))
        chk.configure(command=lambda c=chk, _l=lbl, v=vars[k]: on_check_click(_l, v))
        chk.pack(side="left"); lbl.pack(side="left", padx=2); TÜM_ONAY_KUTULARI.append(chk)
    return vars

class YardimPenceresi(ctk.CTkToplevel):
    def __init__(self, master=None, widget_haritasi=None):
        super().__init__(master)
        self.title("BiTTuRK.NeT Yardım")
        self.geometry("620x420")
        self.minsize(520, 300)
        self.transient(master)
        self.grab_set()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        panel = ctk.CTkScrollableFrame(self, corner_radius=12)
        panel.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(
            panel,
            text="Yardım ve kullanım notları",
            image=app_icons.get_icon("help_notes", 20),
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 12), padx=10)

        bilgi = """
Kullanım adımları:
• Sol panelde verileri doldurun.
• Görsel yükleme alanlarındaki Yükle düğmesiyle resim bağlantısı alabilirsiniz.
• Sağ panelde oluşan BBCode çıktısını kopyalayıp forum / sunum alanına yapıştırabilirsiniz.
• 'Kaydet' ile taslağı .txt dosyası olarak saklayın, 'Yükle' ile geri açın.
• 'Temizle' ile formu sıfırlayabilirsiniz.

Not:
Bu yardım penceresi, proje içinde hazırlanan BBCode oluşturma akışını anlatır.
Bu pencere açıldığında formu kullanmaya devam edebilirsiniz.
        """.strip()

        ctk.CTkLabel(
            panel,
            text=bilgi,
            font=ctk.CTkFont(size=12),
            justify="left",
            wraplength=560,
            anchor="w",
        ).pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            panel,
            text="Kapat",
            image=app_icons.get_icon("close", 16),
            compound="left",
            command=self.destroy,
            width=120,
            height=32,
        ).pack(pady=(8, 10))
