import pygame
from game_state import game_state


class Arrow(pygame.sprite.Sprite):
    # Class variable for the sound - load this once
    hit_sound = None
    
    def __init__(self, x, y, direction, speed=8):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player sprite sheets/Arrow.png").convert_alpha()  # Ok görseli
        self.rect = self.image.get_rect()
        self.rect.center = (x, y+15)
        self.speed = speed
        self.direction = direction  # 1: sağ, -1: sol
        self.damage = 25  # Okun vereceği hasar
        
        # Load the sound if it hasn't been loaded yet
        if Arrow.hit_sound is None:
            Arrow.hit_sound = pygame.mixer.Sound("sounds/arrow_hit.wav")  # Ses dosyasının adını değiştirin
    
    def update(self, collision_rects, enemies):
        # Okun hareketi
        self.rect.x += self.speed * self.direction
        
        # Duvarlarla çarpışma kontrolü
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                self.kill()  # Duvara çarparsa oku kaldır
                return
        
        # Düşmanlarla çarpışma kontrolü
        for enemy in enemies:
            if enemy.alive and self.rect.colliderect(enemy.hitbox):
                enemy.get_hit(self.damage)
                # Ses çal
                pygame.mixer.Channel(2).play(Arrow.hit_sound)  # 2 numaralı kanalı kullan (değiştirilebilir)
                Arrow.hit_sound.set_volume(0.5)  # 50% volume
                self.kill()  # Düşmana çarparsa oku kaldır
                return
    
    def draw(self, surface, camera_x, camera_y):
        screen_x = (self.rect.x - camera_x) * game_state.game_state.zoom_factor
        screen_y = (self.rect.y - camera_y) * game_state.game_state.zoom_factor
        scaled_image = pygame.transform.scale(self.image,
                                             (int(self.rect.width * game_state.game_state.zoom_factor),
                                              int(self.rect.height * game_state.game_state.zoom_factor)))
        if self.direction == -1:  # Sola giderken oku çevir
            scaled_image = pygame.transform.flip(scaled_image, True, False)
        surface.blit(scaled_image, (screen_x, screen_y))


