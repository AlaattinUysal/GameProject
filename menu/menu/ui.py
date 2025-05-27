import pygame
import os
import sys

# Add parent directory to path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from menu.config import (
    ORANGE, DARK_GRAY, WHITE, BRIGHT_ORANGE, DARK_ORANGE, 
    GREEN, GOLD, RED, LIGHT_GRAY
)
from menu.assets import load_font

# Piksel efektli buton için yardımcı fonksiyon
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
        self.current_val = max(min_val, min(max_val, current_val))  # Değeri sınırlar içinde tut
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
        
        # Değeri sınırlar içinde tut ve en yakın tam sayıya yuvarla
        self.current_val = max(self.min_val, min(self.max_val, round(self.current_val)))

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