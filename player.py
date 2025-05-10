import pygame
import pytmx
import sys
import json
import random
pygame.mixer.pre_init(44100, -16, 2, 2048)  # Frekans: 44.1kHz, 16-bit, stereo, 2048 buffer
pygame.mixer.init()
pygame.init()
# Screen settings
SCREEN_WIDTH = 1200 
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Samurai's path ")
clock = pygame.time.Clock()
FPS = 60
# Kod başında global değişkenleri tanımla
game_over = False
# Mesaj gösterimi için değişkenler
show_message = False
show2_message= False 
show3_message= False 
message_timer = 0
message2_timer = 0
message3_timer =0
message_duration = 5 * FPS  # 5 saniye (FPS cinsinden)
message_text = "The new feature is opened with the \"K\" button!"  # Gösterilecek mesaj
message2_text = "The new feature is opened with the \"L\" button!"
message3_text="The new feature is opened with the \"0\" button!"
# Game state and map management
current_map = "frozen_cave"  # Starting map
maps_data = {}  # Cache for loaded maps
transition_rects = {}  # Transition zones for each map

# Camera settings
ZOOM_FACTOR = 1.5  # 150% zoom
camera_x, camera_y = 0, 0
front_layer_index = 17
tile_cache = {}
parallax_factors_x = {}
parallax_factors_y = {}
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
hit_channel = pygame.mixer.Channel(0)  # Özel bir kanal ayır



# Camera class
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + SCREEN_WIDTH / (2 * ZOOM_FACTOR)
        y = -target.rect.centery + SCREEN_HEIGHT / (2 * ZOOM_FACTOR)
        x = max(-(self.width - SCREEN_WIDTH / ZOOM_FACTOR), min(0, x))
        y = max(-(self.height - SCREEN_HEIGHT / ZOOM_FACTOR), min(0, y))
        self.camera = pygame.Rect(x, y, self.width, self.height)

def load_map(map_name):
    global tmx_data, map_width, map_height, collision_rects, spike_rects
    global transition_rects, parallax_factors_x, parallax_factors_y, health_potions

    # Harita zaten önbellekteyse, önbellekten yükle
    if map_name in maps_data:
        map_data = maps_data[map_name]
        tmx_data = map_data["tmx_data"]
        map_width = map_data["map_width"]
        map_height = map_data["map_height"]
        collision_rects = map_data["collision_rects"]
        spike_rects = map_data["spike_rects"]
        transition_rects = map_data["transition_rects"]
        parallax_factors_x = map_data["parallax_factors_x"]
        parallax_factors_y = map_data["parallax_factors_y"]
        health_potions = map_data["health_potions"]
        return

    # Önbellekleri temizle
    tile_cache.clear()
    if 'player' in globals() and hasattr(player, 'scaled_image_cache'):
        player.scaled_image_cache.clear()

    # Harita dosyasını yükle
    map_file = f'levels/{map_name}/{map_name}.tmx'
    tmx_data = pytmx.load_pygame(map_file)
    map_width = tmx_data.width * tmx_data.tilewidth
    map_height = tmx_data.height * tmx_data.tileheight

    # Sağlık iksirlerini yükle
    health_potions = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "items":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y') and obj.name.lower() == "health_potion":
                    potion = HealthPotion(obj.x, obj.y)
                    health_potions.append(potion)

    # Çarpışma nesnelerini yükle
    collision_rects = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y'):
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    collision_rects.append(rect)

    # Tehlike nesnelerini yükle
    spike_rects = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "hazards":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y'):
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    spike_rects.append(rect)

    # Geçiş bölgelerini yükle
    transition_rects = {}
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "transitions":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y'):
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    if hasattr(obj, 'properties') and 'target_map' in obj.properties:
                        transition_info = {
                            'target_map': obj.properties['target_map'],
                            'target_spawn': obj.properties.get('target_spawn', 'spawn_point')
                        }
                        transition_rects[obj.name] = {
                            'rect': rect,
                            'info': transition_info
                        }

    # Paralaks faktörlerini güncelle
    update_parallax_factors()

    # Harita verilerini önbelleğe al
    maps_data[map_name] = {
        "tmx_data": tmx_data,
        "map_width": map_width,
        "map_height": map_height,
        "collision_rects": collision_rects,
        "spike_rects": spike_rects,
        "transition_rects": transition_rects,
        "parallax_factors_x": parallax_factors_x,
        "parallax_factors_y": parallax_factors_y,
        "health_potions": health_potions,
    }

