import pygame
import pytmx
import sys
from pygame.time import get_ticks

# Pygame'i başlat
pygame.init()

# Ekran ayarları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Güncellemeniz gerekmekte
tmx_data = pytmx.load_pygame('C:/Users/dell/Desktop/sw eng project/levels/village/village.tmx')

# Harita boyutları
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

# Kamera ayarları
camera_x, camera_y = 0, 0

# Çarpışma objelerini sakla
collision_rects = []
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
        for obj in layer:
            if hasattr(obj, 'x') and hasattr(obj, 'y'):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                collision_rects.append(rect)

# Başlangıç pozisyonunu
player_spawn = (250, 1200)
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "spawn":
        for obj in layer:
            if obj.name.lower() == "spawn_point":
                player_spawn = (obj.x, obj.y)

# Oyuncu sınıfı
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5
        self.jump_power = -10
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.on_ground = False

    def update(self, collision_rects):
        # Yatay hareket
        self.rect.x += self.velocity_x
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if self.velocity_x > 0:
                    self.rect.right = rect.left
                elif self.velocity_x < 0:
                    self.rect.left = rect.right
                self.velocity_x = 0

        # Dikey hareket
        self.velocity_y += self.gravity
        if self.velocity_y > self.max_fall_speed:
            self.velocity_y = self.max_fall_speed
        self.rect.y += self.velocity_y

        # Dikey çarpışma kontrolü
        self.on_ground = False
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if self.velocity_y > 0:
                    self.rect.bottom = rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = rect.bottom
                    self.velocity_y = 0

    def draw(self, surface, camera_x, camera_y):
        screen_x = self.rect.x - int(camera_x)
        screen_y = self.rect.y - int(camera_y)
        pygame.draw.rect(surface, (255, 0, 0), (screen_x, screen_y, self.rect.width, self.rect.height))

# Haritayı çiz
def draw_map(tmx_data, surface, camera_x, camera_y):
    surface.fill((0, 0, 0))
    
    # Tam sayı bölmesi kullan ve kamera offsetini hesapla
    start_x = max(0, int(camera_x / tmx_data.tilewidth))
    end_x = min(tmx_data.width, int((camera_x + SCREEN_WIDTH) / tmx_data.tilewidth) + 2)
    start_y = max(0, int(camera_y / tmx_data.tileheight))
    end_y = min(tmx_data.height, int((camera_y + SCREEN_HEIGHT) / tmx_data.tileheight) + 2)
    
    # Ekstra offset hesapla - kamera pozisyonunun tile grid'ine göre kalan kısmı
    offset_x = -(camera_x % tmx_data.tilewidth)
    offset_y = -(camera_y % tmx_data.tileheight)

    current_time = get_ticks()  # Şu anki zaman (milisaniye)

    for layer_idx, layer in enumerate(tmx_data.layers):
        if isinstance(layer, pytmx.TiledTileLayer):
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    # Tile'ın GID'sini al
                    gid = layer.data[y][x]
                    if gid:
                        # Animasyonlu tile varsa
                        tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                        if tile_properties and 'frames' in tile_properties:
                            frames = tile_properties['frames']
                            total_duration = sum(frame[1] for frame in frames)  # Tüm karelerin toplam süresi
                            if not frames or total_duration <= 0:
                                tile_image = tmx_data.get_tile_image_by_gid(gid)  # İlk kareyi çiz
                            else:
                                elapsed_time = current_time % total_duration  # Döngüde kalan zaman
                                current_frame = 0
                                frame_time = 0

                                # Doğru kareyi bul
                                for frame in frames:
                                    frame_time += frame[1]
                                    if elapsed_time <= frame_time:
                                        current_frame = frame[0]  # GID'yi direkt kullan
                                        break

                                # Animasyonlu tile'ı çiz
                                tile_image = tmx_data.get_tile_image_by_gid(current_frame)
                        else:
                            # Animasyon yoksa normal tile'ı çiz
                            tile_image = tmx_data.get_tile_image_by_gid(gid)

                        if tile_image:
                            # Yeni koordinat hesaplama yöntemi
                            screen_x = (x - start_x) * tmx_data.tilewidth + offset_x
                            screen_y = (y - start_y) * tmx_data.tileheight + offset_y
                            surface.blit(tile_image, (screen_x, screen_y))

# Oyuncuyu başlangıç pozisyonunda oluştur
player = Player(*player_spawn)

# Ana oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Klavye girişleri
    keys = pygame.key.get_pressed()
    player.velocity_x = 0
    if keys[pygame.K_a]:
        player.velocity_x = -player.speed
    if keys[pygame.K_d]:
        player.velocity_x = player.speed
    if keys[pygame.K_w] and player.on_ground:
        player.velocity_y = player.jump_power

    # Oyuncuyu güncelle
    player.update(collision_rects)

    # Kamerayı oyuncuya kilitle
    camera_x = int(max(0, min(player.rect.centerx - SCREEN_WIDTH // 2, map_width - SCREEN_WIDTH)))
    camera_y = int(max(0, min(player.rect.centery - SCREEN_HEIGHT // 2, map_height - SCREEN_HEIGHT)))

    # Haritayı ve oyuncuyu çiz
    draw_map(tmx_data, screen, camera_x, camera_y)
    player.draw(screen, camera_x, camera_y)
    pygame.display.flip()
    clock.tick(60)

# Oyunu kapat
pygame.quit()
sys.exit()