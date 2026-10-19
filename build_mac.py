import os
import sys
import subprocess

# Sanal ortam oluştur
if not os.path.exists(".venv"):
    subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

# Sanal ortamdaki python ve pyinstaller kullan
venv_python = ".venv/bin/python"
venv_pip = ".venv/bin/pip"

# Paketleri yükle
subprocess.run([venv_pip, "install", "-r", "requirements.txt"], check=True)

# PyInstaller ile build
subprocess.run([venv_python, "-m", "PyInstaller", "BiTTuRK_SunumAraci.spec", "--clean"], check=True)

print("Build tamamlandı! Çıktı: dist/")
