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
    """Menü arka planını yükler"""
    background_dir = os.path.join(MENU_ASSETS_DIR, "arka_plan")
    
    # Önce tam dosya adı ile arama yap
    possible_extensions = ['.png', '.jpg', '.jpeg', '.bmp']
    for ext in possible_extensions:
        full_path = os.path.join(background_dir, f"menu_arka_plan3{ext}")
        if os.path.exists(full_path):
            try:
                background = pygame.image.load(full_path)
                return pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                continue
    
    # Eğer tam adla bulunamazsa, dizindeki diğer dosyalara bak
    try:
        if os.path.exists(background_dir):
            files = os.listdir(background_dir)
            # menu_arka_plan3.png gibi alternatif isimleri kontrol et
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
    # Yüklenemezse koyu gri bir arka plan oluştur
    fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fallback.fill(DARKER_GRAY)
    return fallback

def load_samurai_characters():
    """Samuray karakterlerini yükler"""
    try:
        # Samurai_1 idle duruşu
        samurai1_path = os.path.join(MENU_ASSETS_DIR, "Samurai_1", "PNG", "PNG Sequences", "Idle", "0_Samurai_Idle_000.png")
        # Samurai_2 idle duruşu
        samurai2_path = os.path.join(MENU_ASSETS_DIR, "Samurai_2", "PNG", "PNG Sequences", "Idle", "0_Samurai_Idle_000.png")
        
        # PNG dosyalarının var olduğunu kontrol et
        if not os.path.exists(samurai1_path):
            # Alternatif olarak diğer klasörlerde arayalım
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
            # Alternatif olarak diğer klasörlerde arayalım
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
        
        # Resimleri yükle
        samurai1 = None
        samurai2 = None
        
        if samurai1_path and os.path.exists(samurai1_path):
            samurai1 = pygame.image.load(samurai1_path).convert_alpha()
            # Boyutu ayarla - ekranın %30'u kadar yükseklik
            height = int(SCREEN_HEIGHT * 0.4)
            width = int(samurai1.get_width() * (height / samurai1.get_height()))
            samurai1 = pygame.transform.scale(samurai1, (width, height))
            print(f"Samurai 1 resmi yüklendi: {samurai1_path}")
        else:
            print("Samurai 1 resmi bulunamadı.")
        
        if samurai2_path and os.path.exists(samurai2_path):
            samurai2 = pygame.image.load(samurai2_path).convert_alpha()
            # Boyutu ayarla - ekranın %30'u kadar yükseklik
            height = int(SCREEN_HEIGHT * 0.4)
            width = int(samurai2.get_width() * (height / samurai2.get_height()))
            samurai2 = pygame.transform.scale(samurai2, (width, height))
            # Karakteri yatay olarak çevir (sağa baksın)
            samurai2 = pygame.transform.flip(samurai2, True, False)
            print(f"Samurai 2 resmi yüklendi: {samurai2_path}")
        else:
            print("Samurai 2 resmi bulunamadı.")
            
        return samurai1, samurai2
    
    except Exception as e:
        print(f"Samuray resimleri yüklenirken hata oluştu: {e}")
        return None, None

def load_and_play_music():
    """Menü arka plan müziğini yükler ve oynatır"""
    try:
        # Müzik klasörünün varlığını kontrol et
        if not os.path.exists(MUSIC_DIR):
            print(f"Müzik klasörü bulunamadı: {MUSIC_DIR}")
            return False

        # Müzik klasöründeki ilk .mp3 veya .wav dosyasını bul
        for file in os.listdir(MUSIC_DIR):
            if file.endswith(('.mp3', '.wav')):
                music_path = os.path.join(MUSIC_DIR, file)
                try:
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play(-1)  # -1 sonsuz döngü için
                    pygame.mixer.music.set_volume(0.5)  # Başlangıç ses seviyesi
                    print(f"Müzik başarıyla yüklendi ve oynatılıyor: {file}")
                    return True
                except pygame.error as e:
                    print(f"Müzik dosyası yüklenirken hata oluştu: {e}")
                    continue
        
        print("Uygun müzik dosyası bulunamadı!")
        return False
        
    except Exception as e:
        print(f"Müzik yükleme işleminde hata oluştu: {e}")
        return False 