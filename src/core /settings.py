import pygame
pygame.init()

# Ekran ayarları
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animasyonlu Kuş")

# Renkler
DARK_BLUE = (10, 25, 47)
WHITE = (255, 255, 255)
LIGHT_BLUE = (200, 230, 255)
SHADOW_GRAY = (180, 200, 220)
SUN_YELLOW = (255, 223, 0)
MOUNTAIN_COLOR = (34, 45, 65)

# Martı renkleri
BIRD_COLORS = [
    (255, 255, 255),  # Beyaz
    (240, 240, 240),  # Açık gri
    (220, 220, 220),  # Gri
    (200, 200, 200),  # Koyu gri
    (230, 235, 240)   # Grimsi beyaz
]

clock = pygame.time.Clock()
