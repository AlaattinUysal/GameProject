import pygame
from src.core.settings import WIDTH, WHITE, LIGHT_BLUE, SHADOW_GRAY

class Cloud:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x += self.speed
        if self.x > WIDTH + 100:
            self.x = -100

    def draw(self, surface):
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x, self.y + 5), 30)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 40, self.y + 5), 35)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 80, self.y + 5), 30)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 20, self.y - 15 + 5), 35)
        pygame.draw.circle(surface, SHADOW_GRAY, (self.x + 60, self.y - 10 + 5), 30)

        pygame.draw.circle(surface, WHITE, (self.x, self.y), 30)
        pygame.draw.circle(surface, WHITE, (self.x + 40, self.y), 35)
        pygame.draw.circle(surface, WHITE, (self.x + 80, self.y), 30)
        pygame.draw.circle(surface, WHITE, (self.x + 20, self.y - 15), 35)
        pygame.draw.circle(surface, LIGHT_BLUE, (self.x + 40, self.y + 10), 35)
        pygame.draw.circle(surface, LIGHT_BLUE, (self.x + 60, self.y - 10), 30)
