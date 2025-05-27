import pygame
import pytmx
import sys
import json
import pygame.time
from npc import Blacksmith, Trader, Doctor
from game_state import game_state
from camera import Camera
from map import load_map, check_map_transitions, draw_layer, find_spawn_point, draw_transition_prompt, adjust_spawn_to_ground
from player import Samurai
from utils import Spritesheet
from soundmanager import sound_manager
from items import HealthPotion
import enemy_types

pygame.init()
screen = pygame.display.set_mode((game_state.screen_width, game_state.screen_height))
pygame.display.set_caption("Samurai's Path")    
clock = pygame.time.Clock()

def set_zoom(factor):
    game_state.zoom_factor = max(0.5, min(factor, 3))
    game_state.tile_cache.clear()
    if hasattr(player, 'scaled_image_cache'):
        player.scaled_image_cache.clear()

walk_spritesheet = Spritesheet("player sprite sheets/Walk.png")
idle_spritesheet = Spritesheet("player sprite sheets/Idle.png")
jump_spritesheet = Spritesheet("player sprite sheets/Jump.png")
run_spritesheet = Spritesheet("player sprite sheets/Run.png")
attack1_spritesheet = Spritesheet("player sprite sheets/Attack_1.png")
attack2_spritesheet = Spritesheet("player sprite sheets/Attack_2.png")
attack3_spritesheet = Spritesheet("player sprite sheets/Attack_3.png")
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
        elif npc_type == "Doctor":
            npc = Doctor(x, y, scale)
            npcs.append(npc)
            print(f"{npc_type} yüklendi: ({x}, {y})")
        else:
            print(f"Uyarı: Bilinmeyen NPC türü: {npc_type}")

    for enemy_data in game_state.map_characters[current_map]["enemies"]:
        enemy_type = enemy_data["type"]
        x, y = enemy_data["x"], enemy_data["y"]
        scale = enemy_data.get("scale", 1)
        if enemy_type == "AnimeKnight":
            enemy_data = enemy_types.AnimeKnight(x, y, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet)
            enemies.append(enemy_data)
            print(f"{enemy_type} yüklendi: ({x}, {y})")

try:
    load_map(game_state.current_map)
    sound_manager.play_ambiance(game_state.current_map)
    print(f"Harita yüklendi: {game_state.current_map}, tmx_data: {game_state.tmx_data}")
except Exception as e:
    print(f"Başlangıç haritası yüklenirken hata: {e}")
    pygame.quit()
    sys.exit(1)

player_spawn = find_spawn_point()
print(f"Spawn noktası: {player_spawn}")
player = Samurai(walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, 
                 hurt_spritesheet, death_spritesheet, shot_spritesheet,
                 player_spawn[0], player_spawn[1], 1, 3)
player.on_ground = False
player.y_velocity = 1

arrows = pygame.sprite.Group()
npcs = []
enemies = []
load_map_characters()

