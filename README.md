# BiTTuRK.NeT Sunum Hazırlama Aracı

Film, dizi, müzik, oyun ve diğer içerikler için BBCode sunum şablonları oluşturmanın en kolay yolu.

## Özellikler

- **Film**: Afiş, detay, oyuncu görselleri, konu, fragman, NFO ve medya rozetleri
- **Dizi**: Sezon/yayın bilgileri, görseller, konu, fragman ve rozetler
- **Müzik**: Albüm, kapak, teknik bilgiler ve parça listesi
- **Oyun**: Afiş, tanıtım, fragman, sistem gereksinimleri ve rozetler
- **Premium Özellikler**: Altın/Gümüş rozetler, 2X Sunum ve VIP sekmesi
- **Otomatik Görsel Yükleme**: ImgBB entegrasyonu ile kolay görsel upload
- **Taslak Yönetimi**: Kaydet/Yükle ile taslakları yönetin

## Kurulum (Geliştirme)

```bash
# Sanal ortam oluştur
python -m venv .venv

# Sanal ortamı etkinleştir
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Playwright Chromium yükle
python -m playwright install chromium

# Uygulamayı çalıştır
python main.py
```

## Çalıştırılabilir Dosya Oluşturma

### PyInstaller'ı Yükle

```bash
pip install pyinstaller
```

### Windows Build

```bash
python build_windows.py
```

Çıktı: `dist/BiTTuRK_SunumAraci.exe`

### macOS Build

```bash
python build_mac.py
```

Çıktı: `dist/BiTTuRK_SunumAraci`

### Linux Build

```bash
python build_linux.py
```

Çıktı: `dist/BiTTuRK_SunumAraci`

## Daha Fazla Bilgi

Detaylı build bilgisi için [BUILD.md](BUILD.md) dosyasına bakın.

## Lisans

BiTTuRK.NeT - Tüm hakları saklıdır.