class Samurai(pygame.sprite.Sprite):
    def __init__(self, walk_spritesheet, idle_spritesheet, jump_spritesheet, 
                 run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, 
                 elixir_spritesheet, hurt_spritesheet, death_spritesheet, shot_spritesheet, 
                 x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        # Mevcut __init__ içeriği
        self.speed = speed
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(60 / 12))
        self.update_counter = 0
        self.is_moving = False
        self.is_running = False
        self.is_jumping = False
        self.is_attacking = False
        self.is_hurt = False
        self.is_dead = False
        self.is_climbing = False
        self.climbing_finished = True
        self.climb_target_y = 0
        self.attack_finished = True
        self.hurt_finished = True
        self.death_finished = False
        self.jump_power = -12
        self.jump_cut_factor = 0.5
        self.y_velocity = 0
        self.gravity = 0.5
        self.max_fall_speed = 10
        self.on_ground = False
        self.sound_triggered = False
        self.last_hit_sound_time = 0
        self.hit_sound_cooldown = 100
        self.max_health = 100
        self.health = self.max_health
        self.potions_collected = 0
        self.attack_damage = 20
        self.enemies_defeated = 0
        self.power_up_effect_timer = 0
        self.invincibility_frames = 30
        self.invincibility_counter = 0
        self.jump_count = 0
        self.max_jumps = 2
        self.is_charging = False
        self.charge_time = 0
        self.charged_attack_damage = 40
        self.scaled_image_cache = {}
        self.is_collecting_potion = False
        self.potion_frame_index = 0
        self.potion_animation_speed = max(1, round(60 / 40))
        self.potion_update_counter = 0
        self.is_shooting = False
        self.shot_finished = True
        self.shot_cooldown = 0
        self.max_arrows = 10
        self.arrow_count = self.max_arrows
        self.last_jump_time = 0
        self.jump_cooldown = 500
        # Coyote Time için yeni değişkenler
        self.coyote_time = 150  # ms cinsinden coyote time süresi
        self.last_grounded_time = 0  # Son yerde olduğu zaman
        self.is_in_dialogue = False  # Yeni bayrak: Diyalog durumunda mı?

        # Mevcut animasyon yüklemeleri
        self.walk_frames = walk_spritesheet.get_animation_frames(128, 128, scale)
        self.idle_frames = idle_spritesheet.get_animation_frames(128, 128, scale)
        self.elixir_frames = elixir_spritesheet.get_animation_frames(128, 128, scale)
        self.jump_frames = jump_spritesheet.get_animation_frames(128, 128, scale)
        self.run_frames = run_spritesheet.get_animation_frames(128, 128, scale)
        self.attack1_frames = attack1_spritesheet.get_animation_frames(128, 128, scale)[:-1]
        self.attack2_frames = attack2_spritesheet.get_animation_frames(128, 128, scale)
        self.attack3_frames = attack3_spritesheet.get_animation_frames(128, 128, scale)
        self.hurt_frames = hurt_spritesheet.get_animation_frames(128, 128, scale)
        self.death_frames = death_spritesheet.get_animation_frames(128, 128, scale)
        self.shot_frames = shot_spritesheet.get_animation_frames(128, 128, scale)

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
        self.attack_hitbox = pygame.Rect(0, 0, 60, 40)
        self.grab_area = pygame.Rect(0, 0, self.hitbox.width * 1.2, 20)
        self.update_grab_area()

    def check_on_ground(self, collision_rects):
        """Zeminde olup olmadığını kontrol eder ve coyote time'ı günceller"""
        self.update_ground_check()
        self.on_ground = False
        for rect in collision_rects:
            if self.ground_check.colliderect(rect):
                self.on_ground = True
                self.last_grounded_time = pygame.time.get_ticks()
                if self.y_velocity > 0:
                    self.y_velocity = 0
                if self.is_jumping and not self.is_attacking:
                    self.is_jumping = False
                break

    def jump(self):
        """Zıplama işlemini başlatır (Coyote time ile)"""
        if self.is_hurt or self.is_dead or self.is_in_dialogue:
            print(f"Zıplama engellendi: is_hurt={self.is_hurt}, is_dead={self.is_dead}")
            return
        current_time = pygame.time.get_ticks()
        # Coyote time kontrolü: Zeminde veya coyote time içindeyse zıplayabilir
        if not self.on_ground and (current_time - self.last_grounded_time > self.coyote_time):
            print("Zıplama engellendi: Coyote time süresi doldu")
            return
        if self.is_attacking:
            return
        self.is_jumping = True
        self.y_velocity = self.jump_power
        self.frame_index = 0
        self.update_counter = 0
        self.last_jump_time = current_time
        print("Zıplama başladı!")

    def update_grab_area(self):
        """Tutma alanını güncelle (karakterin üst kısmında bir alan)"""
        self.grab_area.midbottom = (self.hitbox.centerx, self.hitbox.top - 5)

    def check_wall_grab(self, collision_rects):
        """Duvarı tutup tırmanma kontrolü"""
        if self.is_climbing or self.is_hurt or self.is_dead or self.on_ground:
            return None

        self.update_grab_area()
        for rect in collision_rects:
            if self.grab_area.colliderect(rect):
                # Duvarın üst kenarını bul
                wall_top = rect.top
                # Duvarın hangi tarafında olduğumuzu kontrol et
                if self.flip:  # Sol tarafa bakıyor
                    if self.hitbox.left <= rect.right and self.hitbox.right > rect.right:
                        return wall_top, rect
                else:  # Sağ tarafa bakıyor
                    if self.hitbox.right >= rect.left and self.hitbox.left < rect.left:
                        return wall_top, rect
        return None

    def start_climbing(self, wall_top, wall_rect):
        """Tırmanmayı başlat"""
        self.is_climbing = True
        self.climbing_finished = False
        self.frame_index = 0
        self.update_counter = 0
        self.y_velocity = 0  # Yerçekimini geçici olarak sıfırla
        self.climb_target_y = wall_top - self.rect.height  # Hedef yükseklik
        # Karakteri duvara hizala
        if self.flip:
            self.rect.right = wall_rect.right
        else:
            self.rect.left = wall_rect.left
        self.update_hitbox()

    def update_climbing(self):
        """Tırmanma sürecini güncelle"""
        if not self.is_climbing:
            return

        # Animasyon oynarken karakteri yavaşça yukarı taşı
        climb_speed = (self.climb_target_y - self.rect.bottom) / len(self.pullup_frames)
        self.rect.y += climb_speed
        self.update_hitbox()

    def update_animation(self, arrow_group=None):
        self.update_counter += 1
        current_speed = self.animation_speed + 3 if not (self.is_moving or self.is_attacking or self.is_jumping or self.is_hurt or self.is_dead or self.is_shooting or self.is_climbing) else self.animation_speed

        # Hasar animasyonu en yüksek önceliğe sahip
        if self.is_hurt:
            frames = self.hurt_frames
            if self.update_counter >= current_speed:
                self.update_counter = 0
                if self.frame_index >= len(frames):
                    self.is_hurt = False
                    self.hurt_finished = True
                    self.frame_index = 0
                else:
                    self.image = frames[self.frame_index]
                    self.frame_index += 1
            return

        # Ölüm animasyonu ikinci öncelik
        if self.is_dead:
            frames = self.death_frames
            if self.update_counter >= current_speed:
                self.update_counter = 0
                if self.frame_index >= len(frames) - 1:
                    self.frame_index = len(frames) - 1
                    self.death_finished = True
                else:
                    self.image = frames[self.frame_index]
                    self.frame_index += 1
            return

        # Diğer animasyonlar sadece hasar alınmadığında oynar
        if self.update_counter < current_speed:
            return

        self.update_counter = 0

        
         # İksir toplama animasyonu (hareket durumlarından bağımsız, yüksek öncelik)
        if self.is_collecting_potion:
            self.potion_update_counter += 1
            if self.potion_update_counter >= self.potion_animation_speed:
                self.potion_update_counter = 0
                self.potion_frame_index += 1
                if self.potion_frame_index >= len(self.elixir_frames):
                    self.is_collecting_potion = False
                    self.potion_frame_index = 0
                    self.frame_index = 0
                else:
                    self.image = self.elixir_frames[self.potion_frame_index]
                    self.frame_index = self.potion_frame_index
            return

        # Tırmanma animasyonu
        if self.is_climbing:
            frames = self.pullup_frames
            if self.frame_index >= len(frames):
                self.is_climbing = False
                self.climbing_finished = True
                self.frame_index = 0
                self.rect.bottom = self.climb_target_y
                self.update_hitbox()
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        # Ok atma animasyonu
        elif self.is_shooting:
            frames = self.shot_frames
            if self.frame_index >= len(frames):
                self.is_shooting = False
                self.shot_finished = True
                self.frame_index = 0
                if arrow_group is not None:
                    direction = 1 if not self.flip else -1
                    arrow_x = self.rect.centerx + (40 * direction)
                    arrow_y = self.rect.centery - 10
                    new_arrow = Arrow(arrow_x, arrow_y, direction)
                    arrow_group.add(new_arrow)
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        # Saldırı animasyonu
        elif self.is_attacking:
            frames = self.current_attack_frames
            if self.frame_index >= len(frames):
                self.is_attacking = False
                self.attack_finished = True
                self.frame_index = 0
                self.sound_triggered = False
            else:
                self.image = frames[self.frame_index]
                self.frame_index += 1
        # Zıplama animasyonu
        elif self.is_jumping:
            frames = self.jump_frames
            if self.frame_index < len(frames) - 1:
                self.frame_index += 1
                self.image = frames[self.frame_index]
        # Koşma animasyonu
        elif self.is_running:
            frames = self.run_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        # Yürüme animasyonu
        elif self.is_moving:
            frames = self.walk_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
        # Boşta animasyonu
        else:
            frames = self.idle_frames if not self.is_collecting_potion else self.elixir_frames
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]


    def update(self, collision_rects, spike_rects, enemies, arrow_group, dt):
        if self.is_dead and self.death_finished:
            return
        if self.invincibility_counter > 0:
            self.invincibility_counter -= 1

        if self.is_in_dialogue:  # Diyalog sırasında yalnızca animasyon güncelleniyor
            self.update_animation()

        # Tırmanma güncellemesi
        if self.is_climbing:
            self.update_climbing()
        else:
            self.check_on_ground(collision_rects)
            for spike_rect in spike_rects:
                if self.hitbox.colliderect(spike_rect) and self.invincibility_counter <= 0:
                    self.get_hit(10)
            self.check_hit_enemies(enemies)
            self.y_velocity += self.gravity * dt * 60
            if self.y_velocity > self.max_fall_speed:
                self.y_velocity = self.max_fall_speed
            self.handle_collisions(0, self.y_velocity, collision_rects)

        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        self.update_animation(arrow_group)
        if self.is_charging:
            self.charge_time += 1

    def collect_potion(self):
        self.is_collecting_potion = True
        self.potion_frame_index = 0
        self.potion_update_counter = 0
        self.potions_collected += 1
        self.health = min(self.health + 50, self.max_health)
        print(f"İksir toplandı! +50 can, Toplam can: {self.health}/{self.max_health}")
        potion_sound = pygame.mixer.Sound("sounds/potion.wav")
        pygame.mixer.Channel(1).play(potion_sound)
        if self.potions_collected % 3 == 0:
            self.increase_max_health(20)

    def increase_max_health(self, amount=20):
        """Maksimum canı artırır ve mevcut canı günceller"""
        self.max_health += amount
        self.health = min(self.health + amount, self.max_health)
        self.power_up_effect_timer = 60  # 1 saniye parlama efekti
        print(f"Maksimum can artırıldı! Yeni maksimum can: {self.max_health}")

    def increase_attack_damage(self, amount=5):
        """Saldırı hasarını artırır"""
        self.attack_damage += amount
        self.power_up_effect_timer = 60  # 1 saniye efekt
        print(f"Saldırı hasarı artırıldı! Yeni hasar: {self.attack_damage}")

    def shoot(self, arrow_group):
        # Hasar alınıyorsa veya ölü ise ok atamaz
        if self.is_hurt or self.is_dead or self.is_in_dialogue:
            print(f"Ok atılamadı: is_hurt={self.is_hurt}, is_dead={self.is_dead}")
            return
        if self.is_shooting or self.shot_cooldown > 0 or self.arrow_count <= 0:
            print(f"Ok atılamadı: is_shooting={self.is_shooting}, shot_cooldown={self.shot_cooldown}, arrow_count={self.arrow_count}")
            return
        if self.is_running or self.is_jumping or self.is_moving or self.is_attacking:
            print("Ok atılamadı: Karakter koşuyor, zıplıyor, hareket ediyor veya saldırıyor!")
            return
        print("Ok atma animasyonu başladı!")
        self.is_shooting = True
        self.shot_finished = False
        self.frame_index = 0
        self.update_counter = 0
        self.shot_cooldown = 30
        self.arrow_count -= 1

    def attack(self, attack_type):
        # Hasar alınıyorsa veya ölü ise saldıramaz
        if self.is_hurt or self.is_dead or self.is_in_dialogue:
            print(f"Saldırı engellendi: is_hurt={self.is_hurt}, is_dead={self.is_dead}")
            return
        if self.is_attacking:
            print("Saldırı engellendi: is_attacking =", self.is_attacking)
            return
        print("Saldırı başladı, attack_type:", attack_type)
        self.is_attacking = True
        self.attack_finished = False
        self.frame_index = 0
        self.update_counter = 0
        self.sound_triggered = False
        if attack_type == 1:
            self.current_attack_frames = self.attack1_frames
    
        elif attack_type == 2:
            self.current_attack_frames = self.attack2_frames

        else:
            self.current_attack_frames = self.attack3_frames


    def release_jump(self):
        """Zıplama tuşu bırakıldığında hızı azaltır (jump cut)"""
        if self.is_jumping and self.y_velocity < 0:  # Sadece yukarı hareket ederken
            self.y_velocity *= self.jump_cut_factor  # Hızı azalt (ör. %50)
            print(f"Zıplama tuşu bırakıldı, y_velocity={self.y_velocity}")


    def check_hit_enemies(self, enemies):
        """Düşman yenildiğinde hasar artışı"""
        current_time = pygame.time.get_ticks()
        if self.is_attacking and not self.attack_finished:
            if self.frame_index == len(self.current_attack_frames) // 2:
                self.update_attack_hitbox()
                for enemy in enemies:
                    if enemy.alive and self.attack_hitbox.colliderect(enemy.hitbox):
                        enemy.get_hit(self.attack_damage)
                        if not enemy.alive:  # Düşman öldüyse
                            self.enemies_defeated += 1
                            if self.enemies_defeated % 5 == 0:  # Her 5 düşmanda hasar artar
                                self.increase_attack_damage(5)
                        if not self.sound_triggered and current_time - self.last_hit_sound_time > self.hit_sound_cooldown:
                            if not game_state.hit_channel.get_busy():
                                game_state.hit_channel.play(game_state.hit_sound)
                                self.last_hit_sound_time = current_time
                                self.sound_triggered = True
                        return True
        return False
    

    def reset(self):
        self.health = self.max_health
        self.is_dead = False
        self.death_finished = False
        self.is_hurt = False
        self.hurt_finished = True
        self.is_attacking = False
        self.attack_finished = True
        self.is_jumping = False
        self.is_moving = False
        self.is_running = False
        self.y_velocity = 0
        self.update_hitbox()
        self.invincibility_counter = 0
        self.frame_index = 0
        self.hit_sound_playing = False  # Sesin çalıp çalmadığını takip et

    # Update the get_hit method:
    def get_hit(self, damage=10):
        """Hasar alma mantığı"""
        if self.invincibility_counter <= 0 and not self.is_dead:
            self.health -= damage
            self.is_hurt = True
            self.hurt_finished = False
            self.frame_index = 0
            self.update_counter = 0
            self.invincibility_counter = self.invincibility_frames
            print(f"Oyuncu hasar aldı! Kalan can: {self.health}")
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                print("Oyuncu öldü!")
    
    def update_ground_check(self):
        self.ground_check.midbottom = (self.hitbox.midbottom[0], self.hitbox.midbottom[1] + 1)
        
    def update_hitbox(self):
        self.hitbox.midbottom = self.rect.midbottom
        self.update_ground_check()
        
                
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
                        if self.is_jumping and not self.is_attacking:
                            self.is_jumping = False
                    elif dy < 0:
                        self.hitbox.top = rect.bottom
                        self.y_velocity = 0
            self.rect.midbottom = self.hitbox.midbottom

                

    # Add a method to update the attack hitbox:
    def update_attack_hitbox(self):
        if self.flip:  # Character is facing left
            self.attack_hitbox.midright = self.hitbox.midleft
        else:  # Character is facing right
            self.attack_hitbox.midleft = self.hitbox.midright

   

    # Update the move method to prevent movement when hurt or dead:
    def move(self, moving_left, moving_right, running, collision_rects):
        if self.is_hurt or self.is_dead or self.is_collecting_potion or self.is_in_dialogue:
            return
            
        dx = 0
        self.is_moving = False
        self.is_running = False

        move_speed = self.speed * 1.5 if running else self.speed

        if moving_left:
            dx = -move_speed
            self.flip = True
            self.is_moving = True
            if running:
                self.is_running = True
        if moving_right:
            dx = move_speed
            self.flip = False
            self.is_moving = True
            if running:
                self.is_running = True

        if self.is_attacking:
            dx = 0

        self.handle_collisions(dx, 0, collision_rects)


    # Add health bar drawing:
    def draw_health_bar(self, surface, camera_x, camera_y):
        """Sağlık çubuğunu çiz"""
        if self.is_dead:
            return
        bar_width = 40
        bar_height = 5
        bar_x = (self.rect.centerx - bar_width // 2 - camera_x) * game_state.zoom_factor
        bar_y = (self.rect.top - 10 - camera_y) * game_state.zoom_factor
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width * game_state.zoom_factor, bar_height * game_state.zoom_factor))
        health_width = (self.health / self.max_health) * bar_width * game_state.zoom_factor
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, health_width, bar_height * game_state.zoom_factor))
        pygame.draw.rect(surface, (0, 0, 0), (bar_x, bar_y, bar_width * game_state.zoom_factor, bar_height * game_state.zoom_factor), 1)

    # Update the draw method to include health bar and flashing when invincible:
    def draw(self, surface, camera_x, camera_y):
        if self.invincibility_counter > 0 and self.invincibility_counter % 4 < 2:
            self.draw_health_bar(surface, camera_x, camera_y)
            return

        screen_x = (self.rect.x - camera_x) * game_state.zoom_factor
        screen_y = (self.rect.y - camera_y) * game_state.zoom_factor
        scaled_width = int(self.rect.width * game_state.zoom_factor)
        scaled_height = int(self.rect.height * game_state.zoom_factor)

        cache_key = (id(self.image), game_state.zoom_factor, self.flip)
        if cache_key not in self.scaled_image_cache:
            scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
            self.scaled_image_cache[cache_key] = pygame.transform.flip(scaled_image, self.flip, False)

        # Draw the character first
        surface.blit(self.scaled_image_cache[cache_key], (screen_x, screen_y))
        
        # Then add power-up effect if active
        if self.power_up_effect_timer > 0:
            effect_surface = self.scaled_image_cache[cache_key].copy()
            effect_surface.fill((255, 255, 0, 100), special_flags=pygame.BLEND_RGBA_ADD)
            surface.blit(effect_surface, (screen_x, screen_y))
            self.power_up_effect_timer -= 1

        # Draw arrow count if available
        if hasattr(self, 'arrow_count'):
            arrow_text = game_state.font.render(f"Arrows: {self.arrow_count}", True, (255, 255, 255))
            surface.blit(arrow_text, (10, 90))

        self.draw_health_bar(surface, camera_x, camera_y)


