# menu/main.py

import pygame
from menu.menu_logic import Menu
from menu.constants import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Way")

if __name__ == "__main__":
    menu = Menu(screen)
    menu.run()
