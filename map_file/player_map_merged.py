import pygame
import pytmx
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
clock = pygame.time.Clock()
FPS = 60

# Game state and map management
current_map = "village"  # Starting map
maps_data = {}  # Cache for loaded maps
transition_rects = {}  # Transition zones for each map

# Global variables
ZOOM_FACTOR = 1.5  # 150% zoom
camera_x, camera_y = 0, 0
front_layer_index = 17
tile_cache = {}
parallax_factors_x = {}
parallax_factors_y = {}

def load_map(map_name):
    """Load a map and extract its data"""
    global tmx_data, map_width, map_height, collision_rects, spike_rects
    global transition_rects, parallax_factors_x, parallax_factors_y
    
    # If map is already cached, use cached data
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
        return
    
    # Clear caches when loading a new map
    tile_cache.clear()
    
    # Only clear player image cache if player exists
    if 'player' in globals() and hasattr(player, 'scaled_image_cache'):
        player.scaled_image_cache.clear()
    
    # Load the map file
    map_file = f'levels/{map_name}/{map_name}.tmx'
    tmx_data = pytmx.load_pygame(map_file)
    map_width = tmx_data.width * tmx_data.tilewidth
    map_height = tmx_data.height * tmx_data.tileheight
    
    # Extract collision objects
    collision_rects = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y'):
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    collision_rects.append(rect)
    
    # Extract hazard objects
    spike_rects = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "hazards":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y'):
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    spike_rects.append(rect)
    
    # Extract transition zones
    transition_rects = {}
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "transitions":
            for obj in layer:
                if hasattr(obj, 'x') and hasattr(obj, 'y'):
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    # Store transition info
                    if hasattr(obj, 'properties') and 'target_map' in obj.properties:
                        transition_info = {
                            'target_map': obj.properties['target_map'],
                            'target_spawn': obj.properties.get('target_spawn', 'spawn_point')
                        }
                        transition_rects[obj.name] = {
                            'rect': rect,
                            'info': transition_info
                        }
    
    # Extract parallax factors
    update_parallax_factors()
    
    # Cache the map data
    maps_data[map_name] = {
        "tmx_data": tmx_data,
        "map_width": map_width,
        "map_height": map_height,
        "collision_rects": collision_rects,
        "spike_rects": spike_rects,
        "transition_rects": transition_rects,
        "parallax_factors_x": parallax_factors_x,
        "parallax_factors_y": parallax_factors_y
    }

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
    """Check if player is in a transition zone, change map if needed"""
    global current_map, camera_x, camera_y, camera
    
    for transition_name, transition_data in transition_rects.items():
        if player.hitbox.colliderect(transition_data['rect']):
            target_map = transition_data['info']['target_map']
            target_spawn = transition_data['info']['target_spawn']
            
            if target_map != current_map:
                # Change map
                current_map = target_map
                load_map(current_map)
                
                # Move player to target spawn point
                spawn_pos = find_spawn_point(target_spawn)
                player.rect.centerx = spawn_pos[0]
                player.rect.bottom = spawn_pos[1]
                player.update_hitbox()
                
                # Reset player velocity on map change
                player.y_velocity = 0
                
                # Reset camera
                camera_x = max(0, min(player.rect.centerx - SCREEN_WIDTH//(2*ZOOM_FACTOR), 
                               map_width - SCREEN_WIDTH//ZOOM_FACTOR))
                camera_y = max(0, min(player.rect.centery - SCREEN_HEIGHT//(2*ZOOM_FACTOR), 
                               map_height - SCREEN_HEIGHT//ZOOM_FACTOR))
                
                # Create new camera object with new map dimensions
                camera = Camera(map_width, map_height)
                return True
    
    return False

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

# Load initial map
load_map(current_map)

# Load spritesheets
walk_spritesheet = Spritesheet("player sprite sheets/Walk.png")
idle_spritesheet = Spritesheet("player sprite sheets/Idle.png")
jump_spritesheet = Spritesheet("player sprite sheets/Jump.png")
run_spritesheet = Spritesheet("player sprite sheets/Run.png")
attack1_spritesheet = Spritesheet("player sprite sheets/Attack_1.png")
attack2_spritesheet = Spritesheet("player sprite sheets/Attack_2.png")

# Find initial spawn point
player_spawn = find_spawn_point()

# Create player and camera
player = Samurai(walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, 
                 player_spawn[0], player_spawn[1], 1, 3)

player.on_ground = False
player.y_velocity = 1

camera = Camera(map_width, map_height)

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
    
    # Check for map transitions
    if check_map_transitions():
        # Skip the rest of this frame if map changed
        continue

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
    
    # Show player status and current map
    player_status = f"Map: {current_map} | Pos: ({int(player.rect.x)}, {int(player.rect.y)}) | Ground: {player.on_ground}"
    status_text = font.render(player_status, True, (255, 255, 255))
    screen.blit(status_text, (10, 50))
    
    pygame.display.flip()

# Quit game
pygame.quit()
sys.exit()
