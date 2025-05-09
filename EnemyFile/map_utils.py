import pygame
import pytmx

def load_map(map_path):
    tmx_data = pytmx.load_pygame(map_path)
    map_genislik = tmx_data.width * tmx_data.tilewidth
    map_yukseklik = tmx_data.height * tmx_data.tileheight
    return tmx_data, map_genislik, map_yukseklik

def get_collision_rects(tmx_data):
    collision_rects = []
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
            for nesne in layer:
                if hasattr(nesne, 'x') and hasattr(nesne, 'y'):
                    rect = pygame.Rect(nesne.x, nesne.y, nesne.width, nesne.height)
                    collision_rects.append(rect)
    return collision_rects

def get_player_spawn(tmx_data):
    player_spawn = (200, 100)
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "spawn":
            for nesne in layer:
                if nesne.name.lower() == "spawn_point":
                    player_spawn = (nesne.x, nesne.y)
    return player_spawn

def draw_map(tmx_data, surface, camera_x, camera_y, genislik, yukseklik):
    surface.fill((0, 0, 0))
    start_x = max(0, int(camera_x / tmx_data.tilewidth))
    end_x = min(tmx_data.width, int((camera_x + genislik) / tmx_data.tilewidth) + 2)
    start_y = max(0, int(camera_y / tmx_data.tileheight))
    end_y = min(tmx_data.height, int((camera_y + yukseklik) / tmx_data.tileheight) + 2)
    offset_x = -(camera_x % tmx_data.tilewidth)
    offset_y = -(camera_y % tmx_data.tileheight)

    current_time = pygame.time.get_ticks()
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    gid = layer.data[y][x]
                    if gid:
                        tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                        if tile_properties and 'frames' in tile_properties:
                            frames = tile_properties['frames']
                            total_duration = sum(frame[1] for frame in frames)
                            if not frames or total_duration <= 0:
                                tile_image = tmx_data.get_tile_image_by_gid(gid)
                            else:
                                elapsed_time = current_time % total_duration
                                frame_time = 0
                                for frame in frames:
                                    frame_time += frame[1]
                                    if elapsed_time <= frame_time:
                                        tile_image = tmx_data.get_tile_image_by_gid(frame[0])
                                        break
                        else:
                            tile_image = tmx_data.get_tile_image_by_gid(gid)
                        if tile_image:
                            screen_x = (x - start_x) * tmx_data.tilewidth + offset_x
                            screen_y = (y - start_y) * tmx_data.tileheight + offset_y
                            surface.blit(tile_image, (screen_x, screen_y))
