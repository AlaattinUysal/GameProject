# game_state.py
import pygame
from utils import Font
class GameState:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.zoom_factor = 1.5
        self.fps = 60
        self.game_over = False
        self.current_map = "village"
        self.camera_x = 0
        self.camera_y = 0
        self.show_message = False
        self.show2_message = False
        self.show3_message = False
        self.message_timer = 0
        self.message2_timer = 0
        self.message3_timer = 0
        self.message_duration = 5 * self.fps
        self.message_text = "The new feature is opened with the \"K\" button!"
        self.message2_text = "The new feature is opened with the \"L\" button!"
        self.message3_text = "The new feature is opened with the \"0\" button!"
        self.maps_data = {}
        self.transition_rects = {}
        self.tile_cache = {}
        self.parallax_factors_x = {}
        self.parallax_factors_y = {}
        self.front_layer_index = 17
        self.tmx_data = None
        self.map_width = 0
        self.map_height = 0
        self.collision_rects = []
        self.spike_rects = []
        self.health_potions = []
        self.font = Font(None, 24)
        self.font_big = Font(None, 36)
        self.clock = pygame.time.Clock()

game_state = GameState()