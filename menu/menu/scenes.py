import pygame
import sys
import os
import numpy

# Add parent directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from menu.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ORANGE, DARK_GRAY, GREEN, BLUE, RED, CYAN, 
    WHITE, BLACK, DARK_ORANGE, LIGHT_GRAY, GOLD, ICONS, BUTTON_WIDTH, 
    BUTTON_HEIGHT, BUTTON_SPACING, PANEL_WIDTH, PANEL_HEIGHT, GAME_TITLE
)
from menu.assets import load_font
from menu.ui import (
    PixelButton, LevelCompleteButton, Slider, TextInputBox, ShopSkill
)

class BaseScene:
    """Temel sahne sınıfı - diğer tüm sahneler bundan türetilir"""
    def __init__(self, menu):
        self.menu = menu
        self.screen = menu.screen
        self.active = False
    
    def enter(self):
        """Sahneye girildiğinde çağrılır"""
        self.active = True
    
    def exit(self):
        """Sahneden çıkıldığında çağrılır"""
        self.active = False
    
    def handle_events(self, events):
        """Olay işleme"""
        pass
    
    def update(self):
        """Güncelleme"""
        pass
    
    def draw(self):
        """Çizim"""
        pass

    def _draw_panel(self, title=None, title_color=ORANGE):
        """Standart panel çizimi"""
        # Panel pozisyonu
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        # Panel arka planı
        panel_rect = pygame.Rect(panel_x, panel_y, PANEL_WIDTH, PANEL_HEIGHT)
        
        # Koyu kenar rengi
        dark_border = (DARK_ORANGE[0]//2, DARK_ORANGE[1]//2, DARK_ORANGE[2]//2)
        
        # Panel gölgesi
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        # Panel arka planı
        pygame.draw.rect(self.screen, dark_border, panel_rect, border_radius=12)
        
        # İç panel
        inner_panel = pygame.Rect(panel_x + 6, panel_y + 6, 
                                 PANEL_WIDTH - 12, PANEL_HEIGHT - 12)
        pygame.draw.rect(self.screen, DARK_GRAY, inner_panel, border_radius=8)
        
        # Panel başlığı
        if title:
            title_font = load_font(36, bold=True)
            title_surface = title_font.render(title, True, title_color)
            title_rect = title_surface.get_rect(midtop=(panel_x + PANEL_WIDTH//2, panel_y + 10))
            self.screen.blit(title_surface, title_rect)
            
            # Dekoratif kenar efekti
            top_highlight = pygame.Rect(panel_x + 8, panel_y + 45, PANEL_WIDTH - 16, 2)
            pygame.draw.rect(self.screen, ORANGE, top_highlight, border_radius=1)
        
        return panel_x, panel_y

class MainScene(BaseScene):
    """Ana menü sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Ana menü butonlarını hazırla
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        self.buttons = [
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60,
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "PLAY", self.start_game, ICONS["play"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "SHOP", self.show_shop, ICONS["shop"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + 2 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "LEADERBOARD", self.show_leaderboard, ICONS["leaderboard"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + 3 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "OPTIONS", self.show_options_menu, ICONS["options"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + 4 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "LOGIN", self.login, ICONS["login"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            )
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            button.check_hover(mouse_pos)
            for event in events:
                if button.handle_event(event):
                    return True
    
    def update(self):
        for button in self.buttons:
            button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="MAIN MENU", title_color=ORANGE)
        
        # Butonları çiz
        for button in self.buttons:
            button.draw(self.screen)
    
    # Buton işlevleri
    def start_game(self):
        self.menu.start_game()
    
    def show_shop(self):
        self.menu.show_shop()
    
    def show_leaderboard(self):
        self.menu.show_leaderboard()
    
    def show_options_menu(self):
        self.menu.set_scene("options")
    
    def login(self):
        self.menu.show_login()

class OptionsScene(BaseScene):
    """Oyun içi seçenekler sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Geri butonu
        self.back_button = PixelButton(
            50, 50, 120, 40, "BACK", self.go_back, ICONS["back"]
        )
        
        # Options butonlarını hazırla
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        self.buttons = [
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60,
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "RESUME", self.resume_game, ICONS["resume"],
                colors=(DARK_GRAY, GREEN, GREEN)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "RESTART", self.restart_game, ICONS["restart"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + 2 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "LEVELS", self.show_levels, ICONS["levels"],
                colors=(DARK_GRAY, CYAN, CYAN)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + 3 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "SETTINGS", self.show_settings_menu, ICONS["settings"],
                colors=(DARK_GRAY, BLUE, BLUE)
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 60 + 4 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "QUIT", self.confirm_quit, ICONS["quit"],
                colors=(DARK_GRAY, RED, RED)
            )
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Back butonu
        self.back_button.check_hover(mouse_pos)
        for event in events:
            if self.back_button.handle_event(event):
                return True
        
        # Diğer butonlar
        for button in self.buttons:
            button.check_hover(mouse_pos)
            for event in events:
                if button.handle_event(event):
                    return True
    
    def update(self):
        self.back_button.update()
        for button in self.buttons:
            button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="OPTIONS", title_color=GREEN)
        
        # Geri butonunu çiz
        self.back_button.draw(self.screen)
        
        # Butonları çiz
        for button in self.buttons:
            button.draw(self.screen)
    
    # Buton işlevleri
    def go_back(self):
        self.menu.set_scene("main")
    
    def resume_game(self):
        self.menu.resume_game()
    
    def restart_game(self):
        self.menu.restart_game()
    
    def show_levels(self):
        self.menu.show_levels()
    
    def show_settings_menu(self):
        self.menu.set_scene("settings")
    
    def confirm_quit(self):
        self.menu.confirm_quit()

class SettingsScene(BaseScene):
    """Ayarlar sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Geri butonu
        self.back_button = PixelButton(
            50, 50, 120, 40, "BACK", self.go_back, ICONS["back"]
        )
        
        # Panel pozisyonu
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        # Ayarlar butonları
        self.settings_buttons = [
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 70,
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "MUSIC", self.toggle_music, ICONS["music"]
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 110 + (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "SOUND", self.toggle_sound, ICONS["sound"]
            ),
            PixelButton(
                panel_x + (PANEL_WIDTH - BUTTON_WIDTH) // 2,
                panel_y + 140 + 2 * (BUTTON_HEIGHT + BUTTON_SPACING),
                BUTTON_WIDTH, BUTTON_HEIGHT, 
                "BRIGHTNESS", self.adjust_brightness, ICONS["bright"]
            )
        ]
        
        # Kaydırıcılar
        self.music_slider = Slider(
            panel_x + 50, 
            panel_y + 130,
            PANEL_WIDTH - 100, 
            40,
            current_val=self.menu.music_volume * 100,
            icon=ICONS["music"]
        )
        
        self.sound_slider = Slider(
            panel_x + 50, 
            panel_y + 130 + 120,
            PANEL_WIDTH - 100, 
            40,
            current_val=self.menu.sound_volume * 100,
            icon=ICONS["sound"]
        )
        
        self.brightness_slider = Slider(
            panel_x + 50, 
            panel_y + 130 + 230,
            PANEL_WIDTH - 100, 
            40,
            min_val=10,  # Minimum değer 10%
            current_val=self.menu.brightness,
            icon=ICONS["bright"]
        )
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Back butonu
        self.back_button.check_hover(mouse_pos)
        for event in events:
            if self.back_button.handle_event(event):
                return True
        
        # Kaydırıcılar
        self.music_slider.update(events, mouse_pos)
        self.sound_slider.update(events, mouse_pos)
        self.brightness_slider.update(events, mouse_pos)
        
        # Butonlar
        for button in self.settings_buttons:
            button.check_hover(mouse_pos)
            for event in events:
                if button.handle_event(event):
                    return True
        
        # Kaydırıcı değerlerini senkronize et
        self.menu.music_volume = self.music_slider.current_val / 100
        self.menu.sound_volume = self.sound_slider.current_val / 100
        self.menu.brightness = self.brightness_slider.current_val
        
        return False
    
    def update(self):
        self.back_button.update()
        for button in self.settings_buttons:
            button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="SETTINGS", title_color=CYAN)
        
        # Geri butonunu çiz
        self.back_button.draw(self.screen)
        
        # Butonları çiz
        for button in self.settings_buttons:
            button.draw(self.screen)
        
        # Kaydırıcıları çiz
        self.music_slider.draw(self.screen)
        self.sound_slider.draw(self.screen)
        self.brightness_slider.draw(self.screen)
    
    # Buton işlevleri
    def go_back(self):
        self.menu.set_scene("options")
    
    def toggle_music(self):
        self.menu.toggle_music()
        # Slider'ı güncelle
        self.music_slider.current_val = self.menu.music_volume * 100
    
    def toggle_sound(self):
        self.menu.toggle_sound()
        # Slider'ı güncelle
        self.sound_slider.current_val = self.menu.sound_volume * 100
    
    def adjust_brightness(self):
        self.menu.adjust_brightness()
        # Slider'ı güncelle
        self.brightness_slider.current_val = self.menu.brightness

class LoginScene(BaseScene):
    """Giriş ekranı sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Panel pozisyonu
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        # Geri butonu
        self.back_button = PixelButton(
            50, 50, 120, 40, "BACK", self.go_back, ICONS["back"]
        )
        
        # Metin giriş kutuları
        self.nickname_input = TextInputBox(
            panel_x + 150, 
            panel_y + 120, 
            200, 40, 
            placeholder="nickname",
            max_length=15  # Maksimum karakter sınırı
        )
        
        self.password_input = TextInputBox(
            panel_x + 150, 
            panel_y + 180, 
            200, 40, 
            placeholder="password", 
            is_password=True
        )
        
        # Login butonu
        self.login_button = PixelButton(
            panel_x + (PANEL_WIDTH - 120) // 2,
            panel_y + 240,
            120, 40, 
            "LOGIN", self.process_login
        )
        
        # Onay kutusu ve butonları
        self.confirm_dialog_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 200, 
            SCREEN_HEIGHT // 2 - 100,
            400, 200
        )
        
        self.confirm_yes_button = PixelButton(
            self.confirm_dialog_rect.x + 60,
            self.confirm_dialog_rect.y + 120,
            120, 40, 
            "EVET", self.confirm_login
        )
        
        self.confirm_no_button = PixelButton(
            self.confirm_dialog_rect.x + 220,
            self.confirm_dialog_rect.y + 120,
            120, 40, 
            "HAYIR", self.cancel_login,
            colors=(DARK_GRAY, RED, RED)
        )
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Onay kutusu açıksa, sadece onay butonlarını işle
        if self.menu.show_login_confirm:
            self.confirm_yes_button.check_hover(mouse_pos)
            self.confirm_no_button.check_hover(mouse_pos)
            
            for event in events:
                if self.confirm_yes_button.handle_event(event):
                    return True
                if self.confirm_no_button.handle_event(event):
                    return True
                
                # Kutu dışına tıklandıysa kapat
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.confirm_dialog_rect.collidepoint(mouse_pos):
                        self.menu.show_login_confirm = False
            
            return False
        
        # Normal login ekranı
        self.back_button.check_hover(mouse_pos)
        self.login_button.check_hover(mouse_pos)
        
        for event in events:
            if self.back_button.handle_event(event):
                return True
            if self.login_button.handle_event(event):
                return True
            
            # Text input'ları güncelle
            if self.nickname_input.update(event):
                pass  # Enter tuşuna basıldığında bir şey yapma
            
            if self.password_input.update(event):
                self.process_login()  # Enter tuşuna basınca form gönder
    
    def update(self):
        self.back_button.update()
        self.login_button.update()
        
        if self.menu.show_login_confirm:
            self.confirm_yes_button.update()
            self.confirm_no_button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="LOGIN", title_color=BLUE)
        
        # Geri butonunu çiz
        self.back_button.draw(self.screen)
        
        # İkonları çiz
        user_font = load_font(24)
        user_icon = user_font.render(ICONS["login"], True, ORANGE)
        password_icon = user_font.render("🔑", True, ORANGE)
        
        self.screen.blit(user_icon, (panel_x + 100, panel_y + 120 + 20))
        self.screen.blit(password_icon, (panel_x + 100, panel_y + 180 + 20))
        
        # Text inputları çiz
        self.nickname_input.draw(self.screen)
        self.password_input.draw(self.screen)
        
        # Login butonu
        self.login_button.draw(self.screen)
        
        # Hata mesajı (varsa)
        if self.menu.login_error:
            error_font = load_font(18)
            error_surface = error_font.render(self.menu.login_error, True, RED)
            error_rect = error_surface.get_rect(center=(panel_x + PANEL_WIDTH//2, panel_y + 300))
            self.screen.blit(error_surface, error_rect)
        
        # Login onay kutusu (varsa)
        if self.menu.show_login_confirm:
            # Karartma arka planı
            darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            darken.fill((0, 0, 0, 150))  # Yarı-saydam siyah
            self.screen.blit(darken, (0, 0))
            
            # Onay kutusu
            pygame.draw.rect(self.screen, DARK_GRAY, self.confirm_dialog_rect, border_radius=10)
            pygame.draw.rect(self.screen, ORANGE, self.confirm_dialog_rect, width=3, border_radius=10)
            
            # Başlık
            dialog_title_font = load_font(24, bold=True)
            dialog_title = "HESAP OLUSTURMA ONAYI"
            dialog_title_surf = dialog_title_font.render(dialog_title, True, ORANGE)
            dialog_title_rect = dialog_title_surf.get_rect(midtop=(self.confirm_dialog_rect.centerx, self.confirm_dialog_rect.y + 15))
            self.screen.blit(dialog_title_surf, dialog_title_rect)
            
            # Uyarı metni
            warning_font = load_font(20)
            warning_text1 = "Sadece 1 kere isim seçebilirsiniz."
            warning_text2 = "Bu ismi kullanmak istediginizden"
            warning_text3 = "emin misiniz?"
            
            text_y = self.confirm_dialog_rect.y + 50
            warning_surf1 = warning_font.render(warning_text1, True, RED)
            warning_rect1 = warning_surf1.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
            self.screen.blit(warning_surf1, warning_rect1)
            
            text_y += 25
            warning_surf2 = warning_font.render(warning_text2, True, WHITE)
            warning_rect2 = warning_surf2.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
            self.screen.blit(warning_surf2, warning_rect2)
            
            text_y += 25
            warning_surf3 = warning_font.render(warning_text3, True, WHITE)
            warning_rect3 = warning_surf3.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
            self.screen.blit(warning_surf3, warning_rect3)
            
            # Butonları çiz
            self.confirm_yes_button.draw(self.screen)
            self.confirm_no_button.draw(self.screen)
    
    # Buton işlevleri
    def go_back(self):
        self.menu.set_scene("main")
        self.menu.show_login_screen = False
    
    def process_login(self):
        if not self.nickname_input.text or not self.password_input.text:
            self.menu.login_error = "Kullanıcı adı ve sifre gerekli!"
            return
        
        # Eğer kullanıcı zaten kayıtlıysa ve farklı bir isimle giriş yapmaya çalışıyorsa
        if self.menu.logged_in_user and self.nickname_input.text != self.menu.logged_in_user:
            self.menu.login_error = "Daha önce kayıt yapıldı!"
            return
        
        # Eğer kullanıcı kayıtlı değilse onay kutusunu göster
        if not self.menu.logged_in_user:
            self.menu.show_login_confirm = True
        else:
            # Kendi hesabıyla giriş yapıyorsa direkt ana menüye dön
            self.menu.show_login_screen = False
            self.menu.set_scene("main")
            print(f"Giriş yapıldı: {self.menu.logged_in_user}")
    
    def confirm_login(self):
        """Login işlemini onayla"""
        self.menu.logged_in_user = self.nickname_input.text
        self.menu.show_login_screen = False
        self.menu.show_login_confirm = False
        self.menu.set_scene("main")
        print(f"Hesap oluşturuldu: {self.menu.logged_in_user}")
    
    def cancel_login(self):
        """Login işlemini iptal et"""
        self.menu.show_login_confirm = False
        self.nickname_input.text = ""
        self.password_input.text = ""
        print("Hesap oluşturma iptal edildi.")

class ShopScene(BaseScene):
    """Yetenekler mağazası sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Panel pozisyonu
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        # Geri butonu
        self.back_button = PixelButton(
            50, 50, 120, 40, "BACK", self.go_back, ICONS["back"]
        )
        
        # Yetenekler
        self.shop_skills = [
            ShopSkill(
                panel_x + 50, 
                panel_y + 100, 
                PANEL_WIDTH - 100, 
                80, 
                "Lightning", 500, 
                icon="⚡"
            ),
            ShopSkill(
                panel_x + 50, 
                panel_y + 190, 
                PANEL_WIDTH - 100, 
                80, 
                "Lightning Bolt", 9000, 
                icon="🔷"
            ),
            ShopSkill(
                panel_x + 50, 
                panel_y + 280, 
                PANEL_WIDTH - 100, 
                80, 
                "Midas Touch", 50000, 
                icon="👆"
            ),
            ShopSkill(
                panel_x + 50, 
                panel_y + 370, 
                PANEL_WIDTH - 100, 
                80, 
                "Sun Strike", 100000, 
                icon="☀️"
            )
        ]
        
        # Satın alma onay kutusu
        self.confirm_dialog_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 150, 
            SCREEN_HEIGHT // 2 - 100,
            300, 200
        )
        
        # Onay butonları
        self.confirm_yes_button = PixelButton(
            self.confirm_dialog_rect.x + 40,
            self.confirm_dialog_rect.y + 120,
            100, 40, 
            "EVET", self.confirm_purchase
        )
        
        self.confirm_no_button = PixelButton(
            self.confirm_dialog_rect.x + 160,
            self.confirm_dialog_rect.y + 120,
            100, 40, 
            "HAYIR", self.cancel_purchase,
            colors=(DARK_GRAY, RED, RED)
        )
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Onay kutusu açıksa, sadece onay butonlarını işle
        if self.menu.show_confirm_dialog:
            self.confirm_yes_button.check_hover(mouse_pos)
            self.confirm_no_button.check_hover(mouse_pos)
            
            for event in events:
                if self.confirm_yes_button.handle_event(event):
                    return True
                if self.confirm_no_button.handle_event(event):
                    return True
                
                # Kutu dışına tıklandıysa kapat
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.confirm_dialog_rect.collidepoint(mouse_pos):
                        self.menu.show_confirm_dialog = False
                        self.menu.confirm_skill = None
            
            return False
        
        # Normal shop ekranı
        self.back_button.check_hover(mouse_pos)
        
        # Yetenekleri güncelle
        for skill in self.shop_skills:
            skill.check_hover(mouse_pos)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and skill.is_hovered and not skill.is_purchased:
                    # Onay kutusu göster
                    self.menu.show_confirm_dialog = True
                    self.menu.confirm_skill = skill
                    return True
        
        for event in events:
            if self.back_button.handle_event(event):
                return True
    
    def update(self):
        self.back_button.update()
        
        # Yetenekleri güncelle
        for skill in self.shop_skills:
            skill.update()
        
        # Hata mesajı süresi doldu mu?
        if self.menu.shop_error and pygame.time.get_ticks() - self.menu.shop_error_timer > 3000:  # 3 saniye
            self.menu.shop_error = ""
        
        # Onay butonları
        if self.menu.show_confirm_dialog:
            self.confirm_yes_button.update()
            self.confirm_no_button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="BUY SKILLS", title_color=GOLD)
        
        # Geri butonunu çiz
        self.back_button.draw(self.screen)
        
        # Token bilgisi
        token_font = load_font(24, bold=False)
        token_text = f"Current Tokens: {self.menu.current_tokens}"
        token_surface = token_font.render(token_text, True, GOLD)
        token_rect = token_surface.get_rect(midtop=(panel_x + PANEL_WIDTH//2, panel_y + 60))
        self.screen.blit(token_surface, token_rect)
        
        # Yetenekleri çiz
        for skill in self.shop_skills:
            skill.draw(self.screen)
        
        # Hata mesajı (varsa)
        if self.menu.shop_error:
            error_font = load_font(20, bold=True)
            error_surface = error_font.render(self.menu.shop_error, True, RED)
            error_rect = error_surface.get_rect(midbottom=(panel_x + PANEL_WIDTH//2, panel_y + PANEL_HEIGHT - 20))
            self.screen.blit(error_surface, error_rect)
        
        # Onay kutusu (varsa)
        if self.menu.show_confirm_dialog and self.menu.confirm_skill:
            # Karartma arka planı (ekranın tamamını biraz karartalım)
            darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            darken.fill((0, 0, 0, 150))  # Yarı-saydam siyah
            self.screen.blit(darken, (0, 0))
            
            # Onay kutusu
            pygame.draw.rect(self.screen, DARK_GRAY, self.confirm_dialog_rect, border_radius=10)
            pygame.draw.rect(self.screen, ORANGE, self.confirm_dialog_rect, width=3, border_radius=10)
            
            # Başlık
            dialog_title_font = load_font(24, bold=True)
            dialog_title = "SATIN ALMA ONAYI"
            dialog_title_surf = dialog_title_font.render(dialog_title, True, ORANGE)
            dialog_title_rect = dialog_title_surf.get_rect(midtop=(self.confirm_dialog_rect.centerx, self.confirm_dialog_rect.y + 15))
            self.screen.blit(dialog_title_surf, dialog_title_rect)
            
            # Onay metni
            confirm_font = load_font(20)
            skill_name = self.menu.confirm_skill.name
            confirm_text = f"{skill_name} yetenegini"
            confirm_text2 = f"{self.menu.confirm_skill.cost} token ile"
            confirm_text3 = " satın almak istiyor musunuz?"
            
            text_y = self.confirm_dialog_rect.y + 50
            confirm_surf = confirm_font.render(confirm_text, True, WHITE)
            confirm_rect = confirm_surf.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
            self.screen.blit(confirm_surf, confirm_rect)
            
            text_y += 25
            confirm_surf2 = confirm_font.render(confirm_text2, True, GOLD)
            confirm_rect2 = confirm_surf2.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
            self.screen.blit(confirm_surf2, confirm_rect2)
            
            text_y += 25
            confirm_surf3 = confirm_font.render(confirm_text3, True, WHITE)
            confirm_rect3 = confirm_surf3.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
            self.screen.blit(confirm_surf3, confirm_rect3)
            
            # Butonları çiz
            self.confirm_yes_button.draw(self.screen)
            self.confirm_no_button.draw(self.screen)
    
    # Buton işlevleri
    def go_back(self):
        self.menu.set_scene("main")
        self.menu.show_shop_screen = False
    
    def confirm_purchase(self):
        """Satın alma işlemini onayla"""
        if self.menu.confirm_skill:
            success, new_tokens, error = self.menu.confirm_skill.handle_click(self.menu.current_tokens)
            if success:
                self.menu.current_tokens = new_tokens
                print(f"{self.menu.confirm_skill.name} satın alındı! Kalan token: {self.menu.current_tokens}")
            elif error:
                self.menu.shop_error = error
                self.menu.shop_error_timer = pygame.time.get_ticks()
                print(f"Satın alma hatası: {error}")
        
        # Onay kutusunu kapat
        self.menu.show_confirm_dialog = False
        self.menu.confirm_skill = None
    
    def cancel_purchase(self):
        """Satın alma işlemini iptal et"""
        self.menu.show_confirm_dialog = False
        self.menu.confirm_skill = None
        print("Satın alma iptal edildi.")

class LevelSelectScene(BaseScene):
    """Seviye seçim sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Geri butonu
        self.back_button = PixelButton(
            50, 50, 120, 40, "BACK", self.go_back, ICONS["back"]
        )
        
        # Seviye butonları için grid düzeni
        small_button_width = 100
        small_button_height = 100
        small_button_spacing = 25
        levels_per_row = 3
        
        # Seviye butonları için başlangıç konumu
        level_start_x = SCREEN_WIDTH // 2 - (small_button_width * 1.5 + small_button_spacing)
        level_start_y = SCREEN_HEIGHT // 2 - small_button_height
        
        # 5 seviye oluştur - 3+2 grid formatında
        self.level_buttons = []
        for i in range(5):  # 9 yerine 5 seviye
            row = i // levels_per_row
            col = i % levels_per_row
            
            level_x = level_start_x + col * (small_button_width + small_button_spacing)
            level_y = level_start_y + row * (small_button_height + small_button_spacing)
            
            # İlk 3 seviye açık, diğerleri kilitli - sadece örnek olarak
            is_completed = (i < 3)
            
            self.level_buttons.append(
                LevelCompleteButton(
                    level_x, level_y, 
                    small_button_width, small_button_height, 
                    i + 1, is_completed, 
                    lambda level=i+1: self.start_level(level)
                )
            )
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Back butonu
        self.back_button.check_hover(mouse_pos)
        for event in events:
            if self.back_button.handle_event(event):
                return True
        
        # Seviye butonları
        for button in self.level_buttons:
            button.check_hover(mouse_pos)
            for event in events:
                if button.handle_event(event):
                    return True
    
    def update(self):
        self.back_button.update()
        for button in self.level_buttons:
            button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="SELECT LEVEL", title_color=CYAN)
        
        # Geri butonunu çiz
        self.back_button.draw(self.screen)
        
        # Seviye butonlarını çiz
        for button in self.level_buttons:
            button.draw(self.screen)
    
    # Buton işlevleri
    def go_back(self):
        self.menu.set_scene("options")
        self.menu.show_level_selection = False
    
    def start_level(self, level):
        print(f"Seviye {level} başlatılıyor...")
        self.menu.show_level_selection = False
        # Seviye başlatma kodları buraya gelecek 

class LeaderboardScene(BaseScene):
    """Liderlik tablosu sahnesi"""
    def __init__(self, menu):
        super().__init__(menu)
        
        # Panel pozisyonu
        panel_x = (SCREEN_WIDTH - PANEL_WIDTH) // 2
        panel_y = (SCREEN_HEIGHT - PANEL_HEIGHT) // 2 + 50
        
        # Geri butonu
        self.back_button = PixelButton(
            50, 50, 120, 40, "BACK", self.go_back, ICONS["back"]
        )
        
        # Başlık yazı tipi
        self.title_font = load_font(24, bold=True)
        self.text_font = load_font(20)
        
        # Tablo başlıkları
        self.headers = [
            "LEVEL",
            "CURRENT-T",
            "BEST-T"
        ]
        
        # Örnek veriler (gerçek veriler oyun ilerledikçe güncellenecek)
        self.leaderboard_data = [
            {"level": 1, "current_time": "02:30", "best_time": "01:45"},
            {"level": 2, "current_time": "03:15", "best_time": "02:30"},
            {"level": 3, "current_time": "04:00", "best_time": "03:20"},
            {"level": 4, "current_time": "--:--", "best_time": "--:--"},
            {"level": 5, "current_time": "--:--", "best_time": "--:--"}
        ]
    
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        
        # Back butonu
        self.back_button.check_hover(mouse_pos)
        for event in events:
            if self.back_button.handle_event(event):
                return True
    
    def update(self):
        self.back_button.update()
    
    def draw(self):
        panel_x, panel_y = self._draw_panel(title="LEADERBOARD 🏆", title_color=GOLD)
        
        # Geri butonunu çiz
        self.back_button.draw(self.screen)
        
        # Tablo başlıklarını çiz
        header_y = panel_y + 100
        header_spacing = PANEL_WIDTH // len(self.headers)
        
        for i, header in enumerate(self.headers):
            header_surface = self.title_font.render(header, True, ORANGE)
            header_rect = header_surface.get_rect(
                midtop=(panel_x + header_spacing * (i + 0.5), header_y)
            )
            self.screen.blit(header_surface, header_rect)
        
        # Tablo verilerini çiz
        data_start_y = header_y + 40
        row_height = 40
        
        for i, row in enumerate(self.leaderboard_data):
            # Level numarası
            level_text = f"LEVEL {row['level']}"
            level_surface = self.text_font.render(level_text, True, WHITE)
            level_rect = level_surface.get_rect(
                midtop=(panel_x + header_spacing * 0.5, data_start_y + i * row_height)
            )
            self.screen.blit(level_surface, level_rect)
            
            # Mevcut süre
            current_time_surface = self.text_font.render(row['current_time'], True, CYAN)
            current_time_rect = current_time_surface.get_rect(
                midtop=(panel_x + header_spacing * 1.5, data_start_y + i * row_height)
            )
            self.screen.blit(current_time_surface, current_time_rect)
            
            # En iyi süre
            best_time_surface = self.text_font.render(row['best_time'], True, GREEN)
            best_time_rect = best_time_surface.get_rect(
                midtop=(panel_x + header_spacing * 2.5, data_start_y + i * row_height)
            )
            self.screen.blit(best_time_surface, best_time_rect)
    
    def go_back(self):
        self.menu.set_scene("main")
        
    def update_times(self, level, current_time, best_time=None):
        """Süreleri güncelle"""
        if 0 <= level - 1 < len(self.leaderboard_data):
            self.leaderboard_data[level - 1]["current_time"] = current_time
            if best_time:
                if self.leaderboard_data[level - 1]["best_time"] == "--:--" or \
                   self._convert_time_to_seconds(best_time) < self._convert_time_to_seconds(self.leaderboard_data[level - 1]["best_time"]):
                    self.leaderboard_data[level - 1]["best_time"] = best_time
    
    def _convert_time_to_seconds(self, time_str):
        """XX:XX formatındaki süreyi saniyeye çevir"""
        if time_str == "--:--":
            return float('inf')
        minutes, seconds = map(int, time_str.split(':'))
        return minutes * 60 + seconds 