import pygame
import pytmx
from game_state import game_state
from items import HealthPotion, PotionSpritesheet
from soundmanager import sound_manager

def load_map(map_name):
    try:
        if not hasattr(load_map, 'potion_spritesheet'):
            sprite_path = "health potion/health 48x48.png"
            load_map.potion_spritesheet = PotionSpritesheet(sprite_path)

        if map_name in game_state.maps_data:
            game_state.tmx_data = game_state.maps_data[map_name]["tmx_data"]
            game_state.map_width = game_state.maps_data[map_name]["map_width"]
            game_state.map_height = game_state.maps_data[map_name]["map_height"]
            game_state.collision_rects = game_state.maps_data[map_name]["collision_rects"]
            game_state.spike_rects = game_state.maps_data[map_name]["spike_rects"]
            game_state.transition_rects = game_state.maps_data[map_name]["transition_rects"]
            game_state.parallax_factors_x = game_state.maps_data[map_name]["parallax_factors_x"]
            game_state.parallax_factors_y = game_state.maps_data[map_name]["parallax_factors_y"]
            game_state.health_potions = game_state.maps_data[map_name].get("health_potions", pygame.sprite.Group())
            return

        game_state.tile_cache.clear()
        if hasattr(game_state, 'player') and hasattr(game_state.player, 'scaled_image_cache'):
            game_state.player.scaled_image_cache.clear()

        map_file = f'levels/{map_name}/{map_name}.tmx'
        game_state.tmx_data = pytmx.load_pygame(map_file)
        game_state.map_width = game_state.tmx_data.width * game_state.tmx_data.tilewidth
        game_state.map_height = game_state.tmx_data.height * game_state.tmx_data.tileheight

        game_state.collision_rects = []
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
                for obj in layer:
                    if hasattr(obj, 'x') and hasattr(obj, 'y'):
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        game_state.collision_rects.append(rect)

        game_state.spike_rects = []
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "hazards":
                for obj in layer:
                    if hasattr(obj, 'x') and hasattr(obj, 'y'):
                        props = getattr(obj, 'properties', {})
                        damage_amount = props.get('damage_amount', 10)
                        game_state.spike_rects.append({
                            'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                            'damage_amount': damage_amount
                        })

        game_state.transition_rects = {}
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "transitions":
                for obj in layer:
                    if hasattr(obj, 'x') and hasattr(obj, 'y'):
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        if hasattr(obj, 'properties') and 'target_map' in obj.properties:
                            transition_info = {
                                'target_map': obj.properties['target_map'],
                                'target_spawn': obj.properties.get('target_spawn', 'spawn_point')
                            }
                            game_state.transition_rects[obj.name] = {
                                'rect': rect,
                                'info': transition_info
                            }

        game_state.health_potions = pygame.sprite.Group()
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Potions":
                for obj in layer:
                    props = getattr(obj, 'properties', {})
                    healing_amount = props.get('healing_amount', 20)
                    potion = HealthPotion(obj.x, obj.y, healing_amount, load_map.potion_spritesheet)
                    game_state.health_potions.add(potion)
                    print(f"İksir yüklendi: ({obj.x}, {obj.y}), iyileştirme: {healing_amount}")

        update_parallax_factors()

        game_state.maps_data[map_name] = {
            "tmx_data": game_state.tmx_data,
            "map_width": game_state.map_width,
            "map_height": game_state.map_height,
            "collision_rects": game_state.collision_rects,
            "spike_rects": game_state.spike_rects,
            "transition_rects": game_state.transition_rects,
            "parallax_factors_x": game_state.parallax_factors_x,
            "parallax_factors_y": game_state.parallax_factors_y,
            "health_potions": game_state.health_potions
        }
    except Exception as e:
        print(f"Harita yüklenirken hata: {e}")
        raise

