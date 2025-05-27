# items.py
import pygame
from game_state import game_state

class PotionSpritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()
        self.frame_width = self.sheet.get_width() // 3  # 3x3 ızgara (9 kare)
        self.frame_height = self.sheet.get_height() // 3
        self.frames = []
        for y in range(3):
            for x in range(3):
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sheet, (0, 0), (x * self.frame_width, y * self.frame_height, self.frame_width, self.frame_height))
                self.frames.append(frame)

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y, healing_amount, spritesheet):
        pygame.sprite.Sprite.__init__(self)     
        self.frames = spritesheet.frames
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0
        self.original_image = self.frames[self.current_frame]
        
        self.healing_amount = healing_amount
        self.rect = self.original_image.get_rect()
        self.rect.topleft = (x, y)
        self.hitbox = self.rect.inflate(-self.rect.width // 8, -self.rect.height // 8)  # %12.5 daha küçük hitbox
        
        self.scaled_image_cache = {}

    def update(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.original_image = self.frames[self.current_frame]
        self.hitbox.topleft = self.rect.topleft

    def draw(self, surface, camera_x, camera_y):
        screen_x = (self.rect.x - camera_x) * game_state.zoom_factor
        screen_y = (self.rect.y - camera_y) * game_state.zoom_factor
        scaled_width = int(self.rect.width * game_state.zoom_factor)
        scaled_height = int(self.rect.height * game_state.zoom_factor)
        
        cache_key = (id(self.original_image), game_state.zoom_factor)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = scaled_image
        
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
