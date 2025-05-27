import os
import sys
import pygame

# Add parent directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from menu.config import SCREEN_WIDTH, SCREEN_HEIGHT, DARKER_GRAY, MENU_ASSETS_DIR, MUSIC_DIR

def load_font(size=36, bold=False, font_name="Segoe UI Emoji"):
    """Font yükleme - Segoe UI Emoji fontu kullanıyoruz (emoji için en iyi görünüm)"""
    try:
        # Varsayılan olarak Segoe UI Emoji font kullan (emoji desteği için)
        return pygame.font.SysFont(font_name, size, bold=bold)
    except (pygame.error, FileNotFoundError, IndexError) as e:
        print(f"Font yükleme hatası: {e}")
        # Herhangi bir hata olursa varsayılan system fontu
        return pygame.font.SysFont(None, size, bold=bold)

def load_background():
    """Menü arka planını yükler (mutlak yol ile)"""
    background_path = r"C:/Users/OMEN/Desktop/CURSOR/GameProject-Dev/GameProject-dev/menu/arka_plan/menu_arka_plan3.png"
    try:
        background = pygame.image.load(background_path)
        return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"Arka plan yüklenemedi: {e}")
        fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fallback.fill(DARKER_GRAY)
        return fallback

def load_samurai_characters():
    """Samuray karakterlerini yükler (mutlak yol ile)"""
    try:
        samurai1_path = r"C:/Users/OMEN/Desktop/CURSOR/GameProject-Dev/GameProject-dev/menu/0_Samurai_Idle_000.png"
        samurai2_path = r"C:/Users/OMEN/Desktop/CURSOR/GameProject-Dev/GameProject-dev/menu/0_Samurai2_Idle_000.png"
        samurai1 = None
        samurai2 = None
        if os.path.exists(samurai1_path):
            samurai1 = pygame.image.load(samurai1_path).convert_alpha()
            height = int(SCREEN_HEIGHT * 0.4)
            width = int(samurai1.get_width() * (height / samurai1.get_height()))
            samurai1 = pygame.transform.scale(samurai1, (width, height))
            print(f"Samurai 1 resmi yüklendi: {samurai1_path}")
        else:
            print("Samurai 1 resmi bulunamadı.")
        if os.path.exists(samurai2_path):
            samurai2 = pygame.image.load(samurai2_path).convert_alpha()
            height = int(SCREEN_HEIGHT * 0.4)
            width = int(samurai2.get_width() * (height / samurai2.get_height()))
            samurai2 = pygame.transform.scale(samurai2, (width, height))
            samurai2 = pygame.transform.flip(samurai2, True, False)  # Sola baksın
            print(f"Samurai 2 resmi yüklendi ve sola çevrildi: {samurai2_path}")
        else:
            print("Samurai 2 resmi bulunamadı.")
        return samurai1, samurai2
    except Exception as e:
        print(f"Samuray resimleri yüklenirken hata oluştu: {e}")
        return None, None

def load_and_play_music():
    """Menü arka plan müziğini yükler ve oynatır (mutlak yol ile)"""
    try:
        music_path = r"C:/Users/OMEN/Desktop/CURSOR/GameProject-Dev/GameProject-dev/menu/sounds/arka_plan_music/Hollow_Knight.mp3"
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # -1 sonsuz döngü için
            pygame.mixer.music.set_volume(0.5)  # Başlangıç ses seviyesi
            print(f"Müzik başarıyla yüklendi ve oynatılıyor: {music_path}")
            return True
        else:
            print(f"Müzik dosyası bulunamadı: {music_path}")
            return False
    except Exception as e:
        print(f"Müzik yükleme işleminde hata oluştu: {e}")
        return False 