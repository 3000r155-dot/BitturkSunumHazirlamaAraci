import customtkinter as ctk
import webbrowser
from tkinter import filedialog
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
PREMIUM_ONAY_KUTULARI = []
PREMIUM_ONAY_AKTIF = False
ANA_YÜKLEME_GÖSTERGESI = None
ANALOG_PROGRESS_BAR = None
BBCODE_RENKLANDIRME_TIMER = None
ANA_PENCERE_REF = None

def premium_ozelliklerini_kilitle():
    global PREMIUM_ONAY_AKTIF
    PREMIUM_ONAY_AKTIF = False
    PREMIUM_ONAY_KUTULARI.clear()


def premium_ozelliklerini_ac():
    global PREMIUM_ONAY_AKTIF
    PREMIUM_ONAY_AKTIF = True
    for checkbox in PREMIUM_ONAY_KUTULARI:
        try:
            checkbox.configure(state="normal")
        except Exception:
            pass


def show_themed_message(parent, title, message, level="warning"):
    app_window = parent.winfo_toplevel()
    dialog = ctk.CTkToplevel(app_window)
    dialog.withdraw()
    dialog.title(title)
    dialog.transient(parent)
    dialog.resizable(False, False)
    app_icon = getattr(app_window, "_window_icon", None)
    if app_icon is not None:
        dialog.iconphoto(True, app_icon)
    icon_ico = getattr(app_window, "_window_icon_ico", None)
    if icon_ico is not None:
        dialog.iconbitmap(str(icon_ico))

    accent = "#C47A00" if level == "warning" else "#C23B3B"
    panel = ctk.CTkFrame(
        dialog,
        fg_color=["#F8FAFC", "#202833"],
        border_color=[accent, accent],
        border_width=1,
        corner_radius=10,
    )
    panel.pack(fill="both", expand=True, padx=12, pady=12)
    ctk.CTkLabel(
        panel,
        text=title,
        image=app_icons.get_app_icon(22),
        compound="left",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=[accent, "#F2C879" if level == "warning" else "#F29B9B"],
        anchor="w",
    ).pack(fill="x", padx=14, pady=(12, 6))
    ctk.CTkLabel(
        panel,
        text=message,
        justify="left",
        anchor="w",
        wraplength=390,
        font=ctk.CTkFont(size=12),
    ).pack(fill="x", padx=14, pady=(0, 12))
    ctk.CTkButton(
        panel,
        text="Tamam",
        width=96,
        height=30,
        command=dialog.destroy,
    ).pack(anchor="e", padx=14, pady=(0, 12))
    dialog.bind("<Escape>", lambda event: dialog.destroy())
    dialog.bind("<Return>", lambda event: dialog.destroy())

    dialog.update_idletasks()
    width = max(340, min(dialog.winfo_reqwidth(), 500))
    height = dialog.winfo_reqheight()
    parent.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
    x = max(8, min(x, dialog.winfo_screenwidth() - width - 8))
    y = max(8, min(y, dialog.winfo_screenheight() - height - 8))
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    dialog.deiconify()
    dialog.update_idletasks()
    decoration_x = dialog.winfo_rootx() - x
    decoration_y = dialog.winfo_rooty() - y
    x -= decoration_x
    y -= decoration_y
    dialog.geometry(f"{width}x{height}+{x}+{y}")
    dialog.update_idletasks()
    dialog.lift()
    dialog.grab_set()
    dialog.focus_force()
    dialog.wait_window()


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
            # Sistem Chrome veya Edge kullan
            try:
                browser = p.chromium.launch(channel="chrome", headless=True)
            except:
                try:
                    browser = p.chromium.launch(channel="msedge", headless=True)
                except:
                    # İkisi de yoksa bundled chromium kullan
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
            hata_metni = str(e)
            ANA_YÜKLEME_GÖSTERGESI.after(
                10,
                lambda text=hata_metni: show_themed_message(
                    ANA_PENCERE_REF,
                    "Görsel Yükleme Hatası",
                    f"Otomatik yükleme motorunda hata oluştu:\n{text}",
                    level="error",
                ),
            )
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