# Clear tile cache when changing maps
tile_cache = {}

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("health.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False

    def draw(self, surface, camera_x, camera_y):
        if self.collected:
            return
        screen_x = (self.rect.x - camera_x) * ZOOM_FACTOR
        screen_y = (self.rect.y - camera_y) * ZOOM_FACTOR
        scaled_width = int(self.rect.width * ZOOM_FACTOR)
        scaled_height = int(self.rect.height * ZOOM_FACTOR)
        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        surface.blit(scaled_image, (screen_x, screen_y))


def update_parallax_factors():
    """Update parallax factors for the current map"""
    global parallax_factors_x, parallax_factors_y
    
    parallax_factors_x = {}
    parallax_factors_y = {}
    
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            # Layer properties
            layer_properties = getattr(layer, 'properties', {})
            
            # X axis parallax factor
            if 'parallax_factor_x' in layer_properties:
                parallax_factors_x[layer.name] = float(layer_properties['parallax_factor_x'])
            elif 'parallax_factor' in layer_properties:
                # Backward compatibility
                parallax_factors_x[layer.name] = float(layer_properties['parallax_factor'])
            elif layer.name.startswith('parallax_'):
                try:
                    index = int(layer.name.split('_')[1])
                    parallax_factors_x[layer.name] = max(0.1, 1.0 - (index * 0.1))
                except (IndexError, ValueError):
                    parallax_factors_x[layer.name] = 0.5
            
            # Y axis parallax factor
            if 'parallax_factor_y' in layer_properties:
                parallax_factors_y[layer.name] = float(layer_properties['parallax_factor_y'])
            elif 'parallax_factor' in layer_properties:
                # Backward compatibility
                parallax_factors_y[layer.name] = float(layer_properties['parallax_factor'])
            elif layer.name.startswith('parallax_'):
                try:
                    index = int(layer.name.split('_')[1])
                    parallax_factors_y[layer.name] = max(0.1, 1.0 - (index * 0.1))
                except (IndexError, ValueError):
                    parallax_factors_y[layer.name] = 0.5

def find_spawn_point(spawn_name="spawn_point"):
    """Find spawn point with given name in the current map"""
    default_spawn = (250, 1200)  # Default position if no spawn found
    
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "spawn":
            for obj in layer:
                if obj.name.lower() == spawn_name.lower():
                    return (obj.x, obj.y)
    
    # Return default spawn if no match found
    return default_spawn

def check_map_transitions():
    global current_map, camera_x, camera_y, camera, health_potions, show_message,show2_message, message_timer,message2_timer,show3_message,message3_timer
    
    for transition_name, transition_data in transition_rects.items():
        if player.hitbox.colliderect(transition_data['rect']):
            target_map = transition_data['info']['target_map']
            target_spawn = transition_data['info']['target_spawn']
            
            if target_map != current_map:
                current_map = target_map
                load_map(current_map)
                
                spawn_pos = find_spawn_point(target_spawn)
                player.rect.centerx = spawn_pos[0]
                player.rect.bottom = spawn_pos[1]
                player.update_hitbox()
                
                # İksirleri Tiled haritasından yeniden yükle
                health_potions = []
                for layer in tmx_data.layers:
                    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "items":
                        for obj in layer:
                            if hasattr(obj, 'x') and hasattr(obj, 'y') and obj.name.lower() == "health_potion":
                                potion = HealthPotion(obj.x, obj.y)
                                health_potions.append(potion)
                
                player.y_velocity = 0
                camera_x = max(0, min(player.rect.centerx - SCREEN_WIDTH//(2*ZOOM_FACTOR), 
                               map_width - SCREEN_WIDTH//ZOOM_FACTOR))
                camera_y = max(0, min(player.rect.centery - SCREEN_HEIGHT//(2*ZOOM_FACTOR), 
                               map_height - SCREEN_HEIGHT//ZOOM_FACTOR))
                
                camera = Camera(map_width, map_height)
                
                # Frozen Cave'e geçişte mesajı başlat
                if current_map == "frozen_cave":
                    show_message = True
                    message_timer = message_duration
                if current_map =="cyberpunk":
                    show2_message = True 
                    message2_timer = message_duration
                if current_map=="lab":
                    show3_message = True 
                    message3_timer=message_duration
                
                return True
    
    return False

# Zoom setting function
def set_zoom(factor):
    global ZOOM_FACTOR
    ZOOM_FACTOR = max(0.5, min(factor, 3))

# Spritesheet class
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()
        self.cache = {}

    def get_image(self, frame, width, height, scale):
        key = (frame, width, height, scale)
        if key not in self.cache:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
            image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
            self.cache[key] = image
        return self.cache[key]

    def get_animation_frames(self, frame_width, frame_height, scale):
        sheet_width, _ = self.sheet.get_size()
        frame_count = sheet_width // frame_width
        return [self.get_image(i, frame_width, frame_height, scale) for i in range(frame_count)]

# Tile cache for improved performance
tile_cache = {}

def draw_layer(layer, surface, camera_x, camera_y):
    if not isinstance(layer, pytmx.TiledTileLayer):
        return
    
    # If this is a parallax layer, adjust camera position according to factors
    adjusted_camera_x = camera_x
    adjusted_camera_y = camera_y
    
    # Apply parallax factor for X axis
    if layer.name in parallax_factors_x:
        factor_x = parallax_factors_x[layer.name]
        adjusted_camera_x *= factor_x
    
    # Apply parallax factor for Y axis
    if layer.name in parallax_factors_y:
        factor_y = parallax_factors_y[layer.name]
        adjusted_camera_y *= factor_y
    
    # Get current time (required for animations)
    current_time = pygame.time.get_ticks()
    
    # Calculate visible tile range
    start_x = max(0, int(adjusted_camera_x / tmx_data.tilewidth))
    end_x = min(tmx_data.width, int((adjusted_camera_x + SCREEN_WIDTH) / tmx_data.tilewidth) + 2)
    start_y = max(0, int(adjusted_camera_y / tmx_data.tileheight))
    end_y = min(tmx_data.height, int((adjusted_camera_y + SCREEN_HEIGHT) / tmx_data.tileheight) + 2)
    
    offset_x = -(adjusted_camera_x % tmx_data.tilewidth) * ZOOM_FACTOR
    offset_y = -(adjusted_camera_y % tmx_data.tileheight) * ZOOM_FACTOR
    
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            gid = layer.data[y][x]
            if gid:
                # Check for animated tiles
                tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                if tile_properties and 'frames' in tile_properties:
                    frames = tile_properties['frames']
                    total_duration = sum(frame[1] for frame in frames)  # Total duration of all frames
                    
                    if frames and total_duration > 0:
                        elapsed_time = current_time % total_duration  # Time in cycle
                        current_frame = 0
                        frame_time = 0

                        # Find the correct frame
                        for frame in frames:
                            frame_time += frame[1]
                            if elapsed_time <= frame_time:
                                current_frame = frame[0]  # Use GID directly
                                break

                        # Create cache key for animated frame
                        cache_key = (current_frame, ZOOM_FACTOR)
                        
                        # Add to cache if not present
                        if cache_key not in tile_cache:
                            tile_image = tmx_data.get_tile_image_by_gid(current_frame)
                            if tile_image:
                                tile_cache[cache_key] = pygame.transform.scale(
                                    tile_image,
                                    (int(tmx_data.tilewidth * ZOOM_FACTOR), int(tmx_data.tileheight * ZOOM_FACTOR))
                                )
                        
                        # Draw to screen
                        if cache_key in tile_cache:
                            screen_x = (x - start_x) * tmx_data.tilewidth * ZOOM_FACTOR + offset_x
                            screen_y = (y - start_y) * tmx_data.tileheight * ZOOM_FACTOR + offset_y
                            surface.blit(tile_cache[cache_key], (screen_x, screen_y))
                else:
                    # Use existing system for normal tiles
                    cache_key = (gid, ZOOM_FACTOR)
                    if cache_key not in tile_cache:
                        tile_image = tmx_data.get_tile_image_by_gid(gid)
                        if tile_image:
                            # Scale the image
                            tile_cache[cache_key] = pygame.transform.scale(
                                tile_image,
                                (int(tmx_data.tilewidth * ZOOM_FACTOR), int(tmx_data.tileheight * ZOOM_FACTOR))
                            )
                    
                    if cache_key in tile_cache:
                        screen_x = (x - start_x) * tmx_data.tilewidth * ZOOM_FACTOR + offset_x
                        screen_y = (y - start_y) * tmx_data.tileheight * ZOOM_FACTOR + offset_y
                        surface.blit(tile_cache[cache_key], (screen_x, screen_y))

import pygame

class Samurai(pygame.sprite.Sprite):
    def __init__(self, walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, 
                 elixir_spritesheet, hurt_spritesheet, death_spritesheet, pullup_spritesheet, 
                 x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        # Mevcut __init__ içeriği
        self.speed = speed
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(60 / 12))
        self.update_counter = 0
        self.is_moving = False
        self.is_running = False
        self.is_jumping = False
        self.is_attacking = False
        self.is_hurt = False
        self.is_dead = False
        self.is_climbing = False
        self.climbing_finished = True
        self.climb_target_y = 0
        self.attack_finished = True
        self.hurt_finished = True
        self.death_finished = False
        self.jump_power = -12
        self.jump_cut_factor = 0.5
        self.y_velocity = 0
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.on_ground = False
        self.sound_triggered = False
        self.last_hit_sound_time = 0
        self.hit_sound_cooldown = 100
        self.max_health = 100
        self.health = self.max_health
        self.potions_collected = 0
        self.attack_damage = 20
        self.enemies_defeated = 0
        self.power_up_effect_timer = 0
        self.invincibility_frames = 30
        self.invincibility_counter = 0
        self.jump_count = 0
        self.max_jumps = 2
        self.is_charging = False
        self.charge_time = 0
        self.charged_attack_damage = 40
        self.scaled_image_cache = {}
        self.shot_spritesheet = Spritesheet("player sprite sheets/Shot.png")
        self.is_collecting_potion = False
        self.potion_frame_index = 0
        self.potion_animation_speed = max(1, round(60 / 40))
        self.potion_update_counter = 0
        self.is_shooting = False
        self.shot_finished = True
        self.shot_cooldown = 0
        self.max_arrows = 10
        self.arrow_count = self.max_arrows
        self.last_jump_time = 0
        self.jump_cooldown = 500
        # Coyote Time için yeni değişkenler
        self.coyote_time = 150  # ms cinsinden coyote time süresi
        self.last_grounded_time = 0  # Son yerde olduğu zaman
        self.is_in_dialogue = False  # Yeni bayrak: Diyalog durumunda mı?

        # Mevcut animasyon yüklemeleri
        self.walk_frames = walk_spritesheet.get_animation_frames(128, 128, scale)
        self.idle_frames = idle_spritesheet.get_animation_frames(128, 128, scale)
        self.elixir_frames = elixir_spritesheet.get_animation_frames(128, 128, scale)
        self.jump_frames = jump_spritesheet.get_animation_frames(128, 128, scale)
        self.run_frames = run_spritesheet.get_animation_frames(128, 128, scale)
        self.attack1_frames = attack1_spritesheet.get_animation_frames(128, 128, scale)[:-1]
        self.attack2_frames = attack2_spritesheet.get_animation_frames(128, 128, scale)
        self.attack3_frames = attack3_spritesheet.get_animation_frames(128, 128, scale)
        self.hurt_frames = hurt_spritesheet.get_animation_frames(128, 128, scale)
        self.death_frames = death_spritesheet.get_animation_frames(128, 128, scale)
        self.shot_frames = self.shot_spritesheet.get_animation_frames(128, 128, scale)
        self.pullup_frames = pullup_spritesheet.get_animation_frames(128, 128, scale)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        hitbox_width = self.rect.width * 0.3
        hitbox_height = self.rect.height * 0.6
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.rect.midbottom
        self.ground_check = pygame.Rect(0, 0, self.hitbox.width * 0.8, 5)
        self.update_ground_check()
        self.rect.bottom = y
        self.update_hitbox()
        self.attack_hitbox = pygame.Rect(0, 0, 60, 40)
        self.grab_area = pygame.Rect(0, 0, self.hitbox.width * 1.2, 20)
        self.update_grab_area()

    def check_on_ground(self, collision_rects):
        """Zeminde olup olmadığını kontrol eder ve coyote time'ı günceller"""
        self.update_ground_check()
        self.on_ground = False
        for rect in collision_rects:
            if self.ground_check.colliderect(rect):
                self.on_ground = True
                self.last_grounded_time = pygame.time.get_ticks()
                if self.y_velocity > 0:
                    self.y_velocity = 0
                if self.is_jumping and not self.is_attacking:
                    self.is_jumping = False
                break

    def jump(self):
        """Zıplama işlemini başlatır (Coyote time ile)"""
        if self.is_hurt or self.is_dead or self.is_in_dialogue:
            print(f"Zıplama engellendi: is_hurt={self.is_hurt}, is_dead={self.is_dead}")
            return
        current_time = pygame.time.get_ticks()
        # Coyote time kontrolü: Zeminde veya coyote time içindeyse zıplayabilir
        if not self.on_ground and (current_time - self.last_grounded_time > self.coyote_time):
            print("Zıplama engellendi: Coyote time süresi doldu")
            return
        if self.is_attacking:
            return
        self.is_jumping = True
        self.y_velocity = self.jump_power
        self.frame_index = 0
        self.update_counter = 0
        self.last_jump_time = current_time
        print("Zıplama başladı!")

    def update_grab_area(self):
        """Tutma alanını güncelle (karakterin üst kısmında bir alan)"""
        self.grab_area.midbottom = (self.hitbox.centerx, self.hitbox.top - 5)

    def check_wall_grab(self, collision_rects):
        """Duvarı tutup tırmanma kontrolü"""
        if self.is_climbing or self.is_hurt or self.is_dead or self.on_ground:
            return None

        self.update_grab_area()
        for rect in collision_rects:
            if self.grab_area.colliderect(rect):
                # Duvarın üst kenarını bul
                wall_top = rect.top
                # Duvarın hangi tarafında olduğumuzu kontrol et
                if self.flip:  # Sol tarafa bakıyor
                    if self.hitbox.left <= rect.right and self.hitbox.right > rect.right:
                        return wall_top, rect
                else:  # Sağ tarafa bakıyor
                    if self.hitbox.right >= rect.left and self.hitbox.left < rect.left:
                        return wall_top, rect
        return None

    def start_climbing(self, wall_top, wall_rect):
        """Tırmanmayı başlat"""
        self.is_climbing = True
        self.climbing_finished = False
        self.frame_index = 0
        self.update_counter = 0
        self.y_velocity = 0  # Yerçekimini geçici olarak sıfırla
        self.climb_target_y = wall_top - self.rect.height  # Hedef yükseklik
        # Karakteri duvara hizala
        if self.flip:
            self.rect.right = wall_rect.right
        else:
            self.rect.left = wall_rect.left
        self.update_hitbox()

    def update_climbing(self):
        """Tırmanma sürecini güncelle"""
        if not self.is_climbing:
            return

        # Animasyon oynarken karakteri yavaşça yukarı taşı
        climb_speed = (self.climb_target_y - self.rect.bottom) / len(self.pullup_frames)
        self.rect.y += climb_speed
        self.update_hitbox()

    def update_animation(self, arrow_group=None):
        self.update_counter += 1
        current_speed = self.animation_speed + 3 if not (self.is_moving or self.is_attacking or self.is_jumping or self.is_hurt or self.is_dead or self.is_shooting or self.is_climbing) else self.animation_speed

        # Hasar animasyonu en yüksek önceliğe sahip
        if self.is_hurt:
            frames = self.hurt_frames
            if self.update_counter >= current_speed:
                self.update_counter = 0
                if self.frame_index >= len(frames):
                    self.is_hurt = False
                    self.hurt_finished = True
                    self.frame_index = 0
                else:
                    self.image = frames[self.frame_index]
                    self.frame_index += 1
            return

        # Ölüm animasyonu ikinci öncelik
        if self.is_dead:
            frames = self.death_frames
            if self.update_counter >= current_speed:
                self.update_counter = 0
                if self.frame_index >= len(frames) - 1:
                    self.frame_index = len(frames) - 1
                    self.death_finished = True
                else:
                    self.image = frames[self.frame_index]
                    self.frame_index += 1
            return

        # Diğer animasyonlar sadece hasar alınmadığında oynar
        if self.update_counter < current_speed:
            return

        self.update_counter = 0

        
         # İksir toplama animasyonu (hareket durumlarından bağımsız, yüksek öncelik)
        if self.is_collecting_potion:
            self.potion_update_counter += 1
            if self.potion_update_counter >= self.potion_animation_speed:
                self.potion_update_counter = 0
                self.potion_frame_index += 1
                if self.potion_frame_index >= len(self.elixir_frames):
                    self.is_collecting_potion = False
                    self.potion_frame_index = 0
                    self.frame_index = 0
                else:
                    self.image = self.elixir_frames[self.potion_frame_index]
                    self.frame_index = self.potion_frame_index
            return

        # Tırmanma animasyonu
        if self.is_climbing:
            frames = self.pullup_frames
            if self.frame_index >= len(frames):
                self.is_climbing = False
                self.climbing_finished = True
                self.frame_index = 0
                self.rect.bottom = self.climb_target_y
                self.update_hitbox()
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        # Ok atma animasyonu
        elif self.is_shooting:
            frames = self.shot_frames
            if self.frame_index >= len(frames):
                self.is_shooting = False
                self.shot_finished = True
                self.frame_index = 0
                if arrow_group is not None:
                    direction = 1 if not self.flip else -1
                    arrow_x = self.rect.centerx + (40 * direction)
                    arrow_y = self.rect.centery - 10
                    new_arrow = Arrow(arrow_x, arrow_y, direction)
                    arrow_group.add(new_arrow)
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        # Saldırı animasyonu
        elif self.is_attacking:
            frames = self.current_attack_frames
            if self.frame_index >= len(frames):
                self.is_attacking = False
                self.attack_finished = True
                self.frame_index = 0
                self.sound_triggered = False
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        # Zıplama animasyonu
        elif self.is_jumping:
            frames = self.jump_frames
            if self.frame_index < len(frames) - 1:
                self.frame_index += 1
                self.image = frames[self.frame_index]
        # Koşma animasyonu
        elif self.is_running:
            frames = self.run_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        # Yürüme animasyonu
        elif self.is_moving:
            frames = self.walk_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        # Boşta animasyonu
        else:
            frames = self.idle_frames if not self.is_collecting_potion else self.elixir_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]


    def update(self, collision_rects, spike_rects, enemies, arrow_group, dt):
        if self.is_dead and self.death_finished:
            return
        if self.invincibility_counter > 0:
            self.invincibility_counter -= 1

        # Tırmanma güncellemesi
        if self.is_climbing:
            self.update_climbing()
        else:
            self.check_on_ground(collision_rects)
            for spike_rect in spike_rects:
                if self.hitbox.colliderect(spike_rect) and self.invincibility_counter <= 0:
                    self.get_hit(10)
            self.check_hit_enemies(enemies)
            self.y_velocity += self.gravity * dt * 60
            if self.y_velocity > self.max_fall_speed:
                self.y_velocity = self.max_fall_speed
            self.handle_collisions(0, self.y_velocity, collision_rects)

        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        self.update_animation(arrow_group)
        if self.is_charging:
            self.charge_time += 1

    def collect_potion(self):
        self.is_collecting_potion = True
        self.potion_frame_index = 0
        self.potion_update_counter = 0
        self.potions_collected += 1
        self.health = min(self.health + 50, self.max_health)
        print(f"İksir toplandı! +50 can, Toplam can: {self.health}/{self.max_health}")
        potion_sound = pygame.mixer.Sound("sounds/potion.wav")
        pygame.mixer.Channel(1).play(potion_sound)
        if self.potions_collected % 3 == 0:
            self.increase_max_health(20)

    def increase_max_health(self, amount=20):
        """Maksimum canı artırır ve mevcut canı günceller"""
        self.max_health += amount
        self.health = min(self.health + amount, self.max_health)
        self.power_up_effect_timer = 60  # 1 saniye parlama efekti
        print(f"Maksimum can artırıldı! Yeni maksimum can: {self.max_health}")

    def increase_attack_damage(self, amount=5):
        """Saldırı hasarını artırır"""
        self.attack_damage += amount
        self.power_up_effect_timer = 60  # 1 saniye efekt
        print(f"Saldırı hasarı artırıldı! Yeni hasar: {self.attack_damage}")

    def shoot(self, arrow_group):
        # Hasar alınıyorsa veya ölü ise ok atamaz
        if self.is_hurt or self.is_dead or self.is_in_dialogue:
            print(f"Ok atılamadı: is_hurt={self.is_hurt}, is_dead={self.is_dead}")
            return
        if self.is_shooting or self.shot_cooldown > 0 or self.arrow_count <= 0:
            print(f"Ok atılamadı: is_shooting={self.is_shooting}, shot_cooldown={self.shot_cooldown}, arrow_count={self.arrow_count}")
            return
        if self.is_running or self.is_jumping or self.is_moving or self.is_attacking:
            print("Ok atılamadı: Karakter koşuyor, zıplıyor, hareket ediyor veya saldırıyor!")
            return
        print("Ok atma animasyonu başladı!")
        self.is_shooting = True
        self.shot_finished = False
        self.frame_index = 0
        self.update_counter = 0
        self.shot_cooldown = 30
        self.arrow_count -= 1

    def attack(self, attack_type):
        # Hasar alınıyorsa veya ölü ise saldıramaz
        if self.is_hurt or self.is_dead or self.is_in_dialogue:
            print(f"Saldırı engellendi: is_hurt={self.is_hurt}, is_dead={self.is_dead}")
            return
        if self.is_attacking:
            print("Saldırı engellendi: is_attacking =", self.is_attacking)
            return
        print("Saldırı başladı, attack_type:", attack_type)
        self.is_attacking = True
        self.attack_finished = False
        self.frame_index = 0
        self.update_counter = 0
        self.sound_triggered = False
        if attack_type == 1:
            self.current_attack_frames = self.attack1_frames
    
        elif attack_type == 2:
            self.current_attack_frames = self.attack2_frames

        else:
            self.current_attack_frames = self.attack3_frames


    def release_jump(self):
        """Zıplama tuşu bırakıldığında hızı azaltır (jump cut)"""
        if self.is_jumping and self.y_velocity < 0:  # Sadece yukarı hareket ederken
            self.y_velocity *= self.jump_cut_factor  # Hızı azalt (ör. %50)
            print(f"Zıplama tuşu bırakıldı, y_velocity={self.y_velocity}")


    def check_hit_enemies(self, enemies):
        """Düşman yenildiğinde hasar artışı"""
        current_time = pygame.time.get_ticks()
        if self.is_attacking and not self.attack_finished:
            if self.frame_index == len(self.current_attack_frames) // 2:
                self.update_attack_hitbox()
                for enemy in enemies:
                    if enemy.alive and self.attack_hitbox.colliderect(enemy.hitbox):
                        enemy.get_hit(self.attack_damage)
                        if not enemy.alive:  # Düşman öldüyse
                            self.enemies_defeated += 1
                            if self.enemies_defeated % 5 == 0:  # Her 5 düşmanda hasar artar
                                self.increase_attack_damage(5)
                        if not self.sound_triggered and current_time - self.last_hit_sound_time > self.hit_sound_cooldown:
                            if not hit_channel.get_busy():
                                hit_channel.play(hit_sound)
                                self.last_hit_sound_time = current_time
                                self.sound_triggered = True
                        return True
        return False
    

    def reset(self):
        self.health = self.max_health
        self.is_dead = False
        self.death_finished = False
        self.is_hurt = False
        self.hurt_finished = True
        self.is_attacking = False
        self.attack_finished = True
        self.is_jumping = False
        self.is_moving = False
        self.is_running = False
        self.y_velocity = 0
        self.update_hitbox()
        self.invincibility_counter = 0
        self.frame_index = 0
        self.hit_sound_playing = False  # Sesin çalıp çalmadığını takip et

    # Update the get_hit method:
    def get_hit(self, damage=10):
        """Hasar alma mantığı"""
        if self.invincibility_counter <= 0 and not self.is_dead:
            self.health -= damage
            self.is_hurt = True
            self.hurt_finished = False
            self.frame_index = 0
            self.update_counter = 0
            self.invincibility_counter = self.invincibility_frames
            print(f"Oyuncu hasar aldı! Kalan can: {self.health}")
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                print("Oyuncu öldü!")
    
    def update_ground_check(self):
        self.ground_check.midbottom = (self.hitbox.midbottom[0], self.hitbox.midbottom[1] + 1)
        
    def update_hitbox(self):
        self.hitbox.midbottom = self.rect.midbottom
        self.update_ground_check()
        
                
    def handle_collisions(self, dx, dy, collision_rects):
        # Horizontal movement
        if dx != 0:
            self.hitbox.x += dx
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                    elif dx < 0:
                        self.hitbox.left = rect.right
            self.rect.midbottom = self.hitbox.midbottom
            
        # Vertical movement
        if dy != 0:
            self.hitbox.y += dy
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dy > 0:
                        self.hitbox.bottom = rect.top
                        self.on_ground = True
                        self.y_velocity = 0
                        if self.is_jumping and not self.is_attacking:
                            self.is_jumping = False
                    elif dy < 0:
                        self.hitbox.top = rect.bottom
                        self.y_velocity = 0
            self.rect.midbottom = self.hitbox.midbottom

                

    # Add a method to update the attack hitbox:
    def update_attack_hitbox(self):
        if self.flip:  # Character is facing left
            self.attack_hitbox.midright = self.hitbox.midleft
        else:  # Character is facing right
            self.attack_hitbox.midleft = self.hitbox.midright

   

    # Update the move method to prevent movement when hurt or dead:
    def move(self, moving_left, moving_right, running, collision_rects):
        if self.is_hurt or self.is_dead or self.is_collecting_potion or self.is_in_dialogue:
            return
            
        dx = 0
        self.is_moving = False
        self.is_running = False

        move_speed = self.speed * 1.5 if running else self.speed

        if moving_left:
            dx = -move_speed
            self.flip = True
            self.is_moving = True
            if running:
                self.is_running = True
        if moving_right:
            dx = move_speed
            self.flip = False
            self.is_moving = True
            if running:
                self.is_running = True

        if self.is_attacking:
            dx = 0

        self.handle_collisions(dx, 0, collision_rects)


    # Add health bar drawing:
    def draw_health_bar(self, surface, camera_x, camera_y):
        """Sağlık çubuğunu çiz"""
        if self.is_dead:
            return
        bar_width = 40
        bar_height = 5
        bar_x = (self.rect.centerx - bar_width // 2 - camera_x) * ZOOM_FACTOR
        bar_y = (self.rect.top - 10 - camera_y) * ZOOM_FACTOR
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width * ZOOM_FACTOR, bar_height * ZOOM_FACTOR))
        health_width = (self.health / self.max_health) * bar_width * ZOOM_FACTOR
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, health_width, bar_height * ZOOM_FACTOR))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width * ZOOM_FACTOR, bar_height * ZOOM_FACTOR), 1)

    # Update the draw method to include health bar and flashing when invincible:
    def draw(self, surface, camera_x, camera_y):
        if self.invincibility_counter > 0 and self.invincibility_counter % 4 < 2:
            self.draw_health_bar(surface, camera_x, camera_y)
            return

        screen_x = (self.rect.x - camera_x) * ZOOM_FACTOR
        screen_y = (self.rect.y - camera_y) * ZOOM_FACTOR
        scaled_width = int(self.rect.width * ZOOM_FACTOR)
        scaled_height = int(self.rect.height * ZOOM_FACTOR)

        cache_key = (id(self.image), ZOOM_FACTOR, self.flip)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = pygame.transform.flip(scaled_image, self.flip, False)

        # Draw the character first
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
        
        # Then add power-up effect if active
        if self.power_up_effect_timer > 0:
            effect_surface = self.scaled_image_cache[cache_key].copy()
            effect_surface.fill((255, 255, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(effect_surface, (screen_x, screen_y))
            self.power_up_effect_timer -= 1

        # Draw arrow count if available
        if hasattr(self, 'arrow_count'):
            arrow_text = font.render(f"Arrows: {self.arrow_count}", True, (255, 255, 255))
            surface.blit(arrow_text, (10, 90))

        self.draw_health_bar(surface, camera_x, camera_y)

        # Debug drawing code...


def check_potion_collisions():
    for potion in health_potions:
        if not potion.collected and player.hitbox.colliderect(potion.rect):
            if player.health == player.max_health:  # Can doluysa
                print("Canın zaten dolu, iksir alınamaz!")
                continue
            # Animasyonu başlat
            potion.collected = True
            player.collect_potion()  # Sağlık artışı ve diğer mantığı çağı
            potion_sound = pygame.mixer.Sound("sounds/potion.wav")
            pygame.mixer.Channel(1).play(potion_sound)
            print("Health potion collected!")
            break  # Birden fazla iksirin aynı anda toplanmasını önlemek için

class Arrow(pygame.sprite.Sprite):
    # Class variable for the sound - load this once
    hit_sound = None
    
    def __init__(self, x, y, direction, speed=8):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player sprite sheets/Arrow.png").convert_alpha()  # Ok görseli
        self.rect = self.image.get_rect()
        self.rect.center = (x, y+15)
        self.speed = speed
        self.direction = direction  # 1: sağ, -1: sol
        self.damage = 25  # Okun vereceği hasar
        
        # Load the sound if it hasn't been loaded yet
        if Arrow.hit_sound is None:
            Arrow.hit_sound = pygame.mixer.Sound("sounds/arrow_hit.wav")  # Ses dosyasının adını değiştirin
    
    def update(self, collision_rects, enemies):
        # Okun hareketi
        self.rect.x += self.speed * self.direction
        
        # Duvarlarla çarpışma kontrolü
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                self.kill()  # Duvara çarparsa oku kaldır
                return
        
        # Düşmanlarla çarpışma kontrolü
        for enemy in enemies:
            if enemy.alive and self.rect.colliderect(enemy.hitbox):
                enemy.get_hit(self.damage)
                # Ses çal
                pygame.mixer.Channel(2).play(Arrow.hit_sound)  # 2 numaralı kanalı kullan (değiştirilebilir)
                Arrow.hit_sound.set_volume(0.5)  # 50% volume
                self.kill()  # Düşmana çarparsa oku kaldır
                return
    
    def draw(self, surface, camera_x, camera_y):
        screen_x = (self.rect.x - camera_x) * ZOOM_FACTOR
        screen_y = (self.rect.y - camera_y) * ZOOM_FACTOR
        scaled_image = pygame.transform.scale(self.image,
                                             (int(self.rect.width * ZOOM_FACTOR),
                                              int(self.rect.height * ZOOM_FACTOR)))
        if self.direction == -1:  # Sola giderken oku çevir
            scaled_image = pygame.transform.flip(scaled_image, True, False)
        surface.blit(scaled_image, (screen_x, screen_y))


# NinjaMonk sınıfı - Devriye gezen ve saldıran düşman
class NinjaMonk(pygame.sprite.Sprite):
    def __init__(self, idle_spritesheet, walk_spritesheet, attack_spritesheet, 
                 hurt_spritesheet, death_spritesheet, x, y, scale, speed, patrol_distance):
        pygame.sprite.Sprite.__init__(self)
        # Mevcut özellikler
        self.speed = speed
        self.initial_position = (x, y)
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(60 / 12))
        self.update_counter = 0
        self.is_moving = False
        self.is_attacking = False
        self.is_hurt = False
        self.is_dead = False
        self.attack_finished = True
        self.hurt_finished = True
        self.death_finished = False
        self.remove_timer = 0
        self.should_remove = False
        self.has_fallen = False
        self.max_health = 80
        self.health = self.max_health
        self.invincibility_frames = 15
        self.invincibility_counter = 0
        self.attack_damage = 15
        self.y_velocity = 0
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.on_ground = False
        self.alive = True
        self.patrol_distance = patrol_distance
        self.start_x = x
        self.direction = 1
        self.patrol_counter = 0
        self.detection_range = 200
        self.attack_range = 50
        self.attack_cooldown = 60
        self.attack_timer = 0

        # Yeni eklenen özellikler (ikinci kodun AI'sından)
        self.devriye_noktasi_1 = (x - patrol_distance, y)  # İlk devriye noktası
        self.devriye_noktasi_2 = (x + patrol_distance, y)  # İkinci devriye noktası
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1  # Hedef başlangıç noktası
        self.jump_power = -10  # Zıplama gücü
        self.son_ziplama_zamani = 0  # Son zıplama zamanı
        self.ziplama_bekleme_suresi = 500  # Zıplama bekleme süresi (ms)

        # Animasyonlar
        self.idle_frames = idle_spritesheet.get_animation_frames(96, 96, scale)
        self.walk_frames = walk_spritesheet.get_animation_frames(96, 96, scale)
        self.attack_frames = attack_spritesheet.get_animation_frames(96, 96, scale)
        self.hurt_frames = hurt_spritesheet.get_animation_frames(96, 96, scale)
        self.death_frames = death_spritesheet.get_animation_frames(96, 96, scale)
        self.jump_frames = jump_spritesheet.get_animation_frames(96, 96, scale)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        hitbox_width = self.rect.width * 0.3
        hitbox_height = self.rect.height * 0.6
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.rect.midbottom
        self.ground_check = pygame.Rect(0, 0, self.hitbox.width * 0.8, 5)
        self.update_ground_check()
        self.rect.bottom = y
        self.update_hitbox()
        self.attack_hitbox = pygame.Rect(0, 0, 40, 60)
        self.update_attack_hitbox()

    # Mevcut metodlar korunuyor, sadece devriye ve zıplama için yenileri ekleniyor
    def platform_kontrolu(self, collision_rects):
        """Platformun kenarında zıplama kontrolü"""
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_ziplama_zamani < self.ziplama_bekleme_suresi:
            return
        
        # Düşman hangi yöne bakıyorsa o yönde kenar kontrolü yap
        yon = -1 if self.flip else 1
        
        # Önde boşluk kontrolü - ayaklarının önünde platform var mı?
        kontrol_noktasi_x = self.hitbox.midbottom[0] + yon * (self.hitbox.width // 2 + 5)
        kontrol_noktasi_y = self.hitbox.bottom + 5
        
        # Platform üzerinde mi?
        on_platform = False
        for rect in collision_rects:
            if rect.collidepoint(self.hitbox.midbottom[0], self.hitbox.bottom + 1):
                on_platform = True
                break
                
        if not on_platform:
            return  # Platform üzerinde değilse zıplama kontrolü yapma
            
        # Önümüzde platform var mı?
        platform_ahead = False
        for rect in collision_rects:
            if rect.collidepoint(kontrol_noktasi_x, kontrol_noktasi_y):
                platform_ahead = True
                break
                
        # Platformun kenarındaysa ve önde platform yoksa zıpla
        if on_platform and not platform_ahead:
            print(f"Düşman platformun kenarında, zıplıyor! Konum: ({self.rect.centerx}, {self.rect.bottom})")
            self.y_velocity = self.jump_power
            self.son_ziplama_zamani = simdiki_zaman

    def devriye_et(self, collision_rects):
        """İkinci kodun devriye mantığı"""
        if self.is_hurt or self.is_dead or self.is_attacking:
            return

        dx = self.hedef_x - self.rect.centerx   
        mesafe = abs(dx)
        
        if mesafe > self.speed:
            dx_normalized = (dx / mesafe) * self.speed * 0.5  # Daha yavaş devriye hızı
            self.handle_collisions(dx_normalized, 0, collision_rects)
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                        print(f"Engel sağda, zıplama kontrolü: {self.rect.centerx}")
                        self.platform_kontrolu(collision_rects)
                    elif dx < 0:
                        self.hitbox.left = rect.right
                        print(f"Engel solda, zıplama kontrolü: {self.rect.centerx}")
                        self.platform_kontrolu(collision_rects)
            self.flip = dx < 0
            self.is_moving = True
        else:
            # Hedef noktaya ulaşıldığında diğer noktaya geç
            if (self.hedef_x, self.hedef_y) == self.devriye_noktasi_1:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_2
            else:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_1
            self.is_moving = False

        self.rect.midbottom = self.hitbox.midbottom

    def update(self, player, collision_rects):
        if self.invincibility_counter > 0:
            self.invincibility_counter -= 1

        self.check_on_ground(collision_rects)
        self.update_hitbox()

        # Yerçekimi
        self.y_velocity += self.gravity * dt * 60
        if self.y_velocity > self.max_fall_speed:
            self.y_velocity = self.max_fall_speed
        self.handle_collisions(0, self.y_velocity, collision_rects)

        if not self.is_dead:
            player_detected = self.detect_player(player)
            if not player_detected and not self.is_attacking and not self.is_hurt:
                self.devriye_et(collision_rects)  # Yeni devriye mantığı
            if self.check_hit_player(player):
                pass

        self.update_animation()

        # Ölüm ve kaldırma mantığı
        if self.is_dead:
            if self.on_ground and not self.has_fallen:
                self.has_fallen = True
            if self.has_fallen and self.death_finished:
                self.remove_timer += 1
                if self.remove_timer >= 120:
                    self.should_remove = True

    # Mevcut `update_animation` metodunda zıplama animasyonu için kontrol ekleme
    def update_animation(self):
        self.update_counter += 1
        current_speed = self.animation_speed + 3 if not (self.is_moving or self.is_attacking or self.is_hurt or self.is_dead) else self.animation_speed
        
        if self.update_counter < current_speed:
            return
            
        self.update_counter = 0
        
        if self.is_dead:
            frames = self.death_frames
            if self.frame_index >= len(frames) - 1:
                self.frame_index = len(frames) - 1
                self.death_finished = True
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.is_hurt:
            frames = self.hurt_frames
            if self.frame_index >= len(frames):
                self.is_hurt = False
                self.hurt_finished = True
                self.frame_index = 0
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.is_attacking:
            frames = self.attack_frames
            if self.frame_index >= len(frames):
                self.is_attacking = False
                self.attack_finished = True
                self.frame_index = 0
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.y_velocity < 0:  # Zıplama animasyonu
            frames = self.jump_frames  # jump_frames kullan
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        elif self.is_moving:
            frames = self.walk_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        else:
            frames = self.idle_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
    # Diğer metodlar (get_hit, detect_player, vb.) aynı kalabilir

    def update_ground_check(self):
        self.ground_check.midbottom = (self.hitbox.midbottom[0], self.hitbox.midbottom[1] + 1)
        
    def update_hitbox(self):
        self.hitbox.midbottom = self.rect.midbottom
        self.update_ground_check()
        
    def check_on_ground(self, collision_rects):
        self.update_ground_check()
        self.on_ground = False
        for rect in collision_rects:
            if self.ground_check.colliderect(rect):
                self.on_ground = True
                if self.y_velocity > 0:
                    self.y_velocity = 0
                break
                
    def handle_collisions(self, dx, dy, collision_rects):
        # Horizontal movement
        if dx != 0:
            self.hitbox.x += dx
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                    elif dx < 0:
                        self.hitbox.left = rect.right
            self.rect.midbottom = self.hitbox.midbottom
            
        # Vertical movement
        if dy != 0:
            self.hitbox.y += dy
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dy > 0:
                        self.hitbox.bottom = rect.top
                        self.on_ground = True
                        self.y_velocity = 0
                    elif dy < 0:
                        self.hitbox.top = rect.bottom
                        self.y_velocity = 0
            self.rect.midbottom = self.hitbox.midbottom
            
    def patrol(self, collision_rects):
        # Patrol back and forth within set distance
        self.patrol_counter += 1
        
        # Change direction if reached patrol distance
        if self.patrol_counter > self.patrol_distance:
            self.direction *= -1
            self.patrol_counter = 0
            self.flip = not self.flip
        
        # Move in current direction
        dx = self.direction * self.speed * 0.5  # Slower than chase speed
        self.is_moving = True
        self.handle_collisions(dx, 0, collision_rects)
        
    def update_attack_hitbox(self):
        if self.flip:  # Character is facing left
            self.attack_hitbox.midright = self.hitbox.midleft
        else:  # Character is facing right
            self.attack_hitbox.midleft = self.hitbox.midright
            
    def attack(self):
        if self.is_attacking or self.is_hurt or self.is_dead:
            return
        
        self.is_attacking = True
        self.attack_finished = False
        self.frame_index = 0
        self.update_counter = 0

    # Update the get_hit method:
    def get_hit(self, damage):
        if self.invincibility_counter <= 0 and not self.is_dead:
            self.health -= damage
            self.is_hurt = True
            self.hurt_finished = False
            self.frame_index = 0
            self.update_counter = 0
            self.invincibility_counter = self.invincibility_frames
            
            # Check if dead
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                self.alive = False
                self.frame_index = 0
                self.update_counter = 0
                print("Enemy died!")

    # Update the detect_player method:
    def detect_player(self, player):
        if self.is_hurt or self.is_dead:
            return False
            
        # Update attack cooldown
        if self.attack_timer > 0:
            self.attack_timer -= 1
            
        # Detect player
        player_distance_x = abs(player.rect.centerx - self.rect.centerx)
        player_distance_y = abs(player.rect.centery - self.rect.centery)
        
        # If player in detection range
        if player_distance_x < self.detection_range and player_distance_y < 50 and not player.is_dead:
            # Turn toward player
            if player.rect.centerx < self.rect.centerx:
                self.flip = True
                self.direction = -1
            else:
                self.flip = False
                self.direction = 1
            
            # If player in attack range and cooldown finished, attack
            if player_distance_x < self.attack_range and self.attack_timer == 0:
                self.attack()
                self.attack_timer = self.attack_cooldown
                return True
                
            # If player detected but not in attack range, follow
            if not self.is_attacking:
                self.patrol_counter = 0  # Reset patrol
                dx = self.direction * self.speed
                self.handle_collisions(dx, 0, collision_rects)
                self.is_moving = True
                return True
        
        return False
        

    

    # Update the check_hit_player method:
    def check_hit_player(self, player):
        if self.is_attacking and not self.attack_finished and not player.is_dead:
            # Only check for hits in the middle of attack animation
            if self.frame_index == len(self.attack_frames) // 2:
                self.update_attack_hitbox()
                if self.attack_hitbox.colliderect(player.hitbox):
                    player.get_hit(self.attack_damage)
                    # Play hit sound when enemy successfully hits player
                    pygame.mixer.Channel(2).play(hit_sound)  # Use channel 2 to avoid conflicts with other sounds
                    return True
        return False

    
    # Add health bar drawing:
    def draw_health_bar(self, surface, camera_x, camera_y):
        if self.is_dead:
            return
            
        bar_width = 30
        bar_height = 4
        
        # Position above character's head
        bar_x = (self.rect.centerx - bar_width // 2 - camera_x) * ZOOM_FACTOR
        bar_y = (self.rect.top - 10 - camera_y) * ZOOM_FACTOR
        
        # Background (red)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width * ZOOM_FACTOR, bar_height * ZOOM_FACTOR))
        
        # Health (green)
        health_width = (self.health / self.max_health) * bar_width * ZOOM_FACTOR
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, health_width, bar_height * ZOOM_FACTOR))
        
        # Border
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width * ZOOM_FACTOR, bar_height * ZOOM_FACTOR), 1)


    def reset(self):
        self.health = self.max_health
        self.alive = True
        self.is_dead = False
        self.death_finished = False
        self.rect.center = self.initial_position  # You would need to store this when creating the enemy
        self.update_hitbox()
        # Reset any other enemy state variables


    # Update the draw method:
    def draw(self, surface, camera_x, camera_y):
        # Don't draw if invincible and should be flashing
        if self.invincibility_counter > 0 and self.invincibility_counter % 4 < 2:
            # Only draw health bar
            self.draw_health_bar(surface, camera_x, camera_y)
            return
            
        screen_x = (self.rect.x - camera_x) * ZOOM_FACTOR
        screen_y = (self.rect.y - camera_y) * ZOOM_FACTOR
        scaled_width = int(self.rect.width * ZOOM_FACTOR)
        scaled_height = int(self.rect.height * ZOOM_FACTOR)
        
        # Cache scaled images
        if not hasattr(self, 'scaled_image_cache'):
            self.scaled_image_cache = {}
        
        cache_key = (id(self.image), ZOOM_FACTOR, self.flip)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = pygame.transform.flip(scaled_image, self.flip, False)
        
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
        
        # Draw health bar
        self.draw_health_bar(surface, camera_x, camera_y)
        
        debug = False
        if debug:
            # Draw hitbox
            hitbox_x = (self.hitbox.x - camera_x) * ZOOM_FACTOR
            hitbox_y = (self.hitbox.y - camera_y) * ZOOM_FACTOR
            hitbox_width = self.hitbox.width * ZOOM_FACTOR
            hitbox_height = self.hitbox.height * ZOOM_FACTOR
            pygame.draw.rect(surface, (255, 0, 0), (hitbox_x, hitbox_y, hitbox_width, hitbox_height), 2)
            
            # Draw ground check box
            ground_x = (self.ground_check.x - camera_x) * ZOOM_FACTOR
            ground_y = (self.ground_check.y - camera_y) * ZOOM_FACTOR
            ground_width = self.ground_check.width * ZOOM_FACTOR
            ground_height = self.ground_check.height * ZOOM_FACTOR
            pygame.draw.rect(surface, (0, 255, 0), (ground_x, ground_y, ground_width, ground_height), 2)
            
            # Draw attack hitbox
            if self.is_attacking:
                self.update_attack_hitbox()
                attack_x = (self.attack_hitbox.x - camera_x) * ZOOM_FACTOR
                attack_y = (self.attack_hitbox.y - camera_y) * ZOOM_FACTOR
                attack_width = self.attack_hitbox.width * ZOOM_FACTOR
                attack_height = self.attack_hitbox.height * ZOOM_FACTOR
                pygame.draw.rect(surface, (255, 165, 0), (attack_x, attack_y, attack_width, attack_height), 2)
                


