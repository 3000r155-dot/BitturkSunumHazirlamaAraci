import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import re

import ayarlar
import tasarim_elemanlari
import sablon_motoru
import os_optimizasyon

# Arayüz ayağa kalkmadan önce işletim sistemi DPI ve Taskbar optimizasyonlarını tetikliyoruz
os_optimizasyon.isletim_sistemi_arayuzunu_ayarla()

class BiTTuRKMuadiliApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Başlığı
        self.title("BiTTuRK.NeT Sunum Hazırlama Aracı - Python Muadili v7.5")
        
        # --- TÜM BUTONLARIN TAŞMADAN SIĞDIĞI İDEAL AÇILIŞ BOYUTU ---
        self.ideal_genislik = 1260
        self.ideal_yukseklik = 880
        
        ekran_genislik = self.winfo_screenwidth()
        ekran_yukseklik = self.winfo_screenheight()
        
        merkez_x = int((ekran_genislik / 2) - (self.ideal_genislik / 2))
        merkez_y = int((ekran_yukseklik / 2) - (self.ideal_yukseklik / 2))
        
        # İlk açılış geometrisi ve standart resizable izni (Maksimize butonu açık kalır)
        self.geometry(f"{self.ideal_genislik}x{self.ideal_yukseklik}+{merkez_x}+{merkez_y}")
        self.resizable(True, True)

        # --- SAF PYTHON EN-BOY MÜHÜR SİSTEMİ (DİNAMİK BIND) ---
        self.bind("<Configure>", self.pencere_oran_kontrolcusu)
        # Üst Panel Layout düzeni
        self.ust_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.ust_panel.pack(pady=10, fill="x")

        self.lbl_ust_baslik = ctk.CTkLabel(
            self.ust_panel, text="BiTTuRK.NeT SUNUM HAZIRLAMA PANELİ", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_ust_baslik.pack(side="left", expand=True, padx=(160, 0))

        # --- YARDIM BUTONU (MERKEZİ ERİŞİM KİLİDİ) ---
        self.btn_yardim = ctk.CTkButton(
            self.ust_panel, text="❓ Yardım", width=70, height=32,
            font=ctk.CTkFont(size=11, weight="bold"), fg_color="#D35400", hover_color="#A04000",
            command=self.yardim_panelini_ac
        )
        self.btn_yardim.pack(side="right", padx=10)

        self.btn_tema_degistir = ctk.CTkButton(
            self.ust_panel, text="🌙 Karanlık", width=70, height=32,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.gorunum_modu_tetikle
        )
        self.btn_tema_degistir.pack(side="right", padx=25)

        self.tab_control = ctk.CTkTabview(self, width=1220, height=800)
        self.tab_control.pack(padx=20, pady=10, fill="both", expand=True)

        self.tab_film = self.tab_control.add("🎬 FİLM")
        self.tab_dizi = self.tab_control.add("📺 DİZİ")
        self.tab_muzik = self.tab_control.add("🎵 MÜZİK")
        self.tab_oyun = self.tab_control.add("🎮 OYUN")
        self.tab_diger = self.tab_control.add("📦 DİĞER")
        self.tab_vip = self.tab_control.add("⭐ V.I.P")

        self.tasarla_film_sekmesi()
        self.tasarla_dizi_sekmesi()
        self.tasarla_muzik_sekmesi()
        self.tasarla_oyun_sekmesi()
        self.tasarla_diger_sekmesi()
        self.tasarla_vip_sekmesi()
    def pencere_oran_kontrolcusu(self, event):
        if event.widget != self:
            return
            
        is_maximized = self.state() == "zoomed" or self.attributes("-fullscreen")
        
        if not is_maximized:
            guncel_genislik = self.winfo_width()
            guncel_yukseklik = self.winfo_height()
            
            if guncel_genislik != self.ideal_genislik or guncel_yukseklik != self.ideal_yukseklik:
                self.geometry(f"{self.ideal_genislik}x{self.ideal_yukseklik}")

    def yardim_panelini_ac(self):
        if hasattr(self, 'aktif_widget_haritasi'):
            tasarim_elemanlari.YardimPenceresi(self, self.aktif_widget_haritasi)
        else:
            tasarim_elemanlari.YardimPenceresi(self, {})

    def gorunum_modu_tetikle(self):
        gecerli_mod = ctk.get_appearance_mode()
        if gecerli_mod == "Dark":
            ctk.set_appearance_mode("Light")
            self.btn_tema_degistir.configure(text="☀️ Aydınlık")
        else:
            ctk.set_appearance_mode("Dark")
            self.btn_tema_degistir.configure(text="🌙 Karanlık")

    def bbcode_renklendir(self, txt_widget):
        txt_widget._textbox.tag_remove("serit_resim", "1.0", "end")
        txt_widget._textbox.tag_remove("dil_resim", "1.0", "end")
        icerik = txt_widget.get("1.0", "end-1c")
        
        for p in ayarlar.DIL_PATTERNLER:
            for match in re.finditer(p, icerik):
                txt_widget._textbox.tag_add("dil_resim", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")

        for p in ayarlar.SERIT_PATTERNLER:
            for match in re.finditer(p, icerik):
                txt_widget._textbox.tag_add("serit_resim", f"1.0 + {match.start()} chars", f"1.0 + {match.end()} chars")
    def tasarla_film_sekmesi(self):
        sol, sag_txt, sag_frame = tasarim_elemanlari.create_layout_structure(self.tab_film)

        o_ad = "Inception 2010 1080p BluRay x264-FGT"
        o_afis = "https://imgur.com"
        o_detay = "https://imgur.com"
        o_oyuncu = "https://imgur.com"
        o_konu = "Dom Cobb çok yetenekli bir hırsızdır. Uzmanlık alanı, zihnin en savunmasız olduğu rüya görme anında bilinçaltından sırları çekmektir."
        o_fragman = "https://youtube.com"
        o_info = "General Information Duration : 02:28:12 Release size : 14.3 GB"

        ent_ad = tasarim_elemanlari.ekle_girdi(sol, "Film Adı", ornek=o_ad, update_callback=lambda: film_bbcode_uret())
        ent_afis = tasarim_elemanlari.ekle_girdi(sol, "Afiş (Resim Linki)", has_upload=True, ornek=o_afis, update_callback=lambda: film_bbcode_uret())
        ent_detay = tasarim_elemanlari.ekle_girdi(sol, "Detay (Resim Linki)", has_upload=True, ornek=o_detay, update_callback=lambda: film_bbcode_uret())
        ent_oyuncu = tasarim_elemanlari.ekle_girdi(sol, "Oyuncular (Resim Linki)", has_upload=True, ornek=o_oyuncu, update_callback=lambda: film_bbcode_uret())
        txt_konu = tasarim_elemanlari.ekle_girdi(sol, "Konu", is_textbox=True, height=75, ornek=o_konu, update_callback=lambda: film_bbcode_uret())
        ent_fragman = tasarim_elemanlari.ekle_girdi(sol, "Fragman (Youtube Linki)", ornek=o_fragman, update_callback=lambda: film_bbcode_uret())
        txt_info = tasarim_elemanlari.ekle_girdi(sol, "NFO / Info", is_textbox=True, height=100, ornek=o_info, update_callback=lambda: film_bbcode_uret())

        vars = tasarim_elemanlari.ekle_medya_onay_kutulari(sol, update_callback=lambda: film_bbcode_uret())

        # 🚨 KATTI STANDART: YAZI RENKLERİNİ GRİDE SABİTLEYEN VE ODAKLANINCA SİLEN PLACEHOLDER MOTORU 🚨
        def text_placeholder_ayarla(box, v_metin):
            box.delete("1.0", "end")
            box.insert("1.0", v_metin)
            box.configure(text_color="#888888")
            
            def odak_giris(event):
                current = box.get("1.0", "end-1c").strip()
                if current == v_metin.strip():
                    box.delete("1.0", "end")
                    yazi_rengi = "#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#000000"
                    box.configure(text_color=yazi_rengi)
                    
            def odak_cikis(event):
                current = box.get("1.0", "end-1c").strip()
                if not current:
                    box.insert("1.0", v_metin)
                    box.configure(text_color="#888888")
                    
            box.bind("<FocusIn>", odak_giris)
            box.bind("<FocusOut>", odak_cikis)

        text_placeholder_ayarla(txt_konu, o_konu)
        text_placeholder_ayarla(txt_info, o_info)
        def film_bbcode_uret():
            current_konu = txt_konu.get('1.0', 'end-1c').strip()
            current_info = txt_info.get('1.0', 'end-1c').strip()
            
            hk = "" if current_konu == o_konu.strip() else txt_konu.get('1.0', 'end-1c')
            hi = "" if current_info == o_info.strip() or "NFO Sekmesindedir" in current_info else txt_info.get('1.0', 'end-1c')
            
            if not (ent_ad.get().strip() or ent_afis.get().strip() or hk.strip()): 
                return
                
            v = {"ad": ent_ad.get(), "afis": ent_afis.get(), "detay": ent_detay.get(), "oyuncu": ent_oyuncu.get(), "konu": hk, "fragman": ent_fragman.get(), "info": hi}
            bb = sablon_motoru.film_sablonu(v, {k: _v.get() for k, _v in vars.items()})
            
            sag_txt.delete("1.0", "end")
            sag_txt.insert("1.0", bb)
            sag_txt._textbox.tag_add("center", "1.0", "end")
            self.bbcode_renklendir(sag_txt)
            
            for g in [ent_ad, ent_afis, ent_detay, ent_oyuncu, txt_konu, ent_fragman, txt_info]:
                if hasattr(g, "renk_tazeleyici"): 
                    g.renk_tazeleyici()

        def temizle_film():
            ent_ad.delete(0, 'end'); ent_afis.delete(0, 'end'); ent_detay.delete(0, 'end'); ent_oyuncu.delete(0, 'end')
            txt_konu.delete('1.0', 'end'); ent_fragman.delete(0, 'end'); txt_info.delete('1.0', 'end'); sag_txt.delete("1.0", "end")
            text_placeholder_ayarla(txt_konu, o_konu); text_placeholder_ayarla(txt_info, o_info)

        def kaydet_film():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                d = {"ad": ent_ad.get(), "afis": ent_afis.get(), "detay": ent_detay.get(), "oyuncu": ent_oyuncu.get(), "konu": txt_konu.get('1.0','end-1c'), "fragman": ent_fragman.get(), "info": txt_info.get('1.0','end-1c'), "chk": {k: _v.get() for k, _v in vars.items()}}
                with open(path, "w", encoding="utf-8") as f: json.dump(d, f)

        def yukle_film():
            path = filedialog.askopenfilename()
            if path:
                with open(path, "r", encoding="utf-8") as f: d = json.load(f)
                temizle_film(); ent_ad.insert(0, d["ad"]); ent_afis.insert(0, d["afis"]); ent_detay.insert(0, d["detay"]); ent_oyuncu.insert(0, d["oyuncu"])
                txt_konu.delete('1.0', 'end'); txt_konu.insert('1.0', d["konu"]); txt_info.delete('1.0', 'end'); txt_info.insert('1.0', d["info"])
                for k, _v in d["chk"].items(): vars[k].set(_v)
                film_bbcode_uret()

        tasarim_elemanlari.ekle_alt_butonlar(self, sag_frame, sag_txt, temizle_film, kaydet_film, yukle_film)
    def tasarla_dizi_sekmesi(self):
        sol, sag_txt, sag_frame = tasarim_elemanlari.create_layout_structure(self.tab_dizi)

        o_ad = "The WONDERfools S01 NF DUAL WEB-DL 1080p AAC2"
        o_afis = "https://imgur.com"
        o_detay = "https://imgur.com"
        o_oyuncu = "https://imgur.com"
        o_konu = "Çılgın bir kasaba ekibi süper güçler kazanıp, yüzyıl dönümünde komik bir maceraya atılırken, dünyayı tehdit eden kötülüklere karşı mücadele ediyor ve sonuçta kıyamet korkusu artıyor."
        o_fragman = "https://youtube.com"
        o_info = "Info Bilgileri NFO Sekmesindedir"

        ent_ad = tasarim_elemanlari.ekle_girdi(sol, "Dizi Adı", ornek=o_ad, update_callback=lambda: dizi_bbcode_uret())
        ent_afis = tasarim_elemanlari.ekle_girdi(sol, "Afiş (Resim Linki)", has_upload=True, ornek=o_afis, update_callback=lambda: dizi_bbcode_uret())
        ent_detay = tasarim_elemanlari.ekle_girdi(sol, "Detay (Resim Linki)", has_upload=True, ornek=o_detay, update_callback=lambda: dizi_bbcode_uret())
        ent_oyuncu = tasarim_elemanlari.ekle_girdi(sol, "Oyuncular (Resim Linki)", has_upload=True, ornek=o_oyuncu, update_callback=lambda: dizi_bbcode_uret())
        txt_konu = tasarim_elemanlari.ekle_girdi(sol, "Konu", is_textbox=True, height=75, ornek=o_konu, update_callback=lambda: dizi_bbcode_uret())
        ent_fragman = tasarim_elemanlari.ekle_girdi(sol, "Fragman (Youtube Linki)", ornek=o_fragman, update_callback=lambda: dizi_bbcode_uret())
        txt_info = tasarim_elemanlari.ekle_girdi(sol, "NFO / Info", is_textbox=True, height=100, ornek=o_info, update_callback=lambda: dizi_bbcode_uret())

        vars = tasarim_elemanlari.ekle_medya_onay_kutulari(sol, update_callback=lambda: dizi_bbcode_uret())

        def text_placeholder_ayarla(box, v_metin):
            box.delete("1.0", "end")
            box.insert("1.0", v_metin)
            box.configure(text_color="#888888")
            
            def odak_giris(event):
                current = box.get("1.0", "end-1c").strip()
                if current == v_metin.strip():
                    box.delete("1.0", "end")
                    yazi_rengi = "#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#000000"
                    box.configure(text_color=yazi_rengi)
                    
            def odak_cikis(event):
                current = box.get("1.0", "end-1c").strip()
                if not current:
                    box.insert("1.0", v_metin)
                    box.configure(text_color="#888888")
                    
            box.bind("<FocusIn>", odak_giris)
            box.bind("<FocusOut>", odak_cikis)

        text_placeholder_ayarla(txt_konu, o_konu)
        text_placeholder_ayarla(txt_info, o_info)
        def dizi_bbcode_uret():
            current_konu = txt_konu.get('1.0', 'end-1c').strip()
            current_info = txt_info.get('1.0', 'end-1c').strip()
            
            hk = "" if current_konu == o_konu.strip() else txt_konu.get('1.0', 'end-1c')
            hi = "" if current_info == o_info.strip() or "NFO Sekmesindedir" in current_info else txt_info.get('1.0', 'end-1c')
            
            if not (ent_ad.get().strip() or ent_afis.get().strip() or hk.strip()): 
                return
                
            v = {"ad": ent_ad.get(), "afis": ent_afis.get(), "detay": ent_detay.get(), "oyuncu": ent_oyuncu.get(), "konu": hk, "fragman": ent_fragman.get(), "info": hi}
            bb = sablon_motoru.dizi_sablonu(v, {k: _v.get() for k, _v in vars.items()})
            
            sag_txt.delete("1.0", "end")
            sag_txt.insert("1.0", bb)
            sag_txt._textbox.tag_add("center", "1.0", "end")
            self.bbcode_renklendir(sag_txt)
            
            for g in [ent_ad, ent_afis, ent_detay, ent_oyuncu, txt_konu, ent_fragman, txt_info]:
                if hasattr(g, "renk_tazeleyici"): 
                    g.renk_tazeleyici()

        def temizle_dizi():
            ent_ad.delete(0, 'end'); ent_afis.delete(0, 'end'); ent_detay.delete(0, 'end'); ent_oyuncu.delete(0, 'end')
            txt_konu.delete('1.0', 'end'); ent_fragman.delete(0, 'end'); txt_info.delete('1.0', 'end'); sag_txt.delete("1.0", "end")
            text_placeholder_ayarla(txt_konu, o_konu); text_placeholder_ayarla(txt_info, o_info)

        def kaydet_dizi():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                d = {"ad": ent_ad.get(), "afis": ent_afis.get(), "detay": ent_detay.get(), "oyuncu": ent_oyuncu.get(), "konu": txt_konu.get('1.0','end-1c'), "fragman": ent_fragman.get(), "info": txt_info.get('1.0','end-1c'), "chk": {k: _v.get() for k, _v in vars.items()}}
                with open(path, "w", encoding="utf-8") as f: json.dump(d, f)

        def yukle_dizi():
            path = filedialog.askopenfilename()
            if path:
                with open(path, "r", encoding="utf-8") as f: d = json.load(f)
                temizle_dizi(); ent_ad.insert(0, d["ad"]); ent_afis.insert(0, d["afis"]); ent_detay.insert(0, d["detay"]); ent_oyuncu.insert(0, d["oyuncu"])
                txt_konu.delete('1.0', 'end'); txt_konu.insert('1.0', d["konu"]); txt_info.delete('1.0', 'end'); txt_info.insert('1.0', d["info"])
                for k, _v in d["chk"].items(): vars[k].set(_v)
                dizi_bbcode_uret()

        tasarim_elemanlari.ekle_alt_butonlar(self, sag_frame, sag_txt, temizle_dizi, kaydet_dizi, yukle_dizi)
    def tasarla_muzik_sekmesi(self):
        sol, sag_txt, sag_frame = tasarim_elemanlari.create_layout_structure(self.tab_muzik)

        o_album = "Toygar Isikli - Babil Original Soundtrack"
        o_afis = "https://bitturk.net"
        o_detay = "Audio #0 : MPEG Audio at 320 kb/s Infos : 2 kanal, 44.1 kHz"
        o_parca = "01.Toygar Işıklı - Babil Main Title\n02.Toygar Işıklı - Money Talk_İrfan"

        ent_album = tasarim_elemanlari.ekle_girdi(sol, "Albüm Adı", ornek=o_album, update_callback=lambda: muzik_bbcode_uret())
        ent_afis = tasarim_elemanlari.ekle_girdi(sol, "Afiş (Resim Linki)", has_upload=True, ornek=o_afis, update_callback=lambda: muzik_bbcode_uret())
        txt_detay = tasarim_elemanlari.ekle_girdi(sol, "Detay", is_textbox=True, height=100, ornek=o_detay, update_callback=lambda: muzik_bbcode_uret())
        txt_parca = tasarim_elemanlari.ekle_girdi(sol, "Parça Listesi", is_textbox=True, height=150, ornek=o_parca, update_callback=lambda: muzik_bbcode_uret())

        def text_placeholder_ayarla(box, v_metin):
            box.delete("1.0", "end")
            box.insert("1.0", v_metin)
            box.configure(text_color="#888888")
            
            def odak_giris(event):
                current = box.get("1.0", "end-1c").strip()
                if current == v_metin.strip():
                    box.delete("1.0", "end")
                    yazi_rengi = "#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#000000"
                    box.configure(text_color=yazi_rengi)
                    
            def odak_cikis(event):
                current = box.get("1.0", "end-1c").strip()
                if not current:
                    box.insert("1.0", v_metin)
                    box.configure(text_color="#888888")
                    
            box.bind("<FocusIn>", odak_giris)
            box.bind("<FocusOut>", odak_cikis)

        text_placeholder_ayarla(txt_detay, o_detay)
        text_placeholder_ayarla(txt_parca, o_parca)
        def muzik_bbcode_uret():
            hd = "" if txt_detay.get('1.0', 'end-1c').strip() == o_detay.strip() else txt_detay.get('1.0', 'end-1c')
            hp = "" if txt_parca.get('1.0', 'end-1c').strip() == o_parca.strip() else txt_parca.get('1.0', 'end-1c')
            
            if not (ent_album.get().strip() or ent_afis.get().strip()): 
                return
                
            v = {"album": ent_album.get(), "afis": ent_afis.get(), "detay": hd, "parca": hp}
            bb = sablon_motoru.muzik_sablonu(v)
            
            sag_txt.delete("1.0", "end")
            sag_txt.insert("1.0", bb)
            sag_txt._textbox.tag_add("center", "1.0", "end")
            self.bbcode_renklendir(sag_txt)
            
            for g in [ent_album, ent_afis, txt_detay, txt_parca]:
                if hasattr(g, "renk_tazeleyici"): 
                    g.renk_tazeleyici()

        def temizle_muzik():
            ent_album.delete(0, 'end'); ent_afis.delete(0, 'end'); txt_detay.delete('1.0', 'end'); txt_parca.delete('1.0', 'end'); sag_txt.delete("1.0", "end")
            text_placeholder_ayarla(txt_detay, o_detay); text_placeholder_ayarla(txt_parca, o_parca)

        def kaydet_muzik():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                d = {"album": ent_album.get(), "afis": ent_afis.get(), "detay": txt_detay.get('1.0','end-1c'), "parca": txt_parca.get('1.0','end-1c')}
                with open(path, "w", encoding="utf-8") as f: json.dump(d, f)

        def yukle_muzik():
            path = filedialog.askopenfilename()
            if path:
                with open(path, "r", encoding="utf-8") as f: d = json.load(f)
                temizle_muzik(); ent_album.insert(0, d["album"]); ent_afis.insert(0, d["afis"])
                txt_detay.delete('1.0', 'end'); txt_detay.insert('1.0', d["detay"]); txt_parca.delete('1.0', 'end'); txt_parca.insert('1.0', d["parca"])
                muzik_bbcode_uret()

        tasarim_elemanlari.ekle_alt_butonlar(self, sag_frame, sag_txt, temizle_muzik, kaydet_muzik, yukle_muzik)
    def tasarla_oyun_sekmesi(self):
        sol, sag_txt, sag_frame = tasarim_elemanlari.create_layout_structure(self.tab_oyun)

        o_ad = "Narcos: Rise of the Cartels"
        o_afis = "https://bitturk.net"
        o_tanitim = "80'lerin Kolombiya'sına hoş geldiniz. El Patrón'un imparatorluğunun ateşi çoktan yakıldı, etkisi sınırları aştı ve hızla büyüyor."
        o_fragman = "https://youtu.be"
        o_sistem = "MİNİMUM: İşletim Sistemi: Windows 7, 8, 8.1, 10 x64 İşlemci: Intel Core i3-2100"
        o_info = "-Iso dosyasından normal kurulum yapın. -CODEX dizininden crackli dosyaları oyunu kurduğunuz dizine kopyalayın."

        ent_ad = tasarim_elemanlari.ekle_girdi(sol, "Oyun Adı", ornek=o_ad, update_callback=lambda: oyun_bbcode_uret())
        ent_afis = tasarim_elemanlari.ekle_girdi(sol, "Afiş (Resim Linki)", has_upload=True, ornek=o_afis, update_callback=lambda: oyun_bbcode_uret())
        txt_tanitim = tasarim_elemanlari.ekle_girdi(sol, "Tanıtım", is_textbox=True, height=80, ornek=o_tanitim, update_callback=lambda: oyun_bbcode_uret())
        ent_fragman = tasarim_elemanlari.ekle_girdi(sol, "Fragman (Youtube Linki)", ornek=o_fragman, update_callback=lambda: oyun_bbcode_uret())
        txt_sistem = tasarim_elemanlari.ekle_girdi(sol, "Minumum Sistem", is_textbox=True, height=100, ornek=o_sistem, update_callback=lambda: oyun_bbcode_uret())
        txt_info = tasarim_elemanlari.ekle_girdi(sol, "NFO / info", is_textbox=True, height=80, ornek=o_info, update_callback=lambda: oyun_bbcode_uret())

        def text_placeholder_ayarla(box, v_metin):
            box.delete("1.0", "end")
            box.insert("1.0", v_metin)
            box.configure(text_color="#888888")
            
            def odak_giris(event):
                current = box.get("1.0", "end-1c").strip()
                if current == v_metin.strip():
                    box.delete("1.0", "end")
                    yazi_rengi = "#FFFFFF" if ctk.get_appearance_mode() == "Dark" else "#000000"
                    box.configure(text_color=yazi_rengi)
                    
            def odak_cikis(event):
                current = box.get("1.0", "end-1c").strip()
                if not current:
                    box.insert("1.0", v_metin)
                    box.configure(text_color="#888888")
                    
            box.bind("<FocusIn>", odak_giris)
            box.bind("<FocusOut>", odak_cikis)

        text_placeholder_ayarla(txt_tanitim, o_tanitim)
        text_placeholder_ayarla(txt_sistem, o_sistem)
        text_placeholder_ayarla(txt_info, o_info)
        def oyun_bbcode_uret():
            ht = "" if txt_tanitim.get('1.0', 'end-1c').strip() == o_tanitim.strip() else txt_tanitim.get('1.0', 'end-1c')
            hs = "" if txt_sistem.get('1.0', 'end-1c').strip() == o_sistem.strip() else txt_sistem.get('1.0', 'end-1c')
            hi = "" if txt_info.get('1.0', 'end-1c').strip() == o_info.strip() else txt_info.get('1.0', 'end-1c')
            
            if not (ent_ad.get().strip() or ent_afis.get().strip()): 
                return
                
            v = {"ad": ent_ad.get(), "afis": ent_afis.get(), "tanitim": ht, "fragman": ent_fragman.get(), "sistem": hs, "info": hi}
            bb = sablon_motoru.oyun_sablonu(v)
            
            sag_txt.delete("1.0", "end")
            sag_txt.insert("1.0", bb)
            sag_txt._textbox.tag_add("center", "1.0", "end")
            self.bbcode_renklendir(sag_txt)
            
            for g in [ent_ad, ent_afis, txt_tanitim, ent_fragman, txt_sistem, txt_info]:
                if hasattr(g, "renk_tazeleyici"): 
                    g.renk_tazeleyici()

        def temizle_oyun():
            ent_ad.delete(0, 'end'); ent_afis.delete(0, 'end'); txt_tanitim.delete('1.0', 'end'); ent_fragman.delete(0, 'end'); txt_sistem.delete('1.0', 'end'); txt_info.delete('1.0', 'end'); sag_txt.delete("1.0", "end")
            text_placeholder_ayarla(txt_tanitim, o_tanitim); text_placeholder_ayarla(txt_sistem, o_sistem); text_placeholder_ayarla(txt_info, o_info)

        def kaydet_oyun():
            path = filedialog.asksaveasfilename(defaultextension=".txt")
            if path:
                d = {"ad": ent_ad.get(), "afis": ent_afis.get(), "tanitim": txt_tanitim.get('1.0','end-1c'), "fragman": ent_fragman.get(), "sistem": txt_sistem.get('1.0','end-1c'), "info": txt_info.get('1.0','end-1c')}
                with open(path, "w", encoding="utf-8") as f: json.dump(d, f)

        def yukle_oyun():
            path = filedialog.askopenfilename()
            if path:
                with open(path, "r", encoding="utf-8") as f: d = json.load(f)
                temizle_oyun(); ent_ad.insert(0, d["ad"]); ent_afis.insert(0, d["afis"]); ent_fragman.insert(0, d["fragman"])
                txt_tanitim.delete('1.0', 'end'); txt_tanitim.insert('1.0', d["tanitim"]); txt_sistem.delete('1.0', 'end'); txt_sistem.insert('1.0', d["sistem"]); txt_info.delete('1.0', 'end'); txt_info.insert('1.0', d["info"])
                oyun_bbcode_uret()

        tasarim_elemanlari.ekle_alt_butonlar(self, sag_frame, sag_txt, temizle_oyun, kaydet_oyun, yukle_oyun)
    def tasarla_diger_sekmesi(self):
        sol, sag_txt, sag_frame = tasarim_elemanlari.create_layout_structure(self.tab_diger)
        o_ad, o_afis, o_tanitim, o_fragman, o_sistem, o_info = "Autodesk AutoCAD", "https://ibb.co", "Mimarlar ve mühendisler tarafından sıklıkla kullanılan...", "https://youtu.be", "Operating System: Microsoft Windows 10...", "1- Programı kurun. Kurulum bittikten sonra..."

        ent_ad = tasarim_elemanlari.ekle_girdi(sol, "Adı", ornek=o_ad, update_callback=lambda: diger_bbcode_uret())
        ent_afis = tasarim_elemanlari.ekle_girdi(sol, "Afiş (Resim Linki)", has_upload=True, ornek=o_afis, update_callback=lambda: diger_bbcode_uret())
        txt_tanitim = tasarim_elemanlari.ekle_girdi(sol, "Tanıtım", is_textbox=True, height=80, ornek=o_tanitim, update_callback=lambda: diger_bbcode_uret())
        ent_fragman = tasarim_elemanlari.ekle_girdi(sol, "Fragman (Youtube Linki)", ornek=o_fragman, update_callback=lambda: diger_bbcode_uret())
        txt_sistem = tasarim_elemanlari.ekle_girdi(sol, "Minumum Sistem", is_textbox=True, height=100, ornek=o_sistem, update_callback=lambda: diger_bbcode_uret())
        txt_info = tasarim_elemanlari.ekle_girdi(sol, "NFO / info", is_textbox=True, height=80, ornek=o_info, update_callback=lambda: diger_bbcode_uret())

        def text_placeholder_ayarla(box, v_metin):
            box.delete("1.0", "end")
            box.insert("1.0", v_metin)
            box.configure(text_color="#888888")
            box.bind("<FocusIn>", lambda event: (box.delete("1.0", "end"), box.configure(text_color=["#000000", "#FFFFFF"])) if box.get("1.0", "end-1c").strip() == v_metin.strip() else None)
            box.bind("<FocusOut>", lambda event: (box.insert("1.0", v_metin), box.configure(text_color="#888888")) if not box.get("1.0", "end-1c").strip() else None)

        text_placeholder_ayarla(txt_tanitim, o_tanitim); text_placeholder_ayarla(txt_sistem, o_sistem); text_placeholder_ayarla(txt_info, o_info)

        def diger_bbcode_uret():
            ht = "" if txt_tanitim.get('1.0', 'end-1c').strip() == o_tanitim.strip() else txt_tanitim.get('1.0', 'end-1c')
            hs = "" if txt_sistem.get('1.0', 'end-1c').strip() == o_sistem.strip() else txt_sistem.get('1.0', 'end-1c')
            hi = "" if txt_info.get('1.0', 'end-1c').strip() == o_info.strip() else txt_info.get('1.0', 'end-1c')
            if not (ent_ad.get().strip() or ent_afis.get().strip()): return
            v = {"ad": ent_ad.get(), "afis": ent_afis.get(), "tanitim": ht, "fragman": ent_fragman.get(), "sistem": hs, "info": hi}
            bb = sablon_motoru.program_sablonu(v)
            sag_txt.delete("1.0", "end"); sag_txt.insert("1.0", bb); sag_txt._textbox.tag_add("center", "1.0", "end"); self.bbcode_renklendir(sag_txt)

        tasarim_elemanlari.ekle_alt_butonlar(self, sag_frame, sag_txt, lambda: None, lambda: None, lambda: None)

    def tasarla_vip_sekmesi(self):
        sol, sag_txt, sag_frame = tasarim_elemanlari.create_layout_structure(self.tab_vip)
        ent_ad = tasarim_elemanlari.ekle_girdi(sol, "Sunum Adı", ornek="Nubiles MFP", update_callback=lambda: vip_bbcode_uret())
        ent_ekran = tasarim_elemanlari.ekle_girdi(sol, "Ekran Görüntüsü (Resim Linki)", has_upload=True, ornek="https://ibb.co", update_callback=lambda: vip_bbcode_uret())

        def vip_bbcode_uret():
            if not (ent_ad.get().strip() or ent_ekran.get().strip()): return
            bb = sablon_motoru.vip_sablonu({"ad": ent_ad.get(), "ekran": ent_ekran.get()})
            sag_txt.delete("1.0", "end"); sag_txt.insert("1.0", bb); sag_txt._textbox.tag_add("center", "1.0", "end"); self.bbcode_renklendir(sag_txt)

        tasarim_elemanlari.ekle_alt_butonlar(self, sag_frame, sag_txt, lambda: (ent_ad.delete(0,'end'), ent_ekran.delete(0,'end'), sag_txt.delete("1.0","end")), lambda: None, lambda: None)

if __name__ == "__main__":
    app = BiTTuRKMuadiliApp()
    app.mainloop()
