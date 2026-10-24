# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# İkon dosyası platforma göre seç
if sys.platform == 'win32':
    icon_file = 'assets/app_icon.ico'
elif sys.platform == 'darwin':
    icon_file = 'assets/app_icon.icns'
else:
    icon_file = 'assets/app_icon.png'

# Playwright driver ve paket dosyalarını ekle (chromium binary hariç)
playwright_datas = []
playwright_datas.extend(collect_data_files('playwright'))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('ayarlar.py', '.'),
        ('tasarim_elemanlari.py', '.'),
        ('app_icons.py', '.'),
        ('sablon_motoru.py', '.'),
        ('os_optimizasyon.py', '.'),
        ('premium_access.py', '.'),
    ] + playwright_datas,
    hiddenimports=[
        'customtkinter',
        'playwright',
        'playwright.sync_api',
        'requests',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BiTTuRK_SunumAraci',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BiTTuRK_SunumAraci',
)
