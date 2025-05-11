# game.py
import pygame
import pytmx
import sys
import json
import pygame.time
from npc import Blacksmith
from game_state import game_state
from camera import Camera
from enemy import NinjaMonk
from map import load_map, check_map_transitions, draw_layer, find_spawn_point
from player import Samurai, Arrow
from items import HealthPotion
from utils import Spritesheet

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((game_state.screen_width, game_state.screen_height))
pygame.display.set_caption("Samurai's path")
clock = pygame.time.Clock()

def check_potion_collisions():
    for potion in game_state.health_potions:
        if not potion.collected and player.hitbox.colliderect(potion.rect):
            if player.health == player.max_health:
                print("Canın zaten dolu, iksir alınamaz!")
                continue
            potion.collected = True
            player.collect_potion()
            potion_sound = pygame.mixer.Sound("sounds/potion.wav")
            pygame.mixer.Channel(1).play(potion_sound)
            print("Health potion collected!")
            break

def set_zoom(factor):
    game_state.zoom_factor = max(0.5, min(factor, 3))
    game_state.tile_cache.clear()
    if hasattr(player, 'scaled_image_cache'):
        player.scaled_image_cache.clear()

# Spritesheet'leri yükle
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

# Haritayı yükle
try:
    load_map(game_state.current_map)
except Exception as e:
    print(f"Başlangıç haritası yüklenirken hata: {e}")
    pygame.quit()
    sys.exit(1)

# Oyuncuyu başlat
player_spawn = find_spawn_point()
player = Samurai(walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, 
                 elixir_spritesheet, hurt_spritesheet, death_spritesheet, shot_spritesheet,
                 player_spawn[0], player_spawn[1], 1, 3)
player.on_ground = False
player.y_velocity = 1

def restart_game():
    game_state.game_over = False
    player.reset()
    enemies.clear()

# Diğer nesneleri başlat
enemies = []
npcs = []
blacksmith = Blacksmith(1200, 1163, 1)
npcs.append(blacksmith)
camera = Camera(game_state.map_width, game_state.map_height)
arrows = pygame.sprite.Group()
layer_surfaces = {}

def save_game():
    saving_text = game_state.font_big.render("Saving...", True, (255, 255, 255))
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
            } for potion in game_state.health_potions
        ]
    }
    try:
        with open("savegame.json", "w") as f:
            json.dump(save_data, f)
        saved_text = game_state.font_big.render("Game Saved!", True, (0, 255, 0))
        text_rect = saved_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(saved_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)
        print("Oyun kaydedildi!")
    except Exception as e:
        print(f"Oyun kaydedilirken hata: {e}")

def load_game():
    global game_state, player, enemies, camera
    loading_text = game_state.font_big.render("Loading...", True, (255, 255, 255))
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
            enemies.clear()
            for enemy_data in save_data["enemies"]:
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
            game_state.health_potions.clear()
            for potion_data in save_data["health_potions"]:
                potion = HealthPotion(potion_data["pos"][0], potion_data["pos"][1])
                potion.collected = potion_data["collected"]
                game_state.health_potions.append(potion)
            loaded_text = game_state.font_big.render("Game Loaded!", True, (0, 255, 0))
            text_rect = loaded_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
            screen.fill((0, 0, 0))
            screen.blit(loaded_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(500)
            print("Oyun yüklendi!")
    except FileNotFoundError:
        error_text = game_state.font_big.render("No Save File Found!", True, (255, 0, 0))
        text_rect = error_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)
        print("Kayıt dosyası bulunamadı!")
    except Exception as e:
        print(f"Oyun yüklenirken hata: {e}")

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
                load_game()
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_j:
                player.attack(1)
            if game_state.current_map in ["frozen_cave", "cyberpunk", "lab"]:
                if event.key == pygame.K_k:
                    player.attack(2)
            if event.key == pygame.K_l:
                if game_state.current_map in ["cyberpunk", "lab"]:
                    player.attack(3)
            if game_state.current_map == "lab":
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
    player.update(game_state.collision_rects, game_state.spike_rects, enemies, arrows, dt)

    for npc in npcs:
        npc.update(player, events)

    check_potion_collisions()

    if check_map_transitions(player):
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

    player.draw(screen, game_state.camera_x, game_state.camera_y)

    for i, layer in enumerate(game_state.tmx_data.layers):
        if i >= game_state.front_layer_index and isinstance(layer, pytmx.TiledTileLayer):
            draw_layer(layer, screen, game_state.camera_x, game_state.camera_y)

    for potion in game_state.health_potions:
        potion.draw(screen, game_state.camera_x, game_state.camera_y)

    for npc in npcs:
        npc.draw(screen, game_state.camera_x, game_state.camera_y, game_state.font, game_state.zoom_factor)

    arrows.update(game_state.collision_rects, enemies)
    for arrow in arrows:
        arrow.draw(screen, game_state.camera_x, game_state.camera_y)

    enemies_to_remove = []
    for enemy in enemies:
        enemy.update(player, game_state.collision_rects)
        if enemy.should_remove:
            enemies_to_remove.append(enemy)

    for enemy in enemies_to_remove:
        enemies.remove(enemy)

    for enemy in enemies:
        if enemy.alive or (enemy.is_dead and not enemy.death_finished):
            enemy.draw(screen, game_state.camera_x, game_state.camera_y)

    if player.is_dead and player.death_finished:
        game_state.game_over = True
        game_over_text = game_state.font_big.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.blit(game_over_text, text_rect)
        restart_text = game_state.font.render("Press R to restart`", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2 + 50))
        screen.blit(restart_text, restart_rect)

    fps_text = game_state.font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))
    player_status = f"Pos: ({int(player.rect.x)}, {int(player.rect.y)}) | Ground: {player.on_ground}"
    status_text = game_state.font.render(player_status, True, (255, 255, 255))
    screen.blit(status_text, (10, 50))

    if game_state.show_message:
        game_state.message_timer -= 1
        if game_state.message_timer <= 0:
            game_state.show_message = False
        msg_surface = game_state.font_big.render(game_state.message_text, True, (0, 0, 0))
        msg_rect = msg_surface.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 20))
        screen.blit(msg_surface, msg_rect)
    if game_state.show2_message:
        game_state.message2_timer -= 1
        if game_state.message2_timer <= 0:
            game_state.show2_message = False
        msg2_surface = game_state.font_big.render(game_state.message2_text, True, (255, 255, 255))
        msg2_rect = msg2_surface.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 20))
        screen.blit(msg2_surface, msg2_rect)
    if game_state.show3_message:
        game_state.message3_timer -= 1
        if game_state.message3_timer <= 0:
            game_state.show3_message = False
        msg3_surface = game_state.font_big.render(game_state.message3_text, True, (0, 0, 0))
        msg3_rect = msg3_surface.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 20))
        screen.blit(msg3_surface, msg3_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()