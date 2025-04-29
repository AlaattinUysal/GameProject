# menu/assets.py

import pygame
import os
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, DARKER_GRAY, MENU_ASSETS_DIR

def load_background():
    background_dir = os.path.join(MENU_ASSETS_DIR, "arka_plan")
    
    possible_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    for ext in possible_extensions:
        full_path = os.path.join(background_dir, f"menu_arka_plan3{ext}")
        if os.path.exists(full_path):
            try:
                background = pygame.image.load(full_path)
                return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                continue
    
    try:
        if os.path.exists(background_dir):
            files = os.listdir(background_dir)
            for file in files:
                if file.startswith("menu_arka_plan3") and any(file.endswith(ext) for ext in possible_extensions):
                    try:
                        background = pygame.image.load(os.path.join(background_dir, file))
                        print(f"Yüklenen arka plan: {file}")
                        return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    except pygame.error:
                        continue
    except (FileNotFoundError, OSError) as e:
        print(f"Arka plan klasörü açılamadı: {e}")
    
    print("Arka plan yüklenemedi, varsayılan arka plan oluşturuluyor.")
    fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fallback.fill(DARKER_GRAY)
    return fallback

def load_samurai_characters():
    try:
        samurai1_path = os.path.join(MENU_ASSETS_DIR, "Samurai_1", "PNG", "PNG Sequences", "Idle", "0_Samurai_Idle_000.png")
        samurai2_path = os.path.join(MENU_ASSETS_DIR, "Samurai_2", "PNG", "PNG Sequences", "Idle", "0_Samurai_Idle_000.png")
        
        if not os.path.exists(samurai1_path):
            samurai1_path = None
            samurai_dir = os.path.join(MENU_ASSETS_DIR, "Samurai_1", "PNG")
            if os.path.exists(samurai_dir):
                for root, dirs, files in os.walk(samurai_dir):
                    for file in files:
                        if file.endswith(".png") and "Idle" in file:
                            samurai1_path = os.path.join(root, file)
                            break
                    if samurai1_path:
                        break
        
        if not os.path.exists(samurai2_path):
            samurai2_path = None
            samurai_dir = os.path.join(MENU_ASSETS_DIR, "Samurai_2", "PNG")
            if os.path.exists(samurai_dir):
                for root, dirs, files in os.walk(samurai_dir):
                    for file in files:
                        if file.endswith(".png") and "Idle" in file:
                            samurai2_path = os.path.join(root, file)
                            break
                    if samurai2_path:
                        break
        
        samurai1 = None
        samurai2 = None
        
        if samurai1_path and os.path.exists(samurai1_path):
            samurai1 = pygame.image.load(samurai1_path).convert_alpha()
            height = int(SCREEN_HEIGHT * 0.4)
            width = int(samurai1.get_width() * (height / samurai1.get_height()))
            samurai1 = pygame.transform.scale(samurai1, (width, height))
            print(f"Samurai 1 resmi yüklendi: {samurai1_path}")
        else:
            print("Samurai 1 resmi bulunamadı.")
        
        if samurai2_path and os.path.exists(samurai2_path):
            samurai2 = pygame.image.load(samurai2_path).convert_alpha()
            height = int(SCREEN_HEIGHT * 0.4)
            width = int(samurai2.get_width() * (height / samurai2.get_height()))
            samurai2 = pygame.transform.scale(samurai2, (width, height))
            samurai2 = pygame.transform.flip(samurai2, True, False)
            print(f"Samurai 2 resmi yüklendi: {samurai2_path}")
        else:
            print("Samurai 2 resmi bulunamadı.")
            
        return samurai1, samurai2
    
    except Exception as e:
        print(f"Samuray resimleri yüklenirken hata oluştu: {e}")
        return None, None

def load_font(size=36, bold=False, font_name="Segoe UI Emoji"):
    try:
        return pygame.font.SysFont(font_name, size, bold=bold)
    except (pygame.error, FileNotFoundError, IndexError) as e:
        print(f"Font yükleme hatası: {e}")
        return pygame.font.SysFont(None, size, bold=bold)
