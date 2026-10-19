import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["customtkinter", "playwright", "requests", "PIL", "tkinter"],
    "includes": ["ayarlar", "tasarim_elemanlari", "app_icons", "sablon_motoru", "os_optimizasyon", "premium_access"],
    "excludes": [],
    "optimize": 0,
    "zip_include_packages": "*",
    "zip_exclude_packages": [],
    "include_files": [
        ("assets", "assets"),
    ],
    "silent": False,
}

base = None

setup(
    name="BiTTuRK_SunumAraci",
    version="5.0",
    description="BiTTuRK.NeT Sunum Hazırlama Aracı",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="BiTTuRK_SunumAraci.exe",
            icon="assets/app_icon.ico",
        )
    ],
)