import pygame
from pygame import Vector2

# Mevcut Spritesheet sınıfını kullanıyoruz
class Font:
    def __init__(self, font_path=None, size=24):
        self.font = pygame.font.Font(font_path, size) if font_path else pygame.font.Font(None, size)
    
    def render(self, text, color=(255, 255, 255), background=None, shadow=False):
        if shadow:
            shadow_surface = self.font.render(text, True, (0, 0, 0))
            main_surface = self.font.render(text, True, color)
            width, height = self.font.size(text)
            final_surface = pygame.Surface((width + 2, height + 2), pygame.SRCALPHA)
            final_surface.blit(shadow_surface, (2, 2))
            final_surface.blit(main_surface, (0, 0))
            return final_surface
        elif background:
            return self.font.render(text, True, color, background)
        return self.font.render(text, True, color)
    
    def get_size(self, text):
        return self.font.size(text)

class NPC(pygame.sprite.Sprite):
    def __init__(self, idle_spritesheet, x, y, scale, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.scale = scale
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(60 / 12))
        self.update_counter = 0
        self.current_animation = "idle"
        
        # Animasyonlar
        self.animations = {
            "idle": idle_spritesheet.get_animation_frames(128, 128, scale)
        }
        
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Hitbox
        hitbox_width = self.rect.width * 0.3
        hitbox_height = self.rect.height * 0.6
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.rect.midbottom
        
        # Etkileşim ve diyalog
        self.is_interacting = False
        self.interaction_range = 100
        self.show_interact_prompt = False
        self.dialogues = []
        self.current_dialogue_index = 0
        
        # Etkileşim ipucu için animasyon değişkenleri
        self.prompt_alpha = 0
        self.prompt_scale = 1.0
        self.prompt_fade_speed = 15
        self.prompt_animation_timer = 0
        
        # Etkileşim ipucu grafiği (isteğe bağlı)
        try:
            self.prompt_image = pygame.image.load("assets/e_prompt.png").convert_alpha()
        except FileNotFoundError:
            self.prompt_image = None
        
        # Önbellek
        self.scaled_image_cache = {}
    
    def update_animation(self):
        self.update_counter += 1
        if self.update_counter < self.animation_speed:
            return
        
        self.update_counter = 0
        frames = self.animations[self.current_animation]
        self.frame_index = (self.frame_index + 1) % len(frames)
        self.image = frames[self.frame_index]
    
    def check_interaction(self, player, events):
        player_pos = Vector2(player.rect.center)
        self_pos = Vector2(self.rect.center)
        distance = player_pos.distance_to(self_pos)
        
        # Mesafe kontrolü
        self.show_interact_prompt = distance <= self.interaction_range
        
        # Etkileşim ipucu animasyonu
        target_alpha = 255 if self.show_interact_prompt else 0
        self.prompt_alpha += (target_alpha - self.prompt_alpha) * self.prompt_fade_speed * 0.1
        self.prompt_alpha = max(0, min(255, self.prompt_alpha))
        
        # Ölçek animasyonu
        self.prompt_animation_timer = pygame.time.get_ticks()
        self.prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)
        
        # Etkileşim kontrolü
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt:
                    if not self.is_interacting:
                        self.is_interacting = True
                        self.current_dialogue_index = 0
                        self.current_animation = "idle_2"
                        self.frame_index = 0
                        self.update_counter = 0
                        print(f"{self.name} ile diyalog başladı")
                        pygame.mixer.Sound("sounds/click.wav").play()
                    else:
                        self.current_dialogue_index += 1
                        if self.current_dialogue_index >= len(self.dialogues):
                            self.is_interacting = False
                            self.current_animation = "idle"
                            self.frame_index = 0
                            self.update_counter = 0
                            print(f"{self.name} ile diyalog bitti")
                        else:
                            print(f"{self.name} diyalog: {self.dialogues[self.current_dialogue_index]}")
    
    def update(self, player, events):
        self.update_animation()
        self.check_interaction(player, events)
    
    def draw(self, surface, camera_x, camera_y, font, zoom_factor):
        # Karakteri çiz
        screen_x = (self.rect.x - camera_x) * zoom_factor
        screen_y = (self.rect.y - camera_y) * zoom_factor
        scaled_width = int(self.rect.width * zoom_factor)
        scaled_height = int(self.rect.height * zoom_factor)
        
        cache_key = (id(self.image), zoom_factor, self.flip)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = pygame.transform.flip(scaled_image, self.flip, False)
        
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
        
        # Etkileşim ipucunu çiz
        if self.prompt_alpha > 0:
            if self.prompt_image:
                # Grafik tabanlı ipucu
                prompt_width = int(self.prompt_image.get_width() * self.prompt_scale * zoom_factor)
                prompt_height = int(self.prompt_image.get_height() * self.prompt_scale * zoom_factor)
                scaled_prompt = pygame.transform.scale(self.prompt_image, (prompt_width, prompt_height))
                scaled_prompt.set_alpha(int(self.prompt_alpha))
                
                # NPC'nin tam üstünde ortalanmış konum
                prompt_x = screen_x + (scaled_width - prompt_width) / 2
                prompt_y = screen_y - prompt_height - 5  # NPC'nin üstüne 5 piksel boşluk bırak
                
                # Arka plan çerçevesi (yuvarlak)
                pygame.draw.circle(surface, (50, 50, 50, 150), 
                                 (int(prompt_x + prompt_width / 2), int(prompt_y + prompt_height / 2)), 
                                 int(prompt_width / 1.5), 0)
                
                surface.blit(scaled_prompt, (prompt_x, prompt_y))
            else:
                # Metin tabanlı ipucu
                prompt_text = font.render("E", True, (255, 255, 255))
                text_width, text_height = prompt_text.get_size()
                scaled_width = int(text_width * self.prompt_scale)
                scaled_height = int(text_height * self.prompt_scale)
                scaled_prompt = pygame.transform.scale(prompt_text, (scaled_width, scaled_height))
                scaled_prompt.set_alpha(int(self.prompt_alpha))
                
                # NPC'nin tam üstünde ortalanmış konum
                prompt_x = screen_x + (self.rect.width * zoom_factor - scaled_width) / 2
                prompt_y = screen_y - scaled_height - 10  # NPC'nin üstüne 10 piksel boşluk bırak
                
                # Arka plan çerçevesi (daire)
                circle_radius = max(scaled_width, scaled_height) * 0.7
                pygame.draw.circle(surface, (50, 50, 50, 150), 
                                 (int(prompt_x + scaled_width / 2), int(prompt_y + scaled_height / 2)), 
                                 int(circle_radius), 0)
                
                surface.blit(scaled_prompt, (prompt_x, prompt_y))
        
        # Diyalog metnini çiz
        if self.is_interacting and self.current_dialogue_index < len(self.dialogues):
            dialogue_text = self.dialogues[self.current_dialogue_index]
            text_surface = font.render(dialogue_text, (255, 255, 255), background=(0, 0, 0))
            text_width, text_height = font.get_size(dialogue_text)
            dialogue_x = (SCREEN_WIDTH - text_width) / 2
            dialogue_y = SCREEN_HEIGHT - text_height - 20
            surface.blit(text_surface, (dialogue_x, dialogue_y))

