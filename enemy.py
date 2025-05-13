import pygame
from game_state import game_state
dt = game_state.clock.tick(game_state.fps)
from soundmanager import sound_manager
# NinjaMonk sınıfı - Devriye gezen ve saldıran düşman

class NinjaMonk(pygame.sprite.Sprite):
    def __init__(self, idle_spritesheet, walk_spritesheet, attack_spritesheet, 
                 hurt_spritesheet, death_spritesheet, x, y, scale, speed, patrol_distance):
        pygame.sprite.Sprite.__init__(self)
        # Mevcut özellikler
        self.speed = speed
        self.initial_position = (x, y)
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(60 / 12))
        self.update_counter = 0
        self.is_moving = False
        self.is_attacking = False
        self.is_hurt = False
        self.is_dead = False
        self.attack_finished = True
        self.hurt_finished = True
        self.death_finished = False
        self.remove_timer = 0
        self.should_remove = False
        self.has_fallen = False
        self.max_health = 80
        self.health = self.max_health
        self.invincibility_frames = 15
        self.invincibility_counter = 0
        self.attack_damage = 15
        self.y_velocity = 0
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.on_ground = False
        self.alive = True
        self.patrol_distance = patrol_distance
        self.start_x = x
        self.direction = 1
        self.patrol_counter = 0
        self.detection_range = 200
        self.attack_range = 50
        self.attack_cooldown = 60
        self.attack_timer = 0

        # Yeni eklenen özellikler (ikinci kodun AI'sından)
        self.devriye_noktasi_1 = (x - patrol_distance, y)  # İlk devriye noktası
        self.devriye_noktasi_2 = (x + patrol_distance, y)  # İkinci devriye noktası
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1  # Hedef başlangıç noktası
        self.jump_power = -10  # Zıplama gücü
        self.son_ziplama_zamani = 0  # Son zıplama zamanı
        self.ziplama_bekleme_suresi = 500  # Zıplama bekleme süresi (ms)

        # Animasyonlar
        self.idle_frames = idle_spritesheet.get_animation_frames(96, 96, scale)
        self.walk_frames = walk_spritesheet.get_animation_frames(96, 96, scale)
        self.attack_frames = attack_spritesheet.get_animation_frames(96, 96, scale)
        self.hurt_frames = hurt_spritesheet.get_animation_frames(96, 96, scale)
        self.death_frames = death_spritesheet.get_animation_frames(96, 96, scale)


        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        hitbox_width = self.rect.width * 0.3
        hitbox_height = self.rect.height * 0.6
        self.hitbox = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.hitbox.midbottom = self.rect.midbottom
        self.ground_check = pygame.Rect(0, 0, self.hitbox.width * 0.8, 5)
        self.update_ground_check()
        self.rect.bottom = y
        self.update_hitbox()
        self.attack_hitbox = pygame.Rect(0, 0, 40, 60)
        self.update_attack_hitbox()

    # Mevcut metodlar korunuyor, sadece devriye ve zıplama için yenileri ekleniyor
    def platform_kontrolu(self, collision_rects):
        """Platformun kenarında zıplama kontrolü"""
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_ziplama_zamani < self.ziplama_bekleme_suresi:
            return
        
        # Düşman hangi yöne bakıyorsa o yönde kenar kontrolü yap
        yon = -1 if self.flip else 1
        
        # Önde boşluk kontrolü - ayaklarının önünde platform var mı?
        kontrol_noktasi_x = self.hitbox.midbottom[0] + yon * (self.hitbox.width // 2 + 5)
        kontrol_noktasi_y = self.hitbox.bottom + 5
        
        # Platform üzerinde mi?
        on_platform = False
        for rect in collision_rects:
            if rect.collidepoint(self.hitbox.midbottom[0], self.hitbox.bottom + 1):
                on_platform = True
                break
                
        if not on_platform:
            return  # Platform üzerinde değilse zıplama kontrolü yapma
            
        # Önümüzde platform var mı?
        platform_ahead = False
        for rect in collision_rects:
            if rect.collidepoint(kontrol_noktasi_x, kontrol_noktasi_y):
                platform_ahead = True
                break
                
        # Platformun kenarındaysa ve önde platform yoksa zıpla
        if on_platform and not platform_ahead:
            print(f"Düşman platformun kenarında, zıplıyor! Konum: ({self.rect.centerx}, {self.rect.bottom})")
            self.y_velocity = self.jump_power
            self.son_ziplama_zamani = simdiki_zaman

    def devriye_et(self, collision_rects):
        """İkinci kodun devriye mantığı"""
        if self.is_hurt or self.is_dead or self.is_attacking:
            return

        dx = self.hedef_x - self.rect.centerx   
        mesafe = abs(dx)
        
        if mesafe > self.speed:
            dx_normalized = (dx / mesafe) * self.speed * 0.5  # Daha yavaş devriye hızı
            self.handle_collisions(dx_normalized, 0, collision_rects)
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                        print(f"Engel sağda, zıplama kontrolü: {self.rect.centerx}")
                        self.platform_kontrolu(collision_rects)
                    elif dx < 0:
                        self.hitbox.left = rect.right
                        print(f"Engel solda, zıplama kontrolü: {self.rect.centerx}")
                        self.platform_kontrolu(collision_rects)
            self.flip = dx < 0
            self.is_moving = True
        else:
            # Hedef noktaya ulaşıldığında diğer noktaya geç
            if (self.hedef_x, self.hedef_y) == self.devriye_noktasi_1:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_2
            else:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_1
            self.is_moving = False

        self.rect.midbottom = self.hitbox.midbottom

    def update(self, player, collision_rects):
        if self.invincibility_counter > 0:
            self.invincibility_counter -= 1

        self.check_on_ground(collision_rects)
        self.update_hitbox()

        # Yerçekimi
        self.y_velocity += self.gravity * dt * 60
        if self.y_velocity > self.max_fall_speed:
            self.y_velocity = self.max_fall_speed
        self.handle_collisions(0, self.y_velocity, collision_rects)

        if not self.is_dead:
            player_detected = self.detect_player(player)
            if not player_detected and not self.is_attacking and not self.is_hurt:
                self.devriye_et(collision_rects)  # Yeni devriye mantığı
            if self.check_hit_player(player):
                pass

        self.update_animation()

        # Ölüm ve kaldırma mantığı
        if self.is_dead:
            if self.on_ground and not self.has_fallen:
                self.has_fallen = True
            if self.has_fallen and self.death_finished:
                self.remove_timer += 1
                if self.remove_timer >= 120:
                    self.should_remove = True

    # Mevcut `update_animation` metodunda zıplama animasyonu için kontrol ekleme
    def update_animation(self):
        self.update_counter += 1
        current_speed = self.animation_speed + 3 if not (self.is_moving or self.is_attacking or self.is_hurt or self.is_dead) else self.animation_speed
        
        if self.update_counter < current_speed:
            return
            
        self.update_counter = 0
        
        if self.is_dead:
            frames = self.death_frames
            if self.frame_index >= len(frames) - 1:
                self.frame_index = len(frames) - 1
                self.death_finished = True
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.is_hurt:
            frames = self.hurt_frames
            if self.frame_index >= len(frames):
                self.is_hurt = False
                self.hurt_finished = True
                self.frame_index = 0
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.is_attacking:
            frames = self.attack_frames
            if self.frame_index >= len(frames):
                self.is_attacking = False
                self.attack_finished = True
                self.frame_index = 0
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        elif self.y_velocity < 0:  # Zıplama animasyonu
            frames = self.jump_frames  # jump_frames kullan
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        elif self.is_moving:
            frames = self.walk_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        else:
            frames = self.idle_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
    # Diğer metodlar (get_hit, detect_player, vb.) aynı kalabilir

    def update_ground_check(self):
        self.ground_check.midbottom = (self.hitbox.midbottom[0], self.hitbox.midbottom[1] + 1)
        
    def update_hitbox(self):
        self.hitbox.midbottom = self.rect.midbottom
        self.update_ground_check()
        
    def check_on_ground(self, collision_rects):
        self.update_ground_check()
        self.on_ground = False
        for rect in collision_rects:
            if self.ground_check.colliderect(rect):
                self.on_ground = True
                if self.y_velocity > 0:
                    self.y_velocity = 0
                break
                
    def handle_collisions(self, dx, dy, collision_rects):
        # Horizontal movement
        if dx != 0:
            self.hitbox.x += dx
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                    elif dx < 0:
                        self.hitbox.left = rect.right
            self.rect.midbottom = self.hitbox.midbottom
            
        # Vertical movement
        if dy != 0:
            self.hitbox.y += dy
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dy > 0:
                        self.hitbox.bottom = rect.top
                        self.on_ground = True
                        self.y_velocity = 0
                    elif dy < 0:
                        self.hitbox.top = rect.bottom
                        self.y_velocity = 0
            self.rect.midbottom = self.hitbox.midbottom
            
    def patrol(self, collision_rects):
        # Patrol back and forth within set distance
        self.patrol_counter += 1
        
        # Change direction if reached patrol distance
        if self.patrol_counter > self.patrol_distance:
            self.direction *= -1
            self.patrol_counter = 0
            self.flip = not self.flip
        
        # Move in current direction
        dx = self.direction * self.speed * 0.5  # Slower than chase speed
        self.is_moving = True
        self.handle_collisions(dx, 0, collision_rects)
        
    def update_attack_hitbox(self):
        if self.flip:  # Character is facing left
            self.attack_hitbox.midright = self.hitbox.midleft
        else:  # Character is facing right
            self.attack_hitbox.midleft = self.hitbox.midright
            
    def attack(self):
        if self.is_attacking or self.is_hurt or self.is_dead:
            return
        
        self.is_attacking = True
        self.attack_finished = False
        self.frame_index = 0
        self.update_counter = 0

    # Update the get_hit method:
    def get_hit(self, damage):
        if self.invincibility_counter <= 0 and not self.is_dead:
            self.health -= damage
            self.is_hurt = True
            self.hurt_finished = False
            self.frame_index = 0
            self.update_counter = 0
            self.invincibility_counter = self.invincibility_frames
            
            # Check if dead
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                self.alive = False
                self.frame_index = 0
                self.update_counter = 0
                print("Enemy died!")

    # Update the detect_player method:
    def detect_player(self, player):
        if self.is_hurt or self.is_dead:
            return False
            
        # Update attack cooldown
        if self.attack_timer > 0:
            self.attack_timer -= 1
            
        # Detect player
        player_distance_x = abs(player.rect.centerx - self.rect.centerx)
        player_distance_y = abs(player.rect.centery - self.rect.centery)
        
        # If player in detection range
        if player_distance_x < self.detection_range and player_distance_y < 50 and not player.is_dead:
            # Turn toward player
            if player.rect.centerx < self.rect.centerx:
                self.flip = True
                self.direction = -1
            else:
                self.flip = False
                self.direction = 1
            
            # If player in attack range and cooldown finished, attack
            if player_distance_x < self.attack_range and self.attack_timer == 0:
                self.attack()
                self.attack_timer = self.attack_cooldown
                return True
                
            # If player detected but not in attack range, follow
            if not self.is_attacking:
                self.patrol_counter = 0  # Reset patrol
                dx = self.direction * self.speed
                self.is_moving = True
                return True
        
        return False
        

    

    # Update the check_hit_player method:
    def check_hit_player(self, player):
        if self.is_attacking and not self.attack_finished and not player.is_dead:
            # Only check for hits in the middle of attack animation
            if self.frame_index == len(self.attack_frames) // 2:
                self.update_attack_hitbox()
                if self.attack_hitbox.colliderect(player.hitbox):
                    player.get_hit(self.attack_damage)
                    # Play hit sound when enemy successfully hits player
                    sound_manager.play_sound("hit")
                    return True
        return False

    
    # Add health bar drawing:
    def draw_health_bar(self, surface, camera_x, camera_y):
        if self.is_dead:
            return
            
        bar_width = 30
        bar_height = 4
        
        # Position above character's head
        bar_x = (self.rect.centerx - bar_width // 2 - camera_x) * game_state.zoom_factor
        bar_y = (self.rect.top - 10 - camera_y) * game_state.zoom_factor
        
        # Background (red)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width * game_state.zoom_factor, bar_height * game_state.zoom_factor))
        
        # Health (green)
        health_width = (self.health / self.max_health) * bar_width * game_state.zoom_factor
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, health_width, bar_height * game_state.zoom_factor))
        
        # Border
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width * game_state.zoom_factor, bar_height * game_state.zoom_factor), 1)


    def reset(self):
        self.health = self.max_health
        self.alive = True
        self.is_dead = False
        self.death_finished = False
        self.rect.center = self.initial_position  # You would need to store this when creating the enemy
        self.update_hitbox()
        # Reset any other enemy state variables


    # Update the draw method:
    def draw(self, surface, camera_x, camera_y):
        # Don't draw if invincible and should be flashing
        if self.invincibility_counter > 0 and self.invincibility_counter % 4 < 2:
            # Only draw health bar
            self.draw_health_bar(surface, camera_x, camera_y)
            return
            
        screen_x = (self.rect.x - camera_x) * game_state.zoom_factor
        screen_y = (self.rect.y - camera_y) * game_state.zoom_factor
        scaled_width = int(self.rect.width * game_state.zoom_factor)
        scaled_height = int(self.rect.height * game_state.zoom_factor)
        
        # Cache scaled images
        if not hasattr(self, 'scaled_image_cache'):
            self.scaled_image_cache = {}
        
        cache_key = (id(self.image), game_state.zoom_factor, self.flip)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = pygame.transform.flip(scaled_image, self.flip, False)
        
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
        
        # Draw health bar
        self.draw_health_bar(surface, camera_x, camera_y)
        
        debug = False
        if debug:
            # Draw hitbox
            hitbox_x = (self.hitbox.x - camera_x) * game_state.zoom_factor
            hitbox_y = (self.hitbox.y - camera_y) * game_state.zoom_factor
            hitbox_width = self.hitbox.width * game_state.zoom_factor
            hitbox_height = self.hitbox.height * game_state.zoom_factor
            pygame.draw.rect(surface, (255, 0, 0), (hitbox_x, hitbox_y, hitbox_width, hitbox_height), 2)
            
            # Draw ground check box
            ground_x = (self.ground_check.x - camera_x) * game_state.zoom_factor
            ground_y = (self.ground_check.y - camera_y) * game_state.zoom_factor
            ground_width = self.ground_check.width * game_state.zoom_factor
            ground_height = self.ground_check.height * game_state.zoom_factor
            pygame.draw.rect(surface, (0, 255, 0), (ground_x, ground_y, ground_width, ground_height), 2)
            
            # Draw attack hitbox
            if self.is_attacking:
                self.update_attack_hitbox()
                attack_x = (self.attack_hitbox.x - camera_x) * game_state.zoom_factor
                attack_y = (self.attack_hitbox.y - camera_y) * game_state.zoom_factor
                attack_width = self.attack_hitbox.width * game_state.zoom_factor
                attack_height = self.attack_hitbox.height * game_state.zoom_factor
                pygame.draw.rect(surface, (255, 165, 0), (attack_x, attack_y, attack_width, attack_height), 2)
