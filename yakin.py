import pygame
import random
import math
from dusman import Dusman
from utils import Spritesheet
import game_state

class Yakin(Dusman):
    def __init__(self, x, y, hiz, can, guc, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet):
        super().__init__(x, y, hiz, can, guc, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet)
        
        # Animasyonları yükle
        animasyonlar = {
            "Walk": 7,  # Örnek kare sayısı, sprite dosyasına göre ayarlayın
            "Idle": 6,
            "Jump": 12,
            "Run": 8,
            "Attack_1": 4,
            "Attack_2": 7,
            "Attack_3": 3,
            "Hurt": 2,
            "Dead": 3
        }
        self.animasyonlari_yukle(animasyonlar)
        
        # Canavar sınıfından gerekli özellikleri al
        self.attack_damage = 15
        self.detection_range = 200
        self.attack_range = 50
        self.attack_cooldown = 60
        self.attack_timer = 0
        self.jump_power = -10
        self.son_ziplama_zamani = 0
        self.ziplama_bekleme_suresi = 500
        self.baslangic_x = x
        self.baslangic_y = y
        self.tespit_mesafesi = 300
        self.saldiri_mesafesi = 80
        self.menzilli_saldiri_mesafesi = 300
        self.durum = "devriye"
        self.devriye_noktasi_1 = (x - 150, y)
        self.devriye_noktasi_2 = (x + 150, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.son_konum_degisimi = pygame.time.get_ticks()
        self.son_saldiri_zamani = 0
        self.saldiri_bekleme_suresi = 1000
        self.jump_power = -10
        self.son_ziplama_zamani = 0
        self.ziplama_bekleme_suresi = 500
        self.onceki_durum = "devriye"
        self.alerted = False
        self.view_angle = 90
        self.attack_count = 2
        self.attacks = ["Attack_1", "Attack_2", "Attack_3"]
        self.available_attacks = self.attacks[:self.attack_count]

        walk_spritesheet = Spritesheet("ENEMIES/anime/Knight/Walk_AnimeKnight.png")
        idle_spritesheet = Spritesheet("ENEMIES/anime/Knight/Idle_AnimeKnight.png")
        jump_spritesheet = Spritesheet("ENEMIES/anime/Knight/Jump_AnimeKnight.png")
        run_spritesheet = Spritesheet("ENEMIES/anime/Knight/Run_AnimeKnight.png")
        attack1_spritesheet = Spritesheet("ENEMIES/anime/Knight/Attack_1_AnimeKnight.png")
        attack2_spritesheet = Spritesheet("ENEMIES/anime/Knight/Attack_2_AnimeKnight.png")
        attack3_spritesheet = Spritesheet("ENEMIES/anime/Knight/Attack_3_AnimeKnight.png")
        hurt_spritesheet = Spritesheet("ENEMIES/anime/Knight/Hurt_AnimeKnight.png")
        death_spritesheet = Spritesheet("ENEMIES/anime/Knight/Dead_AnimeKnight.png")
        
    
    def is_facing_away(self, hedef):
        if hasattr(hedef, 'rect'):
            target_x = hedef.rect.centerx
        else:
            target_x = hedef.x
        return (self.sola_donuk and target_x > self.x) or (not self.sola_donuk and target_x < self.x)
    
    def can_see_player(self, hedef):
        # Calculate distance using the hedef object directly
        mesafe = self.mesafe_hesapla(hedef)
        
        # Determine target coordinates for angle calculation
        if hasattr(hedef, 'rect'):
            target_x = hedef.rect.centerx
            target_y = hedef.rect.centery
        else:
            target_x = hedef.x
            target_y = hedef.y

        if mesafe > self.tespit_mesafesi:
            return False
        
        angle_to_player = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        facing_angle = 180 if self.sola_donuk else 0
        angle_diff = abs((angle_to_player - facing_angle + 180) % 360 - 180)
        return angle_diff <= self.view_angle / 2
    
    # In yakin.py
    def platform_kontrolu(self, collision_rects, target_x, target_y):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_ziplama_zamani < self.ziplama_bekleme_suresi or not self.on_ground:
            return
        
        yon = 1 if target_x > self.x else -1
        kontrol_rect = pygame.Rect(0, 0, 20, self.hitbox.height + 10)
        kontrol_rect.centerx = self.hitbox.centerx + yon * (self.hitbox.width // 2 + 15)
        kontrol_rect.bottom = self.hitbox.bottom

        should_jump = False
        
        for rect in collision_rects:
            if kontrol_rect.colliderect(rect):
                should_jump = True
                break
            
            zemin_kontrol_rect = pygame.Rect(0, 0, 10, 10)
            zemin_kontrol_rect.centerx = self.hitbox.centerx + yon * (self.hitbox.width // 2 + 10)
            zemin_kontrol_rect.top = self.hitbox.bottom
            if not any(zemin_kontrol_rect.colliderect(r) for r in collision_rects):
                should_jump = True
                break
        
        if should_jump:
            self.velocity_y = self.jump_power
            self.animasyon_degistir("Jump")
            self.son_ziplama_zamani = simdiki_zaman

    def devriye_et(self, collision_rects):
        dx = self.hedef_x - self.x
        mesafe = abs(dx)
        
        def handle_horizontal_collision(dx):
            self.rect.x += dx
            self.update_hitbox()
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                        self.rect.right = self.hitbox.right + (self.rect.width - self.hitbox.width) // 2
                    elif dx < 0:
                        self.hitbox.left = rect.right
                        self.rect.left = self.hitbox.left - (self.rect.width - self.hitbox.width) // 2
                    return 0
            return dx
        
        self.platform_kontrolu(collision_rects, self.hedef_x, self.hedef_y)
        
        if mesafe > self.hiz:
            move_dx = (dx / mesafe) * self.hiz
            move_dx = handle_horizontal_collision(move_dx)
            self.sola_donuk = dx < 0
            if self.on_ground and not self.vuruyor and not self.vuruldu and self.mevcut_animasyon != "Jump":
                self.animasyon_degistir("Walk")
        else:
            if (self.hedef_x, self.hedef_y) == self.devriye_noktasi_1:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_2
            else:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_1
            if not self.vuruyor and not self.vuruldu and self.on_ground and self.mevcut_animasyon != "Jump":
                self.animasyon_degistir("Idle")

        self.x = self.rect.centerx
        self.y = self.rect.bottom

    def takip_et(self, hedef, _, collision_rects):  # Ignore second parameter for compatibility
        target_x = hedef.rect.centerx if hasattr(hedef, 'rect') else hedef.x
        target_y = hedef.rect.centery if hasattr(hedef, 'rect') else hedef.y
        dx = target_x - self.x
        dy = target_y - self.y
        mesafe = self.mesafe_hesapla(hedef)

        def handle_horizontal_collisions(dx):
            self.rect.x += dx
            self.update_hitbox()
            for rect in collision_rects:
                if self.hitbox.colliderect(rect):
                    if dx > 0:
                        self.hitbox.right = rect.left
                        self.rect.right = self.hitbox.right + (self.rect.width - self.hitbox.width) // 2
                    elif dx < 0:
                        self.hitbox.left = rect.right
                        self.rect.left = self.hitbox.left - (self.rect.width - self.hitbox.width) // 2
                    return 0
            return dx

        self.platform_kontrolu(collision_rects, target_x, target_y)

        if not self.vuruyor and not self.vuruldu:
            if mesafe > self.saldiri_mesafesi:
                move_dx = (dx / mesafe) * self.hiz * 1.5
                move_dx = handle_horizontal_collisions(move_dx)
                self.sola_donuk = dx < 0
                if self.on_ground and self.mevcut_animasyon != "Jump":
                    if "Run" in self.animasyonlar:
                        self.animasyon_degistir("Run")
                    else:
                        self.animasyon_degistir("Walk")
            else:
                if self.on_ground and self.mevcut_animasyon != "Jump":
                    self.animasyon_degistir("Idle")
        
        self.x = self.rect.centerx
        self.y = self.rect.bottom
    
    def saldiri(self, hedef):
    # Check if target and self are alive
        if hasattr(hedef, 'canli_mi'):
            target_alive = hedef.canli_mi()
        else:
            target_alive = hedef.alive if hasattr(hedef, 'alive') else True  # Default to True if no alive check
        if not target_alive or not self.canli_mi() or self.vuruyor or self.vuruldu:
            return
        mesafe = self.mesafe_hesapla(hedef)
        target_x = hedef.rect.centerx if hasattr(hedef, 'rect') else hedef.x
        self.sola_donuk = target_x < self.x
        if mesafe <= self.saldiri_mesafesi:
            self.vuruyor = True
            self.animasyon_degistir(self.available_attacks[random.randint(0, len(self.available_attacks)-1)])
            self.kare_indeksi = 0
            # Check if target is Samurai (player) or another enemy
            if hasattr(hedef, 'get_hit'):  # Samurai uses get_hit
                hedef.get_hit(self.guc)
            elif hasattr(hedef, 'hasar_al'):  # Other enemies use hasar_al
                hedef.hasar_al(self.guc)
            self.son_saldiri_zamani = pygame.time.get_ticks()
        else:
            self.takip_et(hedef, None, game_state.collision_rects)
    
   # In yakin.py
    def guncelle(self, hedef, collision_rects):
        self.update_physics(collision_rects)
        if not self.canli_mi():
            if self.mevcut_animasyon != "Dead":
                self.mevcut_animasyon = "Dead"
                self.kare_indeksi = 0
            return

        mesafe = self.mesafe_hesapla(hedef)

        self.onceki_durum = self.durum
        if hasattr(hedef, 'is_dead') and hedef.is_dead:
            self.durum = "devriye"
        elif mesafe <= self.saldiri_mesafesi and (self.alerted or (self.can_see_player(hedef) 
            and not self.is_facing_away(hedef))):
            self.durum = "saldiri"
        elif mesafe <= self.tespit_mesafesi and (self.alerted or (self.can_see_player(hedef) 
            and not self.is_facing_away(hedef))):
            self.durum = "takip"
        else:
            self.durum = "devriye"

        if self.durum == "devriye":
            self.devriye_et(collision_rects)
        elif self.durum == "takip":
            self.takip_et(hedef, None, collision_rects)
        elif self.durum == "saldiri":
            self.saldiri(hedef)
        