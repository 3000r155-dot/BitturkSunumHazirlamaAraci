import subprocess
import sys
import os

# Nuitka komutları
cmd = [
    sys.executable,
    "-m",
    "nuitka",
    "--standalone",
    "--onefile",
    "--enable-plugin=tk-inter",
    "--windows-disable-console",
    "--assume-yes-for-downloads",
    "--output-dir=dist",
    "--windows-icon-from-ico=assets/app_icon.ico",
    "main.py",
]

print("Nuitka ile build başlatılıyor...")
print("Komut:", " ".join(cmd))

subprocess.run(cmd, check=True)

print("\nBuild tamamlandı! Çıktı: dist/BiTTuRK_SunumAraci.exe")
