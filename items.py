# items.py
import pygame
from game_state import game_state

class HealthPotion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("health.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collected = False

    def draw(self, surface, camera_x, camera_y):
        if self.collected:
            return
        screen_x = (self.rect.x - camera_x) * game_state.zoom_factor
        screen_y = (self.rect.y - camera_y) * game_state.zoom_factor
        scaled_width = int(self.rect.width * game_state.zoom_factor)
        scaled_height = int(self.rect.height * game_state.zoom_factor)
        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        surface.blit(scaled_image, (screen_x, screen_y))