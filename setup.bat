@echo off
echo BiTTuRK.NeT Sunum Hazırlama Araci - Kurulum
echo ===========================================
echo.

REM Python kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: Python bulunamadi!
    echo Lutfen Python 3.10 veya daha yeni bir surum yukleyin.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python bulundu.
python --version
echo.

REM Sanal ortam oluştur
if not exist ".venv" (
    echo Sanal ortam olusturuluyor...
    python -m venv .venv
) else (
    echo Sanal ortam zaten mevcut.
)

REM Sanal ortami etkinlestir
call .venv\Scripts\activate.bat

REM Paketleri yukle
echo Paketler yukleniyor...
pip install -r requirements.txt

REM Playwright Chromium yukle
echo Playwright Chromium yukleniyor...
python -m playwright install chromium

echo.
echo ===========================================
echo Kurulum tamamlandi!
echo.
echo Uygulamayi calistirmak icin:
echo run.bat dosyasini kullanin veya:
echo .venv\Scripts\python.exe main.py
echo.
pause