class Blacksmith(NPC):
    def __init__(self, x, y, scale=1):
        idle_spritesheet = Spritesheet("npc_sprites/idle.png")
        idle_2_spritesheet = Spritesheet("npc_sprites/idle_2.png")
        
        super().__init__(idle_spritesheet, x, y, scale, "Blacksmith")
        
        self.animations["idle_2"] = idle_2_spritesheet.get_animation_frames(128, 128, scale)
        
        self.dialogues = [
            "Merhaba, ben köyün demircisi! Kılıcını keskinleştirmek ister misin?",
            "İyi bir kılıç, bir samurayın en iyi dostudur.",
            "Eğer malzemelerin varsa, sana özel bir silah yapabilirim!",
            "Yolculuğun nasıl gidiyor, gezgin?"
        ]
        
        # Demir dövme sesi
        try:
            self.hammer_sound = pygame.mixer.Sound("sounds/blacksmith_hammer.wav")
            self.hammer_sound.set_volume(0.3)
        except FileNotFoundError:
            print("Uyarı: sounds/blacksmith_hammer.wav bulunamadı!")
            self.hammer_sound = None
        
        self.sound_range = 650                 # Maksimum duyulabilir mesafe
        self.sound_step = 100                  # Her adımda ses şiddetinin değişeceği mesafe
        self.sound_increment = 0.2            # Her adımda ses şiddetinin artış/azalış miktarı
        self.base_volume = 0.2                # Temel ses seviyesi
        self.current_volume = self.base_volume  # Şu anki ses seviyesi
        self.last_sound_time = 0
        self.sound_cooldown = 2000
        self.sound_active = False
    
    def check_interaction(self, player, events):
        player_pos = Vector2(player.rect.center)
        self_pos = Vector2(self.rect.center)
        distance = player_pos.distance_to(self_pos)
        
        # Mesafe kontrolü
        self.show_interact_prompt = distance <= self.interaction_range
        
        # Etkileşim ipucu animasyonu
        target_alpha = 255 if self.show_interact_prompt else 0
        self.prompt_alpha += (target_alpha - self.prompt_alpha) * self.prompt_fade_speed * 0.1
        self.prompt_alpha = max(0, min(255, self.prompt_alpha))
        
        # Ölçek animasyonu
        self.prompt_animation_timer = pygame.time.get_ticks()
        self.prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)
        
        # Ses kontrolü
        if self.hammer_sound and not self.is_interacting:
            current_time = pygame.time.get_ticks()
            if distance <= self.sound_range:
                steps = (self.sound_range - min(distance, self.sound_range)) / self.sound_step
                new_volume = min(1.0, self.base_volume + (steps * self.sound_increment))
                if not self.sound_active:
                    if current_time - self.last_sound_time >= self.sound_cooldown:
                        pygame.mixer.Channel(3).play(self.hammer_sound, loops=-1)
                        self.last_sound_time = current_time
                        self.sound_active = True
                        print(f"Demir dövme sesi çalındı! Mesafe: {distance:.2f}, Ses: {new_volume:.2f}")
                if self.sound_active and abs(self.current_volume - new_volume) > 0.01:
                    self.current_volume = new_volume
                    pygame.mixer.Channel(3).set_volume(self.current_volume)
                    print(f"Ses seviyesi güncellendi: {self.current_volume:.2f}")
            elif distance > self.sound_range and self.sound_active:
                pygame.mixer.Channel(3).stop()
                self.sound_active = False
                print("Ses durduruldu: Mesafe sınırın dışına çıkıldı")
        
        # Diyalog sırasında sesleri durdur
        elif self.is_interacting and self.sound_active:
            pygame.mixer.Channel(3).stop()
            self.sound_active = False
            print("Ses durduruldu: NPC ile diyalog başladı")
        
        # Etkileşim kontrolü
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt:
                    if not self.is_interacting:
                        self.is_interacting = True
                        player.is_in_dialogue = True  # Oyuncuyu diyalog moduna al
                        self.current_dialogue_index = 0
                        self.current_animation = "idle_2"
                        self.frame_index = 0
                        self.update_counter = 0
                        print(f"{self.name} ile diyalog başladı")
                        pygame.mixer.Sound("sounds/click.wav").play()
                    else:
                        self.current_dialogue_index += 1
                        if self.current_dialogue_index >= len(self.dialogues):
                            self.is_interacting = False
                            player.is_in_dialogue = False  # Oyuncuyu diyalog modundan çıkar
                            self.current_animation = "idle"
                            self.frame_index = 0
                            self.update_counter = 0
                            print(f"{self.name} ile diyalog bitti")
                            pygame.mixer.Sound("sounds/click.wav").play()
                        else:
                            print(f"{self.name} diyalog: {self.dialogues[self.current_dialogue_index]}")
                            pygame.mixer.Sound("sounds/click.wav").play()
