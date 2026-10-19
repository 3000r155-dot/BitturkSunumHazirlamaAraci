import os
import sys
import subprocess

# Python 3.12 kullan
python_path = r"C:\Users\mcilv\AppData\Local\Programs\Python\Python312\python.exe"

# Sanal ortam oluştur (sadece .venv312 kullan)
if not os.path.exists(".venv312"):
    subprocess.run([python_path, "-m", "venv", ".venv312"], check=True)

# Sanal ortamdaki python ve pyinstaller kullan
venv_python = ".venv312\\Scripts\\python.exe"
venv_pip = ".venv312\\Scripts\\pip.exe"

# Paketleri yükle
subprocess.run([venv_pip, "install", "-r", "requirements.txt"], check=True)

# PyInstaller ile build
subprocess.run([venv_python, "-m", "PyInstaller", "BiTTuRK_SunumAraci.spec", "--clean"], check=True)

print("Build tamamlandı! Çıktı: dist/")
