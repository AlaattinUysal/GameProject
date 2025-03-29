import pygame
import pytmx
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Village Game')
clock = pygame.time.Clock()
FPS = 60

# Load map
tmx_data = pytmx.load_pygame('levels/frozen_cave/frozen cave.tmx')
map_width = tmx_data.width * tmx_data.tilewidth
map_height = tmx_data.height * tmx_data.tileheight

# Camera settings
camera_x, camera_y = 0, 0
ZOOM_FACTOR = 1.5  # 150% zoom

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

# Collision objects
collision_rects = []
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
        for obj in layer:
            if hasattr(obj, 'x') and hasattr(obj, 'y'):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                collision_rects.append(rect)

# Starting position
player_spawn = (250, 1200)
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "spawn":
        for obj in layer:
            if obj.name.lower() == "spawn_point":
                player_spawn = (obj.x, obj.y)

# Hazard objects
spike_rects = []
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "hazards":
        for obj in layer:
            if hasattr(obj, 'x') and hasattr(obj, 'y'):
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                spike_rects.append(rect)

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
    
    # Şu anki zamanı al (animasyonlar için gerekli)
    current_time = pygame.time.get_ticks()
    
    # Calculate visible tile range
    start_x = max(0, int(camera_x / tmx_data.tilewidth))
    end_x = min(tmx_data.width, int((camera_x + SCREEN_WIDTH) / tmx_data.tilewidth) + 2)
    start_y = max(0, int(camera_y / tmx_data.tileheight))
    end_y = min(tmx_data.height, int((camera_y + SCREEN_HEIGHT) / tmx_data.tileheight) + 2)
    
    offset_x = -(camera_x % tmx_data.tilewidth) * ZOOM_FACTOR
    offset_y = -(camera_y % tmx_data.tileheight) * ZOOM_FACTOR
    
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            gid = layer.data[y][x]
            if gid:
                # Animasyonlu kareleri kontrol et
                tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                if tile_properties and 'frames' in tile_properties:
                    frames = tile_properties['frames']
                    total_duration = sum(frame[1] for frame in frames)  # Tüm karelerin toplam süresi
                    
                    if frames and total_duration > 0:
                        elapsed_time = current_time % total_duration  # Döngüde kalan zaman
                        current_frame = 0
                        frame_time = 0

                        # Doğru kareyi bul
                        for frame in frames:
                            frame_time += frame[1]
                            if elapsed_time <= frame_time:
                                current_frame = frame[0]  # GID'yi direkt kullan
                                break

                        # Animasyonlu kare için cache key oluştur
                        cache_key = (current_frame, ZOOM_FACTOR)
                        
                        # Cache'te yoksa ekle
                        if cache_key not in tile_cache:
                            tile_image = tmx_data.get_tile_image_by_gid(current_frame)
                            if tile_image:
                                tile_cache[cache_key] = pygame.transform.scale(
                                    tile_image,
                                    (int(tmx_data.tilewidth * ZOOM_FACTOR), int(tmx_data.tileheight * ZOOM_FACTOR))
                                )
                        
                        # Ekrana çiz
                        if cache_key in tile_cache:
                            screen_x = (x - start_x) * tmx_data.tilewidth * ZOOM_FACTOR + offset_x
                            screen_y = (y - start_y) * tmx_data.tileheight * ZOOM_FACTOR + offset_y
                            surface.blit(tile_cache[cache_key], (screen_x, screen_y))
                else:
                    # Normal kareler için mevcut sistemi kullan
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