def ekle_medya_onay_kutulari(parent, update_callback=None, visible_options=None, label_overrides=None, option_rows=None):
    group_box = ctk.CTkFrame(parent, border_width=1, border_color=["#D1D5DB", "#43474B"])
    group_box.pack(fill="x", pady=5, padx=2)
    f1 = ctk.CTkFrame(group_box, fg_color="transparent"); f1.pack(fill="x", pady=2, padx=6)
    f2 = ctk.CTkFrame(group_box, fg_color="transparent"); f2.pack(fill="x", pady=(2, 6), padx=6)
    f3 = ctk.CTkFrame(group_box, fg_color="transparent"); f3.pack(fill="x", pady=(0, 5), padx=6)
    vars = {"orjinal": ctk.StringVar(value="Hayır"), "cift": ctk.StringVar(value="Hayır"), "dublaj": ctk.StringVar(value="Hayır"), "altyazi": ctk.StringVar(value="Hayır"), "anonim": ctk.StringVar(value="Hayır"), "3d": ctk.StringVar(value="Hayır"), "altin": ctk.StringVar(value="Hayır"), "gumus": ctk.StringVar(value="Hayır"), "x2": ctk.StringVar(value="Hayır")}
    visible_options = set(visible_options) if visible_options is not None else None
    label_overrides = label_overrides or {}
    option_metadata = {
        "orjinal": ("Orijinal", "website", False),
        "cift": ("Çift Dil", "dual_audio", False),
        "dublaj": ("Dublaj", "turkish_flag", False),
        "altyazi": ("Altyazı", "synopsis", False),
        "anonim": ("Anonim", "anonymous", False),
        "3d": ("3D", "3d", False),
        "altin": ("Altın", "vip", True),
        "gumus": ("Gümüş", "vip", True),
        "x2": ("2x Sunum", "vip", True),
    }
    option_rows = option_rows or (
        ("orjinal", "cift", "dublaj"),
        ("altyazi", "anonim", "3d"),
        ("altin", "gumus", "x2"),
    )
    row_frames = (f1, f2, f3)

    def on_check_click(label, value, key):
        if value.get() == "Evet":
            if key in {"orjinal", "cift", "dublaj"}:
                exclusive_keys = {"orjinal", "cift", "dublaj"} - {key}
                warning = "Orijinal Dil, Çift Dil ve Dublaj seçeneklerinden yalnızca biri seçilebilir."
            elif key in {"altin", "gumus"}:
                exclusive_keys = {"altin", "gumus"} - {key}
                warning = "Altın ve Gümüş rozetlerinden yalnızca biri seçilebilir."
            else:
                exclusive_keys = set()
                warning = ""

            if any(vars[other_key].get() == "Evet" for other_key in exclusive_keys):
                value.set("Hayır")
                label.configure(text_color=["#000000", "#FFFFFF"])
                show_themed_message(
                    ANA_PENCERE_REF,
                    "Seçim Uyarısı",
                    warning,
                    level="warning",
                )
                return

        label.configure(text_color="#107C41" if value.get() == "Evet" else ["#000000", "#FFFFFF"])
        if update_callback:
            update_callback()

    for row_index, option_keys in enumerate(option_rows):
        for key in option_keys:
            if visible_options is not None and key not in visible_options:
                continue

            default_label, icon_name, is_premium = option_metadata[key]
            item = ctk.CTkFrame(row_frames[row_index], width=95, height=26, fg_color="transparent")
            item.pack(side="left", padx=1)
            item.pack_propagate(False)
            checkbox = ctk.CTkCheckBox(item, text="", width=18, variable=vars[key], onvalue="Evet", offvalue="Hayır")
            label = ctk.CTkLabel(
                item,
                text=label_overrides.get(key, default_label),
                image=app_icons.get_icon(icon_name, 13),
                compound="left",
                font=ctk.CTkFont(size=10),
            )
            checkbox.configure(command=lambda lbl=label, value=vars[key], option=key: on_check_click(lbl, value, option))
            if is_premium:
                if not PREMIUM_ONAY_AKTIF:
                    checkbox.configure(state="disabled")
                PREMIUM_ONAY_KUTULARI.append(checkbox)
            checkbox.pack(side="left")
            label.pack(side="left", padx=2)
            TÜM_ONAY_KUTULARI.append(checkbox)
    return vars

