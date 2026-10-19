# os_optimizasyon.py - İŞLETİM SİSTEMİ ARAYÜZ VE GÖRÜNÜM OPTİMİZASYON MOTORU
import os
import sys

def isletim_sistemi_arayuzunu_ayarla():
    """
    Uygulama pencereleri oluşturulmadan ÖNCE çağrılmalıdır.
    İşletim sistemine göre High-DPI ve modern görsel stilleri tetikler.
    """
    if sys.platform.startswith("win"):
        try:
            import ctypes
            # 1. Görev Çubuğu (Taskbar) İkon Birleşme Koruması
            uygulama_id = "bitturk.sunum.hazirlama.araci.75"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(uygulama_id)
            
            # 2. Dinamik High-DPI Awareness (Yüksek Çözünürlük Netlik Kilidi)
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2) # PROCESS_PER_MONITOR_DPI_AWARE
            except Exception:
                ctypes.windll.user32.SetProcessDPIAware()
                
            # 3. Windows 11 Modern Pencere Stili İpuçları
            ctypes.windll.kernel32.SetThreadErrorMode(0x0001, None)
            
        except Exception:
            pass
            
    elif sys.platform.startswith("linux"):
        try:
            os.environ["GDK_SCALE"] = "1"
            os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
        except Exception:
            pass
