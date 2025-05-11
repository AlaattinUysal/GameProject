# map.py
import pygame
import pytmx
from game_state import game_state
from items import HealthPotion

def load_map(map_name):
    try:
        # Harita önbellekte varsa yükle
        if map_name in game_state.maps_data:
            game_state.tmx_data = game_state.maps_data[map_name]["tmx_data"]
            game_state.map_width = game_state.maps_data[map_name]["map_width"]
            game_state.map_height = game_state.maps_data[map_name]["map_height"]
            game_state.collision_rects = game_state.maps_data[map_name]["collision_rects"]
            game_state.spike_rects = game_state.maps_data[map_name]["spike_rects"]
            game_state.transition_rects = game_state.maps_data[map_name]["transition_rects"]
            game_state.parallax_factors_x = game_state.maps_data[map_name]["parallax_factors_x"]
            game_state.parallax_factors_y = game_state.maps_data[map_name]["parallax_factors_y"]
            game_state.health_potions = game_state.maps_data[map_name]["health_potions"]
            return

        # Önbellekleri temizle
        game_state.tile_cache.clear()

        # Harita dosyasını yükle
        map_file = f'levels/{map_name}/{map_name}.tmx'
        game_state.tmx_data = pytmx.load_pygame(map_file)
        game_state.map_width = game_state.tmx_data.width * game_state.tmx_data.tilewidth
        game_state.map_height = game_state.tmx_data.height * game_state.tmx_data.tileheight

        # Sağlık iksirlerini yükle
        game_state.health_potions = []
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "items":
                for obj in layer:
                    if hasattr(obj, 'x') and hasattr(obj, 'y') and obj.name.lower() == "health_potion":
                        potion = HealthPotion(obj.x, obj.y)
                        game_state.health_potions.append(potion)

        # Çarpışma nesnelerini yükle
        game_state.collision_rects = []
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
                for obj in layer:
                    if hasattr(obj, 'x') and hasattr(obj, 'y'):
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        game_state.collision_rects.append(rect)

        # Tehlike nesnelerini yükle
        game_state.spike_rects = []
        for layer in game_state.tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "hazards":
                for obj in layer:
                    if hasattr(obj, 'x') and hasattr(obj, 'y'):
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        game_state.spike_rects.append(rect)

        # Geçiş bölgelerini yükle
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

        # Paralaks faktörlerini güncelle
        update_parallax_factors()

        # Harita verilerini önbelleğe al
        game_state.maps_data[map_name] = {
            "tmx_data": game_state.tmx_data,
            "map_width": game_state.map_width,
            "map_height": game_state.map_height,
            "collision_rects": game_state.collision_rects,
            "spike_rects": game_state.spike_rects,
            "transition_rects": game_state.transition_rects,
            "parallax_factors_x": game_state.parallax_factors_x,
            "parallax_factors_y": game_state.parallax_factors_y,
            "health_potions": game_state.health_potions,
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

def check_map_transitions(player):
    for transition_name, transition_data in game_state.transition_rects.items():
        if player.hitbox.colliderect(transition_data['rect']):
            target_map = transition_data['info']['target_map']
            target_spawn = transition_data['info']['target_spawn']
            if target_map != game_state.current_map:
                game_state.current_map = target_map
                load_map(game_state.current_map)
                spawn_pos = find_spawn_point(target_spawn)
                player.rect.centerx = spawn_pos[0]
                player.rect.bottom = spawn_pos[1]
                player.update_hitbox()
                player.y_velocity = 0
                game_state.camera_x = max(0, min(player.rect.centerx - game_state.screen_width // (2 * game_state.zoom_factor), 
                                          game_state.map_width - game_state.screen_width // game_state.zoom_factor))
                game_state.camera_y = max(0, min(player.rect.centery - game_state.screen_height // (2 * game_state.zoom_factor), 
                                          game_state.map_height - game_state.screen_height // game_state.zoom_factor))
                if game_state.current_map == "frozen_cave":
                    game_state.show_message = True
                    game_state.message_timer = game_state.message_duration
                if game_state.current_map == "cyberpunk":
                    game_state.show2_message = True 
                    game_state.message2_timer = game_state.message_duration
                if game_state.current_map == "lab":
                    game_state.show3_message = True 
                    game_state.message3_timer = game_state.message_duration
                return True
    return False

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