class YardimPenceresi(ctk.CTkToplevel):
    def __init__(self, master=None, widget_haritasi=None):
        super().__init__(master)
        self.title("❓ BiTTuRK.NeT Yardım")
        self.geometry("1260x880")
        self.transient(master)
        self.resizable(False, False)

        # Pencere ikonunu ayarla
        app_window = master.winfo_toplevel()
        app_icon = getattr(app_window, "_window_icon", None)
        if app_icon is not None:
            self.iconphoto(True, app_icon)
        icon_ico = getattr(app_window, "_window_icon_ico", None)
        if icon_ico is not None:
            self.iconbitmap(str(icon_ico))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        heading = ctk.CTkLabel(
            self,
            text="Yardım ve kullanım kılavuzu",
            image=app_icons.get_icon("help_notes", 22),
            compound="left",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w",
        )
        heading.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 8))

        pages = ctk.CTkTabview(self, corner_radius=8)
        pages.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        pages.add("Kullanım")
        pages.add("Özellikler")
        pages.add("Windows")
        pages.add("macOS")
        pages.add("Linux")

        # Sekmelere simge ekle
        sekme_simgeleri = {
            "Kullanım": "help",
            "Özellikler": "tools",
            "Windows": "settings",
            "macOS": "vip",
            "Linux": "settings",
        }
        for sekme_adi, simge_adi in sekme_simgeleri.items():
            pages._segmented_button._buttons_dict[sekme_adi].configure(
                image=app_icons.get_icon(simge_adi, 18),
                compound="left",
            )

        def add_sections(tab_name, sections):
            content_frame = ctk.CTkFrame(pages.tab(tab_name), fg_color="transparent")
            content_frame.pack(fill="both", expand=True, padx=8, pady=8)
            for section_title, section_text, icon_name in sections:
                section_container = ctk.CTkFrame(content_frame, border_width=1, border_color=["#D1D5DB", "#43474B"], corner_radius=8)
                section_container.pack(fill="x", padx=8, pady=(10, 4))
                header_frame = ctk.CTkFrame(section_container, fg_color=["#F3F4F6", "#2D3748"], corner_radius=8)
                header_frame.pack(fill="x", padx=1, pady=(1, 1))
                ctk.CTkLabel(
                    header_frame,
                    text=section_title,
                    image=app_icons.get_icon(icon_name, 16),
                    compound="left",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w",
                ).pack(fill="x", padx=12, pady=8)
                content_text_frame = ctk.CTkFrame(section_container, fg_color="transparent")
                content_text_frame.pack(fill="x", padx=12, pady=(0, 12))
                ctk.CTkLabel(
                    content_text_frame,
                    text=section_text,
                    font=ctk.CTkFont(size=12),
                    justify="left",
                    wraplength=1100,
                    anchor="w",
                ).pack(fill="x", padx=0, pady=0)

        add_sections("Kullanım", [
            ("Başlangıç", "Üstteki Film, Dizi, Müzik, Oyun ve Diğer sekmelerinden içerik türünü seçin. Alanları doldurdukça BBCode çıktısı sağ tarafta otomatik güncellenir.", "edit"),
            ("Örnek metinler", "Gri görünen örnek metinler yer tutucudur; değiştirilmedikleri sürece sunum çıktısına eklenmez. Metin alanına odaklanıp kendi içeriğinizi yazın.", "edit"),
            ("Görsel yükleme", "Bir görsel alanındaki Yükle düğmesine basıp dosya seçin. Uygulama Playwright Chromium üzerinden görseli ImgBB'ye yükler ve dönen bağlantıyı ilgili alana yerleştirir. Bu işlem internet bağlantısı gerektirir.", "upload"),
            ("Çıktı ve taslak", "Kopyala düğmesi BBCode'u panoya alır. Kaydet, etkin sekmenin taslağını .txt dosyasına yazar; Yükle daha önce kaydedilmiş taslağı geri getirir. Temizle etkin sekmenin alanlarını sıfırlar.", "save"),
            ("BitTurk sayfası", "Yükleme Sayfasına Git düğmesi BitTurk yükleme sayfasını varsayılan tarayıcıda açar. Site hesabı girişi tarayıcıda yapılır; uygulama parolanızı almaz veya kaydetmez.", "website"),
            ("Medya seçenekleri", "Orijinal, Çift Dil ve Dublaj/Türkçe seçeneklerinden yalnızca biri seçilebilir. Altın ve Gümüş rozetleri de birbirini dışlar. 3D, Anonim ve 2X Sunum bağımsız seçeneklerdir. Premium rozetleri kilit açılana kadar devre dışıdır.", "settings"),
            ("Tema", "Tema düğmesi açık ve koyu görünüm arasında geçiş yapar.", "moon"),
        ])

        add_sections("Özellikler", [
            ("Film", "Film adı, afiş, teknik detay görseli, oyuncu görseli, konu, YouTube fragmanı, NFO/Info ve medya rozetleriyle forum BBCode'u oluşturur.", "film"),
            ("Dizi", "Dizi adı, sezon/yayın bilgisi, görseller, konu, fragman, NFO/Info ve medya rozetleri için şablon üretir.", "series"),
            ("Müzik", "Albüm adı, kapak, ses teknik bilgileri ve parça listesini kullanır. Checkbox satırları: Orijinal, Türkçe, Anonim; Altın, Gümüş, 2X Sunum.", "music"),
            ("Oyun ve Diğer", "Oyun veya yazılım adı, afiş, tanıtım, fragman, minimum sistem gereksinimleri, NFO/Info ve medya rozetleriyle sunum hazırlar.", "game"),
            ("Premium ve VIP", "Premium Kilidi eski BTRG erişim parolasıyla açılır. Kilit açılınca Altın, Gümüş, 2X seçenekleri etkinleşir ve VIP sekmesi görünür. VIP çıktısında XXX rozeti, sabit ekran görüntüsü rozeti, girilen ekran bağlantısına tıklanabilir metin, uyarı notu ve BTRG kaynak rozeti bulunur.", "vip"),
            ("Görsel hizmetleri", "Alanlardaki otomatik görsel yükleme ImgBB'yi kullanır. BitTurk yükleme sayfası ise tarayıcıda açılır; bu iki işlem birbirinden ayrıdır.", "website"),
        ])

        add_sections("Windows", [
            ("Kurulum", "BiTTuRK.NeT Sunum Hazırlama Aracı, Windows için çalıştırılabilir .exe dosyası olarak dağıtılır. İndirdiğiniz .exe dosyasını çift tıklayarak doğrudan çalıştırabilirsiniz. Python kurulumu gerekmez.", "settings"),
            ("İlk çalıştırma", "İlk açılışta antivirüs yazılımınız bir uyarı gösterebilir. Bu, uygulamanın yeni imzalanmış olmasından kaynaklanır. Dosyayı güvenilir olarak işaretleyebilirsiniz.", "vip"),
            ("Güncelleme", "Güncel sürümü BiTTuRK.NeT sitesinden indirebilirsiniz. Eski sürümü kapatıp yeni .exe dosyasını çalıştırın.", "tools"),
            ("Sorun giderme", "Eğer uygulama açılmıyorsa, Yönetici olarak çalıştırmayı deneyin. Eğer görsel yükleme çalışmıyorsa, internet bağlantınızı kontrol edin.", "tools"),
        ])

        add_sections("macOS", [
            ("Kurulum", "BiTTuRK.NeT Sunum Hazırlama Aracı, macOS için çalıştırılabilir .app dosyası olarak dağıtılır. İndirdiğiniz .app dosyasını Uygulamalar klasörüne sürükleyip bırakın ve Dock'tan başlatın.", "vip"),
            ("Güvenlik uyarısı", "İlk açılışta macOS'un 'Güvenli olmayan uygulama' uyarısı gösterebilir. Sistem Tercihleri > Güvenlik ve Gizlilik bölümünden uygulamayı açmayı onaylayın.", "vip"),
            ("Gatekeeper", "Gatekeeper kısıtlamaları nedeniyle, uygulamayı Terminal'den 'xattr -cr /Applications/BiTTuRK.app' komutuyla karantinadan kaldırmanız gerekebilir.", "settings"),
            ("İzinler", "Görsel yükleme için internet erişimi gerekir. İlk kullanımda ağ izni istenebilir.", "website"),
        ])

        add_sections("Linux", [
            ("Kurulum", "BiTTuRK.NeT Sunum Hazırlama Aracı, Linux için çalıştırılabilir ikili dosya olarak dağıtılır. İndirdiğiniz dosyaya çalıştırma izni verin (chmod +x BiTTuRK) ve ./BiTTuRK komutuyla başlatın.", "settings"),
            ("Bağımlılıklar", "Uygulama kendi içinde tüm kütüphaneleri içerir. Ek Python kurulumu gerekmez. Sadece sistem düzeyinde temel kütüphaneler (libc, libstdc++ vb.) olmalıdır.", "details"),
            ("Sistem gereksinimleri", "64-bit Linux dağıtımı gerekir. Çoğu modern dağıtımda (Ubuntu 20.04+, Fedora 35+, Debian 11+, Arch Linux) çalışır.", "settings"),
            ("Sorun giderme", "Eğer uygulama açılmıyorsa, libstdc++6 ve diğer temel kütüphanelerin kurulu olduğunu kontrol edin. Görsel yükleme için internet bağlantısı gerekir.", "tools"),
        ])

        ctk.CTkButton(
            self,
            text="Kapat",
            image=app_icons.get_icon("close", 16),
            compound="left",
            command=self.destroy,
            width=120,
            height=32,
        ).grid(row=2, column=0, pady=(0, 12))

        # Pencereyi ekranın tam ortasına yerleştir
        self.update_idletasks()
        width = 1260
        height = 880
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.grab_set()
        self.lift()
        self.focus_force()