# Load initial map
load_map(current_map)

# Load spritesheets
walk_spritesheet = Spritesheet("player sprite sheets/Walk.png")
idle_spritesheet = Spritesheet("player sprite sheets/Idle.png")
jump_spritesheet = Spritesheet("player sprite sheets/Jump.png")
run_spritesheet = Spritesheet("player sprite sheets/Run.png")
attack1_spritesheet = Spritesheet("player sprite sheets/Attack_1.png")
attack2_spritesheet = Spritesheet("player sprite sheets/Attack_2.png")
attack3_spritesheet = Spritesheet("player sprite sheets/Attack_3.png")
elixir_spritesheet = Spritesheet("player sprite sheets/Elixir.png")
pullup_spritesheet = Spritesheet("player sprite sheets/Pull_up.png")

# Load additional spritesheets for hurt and death animations
hurt_spritesheet = Spritesheet("player sprite sheets/Hurt.png")
death_spritesheet = Spritesheet("player sprite sheets/Dead.png")

# Load NinjaMonk hurt and death animations
ninja_hurt_spritesheet = Spritesheet("ENEMIES/Hurt.png")
ninja_death_spritesheet = Spritesheet("ENEMIES/Death.png")

# Ninja Monk spritesheet'lerini yükle
ninja_idle_spritesheet = Spritesheet("ENEMIES/Idle.png")  # Bu dosya yolunu kendi dosya yapınıza göre ayarlayın
ninja_walk_spritesheet = Spritesheet("ENEMIES/Walk.png")
ninja_attack_spritesheet = Spritesheet("ENEMIES/Attack_1.png")
ninja_jump_spritesheet = Spritesheet("ENEMIES/Jump.png")

