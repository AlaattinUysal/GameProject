import os
import pygame
import sys
import math

# Pygame başlatma
pygame.init()

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
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
MENU_ASSETS_DIR = os.path.join(ASSETS_DIR, "menu_tasarim")

# Arka plan
def load_background():
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

# Samuray karakterlerini yükleme
def load_samurai_characters():
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

# Font yükleme - Segoe UI Emoji fontu kullanıyoruz (emoji için en iyi görünüm)
def load_font(size=36, bold=False, font_name="Segoe UI Emoji"):
    try:
        # Varsayılan olarak Segoe UI Emoji font kullan (emoji desteği için)
        return pygame.font.SysFont(font_name, size, bold=bold)
    except (pygame.error, FileNotFoundError, IndexError) as e:
        print(f"Font yükleme hatası: {e}")
        # Herhangi bir hata olursa varsayılan system fontu
        return pygame.font.SysFont(None, size, bold=bold)

# Piksel efektli buton için yardımcı fonksiyonlar
def draw_pixel_button(surface, rect, text, colors, icon=None, border_radius=8, border_width=3, has_screws=True):
    """
    Piksel stili buton çizimi
    
    Parametreler:
    - rect: Butonun konumu ve boyutu
    - text: Buton üzerindeki yazı
    - colors: (iç_renk, kenar_renk, metin_rengi) şeklinde tuple
    - icon: Simge metni veya None
    - border_radius: Köşelerin yuvarlaklık miktarı
    - border_width: Kenar kalınlığı
    - has_screws: Vidaları göster/gizle
    """
    # Renkleri ayarla
    inner_color, border_color, text_color = colors
    
    # Buton gölgesi
    shadow_offset = 3
    shadow_rect = pygame.Rect(rect.x + shadow_offset, rect.y + shadow_offset, 
                             rect.width, rect.height)
    pygame.draw.rect(surface, (0, 0, 0, 128), shadow_rect, border_radius=border_radius)
    
    # Buton dış kenarı (border)
    pygame.draw.rect(surface, border_color, rect, border_radius=border_radius)
    
    # Buton iç kısmı
    inner_rect = pygame.Rect(rect.x + border_width, rect.y + border_width, 
                           rect.width - 2*border_width, rect.height - 2*border_width)
    pygame.draw.rect(surface, inner_color, inner_rect, border_radius=border_radius-2)
    
    # İkon için kare alan çiz (sol tarafta)
    if icon:
        # İkon için kare çerçeve
        icon_box_size = inner_rect.height - 6
        icon_box = pygame.Rect(inner_rect.x + 8, inner_rect.y + 3, icon_box_size, icon_box_size)
        
        # İkon kutucuğunun çerçevesi
        pygame.draw.rect(surface, border_color, icon_box, border_radius=4, width=1)
        
        # İkon çizimi (Unicode emoji desteği için Arial font kullanılıyor)
        font = load_font(size=icon_box_size - 8, bold=True)
        icon_surface = font.render(icon, True, text_color)
        icon_rect = icon_surface.get_rect(center=icon_box.center)
        surface.blit(icon_surface, icon_rect)
        
        # Metin çizimi için boşluk bırak
        text_x = icon_box.right + 13
    else:
        text_x = inner_rect.x + 10
    
    # Metin çizimi
    font = load_font(size=min(24, rect.height//2 - 4), bold=True)
    text_surface = font.render(text, True, text_color)
    if icon:
        # İkon varsa metni sağa yerleştir
        text_rect = text_surface.get_rect(midleft=(text_x, inner_rect.centery))
    else:
        # İkon yoksa metni ortala
        text_rect = text_surface.get_rect(center=inner_rect.center)
    
    surface.blit(text_surface, text_rect)
    
    # Vida vidaları ekle (opsiyonel)
    if has_screws:
        screw_radius = min(3, border_width)  # Küçük vidalar
        screw_positions = [
            (rect.left + screw_radius + 2, rect.top + screw_radius + 2),
            (rect.right - screw_radius - 2, rect.top + screw_radius + 2),
            (rect.left + screw_radius + 2, rect.bottom - screw_radius - 2),
            (rect.right - screw_radius - 2, rect.bottom - screw_radius - 2)
        ]
        
        for pos in screw_positions:
            pygame.draw.circle(surface, (80, 80, 90), pos, screw_radius)
            pygame.draw.circle(surface, (120, 120, 130), 
                              (pos[0]-1, pos[1]-1), screw_radius//2)

class PixelButton:
    def __init__(self, x, y, width, height, text, action=None, icon=None, colors=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.is_hovered = False
        self.icon = icon  # Buton ikonu
        
        # Buton renkleri (özelleştirilebilir)
        if colors:
            self.inner_color, self.border_color, self.text_color = colors
            self.hover_border_color = BRIGHT_ORANGE
            self.hover_text_color = WHITE
        else:
            # Buton renkleri
            self.inner_color = DARK_GRAY
            self.border_color = ORANGE
            self.text_color = ORANGE
            self.hover_border_color = BRIGHT_ORANGE
            self.hover_text_color = WHITE
        
        # Animasyon için değişkenler
        self.hover_transition = 0  # 0 ile 1 arası değer (animasyon için)
        self.pressed = False
        self.press_offset = 0
        
    def update(self):
        # Hover geçiş animasyonu
        target = 1.0 if self.is_hovered else 0.0
        self.hover_transition += (target - self.hover_transition) * 0.2
        
        # Basılma animasyonu
        if self.pressed:
            self.press_offset = 2
        else:
            self.press_offset = 0
        
    def draw(self, surface):
        # Renkleri hesapla
        border_color = tuple(
            int(self.border_color[i] + (self.hover_border_color[i] - self.border_color[i]) * self.hover_transition)
            for i in range(3)
        )
        
        text_color = tuple(
            int(self.text_color[i] + (self.hover_text_color[i] - self.text_color[i]) * self.hover_transition)
            for i in range(3)
        )
        
        # Basılma efekti için buton konumunu ayarla
        draw_rect = self.rect.copy()
        if self.pressed:
            draw_rect.y += self.press_offset
        
        colors = (self.inner_color, border_color, text_color)
        draw_pixel_button(surface, draw_rect, self.text, colors, self.icon)
        
    def check_hover(self, pos):
        old_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(pos)
        return old_hovered != self.is_hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.pressed = True
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            was_pressed = self.pressed
            self.pressed = False
            
            if was_pressed and self.is_hovered and self.action:
                self.action()
                return True
        
        return False

class LevelCompleteButton(PixelButton):
    """Level Complete butonu - kilitli/açık durumunu gösterir"""
    def __init__(self, x, y, width, height, level_number, is_completed=False, action=None):
        super().__init__(x, y, width, height, f"LEVEL {level_number}", action)
        self.level_number = level_number
        self.is_completed = is_completed
        self.star_color = (255, 215, 0)  # Altın rengi
    
    def draw(self, surface):
        # Normal buton çizimi
        super().draw(surface)
        
        # Yıldızlar kaldırıldı - özellik istenmiyor
        pass

class Slider:
    """Ayarlar için kaydırıcı sınıfı"""
    
    def __init__(self, x, y, width, height, min_val=0, max_val=100, current_val=50, 
                 label="", icon=None, colors=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = current_val
        self.label = label
        self.icon = icon
        self.is_dragging = False
        self.track_rect = pygame.Rect(x + 40, y + height//2 - 4, width - 80, 8)
        
        # Buton renkleri
        if colors:
            self.bg_color, self.track_color, self.handle_color, self.text_color = colors
        else:
            self.bg_color = DARK_GRAY       # Arka plan
            self.track_color = DARK_ORANGE  # Kaydırma yolu
            self.handle_color = ORANGE      # Kaydırıcı topuzu
            self.text_color = ORANGE        # Metin rengi
    
    def draw(self, surface):
        # Kaydırıcı arka planı
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=8)
        
        # Kaydırıcı metni
        if self.label:
            font = load_font(20, bold=True)
            label_surface = font.render(self.label, True, self.text_color)
            label_rect = label_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
            surface.blit(label_surface, label_rect)
        
        # İkon
        if self.icon:
            font = load_font(24, bold=True)
            icon_surface = font.render(self.icon, True, self.text_color)
            icon_rect = icon_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
            surface.blit(icon_surface, icon_rect)
        
        # Kaydırıcı yolunu çiz
        pygame.draw.rect(surface, (60, 60, 70), self.track_rect, border_radius=4)
        
        # Değer çubuğu (dolgulu kısım)
        val_percentage = (self.current_val - self.min_val) / (self.max_val - self.min_val)
        filled_width = int(val_percentage * self.track_rect.width)
        if filled_width > 0:
            filled_rect = pygame.Rect(self.track_rect.x, self.track_rect.y, 
                                     filled_width, self.track_rect.height)
            pygame.draw.rect(surface, self.track_color, filled_rect, border_radius=4)
        
        # Kaydırıcı topuzu
        handle_x = self.track_rect.x + filled_width
        handle_y = self.track_rect.centery
        pygame.draw.circle(surface, self.handle_color, (handle_x, handle_y), 10)
        pygame.draw.circle(surface, (255, 255, 255), (handle_x-2, handle_y-2), 3)
        
        # Değer metni
        value_font = load_font(18, bold=True)
        value_text = f"{int(self.current_val)}%"
        value_surface = value_font.render(value_text, True, self.text_color)
        value_rect = value_surface.get_rect(midright=(self.rect.right - 10, self.rect.centery))
        surface.blit(value_surface, value_rect)
    
    def update(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Kaydırıcı çubuğuna tıklandı mı kontrol et
                handle_x = self.track_rect.x + (self.current_val - self.min_val) / (self.max_val - self.min_val) * self.track_rect.width
                handle_rect = pygame.Rect(handle_x - 10, self.track_rect.centery - 10, 20, 20)
                if handle_rect.collidepoint(mouse_pos) or self.track_rect.collidepoint(mouse_pos):
                    self.is_dragging = True
                    self._update_value(mouse_pos[0])
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.is_dragging = False
            
            elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                self._update_value(mouse_pos[0])
    
    def _update_value(self, x_pos):
        # Kaydırıcı değerini güncelle
        if x_pos < self.track_rect.x:
            self.current_val = self.min_val
        elif x_pos > self.track_rect.right:
            self.current_val = self.max_val
        else:
            val_percentage = (x_pos - self.track_rect.x) / self.track_rect.width
            self.current_val = self.min_val + val_percentage * (self.max_val - self.min_val)
        
        # Değeri en yakın tam sayıya yuvarla
        self.current_val = round(self.current_val)

class TextInputBox:
    """Metin giriş kutusu"""
    
    def __init__(self, x, y, width, height, placeholder="", is_password=False, max_length=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.is_password = is_password
        self.is_active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.font = load_font(22)
        self.max_length = max_length  # Maksimum karakter sınırı
        
        # Renkleri ayarla
        self.inactive_color = DARK_ORANGE
        self.active_color = BRIGHT_ORANGE
        self.text_color = WHITE
        self.placeholder_color = LIGHT_GRAY
    
    def draw(self, surface):
        # Kutu arka planı
        border_color = self.active_color if self.is_active else self.inactive_color
        pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=6)
        
        # Metin veya placeholder
        if self.text:
            display_text = '*' * len(self.text) if self.is_password else self.text
            text_surface = self.font.render(display_text, True, self.text_color)
        else:
            text_surface = self.font.render(self.placeholder, True, self.placeholder_color)
        
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surface, text_rect)
        
        # İmleç gösterimi (aktifse)
        if self.is_active and self.cursor_visible:
            display_text = '*' * len(self.text) if self.is_password else self.text
            cursor_pos = self.font.size(display_text)[0]
            cursor_x = self.rect.x + 10 + cursor_pos
            pygame.draw.line(surface, self.text_color, 
                            (cursor_x, self.rect.y + 10), 
                            (cursor_x, self.rect.bottom - 10), 2)
    
    def update(self, event):
        # İmleç animasyonu
        self.cursor_timer += 1
        if self.cursor_timer >= 30:  # Her yarım saniyede değiştir (60 FPS'de)
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        # Tek bir event (olay) işle, events listesi değil
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.is_active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.is_active = False
                return True  # Enter tuşuna basıldı
            elif len(self.text) < self.max_length:  # Maksimum karakter kontrolü
                if event.unicode.isprintable():
                    self.text += event.unicode
        
        return False  # Enter tuşuna basılmadı

class ShopSkill:
    """Yetenekler mağazası için skill kartı"""
    
    def __init__(self, x, y, width, height, name, cost, icon=None, description=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.cost = cost
        self.icon = icon
        self.description = description
        self.is_hovered = False
        self.is_purchased = False
        
        # Animasyon değişkenleri
        self.hover_offset = 0
        self.hover_target = 0
    
    def draw(self, surface):
        # Kart arka planı
        card_color = DARK_GRAY
        border_color = BRIGHT_ORANGE if self.is_hovered else DARK_ORANGE
        
        # Gölge efekti
        shadow_rect = self.rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(surface, (0, 0, 0, 128), shadow_rect, border_radius=8)
        
        # Hover animasyonu
        card_rect = self.rect.copy()
        card_rect.y -= self.hover_offset
        
        # Kart kenarı
        pygame.draw.rect(surface, border_color, card_rect, border_radius=8)
        
        # Kart iç kısmı
        inner_rect = pygame.Rect(card_rect.x + 3, card_rect.y + 3, 
                               card_rect.width - 6, card_rect.height - 6)
        pygame.draw.rect(surface, card_color, inner_rect, border_radius=6)
        
        # İkon (varsa)
        if self.icon:
            icon_font = load_font(36)
            icon_surface = icon_font.render(self.icon, True, ORANGE)
            icon_rect = icon_surface.get_rect(
                topleft=(inner_rect.x + 10, inner_rect.y + 10)
            )
            surface.blit(icon_surface, icon_rect)
        
        # Skill adı
        name_font = load_font(24, bold=True)
        name_surface = name_font.render(self.name, True, WHITE)
        name_rect = name_surface.get_rect(
            topleft=(inner_rect.x + 70, inner_rect.y + 15)
        )
        surface.blit(name_surface, name_rect)
        
        # Fiyat
        cost_font = load_font(22)
        cost_surface = cost_font.render(f"{self.cost:,}", True, GOLD)
        cost_rect = cost_surface.get_rect(
            midright=(inner_rect.right - 15, inner_rect.centery)
        )
        surface.blit(cost_surface, cost_rect)
        
        # Satın alındı işareti
        if self.is_purchased:
            purchased_font = load_font(28, bold=True)
            purchased_surface = purchased_font.render("✓", True, GREEN)
            purchased_rect = purchased_surface.get_rect(
                bottomright=(inner_rect.right - 10, inner_rect.bottom - 10)
            )
            surface.blit(purchased_surface, purchased_rect)
    
    def update(self):
        # Hover animasyonu güncelleme
        self.hover_target = 5 if self.is_hovered else 0
        self.hover_offset += (self.hover_target - self.hover_offset) * 0.2
    
    def check_hover(self, pos):
        old_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(pos)
        return old_hovered != self.is_hovered
    
    def handle_click(self, current_tokens):
        if self.is_hovered and not self.is_purchased:
            # Token kontrolü
            if current_tokens >= self.cost:
                # Yeterli token varsa satın al
                self.is_purchased = True
                return True, current_tokens - self.cost, None
            else:
                # Yetersiz token
                return False, current_tokens, "Yetersiz token!"
        return False, current_tokens, None

class Menu:
    def __init__(self):
        self.background = load_background()
        
        # Samuray karakterlerini yükle
        self.samurai_left, self.samurai_right = load_samurai_characters()
        
        # Arial font ile başlık için (unicode emoji desteği var)
        self.title_font = load_font(90, bold=True)
        
        # Oyun adı
        self.game_title = "THE WAY"
        
        # Menü durumu (main, options, settings)
        self.current_menu = "main"
        
        # Panel oluştur (butonları içerecek)
        self.panel_width = 400
        self.panel_height = 460
        self.panel_x = (SCREEN_WIDTH - self.panel_width) // 2
        self.panel_y = (SCREEN_HEIGHT - self.panel_height) // 2 + 50
        
        # Buton simgeleri (unicode emoji karakterler)
        self.icons = {
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
            "bright": "💡",
            "login": "👤"            # Parlaklık için ampul
        }
        
        # Ayarlar için değişkenler
        self.default_music_volume = 0.5  # Varsayılan değerler
        self.default_sound_volume = 0.5
        self.default_brightness = 50
        
        self.music_volume = self.default_music_volume  # 0.0-1.0 arası
        self.sound_volume = self.default_sound_volume  # 0.0-1.0 arası
        self.brightness = self.default_brightness      # 0-100 arası
        
        # Buton boyutları
        button_width = 280
        button_height = 50
        button_spacing = 30
        
        # Butonları oluştur
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
        
        # Options Menü butonları
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
        
        # Settings Menü butonları
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
        
        # Level Selection menüsü için butonlar
        self.level_buttons = []
        self.show_level_selection = False
        
        # Seviye butonları için grid düzeni
        small_button_width = 100
        small_button_height = 100
        small_button_spacing = 25
        levels_per_row = 3
        
        # Seviye butonları için başlangıç konumu
        level_start_x = SCREEN_WIDTH // 2 - (small_button_width * 1.5 + small_button_spacing)
        level_start_y = SCREEN_HEIGHT // 2 - small_button_height
        
        # 9 seviye oluştur - 3x3 grid formatında
        for i in range(9):
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
        
        # Geri butonu (menüler arası geçiş için)
        self.back_button = PixelButton(
            50, 50,
            120, 40, "BACK", self.go_back, self.icons["back"]
        )
        
        # Ayarlar için kaydırıcılar
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
            self.panel_y + 130 + 120,  # Boşluğu artırdım
            self.panel_width - 100, 
            40,
            current_val=self.sound_volume * 100,
            icon=self.icons["sound"]
        )
        
        self.brightness_slider = Slider(
            self.panel_x + 50, 
            self.panel_y + 130 + 230,  # Boşluğu artırdım
            self.panel_width - 100, 
            40,
            current_val=self.brightness,
            icon=self.icons["bright"]
        )
        
        # Login ekranı
        self.show_login_screen = False
        self.nickname_input = TextInputBox(
            self.panel_x + 150, 
            self.panel_y + 120, 
            200, 40, 
            placeholder="nickname",
            max_length=15  # Maksimum karakter sınırı
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
        
        # Shop menüsü
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
        
        # Token miktarı ve varsayılan değer
        self.default_tokens = 1000  # Varsayılan token değeri
        self.current_tokens = self.default_tokens
        
        # Shop hata mesajı
        self.shop_error = ""
        self.shop_error_timer = 0
        
        # Satın alma onay kutusu
        self.show_confirm_dialog = False
        self.confirm_skill = None
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
        
        # Menü başlıklarının renkleri
        menu_colors = {
            "main": ORANGE,      # Ana menü için turuncu
            "options": GREEN,    # Options menüsü için yeşil
            "settings": CYAN     # Settings menüsü için turkuaz
        }
        
        # Ekran boyutları (tam ekran kontrolü için)
        self.fullscreen = fullscreen
        self.window_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def start_game(self):
        print("Oyun başlatılıyor...")
        pygame.quit()  # Mevcut pygame penceresini kapat
        
        # player.py'yi çalıştır
        import subprocess
        import os
        
        # Geçerli dizini al
        current_dir = os.path.dirname(os.path.abspath(__file__))
        player_path = os.path.join(current_dir, "player.py")
        
        # Python yorumlayıcısını kullanarak player.py'yi çalıştır
        subprocess.run([sys.executable, player_path])
        
        # Oyun kapandığında programı sonlandır
        sys.exit()
        
    def resume_game(self):
        print("Oyuna devam ediliyor...")
        self.go_back()  # Ana menüye dön
        
    def restart_game(self):
        print("Oyun yeniden başlatılıyor...")
        # Tüm ilerlemeyi sıfırla
        
        # Kullanıcı bilgilerini sıfırla
        self.logged_in_user = ""
        self.nickname_input.text = ""
        self.password_input.text = ""
        self.login_error = ""
        
        # Token ve satın almaları sıfırla - varsayılan token değerini kullan
        self.current_tokens = self.default_tokens
        for skill in self.shop_skills:
            skill.is_purchased = False
        
        # Level ilerlemesini sıfırla
        for button in self.level_buttons:
            button.is_completed = (button.level_number <= 3)  # İlk 3 seviye açık
        
        # Ayarları varsayılan değerlere sıfırla
        self.music_volume = self.default_music_volume
        self.sound_volume = self.default_sound_volume
        self.brightness = self.default_brightness
        
        # Slider'ları güncelle
        self.music_slider.current_val = self.music_volume * 100
        self.sound_slider.current_val = self.sound_volume * 100
        self.brightness_slider.current_val = self.brightness
        
        # Ana menüye dön
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
        # Liderlik tablosu kodları buraya gelecek
    
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
        # Örnek olarak parlaklık değerini değiştir
        self.brightness = (self.brightness + 25) % 125
        if self.brightness < 25:
            self.brightness = 25
        self.brightness_slider.current_val = self.brightness
        print(f"Parlaklık: {self.brightness}      %")
        
    def confirm_quit(self):
        print("Oyundan çıkılıyor...")
        self.quit_game()
        
    def start_level(self, level):
        print(f"Seviye {level} başlatılıyor...")
        # Seviye başlatma kodları buraya gelecek
        self.show_level_selection = False
        
    def go_back(self):
        if self.current_menu == "settings":
            # Settings menüsünden Options menüsüne dön
            self.current_menu = "options"
        elif self.current_menu == "options":
            # Options menüsünden ana menüye dön
            self.current_menu = "main"
        elif self.show_level_selection:
            # Seviye seçiminden ana menüye dön
            self.show_level_selection = False
        elif self.show_login_screen:
            # Login ekranından ana menüye dön
            self.show_login_screen = False
        elif self.show_shop_screen:
            # Shop ekranından ana menüye dön
            self.show_shop_screen = False
            
    def quit_game(self):
        pygame.quit()
        sys.exit()
    
    def _draw_panel(self, surface):
        # Panel arka planı
        panel_rect = pygame.Rect(self.panel_x, self.panel_y, self.panel_width, self.panel_height)
        
        # Koyu kenar rengi
        dark_border = (DARK_ORANGE[0]//2, DARK_ORANGE[1]//2, DARK_ORANGE[2]//2)
        
        # Panel gölgesi
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6
        pygame.draw.rect(surface, (0, 0, 0, 100), shadow_rect, border_radius=12)
        
        # Panel arka planı
        pygame.draw.rect(surface, dark_border, panel_rect, border_radius=12)
        
        # İç panel
        inner_panel = pygame.Rect(self.panel_x + 6, self.panel_y + 6, 
                                 self.panel_width - 12, self.panel_height - 12)
        pygame.draw.rect(surface, DARK_GRAY, inner_panel, border_radius=8)
        
        # Panel başlığı - hangi menüdeyiz
        menu_titles = {
            "main": "MAIN MENU",
            "options": "OPTIONS",
            "settings": "SETTINGS"
        }
        
        # Menü başlıklarının renkleri
        menu_colors = {
            "main": ORANGE,      # Ana menü için turuncu
            "options": GREEN,    # Options menüsü için yeşil
            "settings": CYAN     # Settings menüsü için turkuaz
        }
        
        if not self.show_level_selection and not self.show_login_screen and not self.show_shop_screen:
            title_font = load_font(36, bold=True)
            title_text = menu_titles.get(self.current_menu, "")
            if title_text:
                # Geçerli menünün rengini al, yoksa turuncu kullan
                title_color = menu_colors.get(self.current_menu, ORANGE)
                title_surface = title_font.render(title_text, True, title_color)
                title_rect = title_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
                surface.blit(title_surface, title_rect)
        
        # Dekoratif kenar efekti
        top_highlight = pygame.Rect(self.panel_x + 8, self.panel_y + 45, self.panel_width - 16, 2)
        pygame.draw.rect(surface, ORANGE, top_highlight, border_radius=1)
    
    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_game()
            
            # F11 tuşu ile tam ekran modu değiştirme
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
            
            # Fare pozisyonunu kontrol et
            mouse_pos = pygame.mouse.get_pos()
            
            # Buton etkileşimleri - mevcut ekrana göre
            if self.show_login_screen:
                # Login ekranı
                self.back_button.check_hover(mouse_pos)
                self.back_button.handle_event(event)
                
                self.login_button.check_hover(mouse_pos)
                self.login_button.handle_event(event)
                
                # Text inputlar için update - her bir event'i ayrı ayrı işle
                if self.nickname_input.update(event):
                    pass  # Enter tuşuna basıldığında bir şey yapma
                
                if self.password_input.update(event):
                    self.process_login()  # Enter tuşuna basınca form gönder
                
            elif self.show_shop_screen:
                # Shop ekranı
                
                # Onay kutusu açıksa, sadece onay kutusunu işle
                if self.show_confirm_dialog:
                    self.confirm_yes_button.check_hover(mouse_pos)
                    self.confirm_yes_button.handle_event(event)
                    
                    self.confirm_no_button.check_hover(mouse_pos)
                    self.confirm_no_button.handle_event(event)
                    
                    # Kutu dışına tıklandıysa kapat
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if not self.confirm_dialog_rect.collidepoint(mouse_pos):
                            self.show_confirm_dialog = False
                            self.confirm_skill = None
                    
                    continue  # Diğer işlevleri atla
                
                self.back_button.check_hover(mouse_pos)
                self.back_button.handle_event(event)
                
                # Hata mesajı süresi doldu mu?
                if self.shop_error and pygame.time.get_ticks() - self.shop_error_timer > 3000:  # 3 saniye
                    self.shop_error = ""
                
                # Yetenekleri güncelle
                for skill in self.shop_skills:
                    skill.check_hover(mouse_pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and skill.is_hovered and not skill.is_purchased:
                        # Onay kutusu göster
                        self.show_confirm_dialog = True
                        self.confirm_skill = skill
            elif self.show_level_selection:
                self.back_button.check_hover(mouse_pos)
                self.back_button.handle_event(event)
                
                for button in self.level_buttons:
                    button.check_hover(mouse_pos)
                    button.handle_event(event)
            else:
                # Ana menü, Options menüsü ve Settings menüsü için
                active_buttons = {
                    "main": self.main_buttons,
                    "options": self.options_buttons,
                    "settings": self.settings_buttons
                }.get(self.current_menu, [])
                
                for button in active_buttons:
                    button.check_hover(mouse_pos)
                    button.handle_event(event)
                
                # Back butonu (options ve settings menülerinde)
                if self.current_menu in ["options", "settings"]:
                    self.back_button.check_hover(mouse_pos)
                    self.back_button.handle_event(event)
                
                # Settings menüsündeki kaydırıcılar
                if self.current_menu == "settings":
                    self.music_slider.update(events, mouse_pos)
                    self.sound_slider.update(events, mouse_pos)
                    self.brightness_slider.update(events, mouse_pos)
                    
                    # Kaydırıcı değerlerini senkronize et
                    self.music_volume = self.music_slider.current_val / 100
                    self.sound_volume = self.sound_slider.current_val / 100
                    self.brightness = self.brightness_slider.current_val
    
    def render(self):
        # Arka planı çiz
        screen.blit(self.background, (0, 0))
        
        # Arka plandaki piksel karakterleri gizlemek için daha küçük siyah dikdörtgenler çiz
        # Sol taraftaki piksel karakteri için - sol tarafa doğru genişletilmiş
        left_cover = pygame.Rect(50, SCREEN_HEIGHT // 2 + 50, 130, 120)
        pygame.draw.rect(screen, BLACK, left_cover)
        
        # Sağ taraftaki piksel karakteri için - sağ tarafa doğru genişletilmiş
        right_cover = pygame.Rect(SCREEN_WIDTH - 190, SCREEN_HEIGHT // 2 + 50, 120, 120)
        pygame.draw.rect(screen, BLACK, right_cover)
        
        # Samuray karakterlerini çiz (eğer yüklendiyse)
        if self.samurai_left:
            # Sol tarafta konumlandır - Piksel karakterin olduğu yere
            samurai_left_rect = self.samurai_left.get_rect(center=(140, SCREEN_HEIGHT // 2 + 80))
            screen.blit(self.samurai_left, samurai_left_rect)
            
        if self.samurai_right:
            # Sağ tarafta konumlandır - Piksel karakterin olduğu yere
            samurai_right_rect = self.samurai_right.get_rect(center=(SCREEN_WIDTH - 130, SCREEN_HEIGHT // 2 + 80))
            screen.blit(self.samurai_right, samurai_right_rect)
        
        # Başlığı çiz (Arial font ile)
        title_shadow_offset = 4
        
        # Önce gölgeyi çiz
        title_shadow = self.title_font.render(self.game_title, True, (0, 0, 0))
        title_shadow_rect = title_shadow.get_rect(midtop=(SCREEN_WIDTH//2 + title_shadow_offset, 
                                                          80 + title_shadow_offset))
        screen.blit(title_shadow, title_shadow_rect)
        
        # Sonra ana başlığı çiz
        title_surface = self.title_font.render(self.game_title, True, ORANGE)
        title_rect = title_surface.get_rect(midtop=(SCREEN_WIDTH//2, 80))
        screen.blit(title_surface, title_rect)
        
        # Tam ekran bilgisi
        fullscreen_font = load_font(16)
        fullscreen_text = "F11: Tam Ekran Modu"
        fullscreen_surface = fullscreen_font.render(fullscreen_text, True, LIGHT_GRAY)
        screen.blit(fullscreen_surface, (SCREEN_WIDTH - fullscreen_surface.get_width() - 10, SCREEN_HEIGHT - 30))
        
        # Kullanıcı giriş yapmışsa kullanıcı adını göster
        if self.logged_in_user:
            user_font = load_font(20, bold=True)
            user_text = f"User: {self.logged_in_user}"
            user_surface = user_font.render(user_text, True, CYAN)
            screen.blit(user_surface, (20, 20))
        
        if self.show_login_screen:
            # Login panelini çiz
            self._draw_panel(screen)
            
            # Login başlığı
            title_font = load_font(36, bold=True)
            title_text = "LOGIN"
            title_surface = title_font.render(title_text, True, BLUE)
            title_rect = title_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
            screen.blit(title_surface, title_rect)
            
            # Geri butonunu çiz
            self.back_button.update()
            self.back_button.draw(screen)
            
            # İkonları çiz
            user_font = load_font(24)
            user_icon = user_font.render(self.icons["login"], True, ORANGE)
            password_icon = user_font.render("🔑", True, ORANGE)
            
            screen.blit(user_icon, (self.panel_x + 100, self.panel_y + 120 + 20))
            screen.blit(password_icon, (self.panel_x + 100, self.panel_y + 180 + 20))
            
            # Text inputları çiz
            self.nickname_input.draw(screen)
            self.password_input.draw(screen)
            
            # Login butonu
            self.login_button.update()
            self.login_button.draw(screen)
            
            # Hata mesajı (varsa)
            if self.login_error:
                error_font = load_font(18)
                error_surface = error_font.render(self.login_error, True, RED)
                error_rect = error_surface.get_rect(center=(self.panel_x + self.panel_width//2, self.panel_y + 300))
                screen.blit(error_surface, error_rect)
                
        elif self.show_shop_screen:
            # Shop panelini çiz
            self._draw_panel(screen)
            
            # Shop başlığı
            title_font = load_font(36, bold=True)
            title_text = "BUY SKILLS"
            title_surface = title_font.render(title_text, True, GOLD)
            title_rect = title_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
            screen.blit(title_surface, title_rect)
            
            # Token bilgisi
            token_font = load_font(24, bold=False)
            token_text = f"Current Tokens: {self.current_tokens}"
            token_surface = token_font.render(token_text, True, GOLD)
            token_rect = token_surface.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 60))
            screen.blit(token_surface, token_rect)
            
            # Geri butonunu çiz
            self.back_button.update()
            self.back_button.draw(screen)
            
            # Yetenekleri çiz
            for skill in self.shop_skills:
                skill.update()
                skill.draw(screen)
            
            # Hata mesajı (varsa)
            if self.shop_error:
                error_font = load_font(20, bold=True)
                error_surface = error_font.render(self.shop_error, True, RED)
                error_rect = error_surface.get_rect(midbottom=(self.panel_x + self.panel_width//2, self.panel_y + self.panel_height - 20))
                screen.blit(error_surface, error_rect)
                
            # Onay kutusu (varsa)
            if self.show_confirm_dialog and self.confirm_skill:
                # Karartma arka planı (ekranın tamamını biraz karartalım)
                darken = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                darken.fill((0, 0, 0, 150))  # Yarı-saydam siyah
                screen.blit(darken, (0, 0))
                
                # Onay kutusu
                pygame.draw.rect(screen, DARK_GRAY, self.confirm_dialog_rect, border_radius=10)
                pygame.draw.rect(screen, ORANGE, self.confirm_dialog_rect, width=3, border_radius=10)
                
                # Başlık
                dialog_title_font = load_font(24, bold=True)
                dialog_title = "SATIN ALMA ONAYI"
                dialog_title_surf = dialog_title_font.render(dialog_title, True, ORANGE)
                dialog_title_rect = dialog_title_surf.get_rect(midtop=(self.confirm_dialog_rect.centerx, self.confirm_dialog_rect.y + 15))
                screen.blit(dialog_title_surf, dialog_title_rect)
                
                # Onay metni
                confirm_font = load_font(20)
                skill_name = self.confirm_skill.name
                confirm_text = f"{skill_name} yetenegini"
                confirm_text2 = f"{self.confirm_skill.cost} token ile"
                confirm_text3 = " satın almak istiyor musunuz?"
                
                text_y = self.confirm_dialog_rect.y + 50
                confirm_surf = confirm_font.render(confirm_text, True, WHITE)
                confirm_rect = confirm_surf.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
                screen.blit(confirm_surf, confirm_rect)
                
                text_y += 25
                confirm_surf2 = confirm_font.render(confirm_text2, True, GOLD)
                confirm_rect2 = confirm_surf2.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
                screen.blit(confirm_surf2, confirm_rect2)
                
                text_y += 25
                confirm_surf3 = confirm_font.render(confirm_text3, True, WHITE)
                confirm_rect3 = confirm_surf3.get_rect(midtop=(self.confirm_dialog_rect.centerx, text_y))
                screen.blit(confirm_surf3, confirm_rect3)
                
                # Butonları çiz
                self.confirm_yes_button.update()
                self.confirm_yes_button.draw(screen)
                
                self.confirm_no_button.update()
                self.confirm_no_button.draw(screen)
        elif self.show_level_selection:
            # Seviye seçim ekranı için panel çiz
            self._draw_panel(screen)
            
            # Seviye seçim ekranı başlığı
            level_title = load_font(40, bold=True).render("SELECT LEVEL", True, CYAN)
            level_title_rect = level_title.get_rect(midtop=(self.panel_x + self.panel_width//2, self.panel_y + 10))
            screen.blit(level_title, level_title_rect)
            
            # Geri butonunu çiz
            self.back_button.update()
            self.back_button.draw(screen)
            
            # Seviye butonlarını çiz
            for button in self.level_buttons:
                button.update()
                button.draw(screen)
        else:
            # Panel çiz
            self._draw_panel(screen)
            
            # Hangi menüdeyiz ona göre buton çizimi yap
            active_buttons = {
                "main": self.main_buttons,
                "options": self.options_buttons,
                "settings": self.settings_buttons
            }.get(self.current_menu, [])
            
            # Aktif menünün butonlarını çiz
            for button in active_buttons:
                button.update()
                button.draw(screen)
            
            # Options ve Settings menüsünde back butonu göster
            if self.current_menu in ["options", "settings"]:
                self.back_button.update()
                self.back_button.draw(screen)
            
            # Settings menüsündeki kaydırıcıları çiz
            if self.current_menu == "settings":
                self.music_slider.draw(screen)
                self.sound_slider.draw(screen)
                self.brightness_slider.draw(screen)
        
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.render()
            clock.tick(60)  # 60 FPS

    def login(self):
        print("Giriş sayfasi aciliyor...")
        self.show_login_screen = True
    
    def process_login(self):
        # Bu fonksiyon login butonuna basıldığında çalışır
        if not self.nickname_input.text or not self.password_input.text:
            self.login_error = "Kullanıcı adı ve sifre gerekli!"
            return
            
        print(f"Giriş yapılıyor: {self.nickname_input.text}")
        self.logged_in_user = self.nickname_input.text
        self.show_login_screen = False
        self.current_menu = "main"

    def confirm_purchase(self):
        """Satın alma işlemini onayla"""
        if self.confirm_skill:
            success, new_tokens, error = self.confirm_skill.handle_click(self.current_tokens)
            if success:
                self.current_tokens = new_tokens
                print(f"{self.confirm_skill.name} satın alındı! Kalan token: {self.current_tokens}")
            elif error:
                self.shop_error = error
                self.shop_error_timer = pygame.time.get_ticks()
                print(f"Satın alma hatası: {error}")
        
        # Onay kutusunu kapat
        self.show_confirm_dialog = False
        self.confirm_skill = None
    
    def cancel_purchase(self):
        """Satın alma işlemini iptal et"""
        self.show_confirm_dialog = False
        self.confirm_skill = None
        print("Satın alma iptal edildi.")

    def toggle_fullscreen(self):
        """Tam ekran modunu değiştir"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
            print("Tam ekran moduna geçildi")
        else:
            screen = pygame.display.set_mode(self.window_size)
            print("Pencere moduna geçildi")

if __name__ == "__main__":
    menu = Menu()
    menu.run()


