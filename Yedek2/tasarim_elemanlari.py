import customtkinter as ctk
import webbrowser
from tkinter import filedialog, messagebox
import json
import re
from playwright.sync_api import sync_playwright
import ayarlar

# Resim işleme, indirme ve iş parçacığı (threading) modülleri tamamen temizlendi.
TÜM_GİRDİLER = []
TÜM_ONAY_KUTULARI = []
TÜM_ONAY_ETİKETLERİ = []
def create_layout_structure(parent):
    # --- SOL PANEL: GİRDİ FORMLARI (Genişlik sabit) ---
    sol_frame = ctk.CTkFrame(parent, width=350, fg_color="transparent")
    sol_frame.pack(side="left", fill="both", expand=False, padx=10, pady=10)
    sol_frame.pack_propagate(False)

    # --- SAĞ PANEL: TEKİL BBCODE ÇIKTI EKRANI (Önizleme kutusu tamamen kaldırıldı) ---
    sag_frame = ctk.CTkFrame(parent, fg_color="transparent")
    sag_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    bbcode_container = ctk.CTkFrame(sag_frame, border_width=1, border_color=["#D1D5DB", "#43474B"])
    bbcode_container.pack(fill="both", expand=True, pady=(0, 4))
    
    lbl_bbcode_title = ctk.CTkLabel(bbcode_container, text="  📋 Üretilen Saf BBCode Çıktısı", font=ctk.CTkFont(size=12, weight="bold"), text_color=["#4B5563", "#9CA3AF"])
    lbl_bbcode_title.pack(anchor="w", pady=(6, 2), padx=6)

    txt_output = ctk.CTkTextbox(bbcode_container, font=ctk.CTkFont(family="Courier", size=13), fg_color="transparent")
    txt_output.pack(padx=8, pady=(2, 8), fill="both", expand=True)
    # BBCode Editör Alanı İçin Sözdizimi (Syntax) Vurgulama Ayarları
    txt_output._textbox.tag_configure("center", justify="center")
    txt_output._textbox.tag_configure("serit_resim", foreground="#E41414")
    txt_output._textbox.tag_configure("dil_resim", foreground="#107C41")
    txt_output._textbox.tag_configure("bbcode_tag", foreground="#00BFFF", font=ctk.CTkFont(family="Courier", size=13, weight="bold"))
    txt_output._textbox.tag_configure("bbcode_url", foreground="#FF8C00", font=ctk.CTkFont(family="Courier", size=13))
    def bbcode_renklendir_tetikleyici(event=None):
        """Metin dökümündeki etiketleri ve linkleri canlı olarak renklendirir."""
        content = txt_output.get("1.0", "end-1c")
        txt_output._textbox.tag_remove("bbcode_tag", "1.0", "end")
        txt_output._textbox.tag_remove("bbcode_url", "1.0", "end")
        
        # Etiketleri algıla ve boya
        for match in re.finditer(r'\[\/?[a-zA-Z0-9\=\#\s\:\/\.\-\_\?\&\=\%\+\,\;\!\@\^\*\(\)]+\]', content):
            txt_output._textbox.tag_add("bbcode_tag", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
            
        # URL'leri algıla ve boya
        for match in re.finditer(r'https?://[^\s\[\]]+', content):
            txt_output._textbox.tag_add("bbcode_url", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
    def sarmalanmis_insert(index, text, *args):
        """Metin kutusuna kod eklendiğinde otomatik boyama motorunu çağırır."""
        txt_output._textbox._original_insert(index, text, *args)
        bbcode_renklendir_tetikleyici()

    txt_output._textbox._original_insert = txt_output._textbox.insert
    txt_output._textbox.insert = sarmalanmis_insert
    txt_output.bind("<KeyRelease>", bbcode_renklendir_tetikleyici)
    txt_output.bbcode_renklendir = bbcode_renklendir_tetikleyici
    
    return sol_frame, txt_output, sag_frame
def tam_otomatik_imgbb_yukle(girdi_kutusu, update_callback):
    """Playwright otomasyonu ile arka planda sadece resim linkini ayıklar, render tetiklemez."""
    dosya_yolu = filedialog.askopenfilename(title="Yüklenecek Görseli Seçin", filetypes=[("Resim Dosyaları", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if not dosya_yolu: 
        return
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            
            # Ağ trafiğini hafifletmek için gereksiz kaynakları engelliyoruz
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
            if link and "ibb.co" in link:
                if isinstance(girdi_kutusu, ctk.CTkTextbox):
                    girdi_kutusu.delete("1.0", "end")
                    girdi_kutusu.insert("1.0", link)
                else:
                    girdi_kutusu.delete(0, 'end')
                    girdi_kutusu.insert(0, link)
                
                if hasattr(girdi_kutusu, "renk_tazeleyici"): 
                    girdi_kutusu.renk_tazeleyici()
                if update_callback: 
                    update_callback()
    except Exception as e: 
        messagebox.showerror("Hata", f"Otomatik yükleme motorunda hata oluştu:\n{str(e)}")
def ekle_alt_butonlar(app_instance, parent, txt_output, temizle_func, kaydet_func, yukle_func):
    """Alt işlem butonlarını yerleştiren sadeleştirilmiş arayüz paneli."""
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
            try: girdi_obj.configure(fg_color=varsayilan_fg, text_color=["#000000", "#FFFFFF"])
            except Exception: pass
        for chk_obj in TÜM_ONAY_KUTULARI:
            try: chk_obj.configure(fg_color=["#3B8ED0", "#1F6AA5"])
            except Exception: pass
        if hasattr(txt_output, "bbcode_renklendir"): 
            txt_output.bbcode_renklendir()

    def kopyala_panoya():
        app_instance.clipboard_clear()
        app_instance.clipboard_append(txt_output.get("1.0", "end-1c"))

    ctk.CTkButton(btn_frame, text="🧹 Sunumu Temizle", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=zincirleme_temizle).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="📋 BBCode Kopyala", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=kopyala_panoya).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="💾 Taslağı Kaydet", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=kaydet_func).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="📂 Taslak Yükle", font=ctk.CTkFont(size=11, weight="bold"), height=32, command=yukle_func).pack(side="left", fill="both", expand=True, padx=3)
    ctk.CTkButton(btn_frame, text="🌐 Siteye Git", font=ctk.CTkFont(size=11, weight="bold"), height=32, fg_color="green", command=lambda: webbrowser.open(ayarlar.MUHURLU_URL_DEPOLOSU["SITEYE_GIT"])).pack(side="left", fill="both", expand=True, padx=3)
def ekle_girdi(parent, label_text, is_textbox=False, height=60, has_upload=False, ornek="", update_callback=None):
    """Veri girildiğinde kutuyu yeşile boyayan hafifletilmiş form alanı üretici."""
    tekli_container = ctk.CTkFrame(parent, border_width=1, border_color=["#E5E7EB", "#374151"], fg_color="transparent")
    tekli_container.pack(fill="x", pady=3, padx=2)
    lbl = ctk.CTkLabel(tekli_container, text=f" 📦 {label_text}", font=ctk.CTkFont(size=11, weight="bold"), anchor="w")
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
            btn = ctk.CTkButton(f, text="📤 Yükle", width=50, height=24, command=lambda: tam_otomatik_imgbb_yukle(girdi, lambda: sarmalanmis_callback(None, girdi)))
            btn.pack(side="right")
        else:
            girdi = ctk.CTkEntry(tekli_container, placeholder_text=ornek, font=ctk.CTkFont(size=11))
            girdi.pack(fill="x", pady=(1, 4), padx=6)

    girdi.bind("<KeyRelease>", lambda event: sarmalanmis_callback(event, girdi))
    girdi.renk_tazeleyici = lambda: girdi_renk_guncelle(girdi)
    TÜM_GİRDİLER.append(girdi)
    return girdi
def ekle_medya_onay_kutulari(parent, update_callback=None):
    """Dil seçeneklerini ekrana yerleştiren kompakt onay kutusu alanı."""
    group_box = ctk.CTkFrame(parent, border_width=1, border_color=["#D1D5DB", "#43474B"])
    group_box.pack(fill="x", pady=5, padx=2)
    f1 = ctk.CTkFrame(group_box, fg_color="transparent"); f1.pack(fill="x", pady=2, padx=6)
    f2 = ctk.CTkFrame(group_box, fg_color="transparent"); f2.pack(fill="x", pady=(2, 6), padx=6)
    vars = {"orjinal": ctk.StringVar(value="Hayır"), "cift": ctk.StringVar(value="Hayır"), "dublaj": ctk.StringVar(value="Hayır"), "altyazi": ctk.StringVar(value="Hayır"), "anonim": ctk.StringVar(value="Hayır"), "3d": ctk.StringVar(value="Hayır")}
    
    def on_check_click(lbl_obj, str_var):
        lbl_obj.configure(text_color="#107C41" if str_var.get() == "Evet" else ["#000000", "#FFFFFF"])
        if update_callback: update_callback()

    for idx, (k, l) in enumerate([("orjinal", "🌐 Orijinal"), ("cift", "🔄 Çift Dil"), ("dublaj", "🇹🇷 Dublaj")]):
        item = ctk.CTkFrame(f1, width=95, height=26, fg_color="transparent"); item.pack(side="left", padx=1); item.pack_propagate(False)
        chk = ctk.CTkCheckBox(item, text="", width=18, variable=vars[k], onvalue="Evet", offvalue="Hayır")
        lbl = ctk.CTkLabel(item, text=l, font=ctk.CTkFont(size=10))
        chk.configure(command=lambda c=chk, _l=lbl, v=vars[k]: on_check_click(_l, v))
        chk.pack(side="left"); lbl.pack(side="left", padx=2)
        TÜM_ONAY_KUTULARI.append(chk)
    for idx, (k, l) in enumerate([("altyazi", "📝 Altyazı"), ("anonim", "👤 Anonim"), ("3d", "🕶️ 3D")]):
        item = ctk.CTkFrame(f2, width=95, height=26, fg_color="transparent"); item.pack(side="left", padx=1); item.pack_propagate(False)
        chk = ctk.CTkCheckBox(item, text="", width=18, variable=vars[k], onvalue="Evet", offvalue="Hayır")
        lbl = ctk.CTkLabel(item, text=l, font=ctk.CTkFont(size=10))
        chk.configure(command=lambda c=chk, _l=lbl, v=vars[k]: on_check_click(_l, v))
        chk.pack(side="left"); lbl.pack(side="left", padx=2)
        TÜM_ONAY_KUTULARI.append(chk)
    return vars

class YardimPenceresi:
    def __init__(self, e, w): pass
