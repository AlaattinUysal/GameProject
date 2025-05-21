import pygame
import pytmx
import sys
import json
import pygame.time
from npc import Blacksmith, Trader
from game_state import game_state
from camera import Camera
from map import load_map, check_map_transitions, draw_layer, find_spawn_point
from player import Samurai
from utils import Spritesheet
from soundmanager import sound_manager
from items import HealthPotion
#from enemy_types import NinjaMonk, NinjaPeasant

pygame.init()
screen = pygame.display.set_mode((game_state.screen_width, game_state.screen_height))
pygame.display.set_caption("Samurai's Path")
clock = pygame.time.Clock()

def set_zoom(factor):
    game_state.zoom_factor = max(0.5, min(factor, 3))
    game_state.tile_cache.clear()
    if hasattr(player, 'scaled_image_cache'):
        player.scaled_image_cache.clear()

ninja_idle_spritesheet = Spritesheet("ENEMIES/Idle.png")
ninja_walk_spritesheet = Spritesheet("ENEMIES/Walk.png")
ninja_attack_spritesheet = Spritesheet("ENEMIES/Attack_1.png")
ninja_hurt_spritesheet = Spritesheet("ENEMIES/Hurt.png")
ninja_death_spritesheet = Spritesheet("ENEMIES/Death.png")
ninja_jump_spritesheet = Spritesheet("ENEMIES/Jump.png")

walk_spritesheet = Spritesheet("player sprite sheets/Walk.png")
idle_spritesheet = Spritesheet("player sprite sheets/Idle.png")
jump_spritesheet = Spritesheet("player sprite sheets/Jump.png")
run_spritesheet = Spritesheet("player sprite sheets/Run.png")
attack1_spritesheet = Spritesheet("player sprite sheets/Attack_1.png")
attack2_spritesheet = Spritesheet("player sprite sheets/Attack_2.png")
attack3_spritesheet = Spritesheet("player sprite sheets/Attack_3.png")
elixir_spritesheet = Spritesheet("player sprite sheets/Elixir.png")
shot_spritesheet = Spritesheet("player sprite sheets/Shot.png")
hurt_spritesheet = Spritesheet("player sprite sheets/Hurt.png")
death_spritesheet = Spritesheet("player sprite sheets/Dead.png")

def load_map_characters():
    global npcs, enemies
    npcs.clear()
    enemies.clear()
    
    current_map = game_state.current_map
    if current_map not in game_state.map_characters:
        print(f"Uyarı: {current_map} için karakter tanımları bulunamadı!")
        return
    
    for npc_data in game_state.map_characters[current_map]["npcs"]:
        npc_type = npc_data["type"]
        x, y = npc_data["x"], npc_data["y"]
        scale = npc_data.get("scale", 1)
        if npc_type == "Blacksmith":
            npc = Blacksmith(x, y, scale)
            npcs.append(npc)
            print(f"{npc_type} yüklendi: ({x}, {y})")
        elif npc_type == "Trader":
            npc = Trader(x, y, scale)
            npcs.append(npc)
            print(f"{npc_type} yüklendi: ({x}, {y})")
        else:
            print(f"Uyarı: Bilinmeyen NPC türü: {npc_type}")

try:
    load_map(game_state.current_map)
    print(f"Harita yüklendi: {game_state.current_map}, tmx_data: {game_state.tmx_data}")
except Exception as e:
    print(f"Başlangıç haritası yüklenirken hata: {e}")
    pygame.quit()
    sys.exit(1)

player_spawn = find_spawn_point()
print(f"Spawn noktası: {player_spawn}")
player = Samurai(walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, 
                 elixir_spritesheet, hurt_spritesheet, death_spritesheet, shot_spritesheet,
                 player_spawn[0], player_spawn[1], 1, 3)
player.on_ground = False
player.y_velocity = 1

npcs = []
enemies = []
load_map_characters()

def restart_game():
    global npcs, enemies
    game_state.game_over = False
    player.reset()
    enemies.clear()
    load_map_characters()

camera = Camera(game_state.map_width, game_state.map_height)
arrows = pygame.sprite.Group()
layer_surfaces = {}

