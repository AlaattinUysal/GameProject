import pygame
from pygame import Vector2
from game_state import game_state
from utils import Spritesheet
from soundmanager import sound_manager

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
        self.animations = {
            "idle": idle_spritesheet.get_animation_frames(128, 128, scale)
        }
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        hitbox_width = self.rect.width * 0.3
        hitbox_height = self.rect.height * 0.6
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.rect.midbottom
        self.is_interacting = False
        self.interaction_range = 100
        self.show_interact_prompt = False
        self.dialogues = []
        self.current_dialogue_index = 0
        self.prompt_alpha = 0
        self.prompt_scale = 1.0
        self.prompt_fade_speed = 15
        self.prompt_animation_timer = 0
        self.scaled_image_cache = {}
        self.prompt_image = None
        self.dialogue_cache = {}
        self.has_accepted = False

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
        self.show_interact_prompt = distance <= self.interaction_range
        target_alpha = 255 if self.show_interact_prompt else 0
        self.prompt_alpha += (target_alpha - self.prompt_alpha) * self.prompt_fade_speed * 0.1
        self.prompt_alpha = max(0, min(255, self.prompt_alpha))
        self.prompt_animation_timer = pygame.time.get_ticks()
        self.prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt:
                    if not self.is_interacting:
                        self.is_interacting = True
                        player.is_in_dialogue = True
                        self.current_dialogue_index = 0
                        self.current_animation = "idle"
                        self.frame_index = 0
                        self.update_counter = 0
                        print(f"{self.name} ile diyalog başladı")
                        sound_manager.play_sound("click")
                    else:
                        self.current_dialogue_index += 1
                        if self.current_dialogue_index >= len(self.dialogues):
                            self.is_interacting = False
                            player.is_in_dialogue = False
                            self.current_animation = "idle"
                            self.frame_index = 0
                            self.update_counter = 0
                            print(f"{self.name} ile diyalog bitti")
                            sound_manager.play_sound("click")
                        else:
                            print(f"{self.name} diyalog: {self.dialogues[self.current_dialogue_index]}")
                            sound_manager.play_sound("click")

    def update(self, player, events):
        self.update_animation()
        self.check_interaction(player, events)

    def draw(self, surface, camera_x, camera_y, font, zoom_factor, player=None):
        screen_x = (self.rect.x - camera_x) * zoom_factor
        screen_y = (self.rect.y - camera_y) * zoom_factor
        scaled_width = int(self.rect.width * zoom_factor)
        scaled_height = int(self.rect.height * zoom_factor)
        cache_key = (id(self.image), zoom_factor, self.flip)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = pygame.transform.flip(scaled_image, self.flip, False)
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
        if self.prompt_alpha > 0:
            if self.prompt_image:
                prompt_width = int(self.prompt_image.get_width() * self.prompt_scale * zoom_factor)
                prompt_height = int(self.prompt_image.get_height() * self.prompt_scale * zoom_factor)
                scaled_prompt = pygame.transform.scale(self.prompt_image, (prompt_width, prompt_height))
                scaled_prompt.set_alpha(int(self.prompt_alpha))
                prompt_x = screen_x + (scaled_width - prompt_width) / 2
                prompt_y = screen_y - prompt_height - 5
                pygame.draw.circle(surface, (50, 50, 50, 150), 
                                 (int(prompt_x + prompt_width / 2), int(prompt_y + prompt_height / 2)), 
                                 int(prompt_width / 1.5), 0)
                surface.blit(scaled_prompt, (prompt_x, prompt_y))
            else:
                prompt_text = font.render("E", color=(255, 255, 255), shadow=True)
                text_width, text_height = font.get_size("E")
                scaled_width = int(text_width * self.prompt_scale)
                scaled_height = int(text_height * self.prompt_scale)
                scaled_prompt = pygame.transform.scale(prompt_text, (scaled_width, scaled_height))
                scaled_prompt.set_alpha(int(self.prompt_alpha))
                prompt_x = screen_x + (self.rect.width * zoom_factor - scaled_width) / 2
                prompt_y = screen_y - scaled_height - 10
                circle_radius = max(scaled_width, scaled_height) * 0.7
                pygame.draw.circle(surface, (50, 50, 50, 150), 
                                 (int(prompt_x + scaled_width / 2), int(prompt_y + scaled_height / 2)), 
                                 int(circle_radius), 0)
                surface.blit(scaled_prompt, (prompt_x, prompt_y))
        if self.is_interacting and self.current_dialogue_index < len(self.dialogues):
            cache_key = (self.current_dialogue_index, zoom_factor)
            if cache_key not in self.dialogue_cache:
                dialogue_text = self.dialogues[self.current_dialogue_index]
                self.dialogue_cache[cache_key] = game_state.font_big.render(
                    dialogue_text, color=(255, 255, 255), background=(0, 0, 0), shadow=True
                )
            text_surface = self.dialogue_cache[cache_key]
            text_width, text_height = game_state.font_big.get_size(self.dialogues[self.current_dialogue_index])
            dialogue_x = (game_state.screen_width - text_width) / 2
            dialogue_y = game_state.screen_height - text_height - 20
            surface.blit(text_surface, (dialogue_x, dialogue_y))

