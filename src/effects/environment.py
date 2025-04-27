import pygame
import os
import sys
import math
import random
import time

# Pygame başlatılıyor
pygame.init()

# Ekran boyutları
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Ekranı oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("-🎮- THE WAY -🎮-")

# Assets klasörünü ayarla
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "menu_tasarim")

# Renkler
WHITE = (255, 255, 255)
RED = (231, 76, 60)
DARK_BLUE = (25, 25, 50)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
CLOUD_WHITE = (255, 255, 255)
CLOUD_LIGHT = (245, 245, 255)
CLOUD_SHADOW = (225, 235, 245)
LIGHT_BLUE = (200, 230, 255)
SHADOW_GRAY = (180, 200, 220)
SUN_YELLOW = (255, 223, 0)
MOUNTAIN_COLOR = (34, 45, 65)

# Martı Renkleri
BIRD_COLORS = [
    (255, 255, 255),  # Beyaz
    (240, 240, 240),  # Açık gri
    (220, 220, 220),  # Gri
    (200, 200, 200),  # Koyu gri
    (230, 235, 240)   # Grimsi beyaz
]

# Fontlar
try:
    # Press Start 2P fontunu dene
    pixel_font_path = os.path.join(ASSETS_DIR, "Font", "PressStart2P-Regular.ttf")
    if not os.path.exists(pixel_font_path):
        # Alternatif olarak Planes_ValMore kullan
        pixel_font_path = os.path.join(ASSETS_DIR, "Font", "Planes_ValMore.ttf")
        print("Press Start 2P fontu bulunamadı, Planes_ValMore kullanılıyor.")
    
    button_font = pygame.font.Font(pixel_font_path, 36)
    title_font = pygame.font.Font(os.path.join(ASSETS_DIR, "Font", "Planes_ValMore.ttf"), 48)
    small_font = pygame.font.Font(pixel_font_path, 24)
except Exception as e:
    print(f"Font yüklenirken hata: {e}. Varsayılan font kullanılacak.")
    button_font = pygame.font.SysFont(None, 50)
    title_font = pygame.font.SysFont(None, 60)
    small_font = pygame.font.SysFont(None, 30)

# Ayarlar durumu için global değişkenler
settings_states = {
    "Music": True,
    "Sound Effects": True,
    "Fullscreen": False,
    "VSync": True
}

# Güneş animasyonu için değişkenler
sun_pos_y = 80
sun_speed = 0.1

clock = pygame.time.Clock()
FPS = 60

# Cloud sınıfını güncelle - deneme2.py'deki yaklaşımı kullanarak
class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        
        # Bulut renkleri
        self.WHITE = (255, 255, 255)
        self.LIGHT_BLUE = (200, 230, 255)
        self.SHADOW_GRAY = (180, 200, 220)
    
    def update(self, dt):
        # Sadece sağa doğru hareket et
        self.x += self.speed
        # Ekranın sağından çıkınca soldan tekrar gir
        if self.x > 1200 + 100:  # 1200, ekran genişliği olduğunu varsayıyorum
            self.x = -100
    
    def draw(self, surface):
        # Gölge (arkada, biraz aşağıda)
        pygame.draw.circle(surface, self.SHADOW_GRAY, (self.x, self.y + 5), 30)
        pygame.draw.circle(surface, self.SHADOW_GRAY, (self.x + 40, self.y + 5), 35)
        pygame.draw.circle(surface, self.SHADOW_GRAY, (self.x + 80, self.y + 5), 30)
        pygame.draw.circle(surface, self.SHADOW_GRAY, (self.x + 20, self.y - 15 + 5), 35)
        pygame.draw.circle(surface, self.SHADOW_GRAY, (self.x + 60, self.y - 10 + 5), 30)