def save_game():
    saving_text = game_state.font_big.render("Saving...", color=(255, 255, 255), shadow=True)
    text_rect = saving_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
    screen.fill((0, 0, 0))
    screen.blit(saving_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1000)
    save_data = {
        "player_pos": (player.rect.x, player.rect.y),
        "health": player.health,
        "max_health": player.max_health,
        "potions": player.potions_collected,
        "enemies_defeated": player.enemies_defeated,
        "attack_damage": player.attack_damage,
        "arrow_count": player.arrow_count,
        "current_map": game_state.current_map,
        "enemies": [],
        "health_potions": [
            {
                "pos": (potion.rect.x, potion.rect.y),
                "collected": potion.collected
            } for potion in game_state.health_potions
        ],
        "npcs": [
            {
                "type": npc.name,
                "pos": [npc.rect.x, npc.rect.y],
                "scale": npc.scale if hasattr(npc, "scale") else 1,
                "dialogue_index": npc.current_dialogue_index
            } for npc in npcs
        ]
    }
    try:
        with open("savegame.json", "w") as f:
            json.dump(save_data, f)
        saved_text = game_state.font_big.render("Game Saved!", color=(0, 255, 0), shadow=True)
        text_rect = saved_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(saved_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)
        print("Oyun kaydedildi!")
    except Exception as e:
        print(f"Oyun kaydedilirken hata: {e}")

def load_game(screen):
    global game_state, player, enemies, camera, npcs
    loading_text = game_state.font_big.render("Loading...", color=(255, 255, 255), shadow=True)
    text_rect = loading_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
    screen.fill((0, 0, 0))
    screen.blit(loading_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    try:
        with open("savegame.json", "r") as f:
            save_data = json.load(f)
            player.rect.x = save_data["player_pos"][0]
            player.rect.y = save_data["player_pos"][1]
            player.health = save_data["health"]
            player.max_health = save_data["max_health"]
            player.potions_collected = save_data["potions"]
            player.enemies_defeated = save_data["enemies_defeated"]
            player.attack_damage = save_data["attack_damage"]
            player.arrow_count = save_data["arrow_count"]
            player.update_hitbox()
            game_state.current_map = save_data["current_map"]
            load_map(game_state.current_map)
            game_state.camera_x = player.rect.centerx - game_state.screen_width // (2 * game_state.zoom_factor)
            game_state.camera_y = player.rect.centery - game_state.screen_height // (2 * game_state.zoom_factor)
            camera = Camera(game_state.map_width, game_state.map_height)
            load_map_characters()
            game_state.health_potions.clear()
            for potion_data in save_data["health_potions"]:
                potion = HealthPotion(potion_data["pos"][0], potion_data["pos"][1])
                potion.collected = potion_data["collected"]
                game_state.health_potions.append(potion)
            npcs.clear()
            for npc_data in save_data.get("npcs", []):
                npc_type = npc_data["type"]
                x, y = npc_data["pos"]
                scale = npc_data["scale"]
                if npc_type == "Blacksmith":
                    npc = Blacksmith(x, y, scale)
                elif npc_type == "Trader":
                    npc = Trader(x, y, scale)
                else:
                    continue
                npc.current_dialogue_index = npc_data["dialogue_index"]
                npcs.append(npc)
            loaded_text = game_state.font_big.render("Game Loaded!", color=(0, 255, 0), shadow=True)
            text_rect = loaded_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
            screen.fill((0, 0, 0))
            screen.blit(loaded_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(500)
            print("Oyun yüklendi!")
    except FileNotFoundError:
        error_text = game_state.font_big.render("No Save File Found!", color=(255, 0, 0), shadow=True)
        text_rect = error_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)
        print("Kayıt dosyası bulunamadı!")
    except Exception as e:
        print(f"Oyun yüklenirken hata: {e}")
        error_text = game_state.font_big.render(f"Error: {str(e)}", color=(255, 0, 0), shadow=True)
        text_rect = error_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)

# Oyun başlatma
"""enemies = pygame.sprite.Group()
enemies.add(NinjaMonk(1300, 1200))
enemies.add(NinjaPeasant(1900, 1200))"""


running = True
moving_left = False
moving_right = False
running_fast = False