def restart_game():
    global npcs, enemies
    game_state.game_over = False
    player.reset()
    enemies.clear()
    load_map_characters()

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
        "xp": player.xp,
        "level": player.level,
        "max_xp": player.max_xp,
        "current_map": game_state.current_map,
        "current_ambiance": sound_manager.current_ambiance,
        "enemies": [
            {
                "type": enemy.__class__.__name__,
                "pos": (enemy.rect.x, enemy.rect.y),
                "can": getattr(enemy, "can", 0),
                "scale": getattr(enemy, "scale", 1),
                "current_animation": getattr(enemy, "mevcut_animasyon", "idle"),
                "frame_index": getattr(enemy, "kare_indeksi", 0)
            } for enemy in enemies if hasattr(enemy, "can") and enemy.can > 0
        ],
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
                "dialogue_index": npc.current_dialogue_index,
                "has_accepted": getattr(npc, "has_accepted", False),
                "task_completed": getattr(npc, "task_completed", False)
            } for npc in npcs
        ]
    }
    
    try:
        with open("savegame.json", "w") as f:
            json.dump(save_data, f, indent=2)
        saved_text = game_state.font_big.render("Game Saved!", color=(0, 255, 0), shadow=True)
        text_rect = saved_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(saved_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(500)
        print("Oyun kaydedildi!")
    except Exception as e:
        print(f"Oyun kaydedilirken hata: {e}")
        error_text = game_state.font_big.render(f"Error: {str(e)}", color=(255, 0, 0), shadow=True)
        text_rect = error_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)

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
            
            # Oyuncu durumunu yükle
            player.rect.x = save_data.get("player_pos", [player.rect.x, player.rect.y])[0]
            player.rect.y = save_data.get("player_pos", [player.rect.x, player.rect.y])[1]
            player.health = save_data.get("health", player.health)
            player.max_health = save_data.get("max_health", player.max_health)
            player.potions_collected = save_data.get("potions", player.potions_collected)
            player.enemies_defeated = save_data.get("enemies_defeated", player.enemies_defeated)
            player.attack_damage = save_data.get("attack_damage", player.attack_damage)
            player.arrow_count = save_data.get("arrow_count", player.arrow_count)
            player.xp = save_data.get("xp", player.xp)
            player.level = save_data.get("level", player.level)
            player.max_xp = save_data.get("max_xp", player.max_xp)
            player.update_hitbox()
            
            # Harita ve kamera
            game_state.current_map = save_data.get("current_map", game_state.current_map)
            load_map(game_state.current_map)
            if save_data.get("current_ambiance"):
                sound_manager.play_ambiance(save_data["current_ambiance"])
            game_state.camera_x = player.rect.centerx - game_state.screen_width // (2 * game_state.zoom_factor)
            game_state.camera_y = player.rect.centery - game_state.screen_height // (2 * game_state.zoom_factor)
            camera = Camera(game_state.map_width, game_state.map_height)
            
            # Sağlık iksirlerini yükle
            game_state.health_potions.clear()
            for potion_data in save_data.get("health_potions", []):
                potion = HealthPotion(potion_data["pos"][0], potion_data["pos"][1])
                potion.collected = potion_data.get("collected", False)
                game_state.health_potions.add(potion)
            
            # NPC'leri yükle
            npcs.clear()
            for npc_data in save_data.get("npcs", []):
                npc_type = npc_data.get("type")
                x, y = npc_data.get("pos", [0, 0])
                scale = npc_data.get("scale", 1)
                if npc_type == "Blacksmith":
                    npc = Blacksmith(x, y, scale)
                elif npc_type == "Trader":
                    npc = Trader(x, y, scale)
                elif npc_type == "Doctor":
                    npc = Doctor(x, y, scale)
                else:
                    print(f"Uyarı: Bilinmeyen NPC türü: {npc_type}")
                    continue
                npc.current_dialogue_index = npc_data.get("dialogue_index", 0)
                npc.has_accepted = npc_data.get("has_accepted", False)
                npc.task_completed = npc_data.get("task_completed", False)
                npcs.append(npc)
            
            # Düşmanları yükle
            enemies.clear()
            for enemy_data in save_data.get("enemies", []):
                enemy_type = enemy_data.get("type")
                x, y = enemy_data.get("pos", [0, 0])
                scale = enemy_data.get("scale", 1)
                if enemy_type == "AnimeKnight":
                    enemy = enemy_types.AnimeKnight(
                        x, y, walk_spritesheet, idle_spritesheet, jump_spritesheet,
                        run_spritesheet, attack1_spritesheet, attack2_spritesheet,
                        attack3_spritesheet, hurt_spritesheet, death_spritesheet
                    )
                    enemy.can = enemy_data.get("can", enemy.can)
                    enemy.mevcut_animasyon = enemy_data.get("current_animation", "idle")
                    enemy.kare_indeksi = enemy_data.get("frame_index", 0)
                    enemies.append(enemy)
                    print(f"{enemy_type} yüklendi: ({x}, {y}), Can: {enemy.can}")
                else:
                    print(f"Uyarı: Bilinmeyen düşman türü: {enemy_type}")
            
            # Yüklenen pozisyonu zemine hizala
            adjusted_pos = adjust_spawn_to_ground(player, player.rect.x, player.rect.y)
            player.rect.centerx = adjusted_pos[0]
            player.rect.bottom = adjusted_pos[1]
            player.update_hitbox()
            
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
    except json.JSONDecodeError:
        error_text = game_state.font_big.render("Corrupted Save File!", color=(255, 0, 0), shadow=True)
        text_rect = error_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)
        print("Kayıt dosyası bozuk!")
    except Exception as e:
        print(f"Oyun yüklenirken hata: {e}")
        error_text = game_state.font_big.render(f"Error: {str(e)}", color=(255, 0, 0), shadow=True)
        text_rect = error_text.get_rect(center=(game_state.screen_width // 2, game_state.screen_height // 2))
        screen.fill((0, 0, 0))
        screen.blit(error_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1500)

running = True
moving_left = False
moving_right = False
running_fast = False
fade_surface = pygame.Surface((game_state.screen_width, game_state.screen_height))
fade_surface.fill((0, 0, 0))

# --- ESC ile menüye dönme onay kutusu için ek değişkenler ---
show_menu_confirm = False
menu_confirm_selected = 0  # 0: Evet, 1: Hayır

while running:
    dt = clock.tick(game_state.fps) / 1000.0
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            player.hit_sound_playing = False
        if show_menu_confirm:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    menu_confirm_selected = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    menu_confirm_selected = 1
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if menu_confirm_selected == 0:
                        # Menüye dön: Menü programını başlat
                        import subprocess, sys, os
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        project_root = current_dir  # game.py zaten kök dizinde
                        menu_py = os.path.join(project_root, 'menu', 'menu.py')
                        pygame.quit()
                        subprocess.Popen([sys.executable, menu_py], cwd=project_root)
                        sys.exit()
                    else:
                        # Hayır: Onay kutusunu kapat
                        show_menu_confirm = False
                if event.key == pygame.K_ESCAPE:
                    show_menu_confirm = False
            # --- Mouse ile tıklama kontrolü ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                # --- Evet/Hayır butonlarının gerçek çizim konumlarını kullan ---
                box_w, box_h = 585, 180
                box_x = (game_state.screen_width - box_w) // 2
                box_y = (game_state.screen_height - box_h) // 2
                btn_font = game_state.font_big
                evet_surf = btn_font.render("EVET", color=(0,200,0), shadow=True)
                hayir_surf = btn_font.render("HAYIR", color=(200,0,0), shadow=True)
                evet_rect = evet_surf.get_rect(center=(game_state.screen_width//2-80, box_y+130))
                hayir_rect = hayir_surf.get_rect(center=(game_state.screen_width//2+80, box_y+130))
                if evet_rect.collidepoint(mouse_x, mouse_y):
                    # Menüye dön
                    import subprocess, sys, os
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = current_dir
                    menu_py = os.path.join(project_root, 'menu', 'menu.py')
                    pygame.quit()
                    subprocess.Popen([sys.executable, menu_py], cwd=project_root)
                    sys.exit()
                elif hayir_rect.collidepoint(mouse_x, mouse_y):
                    show_menu_confirm = False
            # Onay kutusu açıkken diğer eventleri işlemeden devam et
            continue
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
            if event.key == pygame.K_k:
                player.attack(2)
            if event.key == pygame.K_l:
                player.attack(3)
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
            if event.key == pygame.K_ESCAPE:
                show_menu_confirm = True
                menu_confirm_selected = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running_fast = False
            if event.key == pygame.K_SPACE:
                player.release_jump()

    if game_state.is_fading:
        if game_state.fade_state == "out":
            game_state.fade_alpha += game_state.fade_speed
            if game_state.fade_alpha >= 255:
                game_state.fade_alpha = 255
                game_state.fade_state = "in"
                game_state.current_map = game_state.target_map
                load_map(game_state.current_map)
                spawn_pos = find_spawn_point(game_state.target_spawn)
                adjusted_pos = adjust_spawn_to_ground(player, spawn_pos[0], spawn_pos[1])
                player.rect.centerx = adjusted_pos[0]
                player.rect.bottom = adjusted_pos[1]
                player.update_hitbox()
                player.y_velocity = 0
                load_map_characters()
        elif game_state.fade_state == "in":
            game_state.fade_alpha -= game_state.fade_speed
            if game_state.fade_alpha <= 0:
                game_state.fade_alpha = 0
                game_state.is_fading = False
                sound_manager.play_ambiance(game_state.current_map)
    
    else:
        sound_manager.update_boss_music()
        player.move(moving_left, moving_right, running_fast, game_state.collision_rects)
        if not player.is_in_dialogue:
            player.update(game_state.collision_rects, game_state.spike_rects, enemies, arrows, dt)

        for npc in npcs:
            npc.update(player, events)
        check_map_transitions(player, events)
            
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
                sound_manager.play_sound("potion")
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

    player.update_animation(arrows)
    for dusman in enemies:
        dusman.animasyonu_guncelle()

    for dusman in enemies[:]:
        if hasattr(dusman, 'can') and dusman.can <= 0 and hasattr(dusman, 'olum_animasyonu_tamamlandi') and dusman.olum_animasyonu_tamamlandi:
            enemies.remove(dusman)
            print(f"Düşman listeden kaldırıldı: {dusman.__class__.__name__}")
            continue
        print(f"Düşman: {dusman.__class__.__name__}, Pozisyon: ({dusman.rect.centerx}, {dusman.rect.bottom}), Animasyon: {dusman.mevcut_animasyon}, Can: {dusman.can}")
        dusman.guncelle(player, game_state.collision_rects)
    
    arrows.update(game_state.collision_rects, enemies, player)
    for arrow in arrows:
        arrow.draw(screen, game_state.camera_x, game_state.camera_y)

    draw_transition_prompt(screen, game_state.camera_x, game_state.camera_y)

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

    arrow_text = game_state.font.render(
        f"Arrows: {player.arrow_count}",
        color=(255, 255, 255),
        shadow=True,
        background=(50, 50, 50, 150))
    screen.blit(arrow_text, (10, 90))

    level_text = game_state.font.render(
        f"Seviye: {player.level} XP: {player.xp}/{player.max_xp}",
        color=(255, 255, 255),
        shadow=True,
        background=(50, 50, 50, 150))
    screen.blit(level_text, (10, 135))

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

    if game_state.fade_alpha > 0:
        fade_surface.set_alpha(int(game_state.fade_alpha))
        screen.blit(fade_surface, (0, 0))

    for dusman in enemies:
        dusman.ciz(screen, game_state.camera_x, game_state.camera_y, game_state.zoom_factor)
        

    for dusman in enemies:
        print(f"Düşman: {dusman.__class__.__name__}, Animasyon: {dusman.mevcut_animasyon}, Kare: {dusman.kare_indeksi}, Animasyonlar: {list(dusman.animasyonlar.keys())}")

    # --- ESC onay kutusu açıksa oyun durur, sadece kutu çizilir ---
    if show_menu_confirm:
        # Arka planı karart
        darken = pygame.Surface((game_state.screen_width, game_state.screen_height), pygame.SRCALPHA)
        darken.fill((0, 0, 0, 180))
        screen.blit(darken, (0, 0))
        # Onay kutusu
        box_w, box_h = 585, 180
        box_x = (game_state.screen_width - box_w) // 2
        box_y = (game_state.screen_height - box_h) // 2
        pygame.draw.rect(screen, (40, 40, 40), (box_x, box_y, box_w, box_h), border_radius=12)
        pygame.draw.rect(screen, (255, 140, 0), (box_x, box_y, box_w, box_h), 4, border_radius=12)
        # Başlık
        title_font = game_state.font_big
        title_surf = title_font.render("Menüye dönmek istiyor musunuz?", color=(255,255,255), shadow=True)
        title_rect = title_surf.get_rect(center=(game_state.screen_width//2, box_y+50))
        screen.blit(title_surf, title_rect)
        # Evet/Hayır kutuları
        btn_font = game_state.font_big
        evet_color = (0,200,0) if menu_confirm_selected == 0 else (100,100,100)
        hayir_color = (200,0,0) if menu_confirm_selected == 1 else (100,100,100)
        evet_surf = btn_font.render("EVET", color=evet_color, shadow=True)
        hayir_surf = btn_font.render("HAYIR", color=hayir_color, shadow=True)
        evet_rect = evet_surf.get_rect(center=(game_state.screen_width//2-80, box_y+130))
        hayir_rect = hayir_surf.get_rect(center=(game_state.screen_width//2+80, box_y+130))
        screen.blit(evet_surf, evet_rect)
        screen.blit(hayir_surf, hayir_rect)
        pygame.display.flip()
        continue  # Oyun güncellenmez, sadece kutu çizilir

    pygame.display.flip()

pygame.quit()
sys.exit()