# Ses efektini tanımla

# Find initial spawn point
player_spawn = find_spawn_point()

# Create player and camera


# Samurai nesnesini oluştururken pullup_spritesheet'i ekle
player = Samurai(walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, 
                 elixir_spritesheet, hurt_spritesheet, death_spritesheet, pullup_spritesheet,
                 player_spawn[0], player_spawn[1], 1, 3)

player.on_ground = False
player.y_velocity = 1


def restart_game():
    global game_over, player, enemies
    game_over = False
    
    # Oyuncuyu sıfırla
    player.reset()
    
    # Düşmanları sıfırla/yeniden oluştur
    enemies.clear()  # Mevcut düşmanları temizle

# Düşman listesi oluştur
enemies = []


# Font örneği
npc_font = Font(None, 36)  # Varsayılan font, boyutu 36

# Demirci örneği
npcs = []
blacksmith = Blacksmith(1200, 1163, 1)  # Örnek konum (800, 1120)
npcs.append(blacksmith)

# Spawn noktalarını belirle (veya Tiled'dan al)v
"""enemy_spawn_points = [(600,640),(200,1024),(1592,96)]  # Örnek spawn noktaları

for spawn in enemy_spawn_points:
        ninja = NinjaMonk(ninja_idle_spritesheet, ninja_walk_spritesheet, 
                         ninja_attack_spritesheet, ninja_hurt_spritesheet, 
                         ninja_death_spritesheet,
                         spawn[0], spawn[1], 1, 2, 200)
        ninja.on_ground = False
        ninja.y_velocity = 1
        enemies.append(ninja)"""

