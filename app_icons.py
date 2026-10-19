from pathlib import Path

import customtkinter as ctk
from PIL import Image


_ICON_DIRECTORY = Path(__file__).parent / "assets" / "icons"
_ICON_CACHE = {}
_APP_ICON_CACHE = {}


def get_icon(name, size=18):
    cache_key = (name, size)
    if cache_key not in _ICON_CACHE:
        icon_path = _ICON_DIRECTORY / f"{name}.png"
        with Image.open(icon_path) as image_file:
            image = image_file.convert("RGBA")
        _ICON_CACHE[cache_key] = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(size, size),
        )
    return _ICON_CACHE[cache_key]


def get_app_icon(size=22):
    if size not in _APP_ICON_CACHE:
        icon_path = _ICON_DIRECTORY.parent / "app_icon.png"
        with Image.open(icon_path) as image_file:
            image = image_file.convert("RGBA")
        _APP_ICON_CACHE[size] = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(size, size),
        )
    return _APP_ICON_CACHE[size]