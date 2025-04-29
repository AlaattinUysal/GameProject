# menu/menu_logic.py

import pygame
import sys
from .constants import *
from .assets import load_background, load_samurai_characters, load_font
from .ui import PixelButton, LevelCompleteButton, Slider, TextInputBox, ShopSkill

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background = load_background()
        self.samurai_left, self.samurai_right = load_samurai_characters()
        self.title_font = load_font(90, bold=True)
        self.game_title = "THE WAY"
        self.current_menu = "main"
        
        self.panel_width = 400
        self.panel_height = 460
        self.panel_x = (SCREEN_WIDTH - self.panel_width) // 2
        self.panel_y = (SCREEN_HEIGHT - self.panel_height) // 2 + 50
        
        self.icons = {
            "play": "▶️",
            "levels": "🎮",
            "shop": "🛒",
            "leaderboard": "🏆",
            "options": "⚙️",
            "back": "↩️",
            "resume": "▶️",
            "restart": "🔄",
            "settings": "⚙️",
            "quit": "🚪",
            "music": "🎵",
            "sound": "🔊",
            "bright": "💡",
            "login": "👤"
        }
        
        self.default_music_volume = 0.5
        self.default_sound_volume = 0.5
        self.default_brightness = 50
        
        self.music_volume = self.default_music_volume
        self.sound_volume = self.default_sound_volume
        self.brightness = self.default_brightness
        
        button_width = 280
        button_height = 50
        button_spacing = 30
        
        self.main_buttons = [
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60,
                button_width, button_height, 
                "PLAY", self.start_game, self.icons["play"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + (button_height + button_spacing),
                button_width, button_height, 
                "SHOP", self.show_shop, self.icons["shop"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + 2 * (button_height + button_spacing),
                button_width, button_height, 
                "LEADERBOARD", self.show_leaderboard, self.icons["leaderboard"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + 3 * (button_height + button_spacing),
                button_width, button_height, 
                "OPTIONS", self.show_options_menu, self.icons["options"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + 4 * (button_height + button_spacing),
                button_width, button_height, 
                "LOGIN", self.login, self.icons["login"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            )
        ]
        
        self.options_buttons = [
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60,
                button_width, button_height, 
                "RESUME", self.resume_game, self.icons["resume"],
                colors=(DARK_GRAY, GREEN, GREEN)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + (button_height + button_spacing),
                button_width, button_height, 
                "RESTART", self.restart_game, self.icons["restart"],
                colors=(DARK_GRAY, ORANGE, ORANGE)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + 2 * (button_height + button_spacing),
                button_width, button_height, 
                "LEVELS", self.show_levels, self.icons["levels"],
                colors=(DARK_GRAY, CYAN, CYAN)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + 3 * (button_height + button_spacing),
                button_width, button_height, 
                "SETTINGS", self.show_settings_menu, self.icons["settings"],
                colors=(DARK_GRAY, BLUE, BLUE)
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 60 + 4 * (button_height + button_spacing),
                button_width, button_height, 
                "QUIT", self.confirm_quit, self.icons["quit"],
                colors=(DARK_GRAY, RED, RED)
            )
        ]
        
        self.settings_buttons = [
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 70,
                button_width, button_height, 
                "MUSIC", self.toggle_music, self.icons["music"]
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 110 + (button_height + button_spacing),
                button_width, button_height, 
                "SOUND", self.toggle_sound, self.icons["sound"]
            ),
            PixelButton(
                self.panel_x + (self.panel_width - button_width) // 2,
                self.panel_y + 140 + 2 * (button_height + button_spacing),
                button_width, button_height, 
                "BRIGHTNESS", self.adjust_brightness, self.icons["bright"]
            )
        ]
        
        self.level_buttons = []
        self.show_level_selection = False
        
        small_button_width = 100
        small_button_height = 100
        small_button_spacing = 25
        levels_per_row = 3
        
        level_start_x = SCREEN_WIDTH // 2 - (small_button_width * 1.5 + small_button_spacing)
        level_start_y = SCREEN_HEIGHT // 2 - small_button_height
        
        for i in range(9):
            row = i // levels_per_row
            col = i % levels_per_row
            
            level_x = level_start_x + col * (small_button_width + small_button_spacing)
            level_y = level_start_y + row * (small_button_height + small_button_spacing)
            
            is_completed = (i < 3)
            
            self.level_buttons.append(
                LevelCompleteButton(
                    level_x, level_y, 
                    small_button_width, small_button_height, 
                    i + 1, is_completed, 
                    lambda level=i+1: self.start_level(level)
                )
            )
        
        self.back_button = PixelButton(
            50, 50,
            120, 40, "BACK", self.go_back, self.icons["back"]
        )
        
        self.music_slider = Slider(
            self.panel_x + 50, 
            self.panel_y + 130,
            self.panel_width - 100, 
            40,
            current_val=self.music_volume * 100,
            icon=self.icons["music"]
        )
        
        self.sound_slider = Slider(
            self.panel_x + 50, 
            self.panel_y + 130 + 120,
            self.panel_width - 100, 
            40,
            current_val=self.sound_volume * 100,
            icon=self.icons["sound"]
        )
        
        self.brightness_slider = Slider(
            self.panel_x + 50, 
            self.panel_y + 130 + 230,
            self.panel_width - 100, 
            40,
            current_val=self.brightness,
            icon=self.icons["bright"]
        )
        
        self.show_login_screen = False
        self.nickname_input = TextInputBox(
            self.panel_x + 150, 
            self.panel_y + 120, 
            200, 40, 
            placeholder="nickname",
            max_length=15
        )
        
        self.password_input = TextInputBox(
            self.panel_x + 150, 
            self.panel_y + 180, 
            200, 40, 
            placeholder="password", 
            is_password=True
        )
        
        self.login_button = PixelButton(
            self.panel_x + (self.panel_width - 120) // 2,
            self.panel_y + 240,
            120, 40, 
            "LOGIN", self.process_login
        )
        
        self.login_error = ""
        self.logged_in_user = ""
        
        self.show_shop_screen = False
        self.shop_skills = [
            ShopSkill(
                self.panel_x + 50, 
                self.panel_y + 100, 
                self.panel_width - 100, 
                80, 
                "Lightning", 500, 
                icon="⚡"
            ),
            ShopSkill(
                self.panel_x + 50, 
                self.panel_y + 190, 
                self.panel_width - 100, 
                80, 
                "Lightning Bolt", 9000, 
                icon="🔷"
            ),
            ShopSkill(
                self.panel_x + 50, 
                self.panel_y + 280, 
                self.panel_width - 100, 
                80, 
                "Midas Touch", 50000, 
                icon="👆"
            ),
            ShopSkill(
                self.panel_x + 50, 
                self.panel_y + 370, 
                self.panel_width - 100, 
                80, 
                "Sun Strike", 100000, 
                icon="☀️"
            )
        ]
        
        self.default_tokens = 1000
        self.current_tokens = self.default_tokens
        
        self.shop_error = ""
        self.shop_error_timer = 0
        
        self.show_confirm_dialog = False
        self.confirm_skill = None
        self.confirm_dialog_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - 150, 
            SCREEN_HEIGHT // 2 - 100,
            300, 200
        )
        
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
        
        self.fullscreen = FULLSCREEN
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def start_game(self):
        print("Oyun başlatılıyor...")

    def resume_game(self):
        print("Oyuna devam ediliyor...")
        self.go_back()

    def restart_game(self):
        print("Oyun yeniden başlatılıyor...")
        self.logged_in_user = ""
        self.nickname_input.text = ""
        self.password_input.text = ""
        self.login_error = ""
        
        self.current_tokens = self.default_tokens
        for skill in self.shop_skills:
            skill.is_purchased = False
        
        for button in self.level_buttons:
            button.is_completed = (button.level_number <= 3)
        
        self.music_volume = self.default_music_volume
        self.sound_volume = self.default_sound_volume
        self.brightness = self.default_brightness
        
        self.music_slider.current_val = self.music_volume * 100
        self.sound_slider.current_val = self.sound_volume * 100
        self.brightness_slider.current_val = self.brightness
        
        self.current_menu = "main"
        print("Tüm oyun ilerlemeniz sıfırlandı.")

    def show_levels(self):
        print("Seviye seçimi gösteriliyor...")
        self.show_level_selection = True

    def show_shop(self):
        print("Mağaza açılıyor...")
        self.show_shop_screen = True

    def show_leaderboard(self):
        print("Liderlik tablosu gösteriliyor...")

    def show_options_menu(self):
        print("Options menüsü açılıyor...")
        self.current_menu = "options"

    def show_settings_menu(self):
        print("Settings menüsü açılıyor...")
        self.current_menu = "settings"

    def toggle_music(self):
        self.music_volume = 0 if self.music_volume > 0 else 0.7
        self.music_slider.current_val = self.music_volume * 100
        print(f"Müzik {'açık' if self.music_volume > 0 else 'kapalı'}")

    def toggle_sound(self):
        self.sound_volume = 0 if self.sound_volume > 0 else 0.5
        self.sound_slider.current_val = self.sound_volume * 100
        print(f"Ses {'açık' if self.sound_volume > 0 else 'kapalı'}")

    def adjust_brightness(self):
        self.brightness = (self.brightness + 25) % 125
        if self.brightness < 25:
            self.brightness = 25
        self.brightness_slider.current_val = self.brightness
        print(f"Parlaklık: {self.brightness}%")

    def confirm_quit(self):
        print("Oyundan çıkılıyor...")
        self.quit_game()

    def start_level(self, level):
        print(f"Seviye {level} başlatılıyor...")
        self.show_level_selection = False

    def go_back(self):
        if self.current_menu == "settings":
            self.current_menu = "options"
        elif self.current_menu == "options":
            self.current_menu = "main"
        elif self.show_level_selection:
            self.show_level_selection = False
        elif self.show_login_screen:
            self.show_login_screen = False
        elif self.show_shop_screen:
            self.show_shop_screen = False

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def _draw_panel(self, surface):
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_width, self.panel_height)
        dark_border = (DARK_ORANGE[0]//2, DARK_ORANGE[1]//2, DARK_ORANGE[2]//2)
        
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        pygame.draw.rect(surface, dark_border, panel_rect, border_radius=12)
        
        inner_panel = pygame.Rect(self.panel_x + 6, self.panel_y + 6, 
                                 self.panel_width - 12, self.panel_height - 12)
        pygame.draw.rect(surface, DARK_GRAY, inner_panel, border_radius=8)
        
        menu_titles = {
            "main": "MAIN MENU",
            "options": "OPTIONS",
            "settings": "SETTINGS"
        }
        
        menu_colors = {
            "main": ORANGE,
            "options": GREEN,
            "settings": CYAN
        }
        
        if not self.show_level_selection and not self.show_login_screen and not self.show_shop_screen:
            title_font = load_font(36, bold=True)
            title_text = menu_titles.get(self.current_menu, "")
            if title_text:
                title_color = menu_colors.get(self.current_menu, ORANGE)
                title_surface = title_font.render(title_text, True, title_color)
                title_rect = title_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
                surface.blit(title_surface, title_rect)
        
        top_highlight = pygame.Rect(self.panel_x + 8, self.panel_y + 45, self.panel_width - 16, 2)
        pygame.draw.rect(surface, ORANGE, top_highlight, border_radius=1)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                elif event.key == pygame.K_ESCAPE:
                    if self.show_confirm_dialog:
                        self.show_confirm_dialog = False
                        self.confirm_skill = None
                    elif self.current_menu == "settings":
                        self.current_menu = "options"
                    elif self.current_menu == "options":
                        self.current_menu = "main"
                    elif self.show_level_selection:
                        self.show_level_selection = False
                    elif self.show_login_screen:
                        self.show_login_screen = False
                    elif self.show_shop_screen:
                        self.show_shop_screen = False
                    else:
                        self.quit_game()
            
            mouse_pos = pygame.mouse.get_pos()
            
            if self.show_login_screen:
                self.back_button.check_hover(mouse_pos)
                self.back_button.handle_event(event)
                
                self.login_button.check_hover(mouse_pos)
                self.login_button.handle_event(event)
                
                if self.nickname_input.update(event):
                    pass
                
                if self.password_input.update(event):
                    self.process_login()
                
            elif self.show_shop_screen:
                if self.show_confirm_dialog:
                    self.confirm_yes_button.check_hover(mouse_pos)
                    self.confirm_yes_button.handle_event(event)
                    
                    self.confirm_no_button.check_hover(mouse_pos)
                    self.confirm_no_button.handle_event(event)
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if not self.confirm_dialog_rect.collidepoint(mouse_pos):
                            self.show_confirm_dialog = False
                            self.confirm_skill = None
                    
                    continue
                
                self.back_button.check_hover(mouse_pos)
                self.back_button.handle_event(event)
                
                if self.shop_error and pygame.time.get_ticks() - self.shop_error_timer > 3000:
                    self.shop_error = ""
                
                for skill in self.shop_skills:
                    skill.check_hover(mouse_pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and skill.is_hovered and not skill.is_purchased:
                        self.show_confirm_dialog = True
                        self.confirm_skill = skill
            elif self.show_level_selection:
                self.back_button.check_hover(mouse_pos)
                self.back_button.handle_event(event)
                
                for button in self.level_buttons:
                    button.check_hover(mouse_pos)
                    button.handle_event(event)
            else:
                active_buttons = {
                    "main": self.main_buttons,
                    "options": self.options_buttons,
                    "settings": self.settings_buttons
                }.get(self.current_menu, [])
                
                for button in active_buttons:
                    button.check_hover(mouse_pos)
                    button.handle_event(event)
                
                if self.current_menu in ["options", "settings"]:
                    self.back_button.check_hover(mouse_pos)
                    self.back_button.handle_event(event)
                
                if self.current_menu == "settings":
                    self.music_slider.update(events, mouse_pos)
                    self.sound_slider.update(events, mouse_pos)
                    self.brightness_slider.update(events, mouse_pos)
                    
                    self.music_volume = self.music_slider.current_val / 100
                    self.sound_volume = self.sound_slider.current_val / 100
                    self.brightness = self.brightness_slider.current_val

    def render(self):
        self.screen.blit(self.background, (0, 0))
        
        left_cover = pygame.Rect(50, SCREEN_HEIGHT // 2 + 50, 130, 120)
        pygame.draw.rect(self.screen, BLACK, left_cover)
        
        right_cover = pygame.Rect(SCREEN_WIDTH - 190, SCREEN_HEIGHT // 2 + 50, 120, 120)
        pygame.draw.rect(self.screen, BLACK, right_cover)
        
        if self.samurai_left:
            samurai_left_rect = self.samurai_left.get_rect(center=(140, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(self.samurai_left, samurai_left_rect)
            
        if self.samurai_right:
            samurai_right_rect = self.samurai_right.get_rect(center=(SCREEN_WIDTH - 130, SCREEN_HEIGHT // 2 + 80))
            self.screen.blit(self.samurai_right, samurai_right_rect)
        
        title_shadow_offset = 4
        title_shadow = self.title_font.render(self.game_title, True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(midtop=(SCREEN_WIDTH//2 + title_shadow_offset, 
                                                          80 + title_shadow_offset))
        self.screen.blit(title_shadow, title_shadow_rect)
        
        title_surface = self.title_font.render(self.game_title, True, ORANGE)
        title_rect = title_surface.get_rect(midtop=(SCREEN_WIDTH//2, 80))
        self.screen.blit(title_surface, title_rect)
        
        fullscreen_font = load_font(16)
        fullscreen_text = "F11: Tam Ekran Modu"
        fullscreen_surface = fullscreen_font.render(fullscreen_text, True, LIGHT_GRAY)
        self.screen.blit(fullscreen_surface, (SCREEN_WIDTH - fullscreen_surface.get_width() - 10, SCREEN_HEIGHT - 30))
        
        if self.logged_in_user:
            user_font = load_font(20, bold=True)
            user_text = f"User: {self.logged_in_user}"
            user_surface = user_font.render(user_text, True, CYAN)
            self.screen.blit(user_surface, (20, 20))
        
        if self.show_login_screen:
            self._draw_panel(self.screen)
            
            title_font = load_font(36, bold=True)
            title_text = "LOGIN"
            title_surface = title_font.render(title_text, True, BLUE)
            title_rect = title_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
            self.screen.blit(title_surface, title_rect)
            
            self.back_button.update()
            self.back_button.draw(self.screen)
            
            user_font = load_font(24)
            user_icon = user_font.render(self.icons["login"], True, ORANGE)
            password_icon = user_font.render("🔑", True, ORANGE)
            
            self.screen.blit(user_icon, (self.panel_x + 100, self.panel_y + 120 + 20))
            self.screen.blit(password_icon, (self.panel_x + 100, self.panel_y + 180 + 20))
            
            self.nickname_input.draw(self.screen)
            self.password_input.draw(self.screen)
            
            self.login_button.update()
            self.login_button.draw(self.screen)
            
            if self.login_error:
                error_font = load_font(18)
                error_surface = error_font.render(self.login_error, True, RED)
                error_rect = error_surface.get_rect(center=(self.panel_x + self.panel_width//2, self.panel_y + 300))
                self.screen.blit(error_surface, error_rect)
                
        elif self.show_shop_screen:
            self._draw_panel(self.screen)
            
            title_font = load_font(36, bold=True)
            title_text = "BUY SKILLS"
            title_surface = title_font.render(title_text, True, GOLD)
            title_rect = title_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
            self.screen.blit(title_surface, title_rect)
            
            token_font = load_font(24, bold=False)
            token_text = f"Current Tokens: {self.current_tokens}"
            token_surface = token_font.render(token_text, True, GOLD)
            token_rect = token_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 60))
            self.screen.blit(token_surface, token_rect)
            
            self.back_button.update()
            self.back_button.draw(self.screen)
            
            for skill in self.shop_skills:
                skill.update()
                skill.draw(self.screen)
            
            if self.shop_error:
                error_font = load_font(20, bold=True)
                error_surface = error_font.render(self.shop_error, True, RED)
                error_rect = error_surface.get_rect(midbottom=(self.panel_x + self.panel_width//2, self.panel_y + self.panel_height - 20))
                self.screen.blit(error_surface, error_rect)
                
            if self.show_confirm_dialog and self.confirm_skill:
                darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                darken.fill((0, 0, 0, 150))
                self.screen.blit(darken, (0, 0))
                
                pygame.draw.rect(self.screen, DARK_GRAY, self.confirm_dialog_rect, border_radius=10)
                pygame.draw.rect(self.screen, ORANGE, self.confirm_dialog_rect, width=3, border_radius=10)
                
                dialog_title_font = load_font(24, bold=True)
                dialog_title = "SATIN ALMA ONAYI"
                dialog_title_surf = dialog_title_font.render(dialog_title, True, ORANGE)
                dialog_title_rect = dialog_title_surf.get_rect(midtop=(self.confirm_dialog_rect.centerx, self.confirm_dialog_rect.y + 15))
                self.screen.blit(dialog_title_surf, dialog_title_rect)
                
                confirm_font = load_font(20)
                skill_name = self.confirm_skill.name
                confirm_text = f"{skill_name} yetenegini"
                confirm_text2 = f"{self.confirm_skill.cost} token ile"
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
                
                self.confirm_yes_button.update()
                self.confirm_yes_button.draw(self.screen)
                
                self.confirm_no_button.update()
                self.confirm_no_button.draw(self.screen)
        elif self.show_level_selection:
            self._draw_panel(self.screen)
            
            level_title = load_font(40, bold=True).render("SELECT LEVEL", True, CYAN)
            level_title_rect = level_title.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
            self.screen.blit(level_title, level_title_rect)
            
            self.back_button.update()
            self.back_button.draw(self.screen)
            
            for button in self.level_buttons:
                button.update()
                button.draw(self.screen)
        else:
            self._draw_panel(self.screen)
            
            active_buttons = {
                "main": self.main_buttons,
                "options": self.options_buttons,
                "settings": self.settings_buttons
            }.get(self.current_menu, [])
            
            for button in active_buttons:
                button.update()
                button.draw(self.screen)
            
            if self.current_menu in ["options", "settings"]:
                self.back_button.update()
                self.back_button.draw(self.screen)
            
            if self.current_menu == "settings":
                self.music_slider.draw(self.screen)
                self.sound_slider.draw(self.screen)
                self.brightness_slider.draw(self.screen)
        
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.render()
            clock.tick(60)

    def login(self):
        print("Giriş sayfasi aciliyor...")
        self.show_login_screen = True

    def process_login(self):
        if not self.nickname_input.text or not self.password_input.text:
            self.login_error = "Kullanıcı adı ve sifre gerekli!"
            return
            
        print(f"Giriş yapılıyor: {self.nickname_input.text}")
        self.logged_in_user = self.nickname_input.text
        self.show_login_screen = False
        self.current_menu = "main"

    def confirm_purchase(self):
        if self.confirm_skill:
            success, new_tokens, error = self.confirm_skill.handle_click(self.current_tokens)
            if success:
                self.current_tokens = new_tokens
                print(f"{self.confirm_skill.name} satın alındı! Kalan token: {self.current_tokens}")
            elif error:
                self.shop_error = error
                self.shop_error_timer = pygame.time.get_ticks()
                print(f"Satın alma hatası: {error}")
        
        self.show_confirm_dialog = False
        self.confirm_skill = None

    def cancel_purchase(self):
        self.show_confirm_dialog = False
        self.confirm_skill = None
        print("Satın alma iptal edildi.")

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
            print("Tam ekran moduna geçildi")
        else:
            self.screen = pygame.display.set_mode(self.window_size)
            print("Pencere moduna geçildi")
