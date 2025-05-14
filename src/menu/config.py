import os
import pygame

# Pygame başlatma
pygame.init()
pygame.mixer.init()  # Mixer'ı başlat

# Ekran boyutları
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Way")

# Tam ekran değişkeni
fullscreen = False

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 40)
DARKER_GRAY = (20, 20, 30)
ORANGE = (255, 120, 50)
BRIGHT_ORANGE = (255, 140, 60)
DARK_ORANGE = (200, 80, 30)
RED = (220, 60, 40)
GREEN = (80, 220, 100)
BLUE = (50, 150, 255)
CYAN = (0, 180, 220)
PURPLE = (128, 0, 128)
LIGHT_GRAY = (180, 180, 190)
GOLD = (255, 215, 0)

# Kaynaklar dizini
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets")
MENU_ASSETS_DIR = os.path.join(ASSETS_DIR, "menu_tasarim")
MUSIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "sounds", "arka_plan_music")

# Buton simgeleri (unicode emoji karakterler)
ICONS = {
    "play": "▶️",             # Play (başlat) için üçgen ok
    "levels": "🎮",           # Seviyeler için oyun kontrolü
    "shop": "🛒",             # Mağaza için alışveriş arabası
    "leaderboard": "🏆",      # Liderlik tablosu için kupa
    "options": "⚙️",          # Ayarlar için dişli
    "back": "↩️",             # Geri için ok
    "resume": "▶️",           # Devam et için üçgen ok
    "restart": "🔄",          # Yeniden başlat için yenile
    "settings": "⚙️",         # Ayarlar için dişli
    "quit": "🚪",             # Çıkış için kapı
    "music": "🎵",            # Müzik için nota
    "sound": "🔊",            # Ses için hoparlör
    "bright": "💡",           # Parlaklık için ampul
    "login": "👤"             # Kullanıcı girişi için simge
}

# Ayarlar için varsayılan değerler
DEFAULT_MUSIC_VOLUME = 0.5  # 0.0-1.0 arası
DEFAULT_SOUND_VOLUME = 0.5  # 0.0-1.0 arası
DEFAULT_BRIGHTNESS = 50     # 0-100 arası
MIN_BRIGHTNESS = 10         # Minimum parlaklık değeri

# Buton boyutları
BUTTON_WIDTH = 280
BUTTON_HEIGHT = 50
BUTTON_SPACING = 30

# Panel boyutları
PANEL_WIDTH = 400
PANEL_HEIGHT = 460

# Oyun adı
GAME_TITLE = "THE WAY"

# Default token değeri
DEFAULT_TOKENS = 1000 