# Mantar sınıfı
class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # Mantar renkleri
        self.cap_color = (198, 40, 40)  # Kırmızı şapka
        self.stem_color = (240, 235, 220)  # Krem renkli gövde
        self.size = random.randint(15, 25)  # Rastgele mantar boyutu
        
    def update(self, dt):
        # Sabit duruyor
        pass
        
    def draw(self, surface):
        # Mantarın gövdesini çiz
        stem_width = self.size // 2
        stem_height = self.size * 1.2
        pygame.draw.rect(surface, self.stem_color, 
                         (self.x - stem_width//2, self.y - stem_height, 
                          stem_width, stem_height))
        
        # Gövdede hafif gölge
        stem_shadow = (230, 225, 210)
        pygame.draw.line(surface, stem_shadow,
                        (self.x - stem_width//2 + 2, self.y - stem_height + 5),
                        (self.x - stem_width//2 + 2, self.y - 5),
                        2)
        
        # Mantarın şapkasını çiz (yarım elips şeklinde) - benekler olmadan düz renk
        cap_radius = self.size
        cap_rect = pygame.Rect(
            self.x - cap_radius, 
            self.y - stem_height - cap_radius//2,
            cap_radius * 2,
            cap_radius
        )
        pygame.draw.ellipse(surface, self.cap_color, cap_rect)
        
        # Benekleri tamamen kaldırdık

# Ağaç sınıfı
class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # Ağaç boyutu ve özellikleri
        self.trunk_color = (120, 81, 45)        # Ana gövde rengi
        self.dark_trunk_color = (90, 60, 35)    # Koyu gövde rengi (gölgeler için)
        
        # Yaprak renkleri
        leaf_colors = [
            (34, 139, 34),  # Orman yeşili
            (50, 120, 50),  # Açık yeşil
            (60, 150, 60),  # Parlak yeşil
        ]
        self.leaf_color = random.choice(leaf_colors)
        
        # Ağaç boyutu
        self.trunk_width = random.randint(25, 35)
        self.trunk_height = random.randint(140, 180)
        
        # Ağaç yapısı - sadece gövde ve yaprak kümeleri
        self.treetop_radius = self.trunk_width * 3  # Ağaç tepesi boyutu
        
        # Yaprak kümeleri - sadece ağacın üst kısmında
        self.leaf_clusters = []
        
        # Ana yaprak kümesi (ağacın tepesinde büyük küme)
        self.leaf_clusters.append({
            'x': self.x,
            'y': self.y - self.trunk_height - self.treetop_radius * 0.3,
            'radius': self.treetop_radius
        })
        
        # Yan yaprak kümeleri (ana kümenin etrafında)
        for i in range(3):
            angle = random.uniform(0, 360)
            distance = self.treetop_radius * 0.6
            
            leaf_x = self.x + math.cos(math.radians(angle)) * distance
            leaf_y = self.y - self.trunk_height - self.treetop_radius * 0.3 + math.sin(math.radians(angle)) * distance * 0.7
            
            self.leaf_clusters.append({
                'x': leaf_x,
                'y': leaf_y,
                'radius': self.treetop_radius * 0.7
            })
        
        # Elmaları yaprakların içinde rastgele konumlandır (2-3 elma)
        self.apples = []
        apple_count = random.randint(2, 3)
        
        # Elmalar yaprak kümelerinin içinde rastgele yerleştirilir
        for _ in range(apple_count):
            # Rastgele bir yaprak kümesi seç
            leaf_cluster = random.choice(self.leaf_clusters)
            
            # Yaprak kümesinin içinde rastgele bir konum belirle
            angle = random.uniform(0, 360)
            distance = random.uniform(0, leaf_cluster['radius'] * 0.7)  # Kümenin kenarlarına yaklaşmasın
            
            apple_x = leaf_cluster['x'] + math.cos(math.radians(angle)) * distance
            apple_y = leaf_cluster['y'] + math.sin(math.radians(angle)) * distance
            
            self.apples.append(Apple(apple_x, apple_y))
    
    def update(self, dt):
        # Artık sallanma efekti yok
        # Elmaları güncelle
        for apple in self.apples:
            apple.update(dt)
    
    def draw(self, surface):
        # 1. Gövdeyi çiz (düz gövde)
        trunk_points = [
            (self.x - self.trunk_width // 2, self.y),  # Sol alt
            (self.x + self.trunk_width // 2, self.y),  # Sağ alt
            (self.x + self.trunk_width // 2, self.y - self.trunk_height),  # Sağ üst
            (self.x - self.trunk_width // 2, self.y - self.trunk_height)   # Sol üst
        ]
        pygame.draw.polygon(surface, self.trunk_color, trunk_points)
        
        # Gövde detayları
        trunk_center = self.x
        pygame.draw.line(surface, self.dark_trunk_color,
                       (trunk_center - self.trunk_width // 6, self.y),
                       (trunk_center - self.trunk_width // 6, self.y - self.trunk_height * 0.9),
                       2)
        
        # 2. Yaprak kümelerini çiz - artık içlerindeki koyu detaylar yok
        for cluster in self.leaf_clusters:
            # Yaprak kümesini çiz - sabit konum
            pygame.draw.circle(surface, self.leaf_color,
                             (int(cluster['x']), int(cluster['y'])),
                             int(cluster['radius']))
            
            # Koyu detaylar tamamen kaldırıldı
        
        # 3. Elmaları çiz
        for apple in self.apples:
            apple.draw(surface)

# Çiçek sınıfı
class Flower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # Çiçek özellikleri
        self.stem_color = (0, 100, 0)  # Koyu yeşil
        
        # Rastgele çiçek rengi seç
        flower_colors = [
            (255, 0, 0),    # kırmızı
            (255, 165, 0),  # turuncu
            (255, 192, 203),# pembe
            (255, 255, 0),  # sarı
            (238, 130, 238),# mor
            (255, 255, 255) # beyaz
        ]
        self.flower_color = random.choice(flower_colors)
        
        # Çiçek boyutları
        self.flower_radius = random.randint(10, 20)
        self.stem_height = random.randint(30, 60)
        
        # Sallantı efekti için
        self.time_passed = random.random() * 1000
        self.sway_speed = 0.002
        self.sway_amount = 5
    
    def update(self, dt):
        self.time_passed += dt
    
    def draw(self, surface):
        # Sallantı miktarını hesapla
        sway_offset = math.sin(self.time_passed * self.sway_speed) * self.sway_amount
        
        # Çiçek sapını çiz
        stem_top_x = self.x + sway_offset
        pygame.draw.line(surface, self.stem_color, 
                        (self.x, self.y), 
                        (stem_top_x, self.y - self.stem_height), 
                        3)
        
        # Çiçeği çiz (merkez ve taç yapraklar)
        center_x = stem_top_x
        center_y = self.y - self.stem_height
        
        # Taç yapraklar
        for i in range(8):  # 8 taç yaprak
            angle = math.radians(i * 45)
            petal_x = center_x + math.cos(angle) * self.flower_radius
            petal_y = center_y + math.sin(angle) * self.flower_radius
            pygame.draw.circle(surface, self.flower_color, 
                              (int(petal_x), int(petal_y)), 
                              int(self.flower_radius * 0.7))
        
        # Çiçeğin merkezi
        pygame.draw.circle(surface, (255, 255, 0), 
                          (int(center_x), int(center_y)), 
                          int(self.flower_radius * 0.5))

# Martı (Bird) sınıfı
class Bird:
    def __init__(self, x, y, image_name):
        self.x = x
        # Kuşların daha yüksekten uçması için y pozisyonunu yukarı taşı
        # SCREEN_HEIGHT'ın 1/3'ü ve 1/5'i arasında rasgele bir yükseklik
        self.base_y = random.randint(int(SCREEN_HEIGHT / 5), int(SCREEN_HEIGHT / 3))
        self.y = self.base_y
        
        # Daha sakin bir hareket için hızı azalt
        self.speed = random.uniform(0.8, 1.5)
        
        # Kuş renkleri ve boyutları
        self.color = random.choice(BIRD_COLORS)
        self.size = pygame.math.Vector2(50, 15)  # Boyut için vektör kullan - biraz daha büyük
        
        # Kanat çırpma ve süzülme modelleri
        self.wing_position = 0
        self.wing_direction = 1
        self.wing_delay = random.randint(6, 12)  # Kanat çırpma gecikmesi - daha yavaş
        self.wing_timer = random.randint(0, self.wing_delay)
        
        # Uçuş modları
        self.flight_mode = "flap"  # "flap" veya "glide"
        self.flight_timer = 0
        self.flap_duration = random.randint(100, 180)  # Daha uzun kanat çırpma süresi
        self.glide_duration = random.randint(120, 240)  # Daha uzun süzülme süresi
        
        # Uçuş hareketi parametreleri - daha sakin hareketler için düşük değerler
        self.vertical_drift = random.uniform(0.003, 0.01)  # Daha da yavaş dikey hareket
        self.vertical_amplitude = random.uniform(0.8, 1.5)  # Daha az salınım
        self.flying_offset = 0
        self.horizontal_speed_factor = random.uniform(0.9, 1.0)  # Yatay hız faktörü
        
    def update(self, dt):
        # Daha stabil bir hareket için farklı zaman ölçeği kullan
        time_scale = dt * 0.05
        
        # Hız hesaplama
        adjusted_speed = self.speed * self.horizontal_speed_factor
        if self.flight_mode == "glide":
            adjusted_speed *= 1.05  # Süzülürken biraz daha hızlı
        
        # Pozisyon güncelleme
        self.x += adjusted_speed
        if self.x > SCREEN_WIDTH + 50:
            self.x = -50
            # Yeni bir yükseklik belirle, ancak minimum yüksekliği koru
            self.base_y = random.randint(int(SCREEN_HEIGHT / 5), int(SCREEN_HEIGHT / 3))
            self.y = self.base_y
        
        # Uçuş modu sürelerini güncelle
        self.flight_timer += 1
        
        # Uçuş modunu değiştir
        if self.flight_mode == "flap" and self.flight_timer > self.flap_duration:
            self.flight_mode = "glide"
            self.flight_timer = 0
            self.wing_position = 0
            self.wing_direction = 0
        elif self.flight_mode == "glide" and self.flight_timer > self.glide_duration:
            self.flight_mode = "flap"
            self.flight_timer = 0
            self.wing_direction = 1
        
        # Kanat animasyonu
        if self.flight_mode == "flap":
            self.wing_timer += 1
            if self.wing_timer >= self.wing_delay:
                self.wing_timer = 0
                self.wing_position += self.wing_direction
                
                if self.wing_position >= 2:
                    self.wing_position = 2
                    self.wing_direction = -1
                elif self.wing_position <= 0:
                    self.wing_position = 0
                    self.wing_direction = 1
        
        # Dikey hareket hesaplama
        if self.flight_mode == "flap":
            flap_lift = 0
            if self.wing_position == 0 and self.wing_direction == 1:
                flap_lift = -0.3  # Kanat çırparken yukarı kuvvet
            
            # Çok hafif bir titreşim ekle
            flutter = math.sin(pygame.time.get_ticks() * 0.05) * 0.3
            self.flying_offset = math.sin(pygame.time.get_ticks() * self.vertical_drift) * self.vertical_amplitude + flap_lift + flutter
        else:
            # Süzülme modunda daha düz bir yol
            self.flying_offset = math.sin(pygame.time.get_ticks() * (self.vertical_drift * 0.3)) * self.vertical_amplitude
        
    def draw(self, surface):
        body_length = self.size.x
        body_height = self.size.y
        
        # Ana gövde (oval)
        pygame.draw.ellipse(surface, self.color, 
                           (self.x, self.y + self.flying_offset, 
                            body_length, body_height))
        
        # Kuş başı
        head_radius = body_height * 0.7
        head_x = self.x + body_length - head_radius
        head_y = self.y + body_height/2 + self.flying_offset - 1
        pygame.draw.circle(surface, self.color, 
                          (int(head_x), int(head_y)), 
                          int(head_radius))
        
        # Göz
        eye_x = head_x + head_radius/2
        eye_y = head_y - 1
        pygame.draw.circle(surface, (0, 0, 0), (int(eye_x), int(eye_y)), 2)
        
        # Gaga
        beak_points = [
            (head_x + head_radius, head_y),
            (head_x + head_radius + 12, head_y + 1),
            (head_x + head_radius, head_y + 3)
        ]
        pygame.draw.polygon(surface, (255, 200, 0), beak_points)
        
        # Kanatlar için başlangıç pozisyonu
        wing_x = self.x + body_length/3
        wing_y = self.y + body_height/2 + self.flying_offset
        
        # Kanat renkleri
        wing_color = (max(self.color[0]-60, 100), max(self.color[1]-60, 100), max(self.color[2]-60, 100))
        secondary_color = (max(self.color[0]-120, 80), max(self.color[1]-120, 80), max(self.color[2]-120, 80))
        
        # Uçuş moduna göre kanat pozisyonları
        if self.flight_mode == "glide":
            # Süzülme modu - yatay kanatlar
            left_wing_points = [
                (wing_x, wing_y),
                (wing_x - 40, wing_y - 8),
                (wing_x - 30, wing_y - 3)
            ]
            right_wing_points = [
                (wing_x + 5, wing_y),
                (wing_x + 40, wing_y - 8),
                (wing_x + 30, wing_y - 3)
            ]
        else:
            # Kanat çırpma modu
            if self.wing_position == 0:
                # Yukarda
                left_wing_points = [
                    (wing_x, wing_y),
                    (wing_x - 35, wing_y - 25),
                    (wing_x - 25, wing_y - 5)
                ]
                right_wing_points = [
                    (wing_x + 5, wing_y),
                    (wing_x + 35, wing_y - 25),
                    (wing_x + 25, wing_y - 5)
                ]
            elif self.wing_position == 1:
                # Ortada
                left_wing_points = [
                    (wing_x, wing_y),
                    (wing_x - 30, wing_y - 5),
                    (wing_x - 20, wing_y)
                ]
                right_wing_points = [
                    (wing_x + 5, wing_y),
                    (wing_x + 30, wing_y - 5),
                    (wing_x + 20, wing_y)
                ]
            else:
                # Aşağıda
                left_wing_points = [
                    (wing_x, wing_y),
                    (wing_x - 30, wing_y + 15),
                    (wing_x - 15, wing_y + 5)
                ]
                right_wing_points = [
                    (wing_x + 5, wing_y),
                    (wing_x + 30, wing_y + 15),
                    (wing_x + 15, wing_y + 5)
                ]
        
        # Kanatları çiz
        pygame.draw.polygon(surface, wing_color, left_wing_points)
        pygame.draw.polygon(surface, wing_color, right_wing_points)
        pygame.draw.line(surface, secondary_color, left_wing_points[0], left_wing_points[1], 2)
        pygame.draw.line(surface, secondary_color, right_wing_points[0], right_wing_points[1], 2)
        
        # Kuyruk çizimi
        tail_width = body_height * 1.2
        tail_length = body_height * 1.5
        tail_points = [
            (self.x, self.y + body_height/2 + self.flying_offset),
            (self.x - tail_length, self.y + body_height/2 - tail_width/2 + self.flying_offset),
            (self.x - tail_length/2, self.y + body_height/2 + self.flying_offset),
            (self.x - tail_length, self.y + body_height/2 + tail_width/2 + self.flying_offset)
        ]
        pygame.draw.polygon(surface, self.color, tail_points)
        pygame.draw.lines(surface, (max(self.color[0]-40, 100), max(self.color[1]-40, 100), max(self.color[2]-40, 100)), 
                         False, [tail_points[1], tail_points[2], tail_points[3]], 1)
                         
        # Ayaklar (kuş uçarken görünmez)
        if self.flying_offset > 2:
            foot_y = self.y + body_height + 5 + self.flying_offset
            pygame.draw.line(surface, (255, 165, 0), 
                           (self.x + body_length/3, self.y + body_height + self.flying_offset),
                           (self.x + body_length/3 - 3, foot_y), 1)
            pygame.draw.line(surface, (255, 165, 0), 
                           (self.x + body_length/3 + 6, self.y + body_height + self.flying_offset),
                           (self.x + body_length/3 + 9, foot_y), 1)

# Gelişmiş Bulut Sınıfı
class ImprovedCloud:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = random.uniform(0.2, 0.5)  # Rastgele hız

    def update(self, dt):
        self.x += self.speed
        if self.x > SCREEN_WIDTH + 100:
            self.x = -100

    def draw(self, surface):
        # Gölge (arkada, biraz aşağıda)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x, self.y + 5), 30)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 40, self.y + 5), 35)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 80, self.y + 5), 30)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 20, self.y - 15 + 5), 35)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 60, self.y - 10 + 5), 30)

        # Üst bulutlar (beyaz ve açık mavi)
        pygame.draw.circle(surface, WHITE, (self.x, self.y), 30)
        pygame.draw.circle(surface, WHITE, (self.x + 40, self.y), 35)
        pygame.draw.circle(surface, WHITE, (self.x + 80, self.y), 30)
        pygame.draw.circle(surface, WHITE, (self.x + 20, self.y - 15), 35)
        pygame.draw.circle(surface, LIGHT_BLUE, (self.x + 40, self.y + 10), 35)
        pygame.draw.circle(surface, LIGHT_BLUE, (self.x + 60, self.y - 10), 30)

# Sun (Güneş) sınıfı
class Sun:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 223, 0)  # Sarı
        self.ray_length = radius * 1.5
        
    def update(self, dt):
        # Artık nabız efekti yok
        pass

    def draw(self, surface):
        # Sadece sabit boyutta güneş çiz - nabız efekti yok
        # Güneş diskini çiz
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        
        # Işınları çiz
        for i in range(12):  # 12 ışın
            angle = math.radians(i * 30)
            start_x = self.x + math.cos(angle) * self.radius
            start_y = self.y + math.sin(angle) * self.radius
            end_x = self.x + math.cos(angle) * (self.radius + self.ray_length)
            end_y = self.y + math.sin(angle) * (self.radius + self.ray_length)
            
            # Işın kalınlığını değiştir (merkeze yakın daha kalın)
            pygame.draw.line(surface, self.color, 
                            (int(start_x), int(start_y)),
                            (int(end_x), int(end_y)),
                            3)
        
        # Güneş yüzeyi için turuncu çemberi çiz
        pygame.draw.circle(surface, (255, 165, 0), (int(self.x), int(self.y)), int(self.radius * 0.7))

# Moon (Ay) sınıfı
class Moon:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (220, 220, 255)  # Açık mavi-beyaz
        self.crater_color = (200, 200, 235)  # Kraterlerin rengi
        self.time_passed = 0
        self.twinkle_speed = 0.002
        
        # Kraterlerin konumları
        self.craters = []
        for _ in range(8):
            # Rasrgele krater pozisyonları oluştur (ay içinde)
            crater_x = random.randint(-radius//2, radius//2)
            crater_y = random.randint(-radius//2, radius//2)
            
            # Krater merkezden çok uzaksa, ayın içinde kalmasını sağla
            dist = math.sqrt(crater_x**2 + crater_y**2)
            if dist > radius * 0.6:
                crater_x *= (radius * 0.6) / dist
                crater_y *= (radius * 0.6) / dist
                
            crater_size = random.randint(3, 8)
            self.craters.append((crater_x, crater_y, crater_size))
    
    def update(self, dt):
        # Zamanı güncelle
        self.time_passed += dt
        
    def draw(self, surface):
        # Hafif parıldama efekti için
        twinkle = math.sin(self.time_passed * self.twinkle_speed) * 10
        glow_radius = self.radius + 5 + twinkle
        
        # Önce ışık halesini çiz
        for i in range(5):
            alpha = 50 - i * 10  # Dış kenara doğru saydamlık artar
            glow_surface = pygame.Surface((glow_radius * 2.5, glow_radius * 2.5), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (220, 220, 255, alpha), 
                            (int(glow_surface.get_width() // 2), int(glow_surface.get_height() // 2)), 
                            int(glow_radius + i * 4))
            surface.blit(glow_surface, 
                        (int(self.x - glow_surface.get_width() // 2), 
                        int(self.y - glow_surface.get_height() // 2)))
        
        # Ayın kendisini çiz
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))
        
        # Kraterleri çiz
        for crater in self.craters:
            x, y, size = crater
            pygame.draw.circle(surface, self.crater_color, 
                            (int(self.x + x), int(self.y + y)), int(size))

# Star (Yıldız) sınıfı
class Star:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 255, 255)  # Beyaz
        self.time_passed = random.random() * 1000  # Başlangıç fazını rastgele yap
        self.twinkle_speed = 0.003 + random.random() * 0.005  # Daha yavaş parıldama hızı
        
    def update(self, dt):
        # Zamanı yavaşça güncelle - daha sakin bir parıldama için
        self.time_passed += dt * 0.05
    
    def draw(self, surface, opacity=255):
        # Yıldız parıldama efekti
        brightness = 0.7 + abs(math.sin(self.time_passed * self.twinkle_speed)) * 0.3  # Daha az parıldama
        
        # Opaklığı ayarla (0-255 arası)
        opacity = max(0, min(255, opacity))
        
        # Renk ve opaklık hesapla
        alpha_factor = opacity / 255.0
        star_color = (
            int(self.color[0] * brightness * alpha_factor),
            int(self.color[1] * brightness * alpha_factor),
            int(self.color[2] * brightness * alpha_factor)
        )
        
        # Küçük yıldızları nokta olarak çiz
        if self.size <= 1:
            surface.set_at((int(self.x), int(self.y)), star_color)
        else:
            # Büyük yıldızları daire olarak çiz
            pygame.draw.circle(surface, star_color, (int(self.x), int(self.y)), self.size)
            
            # Parıldama efekti için küçük çizgiler ekle (çok nadiren)
            if brightness > 0.95 and opacity > 200 and self.size >= 2:  # Daha nadir parıldama
                # Yatay ve dikey çizgiler
                pygame.draw.line(surface, star_color, 
                                (int(self.x - self.size*1.5), int(self.y)), 
                                (int(self.x + self.size*1.5), int(self.y)), 1)
                pygame.draw.line(surface, star_color, 
                                (int(self.x), int(self.y - self.size*1.5)), 
                                (int(self.x), int(self.y + self.size*1.5)), 1)

# Elma sınıfı
class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # Elma özellikleri
        self.radius = 15  # Elmanın yarıçapı
        self.color = (255, 0, 0)  # Kırmızı
        self.stem_color = (139, 69, 19)  # Kahverengi
    
    def update(self, dt):
        # Artık elma sallanmıyor, sabit duruyor
        pass
    
    def draw(self, surface):
        # Elmayı çiz - artık sallanma efekti yok
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Elmanın sapını çiz
        stem_height = 10
        pygame.draw.line(surface, self.stem_color, 
                         (int(self.x), int(self.y - self.radius)), 
                         (int(self.x), int(self.y - self.radius - stem_height)), 2)
        
        # Küçük bir yaprak ekle
        leaf_size = 5
        pygame.draw.circle(surface, (0, 150, 0), 
                          (int(self.x + 5), int(self.y - self.radius - stem_height + 5)), 
                          leaf_size)

# --- Ana Oyun Döngüsü ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kuş Animasyonu - Pygame")
    clock = pygame.time.Clock()
    
    # Fontu yükle
    font = pygame.font.SysFont('Arial', 16)
    
    # Animasyon nesnelerini oluştur
    clouds = [
        Cloud(100, 50, 0.5),    # Sol üst, hızlı
        Cloud(400, 80, 0.3),    # Orta üst, orta hızda
        Cloud(700, 60, 0.4),    # Sağ üst, orta-hızlı
        Cloud(200, 120, 0.45),  # Sol orta, orta-hızlı
        Cloud(600, 100, 0.35),  # Sağ orta, orta hızda
        Cloud(900, 90, 0.5),    # Sağ üst, hızlı
        Cloud(300, 150, 0.4)    # Orta, orta-hızlı
    ]
    
    improved_clouds = [
        ImprovedCloud(150, 30, 40, 20),  # Sol üst, küçük bulut
        ImprovedCloud(450, 40, 60, 30),  # Orta üst, orta boy bulut
        ImprovedCloud(750, 50, 50, 25)   # Sağ üst, orta boy bulut
    ]
    
    # Kuşları oluştur
    birds = [
        Bird(200, 200, "bird1"),
        Bird(300, 150, "bird2"),
        Bird(500, 250, "bird3"),
        Bird(700, 180, "bird4")
    ]
    
    # Güneşi ve ayı oluştur - güneş sağda, ay solda olacak
    sun = Sun(SCREEN_WIDTH - 150, -100, 50)  # Ekranın sağ tarafında, üst dışında başlıyor
    moon = Moon(150, SCREEN_HEIGHT + 100, 40)  # Ekranın sol tarafında, alt dışında başlıyor
    
    # Yıldızları oluştur
    stars = []
    for _ in range(50):  # Daha fazla yıldız
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT // 2)  # Ekranın yarısına kadar
        size = random.choice([1, 1, 1, 2, 3])  # Daha çok küçük yıldız
        stars.append(Star(x, y, size))
    
    # Mantarları oluştur - yere daha yakın olacak şekilde
    mushrooms = [
        Mushroom(150, SCREEN_HEIGHT - 10),
        Mushroom(250, SCREEN_HEIGHT - 10),
        Mushroom(650, SCREEN_HEIGHT - 10),
        Mushroom(850, SCREEN_HEIGHT - 10)
    ]
    
    # Ağaçları oluştur
    trees = [
        Tree(450, SCREEN_HEIGHT - 20),
        Tree(950, SCREEN_HEIGHT - 20),
        Tree(1100, SCREEN_HEIGHT - 20),
        Tree(200, SCREEN_HEIGHT - 20)
    ]
    
    # Çiçekleri oluştur
    flowers = [
        Flower(100, SCREEN_HEIGHT - 20),
        Flower(300, SCREEN_HEIGHT - 20),
        Flower(600, SCREEN_HEIGHT - 20),
        Flower(750, SCREEN_HEIGHT - 20),
        Flower(900, SCREEN_HEIGHT - 20),
        Flower(1050, SCREEN_HEIGHT - 20),
        Flower(400, SCREEN_HEIGHT - 20),
        Flower(550, SCREEN_HEIGHT - 20)
    ]
    
    # Gün/gece döngüsünü takip etmek için zaman değişkeni
    time_of_day = 0
    day_length = 60000  # 60 saniye = 1 dakika = 1 oyun günü
    
    running = True
    while running:
        dt = clock.tick(60)  # ms cinsinden geçen süre
        
        # Zamanı güncelle
        time_of_day = (time_of_day + dt) % day_length
        day_ratio = time_of_day / day_length  # 0 ile 1 arası, günün hangi noktasında olduğumuz
        
        # Gece-gündüz durumunu belirle
        is_night = day_ratio > 0.5
        
        # Güneş ve ay hareketlerini güncelle
        if not is_night:  # Gündüz: Güneş yukarıdan aşağıya (sağ tarafta)
            # Güneş hareketi - yukarıdan aşağıya (0 -> 0.5 arası)
            sun_progress = day_ratio / 0.5  # 0-1 arası
            
            # Güneş sağ tarafta sabit X konumunda, yukarıdan aşağıya
            sun.x = SCREEN_WIDTH - 150  # Sağ tarafta sabit
            sun.y = -100 + (SCREEN_HEIGHT + 200) * sun_progress  # Yukarıdan aşağıya
            sun.update(dt)
            
            # Ay ekranın sol alt dışında bekliyor
            moon.x = 150  # Sol tarafta sabit
            moon.y = SCREEN_HEIGHT + 100  # Ekranın altında (görünmez)
            moon.update(dt)
            
        else:  # Gece: Ay aşağıdan yukarıya (sol tarafta)
            # Ay hareketi - aşağıdan yukarıya (0.5 -> 1 arası)
            moon_progress = (day_ratio - 0.5) / 0.5  # 0-1 arası
            
            # Ay sol tarafta sabit X konumunda, aşağıdan yukarıya
            moon.x = 150  # Sol tarafta sabit
            moon.y = SCREEN_HEIGHT + 100 - (SCREEN_HEIGHT + 200) * moon_progress  # Aşağıdan yukarıya
            moon.update(dt)
            
            # Güneş ekranın sağ üst dışında bekliyor
            sun.x = SCREEN_WIDTH - 150  # Sağ tarafta sabit 
            sun.y = -100  # Ekranın üstünde (görünmez)
            sun.update(dt)
        
        # Gökyüzü rengi hesaplaması
        if is_night:
            # Gece yarısından sabaha
            if day_ratio > 0.9 or day_ratio < 0.1:
                # Şafak/gün doğumu geçişi
                if day_ratio > 0.9:
                    transition_progress = (day_ratio - 0.9) / 0.1
                else:
                    transition_progress = day_ratio / 0.1
                
                # Gece mavisi ile gündoğumu turuncu arasında geçiş
                bg_color = (
                    int(10 + transition_progress * 245),  # R: koyu maviden turuncuya
                    int(10 + transition_progress * 130),  # G: koyu maviden turuncuya
                    int(50 + transition_progress * 130)   # B: koyu maviden turuncuya
                )
            else:
                # Tam gece
                bg_color = (10, 10, 50)  # Koyu mavi
        else:
            # Sabahtan gece yarısına
            if day_ratio > 0.4 and day_ratio < 0.6:
                # Gün batımı geçişi
                transition_progress = (day_ratio - 0.4) / 0.2
                
                # Açık maviden gün batımı turuncusuna geçiş
                bg_color = (
                    int(135 + transition_progress * 120),  # R: açık maviden turuncuya
                    int(206 - transition_progress * 76),   # G: açık maviden turuncuya
                    int(235 - transition_progress * 185)   # B: açık maviden turuncuya
                )
            else:
                # Tam gündüz
                bg_color = (135, 206, 235)  # Açık mavi
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Ekranı temizle
        screen.fill(bg_color)
        
        # Yıldızları güncelle
        for star in stars:
            star.update(dt)
        
        # Yıldızları çiz (geceyse veya alacakaranlıksa görünür)
        if is_night or day_ratio > 0.4 and day_ratio < 0.6 or day_ratio > 0.9 or day_ratio < 0.1:
            star_opacity = 255
            if day_ratio > 0.4 and day_ratio < 0.5:  # Gün batımı başlangıcı
                star_opacity = int(255 * (day_ratio - 0.4) / 0.1)
            elif day_ratio > 0.5 and day_ratio < 0.6:  # Gün batımı sonu
                star_opacity = 255
            elif day_ratio > 0.9:  # Gün doğumu başlangıcı
                star_opacity = int(255 * (1 - (day_ratio - 0.9) / 0.1))
            elif day_ratio < 0.1:  # Gün doğumu sonu
                star_opacity = int(255 * (1 - day_ratio / 0.1))
            
            for star in stars:
                star.draw(screen, star_opacity)
        
        # Güneş ve ay çizimi - güneş gündüz, ay gece görünür
        if not is_night and sun.y < SCREEN_HEIGHT + 100:
            sun.draw(screen)
        
        if is_night and moon.y < SCREEN_HEIGHT + 100:
            moon.draw(screen)
        
        # Nesneleri güncelle ve çiz
        for cloud in clouds:
            cloud.update(dt)
            cloud.draw(screen)
        
        for cloud in improved_clouds:
            cloud.update(dt)
            cloud.draw(screen)
        
        # Yer çizgisini çiz
        ground_color = (100, 100, 40) if is_night else (34, 139, 34)  # Gece: koyu yeşil, Gündüz: çimen yeşili
        pygame.draw.rect(screen, ground_color, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))
        
        # Önce arka plandaki öğeleri çiz (derinlik hissi için)
        for tree in trees:
            tree.update(dt)
            tree.draw(screen)
        
        for mushroom in mushrooms:
            mushroom.update(dt)
            mushroom.draw(screen)
        
        for flower in flowers:
            flower.update(dt)
            flower.draw(screen)
            
        # Kuşları güncelle ve çiz
        for bird in birds:
            bird.update(dt)
            bird.draw(screen)
        
        # FPS ve gün/gece bilgisini göster
        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
        time_text = font.render("Gece" if is_night else "Gündüz", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        screen.blit(time_text, (10, 30))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 
