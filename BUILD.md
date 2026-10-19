# BiTTuRK.NeT Sunum Hazırlama Aracı - Build Guide

## Yöntem 1: GitHub Actions (Önerilen)

Tüm platformlar için otomatik build:

1. GitHub'a bu projeyi push edin
2. GitHub'da "Actions" sekmesine gidin
3. "Build Multi-Platform" workflow'unu çalıştırın
4. Build tamamlandığında "Artifacts" bölümünden dosyaları indirin

Platformlar:
- Windows: `BiTTuRK_SunumAraci-windows-latest.exe`
- macOS: `BiTTuRK_SunumAraci-macos-latest`
- Linux: `BiTTuRK_SunumAraci-ubuntu-latest`

## Yöntem 2: Manuel Build

### Windows için Build

```bash
py -3.12 build_windows.py
```

Çıktı: `dist/BiTTuRK_SunumAraci.exe`

### macOS için Build

```bash
python3 build_mac.py
```

Çıktı: `dist/BiTTuRK_SunumAraci`

### Linux için Build

Önce bağımlılıkları yükleyin:
```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
```

Sonra build edin:
```bash
python3 build_linux.py
chmod +x dist/BiTTuRK_SunumAraci
```

Çıktı: `dist/BiTTuRK_SunumAraci`

## Kod Güncellemeleri

Uygulamayı geliştirmek için Python kaynak kodlarını kullanabilirsiniz:

```bash
python main.py
```

## Build Sonrası

Build işlemleri çalıştırılabilir dosyaları oluşturur:
- **Windows**: Tek `.exe` dosyası - Python gerektirmez
- **macOS**: İkili dosya - Python gerektirmez
- **Linux**: İkili dosya - Python gerektirmez

## Notlar

- Python 3.12 ile build edildi (daha stabil)
- Tüm bağımlılıklar paketlendi
- Playwright Chromium bileşenleri dahil değil
- Görsel yükleme için internet gerekir
