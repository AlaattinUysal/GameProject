import pygame
from src.core.settings import HEIGHT, DARK_BLUE, SUN_YELLOW, MOUNTAIN_COLOR

# Güneşin hareket etmesi için zamanla değişen y koordinatını hesaplamak
sun_pos_y = 80  # Başlangıç yüksekliği
sun_speed = 0.1  # Güneşin hareket hızı

def update_sun_position():
    global sun_pos_y, sun_speed
    sun_pos_y += sun_speed
    if sun_pos_y > HEIGHT - 40:
        sun_pos_y = HEIGHT - 40
        sun_speed = -0.1
    if sun_pos_y < 80:
        sun_pos_y = 80
        sun_speed = 0.1

def update_background(surface):
    if sun_pos_y > HEIGHT / 2:
        surface.fill((255, 130, 50))  # Gün batımı sarı-şafak rengi
    else:
        surface.fill(DARK_BLUE)  # Gece rengini değiştirme

def draw_background(surface):
    update_background(surface)
    pygame.draw.circle(surface, SUN_YELLOW, (700, int(sun_pos_y)), 40)
    pygame.draw.polygon(surface, MOUNTAIN_COLOR, [(0, HEIGHT), (200, 250), (400, HEIGHT)])
    pygame.draw.polygon(surface, MOUNTAIN_COLOR, [(300, HEIGHT), (500, 220), (700, HEIGHT)])
    pygame.draw.polygon(surface, MOUNTAIN_COLOR, [(600, HEIGHT), (750, 300), (900, HEIGHT)])