def update_parallax_factors():
    game_state.parallax_factors_x = {}
    game_state.parallax_factors_y = {}
    for layer in game_state.tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            layer_properties = getattr(layer, 'properties', {})
            if 'parallax_factor_x' in layer_properties:
                game_state.parallax_factors_x[layer.name] = float(layer_properties['parallax_factor_x'])
            elif 'parallax_factor' in layer_properties:
                game_state.parallax_factors_x[layer.name] = float(layer_properties['parallax_factor'])
            elif layer.name.startswith('parallax_'):
                try:
                    index = int(layer.name.split('_')[1])
                    game_state.parallax_factors_x[layer.name] = max(0.1, 1.0 - (index * 0.1))
                except (IndexError, ValueError):
                    game_state.parallax_factors_x[layer.name] = 0.5
            if 'parallax_factor_y' in layer_properties:
                game_state.parallax_factors_y[layer.name] = float(layer_properties['parallax_factor_y'])
            elif 'parallax_factor' in layer_properties:
                game_state.parallax_factors_y[layer.name] = float(layer_properties['parallax_factor'])
            elif layer.name.startswith('parallax_'):
                try:
                    index = int(layer.name.split('_')[1])
                    game_state.parallax_factors_y[layer.name] = max(0.1, 1.0 - (index * 0.1))
                except (IndexError, ValueError):
                    game_state.parallax_factors_y[layer.name] = 0.5

def find_spawn_point(spawn_name="spawn_point"):
    default_spawn = (250, 1200)
    for layer in game_state.tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "spawn":
            for obj in layer:
                if obj.name.lower() == spawn_name.lower():
                    return (obj.x, obj.y)
    return default_spawn

def adjust_spawn_to_ground(player, spawn_x, spawn_y):
    """Spawn noktasını zemine hizalar."""
    player.rect.centerx = spawn_x
    player.rect.bottom = spawn_y
    player.update_hitbox()
    
    # Zemine kadar düşme simülasyonu
    max_attempts = 100  # Sonsuz döngüyü önlemek için
    for _ in range(max_attempts):
        prev_y = player.rect.y
        player.y_velocity += player.gravity * 0.016  # 60 FPS için dt simülasyonu
        player.rect.y += player.y_velocity
        player.update_hitbox()
        
        for rect in game_state.collision_rects:
            if player.hitbox.colliderect(rect):
                player.rect.bottom = rect.top
                player.update_hitbox()
                player.y_velocity = 0
                player.on_ground = True
                return player.rect.centerx, player.rect.bottom
        
        if player.rect.y == prev_y:  # Hareket yoksa çık
            break
    
    # Eğer zemin bulunamazsa orijinal spawn noktasına dön
    player.rect.centerx = spawn_x
    player.rect.bottom = spawn_y
    player.update_hitbox()
    player.y_velocity = 0
    player.on_ground = True
    return spawn_x, spawn_y

def check_map_transitions(player, events):
    game_state.show_transition_prompt = False
    game_state.active_transition = None

    for transition_name, transition_data in game_state.transition_rects.items():
        if player.hitbox.colliderect(transition_data['rect']):
            game_state.show_transition_prompt = True
            game_state.active_transition = transition_data
            break

    target_alpha = 255 if game_state.show_transition_prompt else 0
    game_state.transition_prompt_alpha += (target_alpha - game_state.transition_prompt_alpha) * game_state.transition_prompt_fade_speed * 0.016
    game_state.transition_prompt_alpha = max(0, min(255, game_state.transition_prompt_alpha))
    game_state.transition_prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)

    if game_state.show_transition_prompt and not game_state.is_fading:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if game_state.active_transition:
                    target_map = game_state.active_transition['info']['target_map']
                    target_spawn = game_state.active_transition['info']['target_spawn']
                    if target_map != game_state.current_map:
                        game_state.is_fading = True
                        game_state.fade_state = "out"
                        game_state.target_map = target_map
                        game_state.target_spawn = target_spawn
                        sound_manager.play_sound("click")
                        print(f"Geçiş başlatıldı: {target_map}")
                        return True
    return False