# Samurai (Player) class
class Samurai(pygame.sprite.Sprite):
    def __init__(self, walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet,
                 x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(60 / 12))
        self.update_counter = 0
        self.is_moving = False
        self.is_running = False
        self.is_jumping = False
        self.is_attacking = False
        self.attack_finished = True
        self.jump_power = -10.5
        self.y_velocity = 0
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.on_ground = False

        # Animations
        self.walk_frames = walk_spritesheet.get_animation_frames(128, 128, scale)
        self.idle_frames = idle_spritesheet.get_animation_frames(128, 128, scale)
        self.jump_frames = jump_spritesheet.get_animation_frames(128, 128, scale)
        self.run_frames = run_spritesheet.get_animation_frames(128, 128, scale)
        self.attack1_frames = attack1_spritesheet.get_animation_frames(128, 128, scale)[:-1]
        self.attack2_frames = attack2_spritesheet.get_animation_frames(128, 128, scale)

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

    def update_hitbox(self):
        self.hitbox.midbottom = self.rect.midbottom
        
    def update_ground_check(self):
        self.ground_check.centerx = self.hitbox.centerx
        self.ground_check.top = self.hitbox.bottom

    def check_on_ground(self, collision_rects):
        self.on_ground = False
        self.update_ground_check()
        
        for rect in collision_rects:
            if self.ground_check.colliderect(rect):
                self.on_ground = True
                return

    def handle_collisions(self, dx, dy, collision_rects):
        if dx != 0:
            self.rect.x += dx
            self.update_hitbox()
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                        self.rect.right = self.hitbox.right + (self.rect.width - self.hitbox.width) // 2
                    elif dx < 0:
                        self.hitbox.left = rect.right
                        self.rect.left = self.hitbox.left - (self.rect.width - self.hitbox.width) // 2

        if dy != 0:
            self.rect.y += dy
            self.update_hitbox()
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dy > 0:
                        self.hitbox.bottom = rect.top
                        self.rect.bottom = self.hitbox.bottom
                        self.y_velocity = 0
                        self.on_ground = True
                        self.is_jumping = False
                    elif dy < 0:
                        self.hitbox.top = rect.bottom
                        self.rect.bottom = self.hitbox.bottom
                        self.y_velocity = 0

    def move(self, moving_left, moving_right, running, collision_rects):
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

    def jump(self):
        if self.on_ground and not self.is_attacking:
            self.is_jumping = True
            self.y_velocity = self.jump_power
            self.frame_index = 0
            self.update_counter = 0
            self.on_ground = False

    def attack(self, attack_type):
        if self.is_attacking:
            return

        self.is_attacking = True
        self.attack_finished = False
        self.frame_index = 0
        self.update_counter = 0

        if attack_type == 1:
            self.current_attack_frames = self.attack1_frames
        else:
            self.current_attack_frames = self.attack2_frames

    def update_animation(self):
        self.update_counter += 1
        current_speed = self.animation_speed + 3 if not (self.is_moving or self.is_attacking or self.is_jumping) else self.animation_speed

        if self.update_counter < current_speed:
            return

        self.update_counter = 0
        
        if self.is_attacking:
            frames = self.current_attack_frames
            if self.frame_index >= len(frames):
                self.is_attacking = False
                self.attack_finished = True
                self.frame_index = 0
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.is_jumping:
            frames = self.jump_frames
            if self.frame_index < len(frames) - 1:
                self.frame_index += 1
                self.image = frames[self.frame_index]
        elif self.is_running:
            frames = self.run_frames
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

    def get_hit(self):
        print("Character took damage!")

    def update(self, collision_rects, spike_rects):
        self.check_on_ground(collision_rects)
        
        for spike_rect in spike_rects:
            if self.hitbox.colliderect(spike_rect):
                self.get_hit()

        self.y_velocity += self.gravity
        if self.y_velocity > self.max_fall_speed:
            self.y_velocity = self.max_fall_speed

        self.handle_collisions(0, self.y_velocity, collision_rects)
        self.update_animation()

    def draw(self, surface, camera_x, camera_y):
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
        
        debug = False
        if debug:
            hitbox_x = (self.hitbox.x - camera_x) * ZOOM_FACTOR
            hitbox_y = (self.hitbox.y - camera_y) * ZOOM_FACTOR
            hitbox_width = self.hitbox.width * ZOOM_FACTOR
            hitbox_height = self.hitbox.height * ZOOM_FACTOR
            pygame.draw.rect(surface, (255, 0, 0), (hitbox_x, hitbox_y, hitbox_width, hitbox_height), 2)
            
            ground_x = (self.ground_check.x - camera_x) * ZOOM_FACTOR
            ground_y = (self.ground_check.y - camera_y) * ZOOM_FACTOR
            ground_width = self.ground_check.width * ZOOM_FACTOR
            ground_height = self.ground_check.height * ZOOM_FACTOR
            pygame.draw.rect(surface, (0, 255, 0), (ground_x, ground_y, ground_width, ground_height), 2)

# Load spritesheets
walk_spritesheet = Spritesheet("player sprite sheets/Walk.png")
idle_spritesheet = Spritesheet("player sprite sheets/Idle.png")
jump_spritesheet = Spritesheet("player sprite sheets/Jump.png")
run_spritesheet = Spritesheet("player sprite sheets/Run.png")
attack1_spritesheet = Spritesheet("player sprite sheets/Attack_1.png")
attack2_spritesheet = Spritesheet("player sprite sheets/Attack_2.png")

# Create player and camera
player = Samurai(walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, 
                 player_spawn[0], player_spawn[1], 1, 3)

player.on_ground = False
player.y_velocity = 1

camera = Camera(map_width, map_height)

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

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump()
            if event.key == pygame.K_j:
                player.attack(1)
            if event.key == pygame.K_k:
                player.attack(2)
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running_fast = True
            if event.key == pygame.K_EQUALS:
                set_zoom(ZOOM_FACTOR + 0.1)
                # Clear cache when zoom changes
                tile_cache.clear()
                if hasattr(player, 'scaled_image_cache'):
                    player.scaled_image_cache.clear()
            if event.key == pygame.K_MINUS:
                set_zoom(ZOOM_FACTOR - 0.1)
                # Clear cache when zoom changes
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

    player.move(moving_left, moving_right, running_fast, collision_rects)
    player.update(collision_rects, spike_rects)

    # Update camera with smoothing
    CAMERA_LERP = 0.05
    target_x = player.rect.centerx - SCREEN_WIDTH // (2 * ZOOM_FACTOR)
    target_y = player.rect.centery - SCREEN_HEIGHT // (2 * ZOOM_FACTOR)
    camera_x += (target_x - camera_x) * CAMERA_LERP
    camera_y += (target_y - camera_y) * CAMERA_LERP

    camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH / ZOOM_FACTOR))
    camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT / ZOOM_FACTOR))

    screen.fill((0, 0, 0))
    
    # Draw background layers
    for i, layer in enumerate(tmx_data.layers):
        if i < front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, camera_x, camera_y)
    
    # Draw player
    player.draw(screen, camera_x, camera_y)
    
    # Draw foreground layers
    for i, layer in enumerate(tmx_data.layers):
        if i >= front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, camera_x, camera_y)

    # Show FPS
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    
    # Show player status
    player_status = f"Pos: ({int(player.rect.x)}, {int(player.rect.y)}) | Ground: {player.on_ground}"
    status_text = font.render(player_status, True, (255, 255, 255))
    screen.blit(status_text, (10, 50))
    
    pygame.display.flip()

# Quit game
pygame.quit()
sys.exit()