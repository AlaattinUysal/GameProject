import pygame
import os

# Pygame başlat
pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Karakter Animasyonu")

# Renkler
WHITE = (255, 255, 255)

# Saat (FPS kontrolü için)
clock = pygame.time.Clock()

# --- Karakter Sınıfı ---
class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_folder):
        super().__init__()

        self.scale_factor = 3  # Karakteri 3 kat büyüt
        
        # Animasyonları yükle
        self.animations = {
            'idle': self.load_idle_image(os.path.join(sprite_folder, 'Idle.png')),
            'walk': self.load_images(os.path.join(sprite_folder, 'Walk.png'), 6),
            'attack': self.load_images(os.path.join(sprite_folder, 'Attack1.png'), 4)
        }

        # **Başlangıç animasyonu kesin "idle" olacak**
        self.current_action = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.current_action][self.frame_index]

        # **Karakter başlangıçta ekranda sabit**
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))

        # **Hareket değişkenleri**
        self.vel_x = 0  
        self.vel_y = 0
        self.speed = 3  
        self.gravity = 0.5
        self.jump_power = -10
        self.on_ground = False

        # Animasyon zamanlayıcı
        self.animation_speed = 15  
        self.animation_counter = 0

    def load_idle_image(self, sprite_path):
        """Idle için sadece ilk kareyi al"""
        try:
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            sheet_width, sheet_height = sprite_sheet.get_size()
            frame_width = sheet_width // 5  # 5 kare var diyelim
            frame = sprite_sheet.subsurface((0, 0, frame_width, sheet_height))
            frame = pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor))
            return [frame]  # Tek kare liste olarak döndür
        except Exception as e:
            print(f"Hata: {e}")
            return [pygame.Surface((50, 50))]  

    def load_images(self, sprite_path, frame_count):
        """Sprite sheet'ten belirli sayıda kare keserek bir liste döndürür."""
        images = []
        try:
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            sheet_width, sheet_height = sprite_sheet.get_size()
            frame_width = sheet_width // frame_count  
            
            for i in range(frame_count):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
                frame = pygame.transform.scale(frame, (frame.get_width() * self.scale_factor, frame.get_height() * self.scale_factor))
                images.append(frame)
        except Exception as e:
            print(f"Hata: {e}")
        
        return images if images else [pygame.Surface((50, 50))]  

    def update(self):
        """Hareketi uygula ve animasyonu güncelle."""
        
        self.rect.x += self.vel_x  # **Hareket yalnızca tuşa basılınca olacak!**
        self.rect.y += self.vel_y  # **Zıplama için**

        # Yerçekimi
        self.vel_y += self.gravity
        
        # Yere temas kontrolü
        if self.rect.bottom >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.vel_y = 0
            self.on_ground = True
        
        # Animasyon Güncelleme
        self.animate()
    
    def animate(self):
        """Mevcut eyleme göre animasyonu değiştirir."""
        self.animation_counter += 1
        if self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.current_action])
            self.image = self.animations[self.current_action][self.frame_index]

    def move_left(self):
        """Sola hareket et"""
        self.vel_x = -self.speed  # **Sol hareket**
        self.current_action = 'walk'

    def move_right(self):
        """Sağa hareket et"""
        self.vel_x = self.speed  # **Sağ hareket**
        self.current_action = 'walk'

    def stop_moving(self):
        """Hareketi durdur"""
        self.vel_x = 0  # **Tuştan el çekilince durmalı**
        if self.current_action != 'attack':  
            self.current_action = 'idle'

    def jump(self):
        """Zıplama işlemi"""
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def attack(self):
        """Saldırı animasyonunu başlat"""
        self.current_action = 'attack'

# --- Oyun Döngüsü ---

# **Karakter oluştur (EKRAN ORTASINDA BAŞLAT)**
sprite_folder = "C:/Users/Alperen/Masaüstü/OYUN/animasyonlar/1"
char = Character(sprite_folder)

# Pygame ana döngüsü
running = True
while running:
    screen.fill(WHITE)
    
    # Tuşları kontrol et
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        char.move_left()
    elif keys[pygame.K_RIGHT]:
        char.move_right()
    else:
        char.stop_moving()  # **Tuşu bırakınca hareket dursun**
    
    if keys[pygame.K_SPACE]:
        char.jump()
    if keys[pygame.K_f]:
        char.attack()
    
    # Karakteri güncelle
    char.update()

    screen.blit(char.image, char.rect.topleft)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()
    clock.tick(60)  

pygame.quit()
#karakter oluşturuldu.Yürüme ve zıplama fonskiyonları doğru bir şekilde çalışmakta.Saldırı kısmı sorunlu çalışıyor.
#425468 ALPEREN ALTUNEL TARAFINDAN YAZILDI.