def draw_transition_prompt(surface, camera_x, camera_y):
    if not game_state.show_transition_prompt or game_state.transition_prompt_alpha <= 0:
        return

    prompt_text = game_state.font.render("E", color=(255, 255, 255), background=(0, 0, 0), shadow=True)
    prompt_text.set_alpha(int(game_state.transition_prompt_alpha))
    text_width, text_height = game_state.font.get_size("E")
    
    if game_state.active_transition:
        rect = game_state.active_transition['rect']
        screen_x = ((rect.centerx - camera_x) * game_state.zoom_factor) - text_width // 2
        screen_y = ((rect.top - camera_y - 20) * game_state.zoom_factor) - text_height // 2
        scaled_width = text_width * game_state.transition_prompt_scale
        scaled_height = text_height * game_state.transition_prompt_scale
        scaled_prompt = pygame.transform.scale(prompt_text, (int(scaled_width), int(scaled_height)))
        surface.blit(scaled_prompt, (screen_x, screen_y - scaled_height // 2))

def draw_layer(layer, surface, camera_x, camera_y):
    if not isinstance(layer, pytmx.TiledTileLayer):
        return
    adjusted_camera_x = camera_x
    adjusted_camera_y = camera_y
    if layer.name in game_state.parallax_factors_x:
        factor_x = game_state.parallax_factors_x[layer.name]
        adjusted_camera_x *= factor_x
    if layer.name in game_state.parallax_factors_y:
        factor_y = game_state.parallax_factors_y[layer.name]
        adjusted_camera_y *= factor_y
    current_time = pygame.time.get_ticks()
    start_x = max(0, int(adjusted_camera_x / game_state.tmx_data.tilewidth))
    end_x = min(game_state.tmx_data.width, int((adjusted_camera_x + game_state.screen_width) / game_state.tmx_data.tilewidth) + 2)
    start_y = max(0, int(adjusted_camera_y / game_state.tmx_data.tileheight))
    end_y = min(game_state.tmx_data.height, int((adjusted_camera_y + game_state.screen_height) / game_state.tmx_data.tileheight) + 2)
    offset_x = -(adjusted_camera_x % game_state.tmx_data.tilewidth) * game_state.zoom_factor
    offset_y = -(adjusted_camera_y % game_state.tmx_data.tileheight) * game_state.zoom_factor
    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            gid = layer.data[y][x]
            if gid:
                tile_properties = game_state.tmx_data.get_tile_properties_by_gid(gid)
                if tile_properties and 'frames' in tile_properties:
                    frames = tile_properties['frames']
                    total_duration = sum(frame[1] for frame in frames)
                    if frames and total_duration > 0:
                        elapsed_time = current_time % total_duration
                        current_frame = 0
                        frame_time = 0
                        for frame in frames:
                            frame_time += frame[1]
                            if elapsed_time <= frame_time:
                                current_frame = frame[0]
                                break
                        cache_key = (current_frame, game_state.zoom_factor)
                        if cache_key not in game_state.tile_cache:
                            tile_image = game_state.tmx_data.get_tile_image_by_gid(current_frame)
                            if tile_image:
                                game_state.tile_cache[cache_key] = pygame.transform.scale(
                                    tile_image,
                                    (int(game_state.tmx_data.tilewidth * game_state.zoom_factor), int(game_state.tmx_data.tileheight * game_state.zoom_factor))
                                )
                        if cache_key in game_state.tile_cache:
                            screen_x = (x - start_x) * game_state.tmx_data.tilewidth * game_state.zoom_factor + offset_x
                            screen_y = (y - start_y) * game_state.tmx_data.tileheight * game_state.zoom_factor + offset_y
                            surface.blit(game_state.tile_cache[cache_key], (screen_x, screen_y))
                else:
                    cache_key = (gid, game_state.zoom_factor)
                    if cache_key not in game_state.tile_cache:
                        tile_image = game_state.tmx_data.get_tile_image_by_gid(gid)
                        if tile_image:
                            game_state.tile_cache[cache_key] = pygame.transform.scale(
                                tile_image,
                                (int(game_state.tmx_data.tilewidth * game_state.zoom_factor), int(game_state.tmx_data.tileheight * game_state.zoom_factor))
                            )
                    if cache_key in game_state.tile_cache:
                        screen_x = (x - start_x) * game_state.tmx_data.tilewidth * game_state.zoom_factor + offset_x
                        screen_y = (y - start_y) * game_state.tmx_data.tileheight * game_state.zoom_factor + offset_y
                        surface.blit(game_state.tile_cache[cache_key], (screen_x, screen_y))
