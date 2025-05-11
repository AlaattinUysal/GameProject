# settings.py (boşaltılır, sadece pygame başlatma kalabilir)
import pygame
pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Samurai's path")
clock = pygame.time.Clock()