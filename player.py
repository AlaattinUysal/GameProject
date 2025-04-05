import pygame

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

clock = pygame.time.Clock()
FPS = 60

moving_left = False
moving_right = False
running = False
attacking = False

BG = (144, 201, 120)
GRAVITY = 0.8



def show_death_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("YOU ARE DEAD", True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

    global run  # Ana oyun döngüsünü bitir
    run = False


def draw_bg():
    screen.fill(BG)

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

    def get_animation_frames(self, frame_width, frame_height, scale):
        sheet_width, _ = self.sheet.get_size()
        frame_count = sheet_width // frame_width
        return [self.get_image(i, frame_width, frame_height, scale) for i in range(frame_count)]
    
dead_spritesheet = Spritesheet("Dead.png")  # Ölüm animasyonu için spritesheet
hurt_spritesheet = Spritesheet("Hurt.png")  # Yara alma animasyonu için spritesheet


class Samurai(pygame.sprite.Sprite):
    def __init__(self, walk_spritesheet, idle_spritesheet, idle2_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, run_attack_spritesheet, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.flip = False
        self.frame_index = 0
        self.animation_speed = max(1, round(FPS / 12))
        self.idle_animation_speed = self.animation_speed + 3  # Idle süresi biraz artırıldı
        self.update_counter = 0
        self.is_moving = False
        self.is_running = False
        self.is_jumping = False
        self.is_attacking = False
        self.attack_finished = True
        self.is_hurt = False
        self.hurt_timer = 0
        self.jump_power = -14
        self.y_velocity = 0
        self.ground_y = y
        self.dead_frames = dead_spritesheet.get_animation_frames(128, 128, scale)
        self.hurt_frames = hurt_spritesheet.get_animation_frames(128, 128, scale)
        self.is_dead = False  # Başlangıçta karakter ölü değil
        self.dead_timer = 0  # Ölüm animasyonu zamanlayıcısı
        # Animasyonlar

        self.walk_frames = walk_spritesheet.get_animation_frames(128, 128, scale)
        self.idle_frames = idle_spritesheet.get_animation_frames(128, 128, scale) + idle2_spritesheet.get_animation_frames(128, 128, scale)
        self.jump_frames = jump_spritesheet.get_animation_frames(128, 128, scale)
        self.run_frames = run_spritesheet.get_animation_frames(128, 128, scale)
        self.attack1_frames = attack1_spritesheet.get_animation_frames(128, 128, scale)
        self.attack2_frames = attack2_spritesheet.get_animation_frames(128, 128, scale)
        self.run_attack_frames = run_attack_spritesheet.get_animation_frames(128, 128, scale) if run_attack_spritesheet else []

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def hurt(self):
        if self.is_dead or self.is_attacking or self.is_jumping:
            return  # Hasar alırken veya atlarken zarar görme iptal edilir.
        self.is_hurt = True

    def move(self, moving_left, moving_right, running):
        if self.is_dead:
            return  # Ölü karakter hareket edemez.

        dx = 0
        self.is_moving = False
        self.is_running = False

        if running:
            move_speed = min(self.speed * 2, 10)  # Max hız 10 olsun.
        else:
            move_speed = self.speed


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
                
                
        self.rect.x = max(0, min(self.rect.x + dx, SCREEN_WIDTH - self.rect.width))

    def jump(self):
        if not self.is_jumping and not self.is_attacking:
            self.is_jumping = True
            self.y_velocity = self.jump_power
            self.frame_index = 0
            self.update_counter = 0

    def attack(self, attack_type):
        if self.is_attacking or self.is_jumping:
            return
        
        self.is_attacking = True
        self.attack_finished = False
        self.frame_index = 0
        self.update_counter = 0

        if self.is_running and self.run_attack_frames:
            self.current_attack_frames = self.run_attack_frames
        elif attack_type == 1:
            self.current_attack_frames = self.attack1_frames
        else:
            self.current_attack_frames = self.attack2_frames

    def apply_gravity(self):
        self.y_velocity += GRAVITY
        self.rect.y += self.y_velocity

        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.is_jumping = False

        if self.rect.y < 50:  # Karakter çok yukarı çıkmasın
            self.rect.y = 50
            self.y_velocity = 0


    def update_animation(self):
        self.update_counter += 1

        if self.is_dead:
            if self.update_counter >= self.animation_speed:
                self.update_counter = 0
                if self.frame_index < len(self.dead_frames) - 1:
                    self.frame_index += 1
                    self.image = self.dead_frames[self.frame_index]
                else:
                    self.dead_timer += 1  # Ölüm animasyonu tamamlandığında sayaç artar
                    if self.dead_timer > FPS:  # 1 saniye beklet
                        show_death_screen()
            return
        
        if self.is_hurt:
            if self.update_counter >= self.animation_speed:
                self.update_counter = 0
                if self.frame_index < len(self.hurt_frames) - 1:
                    self.frame_index += 1
                    self.image = self.hurt_frames[self.frame_index]
                else:
                    self.is_hurt = False  # Yara alma animasyonu bittiğinde normale dön
            return
            

        if self.is_attacking:
            if self.update_counter >= self.animation_speed:
                self.update_counter = 0
                self.frame_index += 1
                if self.frame_index >= len(self.current_attack_frames):
                    self.is_attacking = False
                    self.attack_finished = True
                    self.frame_index = 0
                else:
                    self.image = self.current_attack_frames[self.frame_index]
            

        if self.is_jumping:
            if self.update_counter >= self.animation_speed:
                self.update_counter = 0
                if self.frame_index < len(self.jump_frames) - 1:
                    self.frame_index += 1
                self.image = self.jump_frames[self.frame_index]

        elif self.is_running:
            if self.update_counter >= self.animation_speed:
                self.update_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.run_frames)
                self.image = self.run_frames[self.frame_index]

        elif self.is_moving:
            if self.update_counter >= self.animation_speed:
                self.update_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.frame_index]

        else:
            if self.update_counter >= self.idle_animation_speed:  # Idle süresi burada artırıldı
                self.update_counter = 0
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.frame_index]

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.frame_index = 0
            self.update_counter = 0
            self.dead_timer = 0


# Spritesheet dosyalarını yükle
walk_spritesheet = Spritesheet("Walk.png")
idle_spritesheet = Spritesheet("Idle.png")
idle2_spritesheet = Spritesheet("Idle_2.png")
jump_spritesheet = Spritesheet("Jump.png")
run_spritesheet = Spritesheet("Run.png")
attack1_spritesheet = Spritesheet("Attack_1.png")
attack2_spritesheet = Spritesheet("Attack_2.png")
run_attack_spritesheet = Spritesheet("Run+Attack.png")


player = Samurai(walk_spritesheet, idle_spritesheet, idle2_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, run_attack_spritesheet, 200, 200, 2, 5)

run = True
while run:
    clock.tick(FPS)
    draw_bg()

    player.apply_gravity()
    player.move(moving_left, moving_right, running)
    player.update_animation()
    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump()
            if event.key == pygame.K_j:
                player.attack(1)
            if event.key == pygame.K_k:
                player.attack(2)
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running = True
            if event.key == pygame.K_x:
                player.die()
            if event.key == pygame.K_z:
                player.hurt()

            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                running = False

    pygame.display.update()

pygame.quit()
