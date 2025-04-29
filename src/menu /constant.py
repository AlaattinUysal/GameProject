# menu/constants.py

import os

# Ekran boyutları
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Tam ekran değişkeni
FULLSCREEN = False

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
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
MENU_ASSETS_DIR = os.path.join(ASSETS_DIR, "menu_tasarim")
