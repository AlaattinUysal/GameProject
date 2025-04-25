import pygame
import math
import random
from src.core.settings import WIDTH, BIRD_COLORS

class Bird:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        
        self.wing_position = 0
        self.wing_direction = 1
        
        self.flight_mode = "flap"
        self.flight_timer = 0
        
        self.wing_delay = random.randint(4, 8)
        self.flap_duration = random.randint(80, 140)
        self.glide_duration = random.randint(60, 120)
        self.vertical_drift = random.uniform(0.015, 0.04)
        self.vertical_amplitude = random.uniform(2, 4)
        self.horizontal_speed_factor = random.uniform(0.9, 1.1)
        
        self.color = BIRD_COLORS[pygame.time.get_ticks() % len(BIRD_COLORS)]
        self.size = pygame.math.Vector2(40, 12)
        self.flying_offset = 0
        
        self.wing_timer = random.randint(0, self.wing_delay)
        
    def move(self):
        adjusted_speed = self.speed * self.horizontal_speed_factor
        if self.flight_mode == "glide":
            adjusted_speed *= 1.05
        
        self.x += adjusted_speed
        if self.x > WIDTH + 50:
            self.x = -50
        
        self.flight_timer += 1
        
        if self.flight_mode == "flap" and self.flight_timer > self.flap_duration:
            self.flight_mode = "glide"
            self.flight_timer = 0
            self.wing_position = 0
            self.wing_direction = 0
            
        elif self.flight_mode == "glide" and self.flight_timer > self.glide_duration:
            self.flight_mode = "flap"
            self.flight_timer = 0
            self.wing_direction = 1
        
        if self.flight_mode == "flap":
            self.wing_timer += 1
            if self.wing_timer >= self.wing_delay:
                self.wing_timer = 0
                self.wing_position += self.wing_direction
                
                if self.wing_position >= 2:
                    self.wing_position = 2
                    self.wing_direction = -1
                elif self.wing_position <= 0:
                    self.wing_position = 0
                    self.wing_direction = 1
        
        if self.flight_mode == "flap":
            flap_lift = 0
            if self.wing_position == 0 and self.wing_direction == 1:
                flap_lift = -0.5
            
            flutter = math.sin(pygame.time.get_ticks() * 0.1) * 0.5
            self.flying_offset = math.sin(pygame.time.get_ticks() * self.vertical_drift) * 2 + flap_lift + flutter
        else:
            self.flying_offset = math.sin(pygame.time.get_ticks() * (self.vertical_drift * 0.5)) * self.vertical_amplitude

    def draw(self, surface):
        body_length = self.size.x
        body_height = self.size.y
        
        pygame.draw.ellipse(surface, self.color, 
                            (self.x, self.y + self.flying_offset, 
                             body_length, body_height))
        
        head_radius = body_height * 0.7
        head_x = self.x + body_length - head_radius
        head_y = self.y + body_height/2 + self.flying_offset - 1
        pygame.draw.circle(surface, self.color, 
                           (int(head_x), int(head_y)), 
                           int(head_radius))
        
        eye_x = head_x + head_radius/2
        eye_y = head_y - 1
        pygame.draw.circle(surface, (0, 0, 0), (int(eye_x), int(eye_y)), 2)
        
        beak_points = [
            (head_x + head_radius, head_y),
            (head_x + head_radius + 12, head_y + 1),
            (head_x + head_radius, head_y + 3)
        ]
        pygame.draw.polygon(surface, (255, 200, 0), beak_points)
        
        wing_x = self.x + body_length/3
        wing_y = self.y + body_height/2 + self.flying_offset
        
        wing_color = (160, 160, 160)
        secondary_color = (100, 100, 100)
        
        if self.flight_mode == "glide":
            left_wing_points = [
                (wing_x, wing_y),
                (wing_x - 40, wing_y - 8),
                (wing_x - 30, wing_y - 3)
            ]
            right_wing_points = [
                (wing_x + 5, wing_y),
                (wing_x + 40, wing_y - 8),
                (wing_x + 30, wing_y - 3)
            ]
        else:
            if self.wing_position == 0:
                left_wing_points = [
                    (wing_x, wing_y),
                    (wing_x - 35, wing_y - 25),
                    (wing_x - 25, wing_y - 5)
                ]
                right_wing_points = [
                    (wing_x + 5, wing_y),
                    (wing_x + 35, wing_y - 25),
                    (wing_x + 25, wing_y - 5)
                ]
            elif self.wing_position == 1:
                left_wing_points = [
                    (wing_x, wing_y),
                    (wing_x - 30, wing_y - 5),
                    (wing_x - 20, wing_y)
                ]
                right_wing_points = [
                    (wing_x + 5, wing_y),
                    (wing_x + 30, wing_y - 5),
                    (wing_x + 20, wing_y)
                ]
            else:
                left_wing_points = [
                    (wing_x, wing_y),
                    (wing_x - 30, wing_y + 15),
                    (wing_x - 15, wing_y + 5)
                ]
                right_wing_points = [
                    (wing_x + 5, wing_y),
                    (wing_x + 30, wing_y + 15),
                    (wing_x + 15, wing_y + 5)
                ]
        
        pygame.draw.polygon(surface, wing_color, left_wing_points)
        pygame.draw.polygon(surface, wing_color, right_wing_points)
        pygame.draw.line(surface, secondary_color, left_wing_points[0], left_wing_points[1], 2)
        pygame.draw.line(surface, secondary_color, right_wing_points[0], right_wing_points[1], 2)
        
        tail_width = body_height * 1.2
        tail_length = body_height * 1.5
        tail_points = [
            (self.x, self.y + body_height/2 + self.flying_offset),
            (self.x - tail_length, self.y + body_height/2 - tail_width/2 + self.flying_offset),
            (self.x - tail_length/2, self.y + body_height/2 + self.flying_offset),
            (self.x - tail_length, self.y + body_height/2 + tail_width/2 + self.flying_offset)
        ]
        pygame.draw.polygon(surface, self.color, tail_points)
        pygame.draw.lines(surface, (200, 200, 200), False, 
                          [tail_points[1], tail_points[2], tail_points[3]], 1)
        
        if self.flying_offset > 2:
            foot_y = self.y + body_height + 5 + self.flying_offset
            pygame.draw.line(surface, (255, 165, 0), 
                            (self.x + body_length/3, self.y + body_height + self.flying_offset),
                            (self.x + body_length/3 - 3, foot_y), 1)
            pygame.draw.line(surface, (255, 165, 0), 
                            (self.x + body_length/3 + 6, self.y + body_height + self.flying_offset),
                            (self.x + body_length/3 + 9, foot_y), 1)
