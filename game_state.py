# game_state.py
import pygame
from utils import Font
from soundmanager import sound_manager

class GameState:
    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 900
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
        self.health_potions = pygame.sprite.Group()
        self.font = Font(None, 28)
        self.font_big = Font(None, 48)
        self.clock = pygame.time.Clock()
        self.DEVRIYE = "devriye"
        self.TAKIP = "takip"
        self.SALDIRI = "saldiri"
        self.show_transition_prompt = False
        self.transition_prompt_alpha = 0
        self.transition_prompt_fade_speed = 15
        self.transition_prompt_scale = 1.0
        self.active_transition = None
        self.fade_alpha = 0
        self.is_fading = False
        self.fade_speed = 255 / 60
        self.fade_state = None
        self.target_map = None
        self.target_spawn = None
        self.story_progress = 0
        self.player = None  # Oyuncu nesnesi için bir yer tutucu
        self.map_characters = {
            "village": {
                "npcs": [
                    {"type": "Blacksmith", "x": 1200, "y": 1163, "scale": 1}
                ],
                "enemies": [
                    {"type": "AnimeKnight", "x": 1200, "y": 1163},
                    {"type": "AnimeKnight", "x": 1500, "y": 1163},
                    {"type": "AnimeKnight", "x": 1600, "y": 1163},
                    {"type": "AnimeKnight", "x": 1800, "y": 1163}
                ]
            },
            "frozen_cave": {
                "npcs": [{"type": "Trader", "x": 2300, "y": 832, "scale": 1}],
                "enemies": [
                    {"type": "NinjaMonk", "x": 800, "y": 1000, "scale": 1},
                    {"type": "NinjaMonk", "x": 1000, "y": 1000, "scale": 1},
                    {"type": "NinjaMonk", "x": 1200, "y": 1000, "scale": 1},
                    {"type": "NinjaMonk", "x": 1400, "y": 1000, "scale": 1},
                    {"type": "NinjaMonk", "x": 1600, "y": 1000, "scale": 1}
                ]
            },
            "cyberpunk_mahalle": {
                "npcs": [],
                "enemies": [
                    {"type": "NinjaMonk", "x": 900, "y": 1100, "scale": 1, "speed": 2, "range": 200},
                    {"type": "NinjaMonk", "x": 1100, "y": 1100, "scale": 1, "speed": 2, "range": 200},
                    {"type": "NinjaMonk", "x": 1300, "y": 1100, "scale": 1, "speed": 2, "range": 200}
                ]
            },
            "laboratuvar": {
                "npcs": [{"type": "Doctor", "x": 1900, "y": 352, "scale": 1}],
                "enemies": [
                    {"type": "NinjaMonk", "x": 1000, "y": 1200, "scale": 1, "speed": 2, "range": 200},
                    {"type": "NinjaMonk", "x": 1200, "y": 1200, "scale": 1, "speed": 2, "range": 200}
                ]
            },
            "castle": {
                "npcs": [],
                "enemies": [
                    {"type": "KaraSamurai", "x": 2000, "y": 1000, "scale": 1.5}
                ]
            }
        }

game_state = GameState()
