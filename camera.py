# camera.py
import pygame
from game_state import game_state

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + game_state.screen_width / (2 * game_state.zoom_factor)
        y = -target.rect.centery + game_state.screen_height / (2 * game_state.zoom_factor)
        x = max(-(self.width - game_state.screen_width / game_state.zoom_factor), min(0, x))
        y = max(-(self.height - game_state.screen_height / game_state.zoom_factor), min(0, y))
        self.camera = pygame.Rect(x, y, self.width, self.height)