while running:
    dt = clock.tick(game_state.fps) / 1000.0
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
                load_game(screen)
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_j:
                player.attack(1)
            if game_state.current_map in ["frozen_cave", "cyberpunk", "lab", "castle"]:
                if event.key == pygame.K_k:
                    player.attack(2)
            if game_state.current_map in ["cyberpunk", "lab", "castle"]:
                if event.key == pygame.K_l:
                    player.attack(3)
            if game_state.current_map in ["lab", "castle"]:
                if event.key == pygame.K_o:
                    player.shoot(arrows)
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running_fast = True
            if game_state.game_over and event.key == pygame.K_r:
                restart_game()
            if event.key == pygame.K_EQUALS:
                set_zoom(game_state.zoom_factor + 0.1)
            if event.key == pygame.K_MINUS:
                set_zoom(game_state.zoom_factor - 0.1)
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

    player.move(moving_left, moving_right, running_fast, game_state.collision_rects)
    # Güncelleme
    if not player.is_in_dialogue:
        player.update(game_state.collision_rects, game_state.spike_rects, enemies, arrows, dt)
        for enemy in enemies:
            enemy.update(player, game_state.collision_rects)

    for npc in npcs:
        npc.update(player, events)

    if check_map_transitions(player):
        load_map_characters()
        camera = Camera(game_state.map_width, game_state.map_height)
        continue

    CAMERA_LERP = 0.05
    target_x = player.rect.centerx - game_state.screen_width // (2 * game_state.zoom_factor)
    target_y = player.rect.centery - game_state.screen_height // (2 * game_state.zoom_factor)
    game_state.camera_x += (target_x - game_state.camera_x) * CAMERA_LERP
    game_state.camera_y += (target_y - game_state.camera_y) * CAMERA_LERP
    game_state.camera_x = max(0, min(game_state.camera_x, game_state.map_width - game_state.screen_width / game_state.zoom_factor))
    game_state.camera_y = max(0, min(game_state.camera_y, game_state.map_height - game_state.screen_height / game_state.zoom_factor))

    screen.fill((0, 0, 0))

    for i, layer in enumerate(game_state.tmx_data.layers):
        if i < game_state.front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, game_state.camera_x, game_state.camera_y)

    for potion in game_state.health_potions:
        potion.update()

    potion_hits = []
    for potion in game_state.health_potions:
        if player.hitbox.colliderect(potion.hitbox):
            if player.heal(potion.healing_amount):
                potion_hits.append(potion)
    
    for potion in potion_hits:
        game_state.health_potions.remove(potion)

    player.draw(screen, game_state.camera_x, game_state.camera_y)

    for potion in game_state.health_potions:
        potion.draw(screen, game_state.camera_x, game_state.camera_y)

    for i, layer in enumerate(game_state.tmx_data.layers):
        if i >= game_state.front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, game_state.camera_x, game_state.camera_y)

    for npc in npcs:
        npc.draw(screen, game_state.camera_x, game_state.camera_y, game_state.font, game_state.zoom_factor, player)

    for enemy in enemies:
        enemy.draw(screen, game_state.camera_x, game_state.camera_y, game_state.font, game_state.zoom_factor, player)

    arrows.update(game_state.collision_rects, enemies)
    for arrow in arrows:
        arrow.draw(screen, game_state.camera_x, game_state.camera_y)

    

    if player.is_dead and player.death_finished:
        game_state.game_over = True
        game_over_text = game_state.font_big.render("GAME OVER", color=(255, 0, 0), shadow=True)
        text_rect = game_over_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.blit(game_over_text, text_rect)
        restart_text = game_state.font.render("Press R to restart", color=(255, 255, 255), shadow=True)
        restart_rect = restart_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)

    fps_text = game_state.font.render(f"FPS: {int(clock.get_fps())}", color=(255, 255, 255), shadow=True)
    screen.blit(fps_text, (10, 10))
    player_status = f"Pos: ({int(player.rect.x)}, {int(player.rect.y)}) | Ground: {player.on_ground}"
    status_text = game_state.font.render(player_status, color=(255, 255, 255), shadow=True)
    screen.blit(status_text, (10, 50))

    print(f"Current map: {game_state.current_map}, Player pos: ({player.rect.x}, {player.rect.y}), Camera: ({game_state.camera_x}, {game_state.camera_y})")

    arrow_text = game_state.font.render(
        f"Arrows: {player.arrow_count}",
        color=(255, 255, 255),
        shadow=True,
        background=(50, 50, 50, 150))
    
    screen.blit(arrow_text, (10, 90))

    if game_state.show_message:
        game_state.message_timer -= 1
        if game_state.message_timer <= 0:
            game_state.show_message = False
        msg_surface = game_state.font_big.render(game_state.message_text, color=(0, 0, 0), shadow=True)
        msg_rect = msg_surface.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 20))
        screen.blit(msg_surface, msg_rect)
    if game_state.show2_message:
        game_state.message2_timer -= 1
        if game_state.message2_timer <= 0:
            game_state.show2_message = False
        msg2_surface = game_state.font_big.render(game_state.message2_text, color=(255, 255, 255), shadow=True)
        msg2_rect = msg2_surface.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 20))
        screen.blit(msg2_surface, msg2_rect)
    if game_state.show3_message:
        game_state.message3_timer -= 1
        if game_state.message3_timer <= 0:
            game_state.show3_message = False
        msg3_surface = game_state.font_big.render(game_state.message3_text, color=(0, 0, 0), shadow=True)
        msg3_rect = msg3_surface.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 20))
        screen.blit(msg3_surface, msg3_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