class Blacksmith(NPC):
    def __init__(self, x, y, scale=1):
        idle_spritesheet = Spritesheet("npc_sprites/blacksmith/idle.png")
        idle_2_spritesheet = Spritesheet("npc_sprites/blacksmith/idle_2.png")
        super().__init__(idle_spritesheet, x, y, scale, "Blacksmith")
        self.animations["idle_2"] = idle_2_spritesheet.get_animation_frames(128, 128, scale)
        # Diyaloglar: İlk diyalog ve tekrar için ayrı mesaj
        self.dialogues = [
            "Kılıcını keskinleştirmek ister misin?",
            "Kılıcın zaten keskin! Başka ne yapabilirim?"  # has_accepted = True için
        ]
        self.sound_range = 800
        self.sound_step = 100
        self.sound_increment = 0.1
        self.base_volume = 0.1
        self.current_volume = self.base_volume
        self.last_sound_time = 0
        self.sound_cooldown = 2000
        self.sound_active = False
        self.awaiting_choice = False
        self.selected_option = 0  # 0: Evet, 1: Hayır
        self.show_damage_increase = False
        self.damage_increase_timer = 0
        self.damage_increase_alpha = 255

    def check_interaction(self, player, events):
        player_pos = Vector2(player.rect.center)
        self_pos = Vector2(self.rect.center)
        distance = player_pos.distance_to(self_pos)
        self.show_interact_prompt = distance <= self.interaction_range
        target_alpha = 255 if self.show_interact_prompt else 0
        self.prompt_alpha += (target_alpha - self.prompt_alpha) * self.prompt_fade_speed * 0.1
        self.prompt_alpha = max(0, min(255, self.prompt_alpha))
        self.prompt_animation_timer = pygame.time.get_ticks()
        self.prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)

        # Ses mantığı (değişmeden kalır)
        if not self.is_interacting:
            current_time = pygame.time.get_ticks()
            if distance <= self.sound_range:
                steps = (self.sound_range - min(distance, self.sound_range)) / self.sound_step
                new_volume = min(1.0, self.base_volume + (steps * self.sound_increment))
                if not self.sound_active:
                    if current_time - self.last_sound_time >= self.sound_cooldown:
                        sound_manager.play_sound("blacksmith_hammer", volume=new_volume, loops=-1)
                        self.last_sound_time = current_time
                        self.sound_active = True
                        print(f"Demir dövme sesi çalındı! Mesafe: {distance:.2f}, Ses: {new_volume:.2f}")
                if self.sound_active and abs(self.current_volume - new_volume) > 0.01:
                    self.current_volume = new_volume
                    sound_manager.set_volume("blacksmith_hammer", self.current_volume)
                    print(f"Ses seviyesi güncellendi: {self.current_volume:.2f}")
            elif distance > self.sound_range and self.sound_active:
                sound_manager.stop_sound("blacksmith_hammer")
                self.sound_active = False
                self.last_sound_time = 0
                print("Ses durduruldu: Mesafe sınırın dışına çıkıldı")
        elif self.is_interacting and self.sound_active:
            sound_manager.stop_sound("blacksmith_hammer")
            self.sound_active = False
            print("Ses durduruldu: NPC ile diyalog başladı")

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt and not self.is_interacting:
                    self.is_interacting = True
                    player.is_in_dialogue = True
                    self.current_dialogue_index = 1 if self.has_accepted else 0
                    self.current_animation = "idle_2"
                    self.frame_index = 0
                    self.update_counter = 0
                    print(f"{self.name} ile diyalog başladı: {self.dialogues[self.current_dialogue_index]}")
                    sound_manager.play_sound("click")
                elif self.is_interacting and not self.awaiting_choice:
                    if not self.has_accepted:
                        self.awaiting_choice = True
                        self.selected_option = 0
                        print(f"Seçim ekranı açıldı, seçili: {'Evet' if self.selected_option == 0 else 'Hayır'}")
                        sound_manager.play_sound("click")
                    else:
                        # Zaten kabul edilmiş, diyaloğu bitir
                        self.is_interacting = False
                        player.is_in_dialogue = False
                        self.current_animation = "idle"
                        self.frame_index = 0
                        self.update_counter = 0
                        sound_manager.play_sound("click")
                elif self.is_interacting and self.awaiting_choice:
                    print(f"Seçim onaylandı, seçili: {'Evet' if self.selected_option == 0 else 'Hayır'}")
                    if self.selected_option == 0:  # Evet
                        player.increase_attack_damage(5)
                        print(f"Kılıç keskinleştirildi! Yeni hasar: {player.attack_damage}")
                        self.show_damage_increase = True
                        self.damage_increase_timer = 120
                        self.damage_increase_alpha = 255
                        self.has_accepted = True  # Tek seferlik kabul
                    else:  # Hayır
                        print(f"{self.name} ile diyalog bitti: Hayır seçildi")
                    self.is_interacting = False
                    player.is_in_dialogue = False
                    self.awaiting_choice = False
                    self.current_animation = "idle"
                    self.frame_index = 0
                    self.update_counter = 0
                    sound_manager.play_sound("click")
            elif event.type == pygame.KEYDOWN and self.is_interacting and self.awaiting_choice:
                if event.key == pygame.K_a:
                    self.selected_option = 0
                    print(f"Seçili seçenek: Evet")
                    sound_manager.play_sound("click")
                elif event.key == pygame.K_d:
                    self.selected_option = 1
                    print(f"Seçili seçenek: Hayır")
                    sound_manager.play_sound("click")

    def update(self, player, events):
        self.update_animation()
        self.check_interaction(player, events)
        if self.show_damage_increase:
            self.damage_increase_timer -= 1
            self.damage_increase_alpha = max(0, self.damage_increase_alpha - 255 / 120)
            if self.damage_increase_timer <= 0:
                self.show_damage_increase = False

    def draw(self, surface, camera_x, camera_y, font, zoom_factor, player=None):
        super().draw(surface, camera_x, camera_y, font, zoom_factor, player)
        if self.is_interacting and self.awaiting_choice and not self.has_accepted:
            yes_text = game_state.font.render("Evet", color=(255, 255, 255), background=(0, 0, 0), shadow=True)
            no_text = game_state.font.render("Hayır", color=(255, 255, 255), background=(0, 0, 0), shadow=True)
            yes_width, yes_height = game_state.font.get_size("Evet")
            no_width, no_height = game_state.font.get_size("Hayır")
            box_width = max(yes_width, no_width) + 20
            box_height = max(yes_height, no_height) + 10
            yes_x = game_state.screen_width // 2 - box_width - 10
            no_x = game_state.screen_width // 2 + 10
            box_y = game_state.screen_height - box_height - 60

            pygame.draw.rect(surface, (50, 50, 50), (yes_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, (50, 50, 50), (no_x, box_y, box_width, box_height))
            if self.selected_option == 0:
                pygame.draw.rect(surface, (255, 255, 0), (yes_x, box_y, box_width, box_height), 3)
            else:
                pygame.draw.rect(surface, (255, 255, 0), (no_x, box_y, box_width, box_height), 3)
            
            surface.blit(yes_text, (yes_x + (box_width - yes_width) / 2, box_y + (box_height - yes_height) / 2))
            surface.blit(no_text, (no_x + (box_width - no_width) / 2, box_y + (box_height - no_height) / 2))

        if self.show_damage_increase and player:
            damage_text = game_state.font_big.render(
                f"Kılıcın Gücü Arttı! Yeni Hasar: {player.attack_damage}",
                color=(255, 0, 0),
                shadow=True
            )
            damage_text.set_alpha(int(self.damage_increase_alpha))
            text_width, text_height = game_state.font_big.get_size(f"Kılıcın Gücü Arttı! Yeni Hasar: {player.attack_damage}")
            surface.blit(damage_text, ((game_state.screen_width - text_width) / 2, game_state.screen_height - text_height - 20))

class Trader(NPC):
    def __init__(self, x, y, scale=1):
        idle_spritesheet = Spritesheet("npc_sprites/trader/idle.png")
        super().__init__(idle_spritesheet, x, y, scale, "Trader")
        self.flip = True
        self.dialogues = [
            "Bu mağarada Kara Samuray’ın lanetli kristali var. 5 düşmanı yen, kristali bul!",
            "Kristali etkisiz hale getirdin! Cyberpunk Mahalle’ye git, Kara Samuray orada teknolojiyle oynuyor."
        ]
        self.task_completed = False

    def check_interaction(self, player, events):
        player_pos = Vector2(player.rect.center)
        self_pos = Vector2(self.rect.center)
        distance = player_pos.distance_to(self_pos)
        self.show_interact_prompt = distance <= self.interaction_range
        target_alpha = 255 if self.show_interact_prompt else 0
        self.prompt_alpha += (target_alpha - self.prompt_alpha) * self.prompt_fade_speed * 0.1
        self.prompt_alpha = max(0, min(255, self.prompt_alpha))
        self.prompt_animation_timer = pygame.time.get_ticks()
        self.prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)

        if player.enemies_defeated >= 5:
            self.task_completed = True

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt and not self.is_interacting:
                    self.is_interacting = True
                    player.is_in_dialogue = True
                    self.current_dialogue_index = 1 if self.task_completed else 0
                    self.current_animation = "idle"
                    self.frame_index = 0
                    self.update_counter = 0
                    print(f"{self.name} ile diyalog başladı: {self.dialogues[self.current_dialogue_index]}")
                    sound_manager.play_sound("click")
                elif self.is_interacting:
                    self.current_dialogue_index += 1
                    if self.current_dialogue_index >= len(self.dialogues):
                        self.is_interacting = False
                        player.is_in_dialogue = False
                        self.current_animation = "idle"
                        self.frame_index = 0
                        self.update_counter = 0
                        print(f"{self.name} ile diyalog bitti")
                        sound_manager.play_sound("click")
                    else:
                        print(f"{self.name} diyalog: {self.dialogues[self.current_dialogue_index]}")
                        sound_manager.play_sound("click")

