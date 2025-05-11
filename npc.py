# npc.py
import pygame
from pygame import Vector2
from game_state import game_state
from utils import Spritesheet

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
        
        try:
            self.prompt_image = pygame.image.load("assets/e_prompt.png").convert_alpha()
        except FileNotFoundError:
            self.prompt_image = None
        
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
                        self.current_dialogue_index = 0
                        self.current_animation = "idle_2"
                        self.frame_index = 0
                        self.update_counter = 0
                        print(f"{self.name} ile diyalog başladı")
                        try:
                            pygame.mixer.Sound("sounds/click.wav").play()
                        except FileNotFoundError:
                            print("Uyarı: sounds/click.wav bulunamadı!")
                    else:
                        self.current_dialogue_index += 1
                        if self.current_dialogue_index >= len(self.dialogues):
                            self.is_interacting = False
                            self.current_animation = "idle"
                            self.frame_index = 0
                            self.update_counter = 0
                            print(f"{self.name} ile diyalog bitti")
                            try:
                                pygame.mixer.Sound("sounds/click.wav").play()
                            except FileNotFoundError:
                                print("Uyarı: sounds/click.wav bulunamadı!")
                        else:
                            print(f"{self.name} diyalog: {self.dialogues[self.current_dialogue_index]}")
                            try:
                                pygame.mixer.Sound("sounds/click.wav").play()
                            except FileNotFoundError:
                                print("Uyarı: sounds/click.wav bulunamadı!")
    
    def update(self, player, events):
        self.update_animation()
        self.check_interaction(player, events)
    
    def draw(self, surface, camera_x, camera_y, font, zoom_factor):
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
                prompt_text = font.render("E", (255, 255, 255))
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
            dialogue_text = self.dialogues[self.current_dialogue_index]
            text_surface = font.render(dialogue_text, color=(255, 255, 255), background=(0, 0, 0))
            text_width, text_height = font.get_size(dialogue_text)
            dialogue_x = (game_state.screen_width - text_width) / 2
            dialogue_y = game_state.screen_height - text_height - 20
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
        
        try:
            self.hammer_sound = pygame.mixer.Sound("sounds/blacksmith_hammer.wav")
            self.hammer_sound.set_volume(0.3)
        except FileNotFoundError:
            print("Uyarı: sounds/blacksmith_hammer.wav bulunamadı!")
            self.hammer_sound = None
        
        self.sound_range = 650
        self.sound_step = 100
        self.sound_increment = 0.2
        self.base_volume = 0.2
        self.current_volume = self.base_volume
        self.last_sound_time = 0
        self.sound_cooldown = 2000
        self.sound_active = False
    
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
        
        elif self.is_interacting and self.sound_active:
            pygame.mixer.Channel(3).stop()
            self.sound_active = False
            print("Ses durduruldu: NPC ile diyalog başladı")
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self.show_interact_prompt:
                    if not self.is_interacting:
                        self.is_interacting = True
                        player.is_in_dialogue = True
                        self.current_dialogue_index = 0
                        self.current_animation = "idle_2"
                        self.frame_index = 0
                        self.update_counter = 0
                        print(f"{self.name} ile diyalog başladı")
                        try:
                            pygame.mixer.Sound("sounds/click.wav").play()
                        except FileNotFoundError:
                            print("Uyarı: sounds/click.wav bulunamadı!")
                    else:
                        self.current_dialogue_index += 1
                        if self.current_dialogue_index >= len(self.dialogues):
                            self.is_interacting = False
                            player.is_in_dialogue = False
                            self.current_animation = "idle"
                            self.frame_index = 0
                            self.update_counter = 0
                            print(f"{self.name} ile diyalog bitti")
                            try:
                                pygame.mixer.Sound("sounds/click.wav").play()
                            except FileNotFoundError:
                                print("Uyarı: sounds/click.wav bulunamadı!")
                        else:
                            print(f"{self.name} diyalog: {self.dialogues[self.current_dialogue_index]}")
                            try:
                                pygame.mixer.Sound("sounds/click.wav").play()
                            except FileNotFoundError:
                                print("Uyarı: sounds/click.wav bulunamadı!")