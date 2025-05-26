import os
import sys
import pygame
import numpy

# Add parent directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Use absolute imports
from menu.config import (
    screen, SCREEN_WIDTH, SCREEN_HEIGHT, DARK_GRAY, ORANGE, 
    DEFAULT_MUSIC_VOLUME, DEFAULT_SOUND_VOLUME, DEFAULT_BRIGHTNESS,
    MIN_BRIGHTNESS, GAME_TITLE, DEFAULT_TOKENS, ICONS
)
from menu.assets import load_background, load_samurai_characters, load_font, load_and_play_music
from menu.scenes import (
    MainScene, OptionsScene, SettingsScene, LoginScene, ShopScene, LevelSelectScene, LeaderboardScene
)

class Menu:
    def __init__(self):
        # Pygame display
        self.screen = screen
        pygame.display.set_caption("The Way")
        
        # Arkaplan ve karakterler
        self.background = load_background()
        self.samurai_left, self.samurai_right = load_samurai_characters()
        
        # Yazı tipi
        self.title_font = load_font(90, bold=True)
        
        # Müzik yükleme
        load_and_play_music()
        
        # Token ve ayarlar
        self.current_tokens = DEFAULT_TOKENS
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sound_volume = DEFAULT_SOUND_VOLUME
        self.brightness = DEFAULT_BRIGHTNESS
        
        # Kullanıcı bilgileri
        self.logged_in_user = ""
        self.login_error = ""
        
        # Durum değişkenleri
        self.show_level_selection = False
        self.show_login_screen = False
        self.show_login_confirm = False
        self.show_shop_screen = False
        self.show_confirm_dialog = False
        self.confirm_skill = None
        self.shop_error = ""
        self.shop_error_timer = 0
        
        # Ekran parlaklığı için overlay
        self.brightness_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Tam ekran kontrolü
        self.fullscreen = False
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Sahneleri oluştur
        self.scenes = {
            "main": MainScene(self),
            "options": OptionsScene(self),
            "settings": SettingsScene(self),
            "login": LoginScene(self),
            "shop": ShopScene(self),
            "level_select": LevelSelectScene(self),
            "leaderboard": LeaderboardScene(self)
        }
        
        # Aktif sahne
        self.current_scene_name = "main"
        self.current_scene = self.scenes[self.current_scene_name]
        self.current_scene.enter()
    
    def set_scene(self, scene_name):
        """Sahne değiştir"""
        if scene_name in self.scenes:
            self.current_scene.exit()
            self.current_scene_name = scene_name
            self.current_scene = self.scenes[scene_name]
            self.current_scene.enter()
            print(f"Sahne değiştirildi: {scene_name}")
    
    def handle_events(self):
        """Kullanıcı girdilerini işle"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # F11 tuşu ile tam ekran modu değiştirme
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    self.handle_escape_key()
        
        # Aktif sahnenin olaylarını işle
        self.current_scene.handle_events(events)
    
    def handle_escape_key(self):
        """Escape tuşuna basıldığında uygun işlemi yap"""
        if self.show_confirm_dialog:
            self.show_confirm_dialog = False
            self.confirm_skill = None
        elif self.show_login_confirm:
            self.show_login_confirm = False
        elif self.current_scene_name == "settings":
            self.set_scene("options")
        elif self.current_scene_name == "options":
            self.set_scene("main")
        elif self.show_level_selection:
            self.show_level_selection = False
            self.set_scene("options")
        elif self.show_login_screen:
            self.show_login_screen = False
            self.set_scene("main")
        elif self.show_shop_screen:
            self.show_shop_screen = False
            self.set_scene("main")
        else:
            self.confirm_quit()
    
    def update(self):
        """Menüdeki tüm öğeleri güncelle"""
        # Aktif sahneyi güncelle
        self.current_scene.update()
        
        # Ayarlar sahnesi aktifse müzik ve parlaklık ayarlarını güncelle
        if self.current_scene_name == "settings":
            # Müzik ses seviyesini güncelle
            try:
                pygame.mixer.music.set_volume(self.music_volume)
            except:
                pass
    
    def render(self):
        """Menüyü ekrana çiz"""
        # Arka planı çiz
        self.screen.blit(self.background, (0, 0))
        
        # Samuray karakterleri için arkaplanda küçük siyah dikdörtgenler
        left_cover = pygame.Rect(50, SCREEN_HEIGHT // 2 + 50, 130, 120)
        pygame.draw.rect(self.screen, DARK_GRAY, left_cover)
        
        right_cover = pygame.Rect(SCREEN_WIDTH - 190, SCREEN_HEIGHT // 2 + 50, 120, 120)
        pygame.draw.rect(self.screen, DARK_GRAY, right_cover)
        
        # Samuray karakterlerini çiz (eğer yüklendiyse)
        if self.samurai_left:
            samurai_left_rect = self.samurai_left.get_rect(center=(140, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(self.samurai_left, samurai_left_rect)
            
        if self.samurai_right:
            samurai_right_rect = self.samurai_right.get_rect(center=(SCREEN_WIDTH - 130, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(self.samurai_right, samurai_right_rect)
        
        # Başlığı çiz
        title_shadow_offset = 4
        
        # Önce gölgeyi çiz
        title_shadow = self.title_font.render(GAME_TITLE, True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(midtop=(SCREEN_WIDTH//2 + title_shadow_offset, 
                                                          80 + title_shadow_offset))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        # Sonra ana başlığı çiz
        title_surface = self.title_font.render(GAME_TITLE, True, ORANGE)
        title_rect = title_surface.get_rect(midtop=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title_surface, title_rect)
        
        # Kullanıcı bilgisini göster
        if self.logged_in_user:
            user_font = load_font(20, bold=True)
            user_text = f"{self.logged_in_user}"
            user_surface = user_font.render(user_text, True, (220, 60, 40))  # Kırmızı renk
            self.screen.blit(user_surface, (20, 20))
        
        # Tam ekran bilgisi
        fullscreen_font = load_font(16)
        fullscreen_text = "F11: Tam Ekran Modu"
        fullscreen_surface = fullscreen_font.render(fullscreen_text, True, (180, 180, 190))
        self.screen.blit(fullscreen_surface, (SCREEN_WIDTH - fullscreen_surface.get_width() - 10, SCREEN_HEIGHT - 30))
        
        # Aktif sahneyi çiz
        self.current_scene.draw()
        
        # Parlaklık ayarını uygula
        if self.brightness != 50:  # Varsayılan parlaklıkta değilse
            if self.brightness < 50:  # Karartma
                self.brightness_overlay.fill((0, 0, 0))
                alpha = int((50 - self.brightness) * 2.5)  # 10% -> alpha 100, 50% -> alpha 0
            else:  # Aydınlatma
                self.brightness_overlay.fill((255, 255, 255))
                alpha = int((self.brightness - 50) * 1.5)  # 50% -> alpha 0, 100% -> alpha 75
            
            # Alpha değerini sınırla
            alpha = min(100, alpha)  # Maksimum karartma/aydınlatma sınırı
            self.brightness_overlay.set_alpha(alpha)
            self.screen.blit(self.brightness_overlay, (0, 0))
        
        # Ekranı güncelle
        pygame.display.flip()
    
    def run(self):
        """Ana döngü"""
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.update()
            self.render()
            clock.tick(60)  # 60 FPS
    
    # Buton işlevleri
    def start_game(self):
        print("Oyun başlatılıyor...")
        pygame.quit()  # Mevcut pygame penceresini kapat
        
        # player.py'yi çalıştır
        import subprocess
        
        # Geçerli dizini al
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        player_path = os.path.join(current_dir, "player.py")
        
        # Python yorumlayıcısını kullanarak player.py'yi çalıştır
        subprocess.run([sys.executable, player_path])
        
        # Oyun kapandığında programı sonlandır
        sys.exit()
    
    def resume_game(self):
        print("Oyuna devam ediliyor...")
        self.set_scene("main")
    
    def restart_game(self):
        print("Oyun yeniden başlatılıyor...")
        # Tüm ilerlemeyi sıfırla
        
        # Kullanıcı bilgilerini sıfırla
        self.logged_in_user = ""
        self.scenes["login"].nickname_input.text = ""
        self.scenes["login"].password_input.text = ""
        self.login_error = ""
        
        # Token ve satın almaları sıfırla
        self.current_tokens = DEFAULT_TOKENS
        for skill in self.scenes["shop"].shop_skills:
            skill.is_purchased = False
        
        # Level ilerlemesini sıfırla - sadece 5 seviye için
        for button in self.scenes["level_select"].level_buttons:
            button.is_completed = (button.level_number <= 3)  # İlk 3 seviye açık
        
        # Ayarları varsayılan değerlere sıfırla
        self.music_volume = DEFAULT_MUSIC_VOLUME
        self.sound_volume = DEFAULT_SOUND_VOLUME
        self.brightness = DEFAULT_BRIGHTNESS
        
        # Ana menüye dön
        self.set_scene("main")
        
        print("Tüm oyun ilerlemeniz sıfırlandı.")
    
    def show_levels(self):
        print("Seviye seçimi gösteriliyor...")
        self.show_level_selection = True
        self.set_scene("level_select")
    
    def show_leaderboard(self):
        print("Liderlik tablosu gösteriliyor...")
        self.set_scene("leaderboard")
    
    def show_shop(self):
        print("Mağaza açılıyor...")
        self.show_shop_screen = True
        self.set_scene("shop")
    
    def show_login(self):
        print("Giriş sayfası açılıyor...")
        self.show_login_screen = True
        self.login_error = ""
        self.set_scene("login")
    
    def toggle_music(self):
        """Müziği açar/kapatır"""
        try:
            if pygame.mixer.music.get_busy():  # Müzik çalıyorsa
                if self.music_volume > 0:
                    pygame.mixer.music.pause()
                    self.music_volume = 0
                else:
                    pygame.mixer.music.unpause()
                    self.music_volume = 0.7
            else:  # Müzik çalmıyorsa yeniden başlat
                load_and_play_music()
                self.music_volume = 0.7
            
            pygame.mixer.music.set_volume(self.music_volume)
            print(f"Müzik {'açık' if self.music_volume > 0 else 'kapalı'}")
        except Exception as e:
            print(f"Müzik kontrolünde hata: {e}")
    
    def toggle_sound(self):
        self.sound_volume = 0 if self.sound_volume > 0 else 0.5
        print(f"Ses {'açık' if self.sound_volume > 0 else 'kapalı'}")
    
    def adjust_brightness(self):
        """Parlaklık ayarını günceller"""
        try:
            # Brightness slider'dan gelen değeri kullan ve minimum sınırı uygula
            self.brightness = max(MIN_BRIGHTNESS, self.brightness)
            print(f"Parlaklık: {self.brightness}%")
        except Exception as e:
            print(f"Parlaklık ayarlanırken hata oluştu: {e}")
    
    def toggle_fullscreen(self):
        """Tam ekran modunu değiştir"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
            print("Tam ekran moduna geçildi")
        else:
            self.screen = pygame.display.set_mode(self.window_size)
            print("Pencere moduna geçildi")
    
    def confirm_quit(self):
        """Oyundan çıkılıyor"""
        self.quit_game()
    
    def quit_game(self):
        pygame.quit()
        sys.exit() 