class Doctor(NPC):
    def __init__(self, x, y, scale=1):
        idle_spritesheet = Spritesheet("npc_sprites/doctor/Idle.png")
        dialogue_spritesheet = Spritesheet("npc_sprites/doctor/Dialogue.png")
        super().__init__(idle_spritesheet, x, y, scale, "Doctor")
        self.animations["dialogue"] = dialogue_spritesheet.get_animation_frames(128, 128, scale)
        self.dialogues = [
            "Seni iyileştirmemi ister misin?",
            "Canın zaten tam! Başka ne yapabilirim?"  # has_accepted = True için
        ]
        self.interaction_range = 100
        self.awaiting_choice = False
        self.selected_option = 0
        self.show_heal_message = False
        self.heal_message_timer = 0
        self.heal_message_alpha = 255
        self.heal_amount = 50
        self.flip = True

    def check_interaction(self, player, events):
        player_pos = Vector2(player.rect.center)
        self_pos = Vector2(self.rect.center)
        distance = player_pos.distance_to(self_pos)
        self.show_interact_prompt = distance <= self.interaction_range
        target_alpha = 255 if self.show_interact_prompt else 0
        self.prompt_alpha += (target_alpha - self.prompt_alpha) * self.prompt_fade_speed * 0.1
        self.prompt_alpha = max(0, min(255, self.prompt_alpha))
        self.prompt_animation_timer = pygame.time.get_ticks()
        self.prompt_scale = 1.0 + 0.1 * (pygame.time.get_ticks() % 1000 / 1000)

        if self.is_interacting or self.awaiting_choice:
            self.current_animation = "dialogue"
        else:
            self.current_animation = "idle"

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt and not self.is_interacting:
                    self.is_interacting = True
                    player.is_in_dialogue = True
                    self.current_dialogue_index = 1 if self.has_accepted else 0
                    self.current_animation = "dialogue"
                    self.frame_index = 0
                    self.update_counter = 0
                    print(f"{self.name} ile diyalog başladı: {self.dialogues[self.current_dialogue_index]}")
                    sound_manager.play_sound("click")
                elif self.is_interacting and not self.awaiting_choice:
                    if not self.has_accepted:
                        self.awaiting_choice = True
                        self.selected_option = 0
                        print(f"Seçim ekranı açıldı, seçili: {'Evet' if self.selected_option == 0 else 'Hayır'}")
                        sound_manager.play_sound("click")
                    else:
                        self.is_interacting = False
                        player.is_in_dialogue = False
                        self.current_animation = "idle"
                        self.frame_index = 0
                        self.update_counter = 0
                        sound_manager.play_sound("click")
                elif self.is_interacting and self.awaiting_choice:
                    print(f"Seçim onaylandı, seçili: {'Evet' if self.selected_option == 0 else 'Hayır'}")
                    if self.selected_option == 0:
                        if player.heal(self.heal_amount):
                            sound_manager.play_sound("potion")
                            self.show_heal_message = True
                            self.heal_message_timer = 120
                            self.heal_message_alpha = 255
                            print(f"Oyuncu iyileştirildi! Yeni can: {player.health}/{player.max_health}")
                            self.has_accepted = True  # Tek seferlik kabul
                        else:
                            print("İyileştirme yapılamadı: Can zaten dolu!")
                    else:
                        print(f"{self.name} ile diyalog bitti: Hayır seçildi")
                    self.is_interacting = False
                    player.is_in_dialogue = False
                    self.awaiting_choice = False
                    self.current_animation = "idle"
                    self.frame_index = 0
                    self.update_counter = 0
                    sound_manager.play_sound("click")
            elif event.type == pygame.KEYDOWN and self.is_interacting and self.awaiting_choice:
                if event.key == pygame.K_a:
                    self.selected_option = 0
                    print(f"Seçili seçenek: Evet")
                    sound_manager.play_sound("click")
                elif event.key == pygame.K_d:
                    self.selected_option = 1
                    print(f"Seçili seçenek: Hayır")
                    sound_manager.play_sound("click")

    def update(self, player, events):
        self.update_animation()
        self.check_interaction(player, events)
        if self.show_heal_message:
            self.heal_message_timer -= 1
            self.heal_message_alpha = max(0, self.heal_message_alpha - 255 / 120)
            if self.heal_message_timer <= 0:
                self.show_heal_message = False

    def draw(self, surface, camera_x, camera_y, font, zoom_factor, player=None):
        super().draw(surface, camera_x, camera_y, font, zoom_factor, player)
        if self.is_interacting and self.awaiting_choice and not self.has_accepted:
            yes_text = game_state.font.render("Evet", color=(255, 255, 255), background=(0, 0, 0), shadow=True)
            no_text = game_state.font.render("Hayır", color=(255, 255, 255), background=(0, 0, 0), shadow=True)
            yes_width, yes_height = game_state.font.get_size("Evet")
            no_width, no_height = game_state.font.get_size("Hayır")
            box_width = max(yes_width, no_width) + 20
            box_height = max(yes_height, no_height) + 10
            yes_x = game_state.screen_width // 2 - box_width - 10
            no_x = game_state.screen_width // 2 + 10
            box_y = game_state.screen_height - box_height - 60

            pygame.draw.rect(surface, (50, 50, 50), (yes_x, box_y, box_width, box_height))
            pygame.draw.rect(surface, (50, 50, 50), (no_x, box_y, box_width, box_height))
            if self.selected_option == 0:
                pygame.draw.rect(surface, (255, 255, 0), (yes_x, box_y, box_width, box_height), 3)
            else:
                pygame.draw.rect(surface, (255, 255, 0), (no_x, box_y, box_width, box_height), 3)

            surface.blit(yes_text, (yes_x + (box_width - yes_width) / 2, box_y + (box_height - yes_height) / 2))
            surface.blit(no_text, (no_x + (box_width - no_width) / 2, box_y + (box_height - no_height) / 2))

        if self.show_heal_message and player:
            heal_text = game_state.font_big.render(
                f"Canın İyileştirildi! Yeni Can: {player.health}",
                color=(0, 255, 0),
                shadow=True
            )
            heal_text.set_alpha(int(self.heal_message_alpha))
            text_width, text_height = game_state.font_big.get_size(f"Canın İyileştirildi! Yeni Can: {player.health}")
            surface.blit(heal_text, ((game_state.screen_width - text_width) / 2, game_state.screen_height - text_height - 20))