health_potions = []
health_potions.append(HealthPotion(1000,1120))  # x: 300, y: 500 konumuna bir iksir ekle
health_potions.append(HealthPotion(1400,1120))
health_potions.append(HealthPotion(1600,1120))



camera = Camera(map_width, map_height)

arrows = pygame.sprite.Group()

# Prerender visible layers for performance
layer_surfaces = {}
front_layer_index = 17

# FPS font
font = pygame.font.Font(None, 36)

# Game loop
running = True
moving_left = False
moving_right = False
running_fast = False

import json
import pygame.time

# Fontu global olarak tanımlayın (zaten kodunuzda var, sadece emin olun)
font = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 40)

def save_game():
    global current_map, player, enemies, screen
    # "Saving..." mesajını hazırla
    saving_text = font_big.render("Saving...", True, (255, 255, 255))
    text_rect = saving_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Ekranı temizle ve mesajı göster
    screen.fill((0, 0, 0))  # Siyah arka plan
    screen.blit(saving_text, text_rect)
    pygame.display.flip()
    
    # Kısa bir bekleme (örneğin 1 saniye)
    pygame.time.wait(1000)  # 1000 ms = 1 saniye
    
    # Oyun durumunu kaydet
    game_state = {
        "player_pos": (player.rect.x, player.rect.y),
        "health": player.health,
        "max_health": player.max_health,
        "potions": player.potions_collected,
        "enemies_defeated": player.enemies_defeated,
        "attack_damage": player.attack_damage,
        "arrow_count": player.arrow_count,
        "current_map": current_map,
        "enemies": [
            {
                "pos": (enemy.rect.x, enemy.rect.y),
                "health": enemy.health,
                "alive": enemy.alive,
                "initial_position": enemy.initial_position
            } for enemy in enemies
        ],
        "health_potions": [
            {
                "pos": (potion.rect.x, potion.rect.y),
                "collected": potion.collected
            } for potion in health_potions
        ]
    }
    with open("savegame.json", "w") as f:
        json.dump(game_state, f)
    
    # Kaydetme tamamlandı mesajı
    saved_text = font_big.render("Game Saved!", True, (0, 255, 0))
    text_rect = saved_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill((0, 0, 0))
    screen.blit(saved_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(500)  # 0.5 saniye "Game Saved!" göster
    
    print("Oyun kaydedildi!")

def load_game():
    global current_map, player, enemies, camera_x, camera_y, health_potions, screen
    # "Loading..." mesajını hazırla
    loading_text = font_big.render("Loading...", True, (255, 255, 255))
    text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    # Ekranı temizle ve mesajı göster
    screen.fill((0, 0, 0))  # Siyah arka plan
    screen.blit(loading_text, text_rect)
    pygame.display.flip()
    
    # Kısa bir bekleme (örneğin 1.5 saniye)
    pygame.time.wait(1500)  # 1500 ms = 1.5 saniye
    
    try:
        with open("savegame.json", "r") as f:
            game_state = json.load(f)
            player.rect.x = game_state["player_pos"][0]
            player.rect.y = game_state["player_pos"][1]
            player.health = game_state["health"]
            player.max_health = game_state["max_health"]
            player.potions_collected = game_state["potions"]
            player.enemies_defeated = game_state["enemies_defeated"]
            player.attack_damage = game_state["attack_damage"]
            player.arrow_count = game_state["arrow_count"]
            player.update_hitbox()
            current_map = game_state["current_map"]
            load_map(current_map)
            camera_x = player.rect.centerx - SCREEN_WIDTH // (2 * ZOOM_FACTOR)
            camera_y = player.rect.centery - SCREEN_HEIGHT // (2 * ZOOM_FACTOR)
            camera = Camera(map_width, map_height)
            enemies.clear()
            for enemy_data in game_state["enemies"]:
                ninja = NinjaMonk(
                    ninja_idle_spritesheet, ninja_walk_spritesheet, 
                    ninja_attack_spritesheet, ninja_hurt_spritesheet, 
                    ninja_death_spritesheet,
                    enemy_data["pos"][0], enemy_data["pos"][1], 1, 2, 200
                )
                ninja.health = enemy_data["health"]
                ninja.alive = enemy_data["alive"]
                ninja.initial_position = enemy_data["initial_position"]
                ninja.rect.x = enemy_data["pos"][0]
                ninja.rect.y = enemy_data["pos"][1]
                ninja.update_hitbox()
                if not ninja.alive:
                    ninja.is_dead = True
                    ninja.death_finished = True
                enemies.append(ninja)
            health_potions.clear()
            for potion_data in game_state["health_potions"]:
                potion = HealthPotion(potion_data["pos"][0], potion_data["pos"][1])
                potion.collected = potion_data["collected"]
                health_potions.append(potion)
            
            # Yükleme tamamlandı mesajı
            loaded_text = font_big.render("Game Loaded!", True, (0, 255, 0))
            text_rect = loaded_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.fill((0, 0, 0))
            screen.blit(loaded_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(500)  # 0.5 saniye "Game Loaded!" göster
            
            print("Oyun yüklendi!")
    except FileNotFoundError:
        error_text = font_big.render("No Save File Found!", True, (255, 0, 0))
        text_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)  # 1 saniye hata mesajı göster
        print("Kayıt dosyası bulunamadı!")

while running:
    dt = clock.tick(FPS) / 1000.0

    # Olayları bir kez topla
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            player.hit_sound_playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                save_game()
            if event.key == pygame.K_F12:
                load_game()
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_j:
                player.attack(1)
            if current_map in ["frozen_cave", "cyberpunk", "lab"]:
                if event.key == pygame.K_k:
                    player.attack(2)
            if event.key == pygame.K_l:
                if current_map in ["cyberpunk", "lab"]:
                    player.attack(3)
            if current_map == "lab":
                if event.key == pygame.K_o:
                    player.shoot(arrows)
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running_fast = True
            if game_over and event.key == pygame.K_r:
                restart_game()
            if event.key == pygame.K_EQUALS:
                set_zoom(ZOOM_FACTOR + 0.1)
                tile_cache.clear()
                if hasattr(player, 'scaled_image_cache'):
                    player.scaled_image_cache.clear()
            if event.key == pygame.K_MINUS:
                set_zoom(ZOOM_FACTOR - 0.1)
                tile_cache.clear()
                if hasattr(player, 'scaled_image_cache'):
                    player.scaled_image_cache.clear()
            if event.key == pygame.K_g:
                if player.gravity > 0:
                    player.gravity = 0
                    player.y_velocity = 0
                else:
                    player.gravity = 0.5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running_fast = False
            if event.key == pygame.K_SPACE:
                player.release_jump()

    # Oyuncuyu güncelle
    player.move(moving_left, moving_right, running_fast, collision_rects)
    player.update(collision_rects, spike_rects, enemies, arrows, dt)

    # NPC'leri güncelle
    for npc in npcs:
        npc.update(player, events)  # Aynı olay listesini kullan

    check_potion_collisions()

    if check_map_transitions():
        continue


    # Kamera hareketi
    CAMERA_LERP = 0.05
    target_x = player.rect.centerx - SCREEN_WIDTH // (2 * ZOOM_FACTOR)
    target_y = player.rect.centery - SCREEN_HEIGHT // (2 * ZOOM_FACTOR)
    camera_x += (target_x - camera_x) * CAMERA_LERP
    camera_y += (target_y - camera_y) * CAMERA_LERP
    camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH / ZOOM_FACTOR))
    camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT / ZOOM_FACTOR))

    screen.fill((0, 0, 0))

    # Harita katmanlarını çiz
    for i, layer in enumerate(tmx_data.layers):
        if i < front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, camera_x, camera_y)

    # Oyuncuyu çiz
    player.draw(screen, camera_x, camera_y)

    # Ön plan katmanlarını çiz
    for i, layer in enumerate(tmx_data.layers):
        if i >= front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, camera_x, camera_y)

    # İksirleri çiz
    for potion in health_potions:
        potion.draw(screen, camera_x, camera_y)


    # Çizim kısmında, örneğin düşmanları çizdiğin yere ekle
    for npc in npcs:
        npc.draw(screen, camera_x, camera_y, npc_font, ZOOM_FACTOR)

    # Okları güncelle ve çiz
    arrows.update(collision_rects, enemies)
    for arrow in arrows:
        arrow.draw(screen, camera_x, camera_y)

    # Düşmanları güncelle ve çiz
    enemies_to_remove = []
    for enemy in enemies:
        enemy.update(player, collision_rects)
        if enemy.should_remove:
            enemies_to_remove.append(enemy)

    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    for enemy in enemies:
        if enemy.alive or (enemy.is_dead and not enemy.death_finished):
            enemy.draw(screen, camera_x, camera_y)


    # Game over ekranı
    if player.is_dead and player.death_finished:
        game_over = True
        game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        restart_text = font.render("Press R to restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)
        
    # FPS ve durum göstergeleri
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    player_status = f"Pos: ({int(player.rect.x)}, {int(player.rect.y)}) | Ground: {player.on_ground}"
    status_text = font.render(player_status, True, (255, 255, 255))
    screen.blit(status_text, (10, 50))
        # Mesaj zamanlayıcısını güncelle
    if show_message:
        message_timer -= 1
        if message_timer <= 0:
            show_message = False
        
        # Mesajı ekrana çiz
        msg_surface = font_big.render(message_text, True, (0, 0, 0))
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 20))
        screen.blit(msg_surface, msg_rect)
    if show2_message:
        message2_timer -= 1
        if message2_timer <= 0:
            show2_message = False
        
        # Mesajı ekrana çiz
        msg2_surface = font_big.render(message2_text, True, (255, 255, 255))
        msg2_rect = msg2_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 20))
        screen.blit(msg2_surface, msg2_rect)
    print(current_map)    
    if show3_message:
        message3_timer -= 1
        if message3_timer <= 0:
            show3_message = False
        msg3_surface = font_big.render(message3_text, True, (0, 0, 0))
        msg3_rect = msg3_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 20))
        screen.blit(msg3_surface, msg3_rect)


    pygame.display.flip()

# Quit game
pygame.quit()
sys.exit() 
