import pygame
import random
import math
from dusman import Dusman

class Yakin(Dusman):
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        super().__init__(x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki)
        self.baslangic_x = x
        self.baslangic_y = y
        self.tespit_mesafesi = 300
        self.saldiri_mesafesi = 80
        self.menzilli_saldiri_mesafesi=300
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
        self.view_angle=90
        self.attack_count=2
        self.attacks=["Attack_1", "Attack_2", "Attack_3","Attack_4"]
        self.available_attacks=self.attacks[:self.attack_count]
        
    
    def is_facing_away(self, hedef):
        return (self.sola_donuk and hedef.x > self.x) or (not self.sola_donuk and hedef.x < self.x)
    
    def can_see_player(self, hedef):
        mesafe = self.mesafe_hesapla(hedef.x, hedef.y)
        if mesafe > self.tespit_mesafesi:
            return False
        
        angle_to_player = math.degrees(math.atan2(hedef.y - self.y, hedef.x - self.x))
        facing_angle=180 if self.sola_donuk else 0
        angle_diff=abs((angle_to_player - facing_angle+180)%360-180)
        return angle_diff<=self.view_angle/2
    
    def platform_kontrolu(self, collision_rects, hedef_x, hedef_y):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_ziplama_zamani < self.ziplama_bekleme_suresi or not self.on_ground:
            return
        
        yon = 1 if hedef_x > self.x else -1
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

    def takip_et(self, hedef_x, hedef_y, collision_rects):
        dx = hedef_x - self.x
        dy = hedef_y - self.y
        mesafe = math.sqrt(dx**2 + dy**2)

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
            
        self.platform_kontrolu(collision_rects, hedef_x, hedef_y)

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
        if not hedef.canli_mi() or not self.canli_mi() or self.vuruyor or self.vuruldu:
            return
            
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_saldiri_zamani >= self.saldiri_bekleme_suresi:
            self.vuruyor = True
            self.mevcut_animasyon = random.choice(self.available_attacks)
            self.kare_indeksi = 0
            self.son_saldiri_zamani = simdiki_zaman
            self.sola_donuk = hedef.x < self.x
            
            if self.mesafe_hesapla(hedef.x, hedef.y) <= self.saldiri_mesafesi:
                hedef.hasar_al(self.guc)
        elif not self.vuruyor and self.on_ground and not self.vuruldu:
            self.animasyon_degistir("Idle")
    
    def guncelle(self, hedef, collision_rects):
        self.update_physics(collision_rects)
        if not self.canli_mi():
            if self.mevcut_animasyon != "Dead":
                self.mevcut_animasyon = "Dead"
                self.kare_indeksi = 0
            return

        mesafe = self.mesafe_hesapla(hedef.x, hedef.y)
        self.onceki_durum = self.durum
        if not hedef.canli_mi():
            self.durum = "devriye"
        elif mesafe <= self.saldiri_mesafesi and (self.alerted or (self.can_see_player(hedef) 
        and not self.is_facing_away(hedef))):
            self.durum = "saldiri"
        elif mesafe <=self.menzilli_saldiri_mesafesi and (self.alerted or (self.can_see_player(hedef)
        and not self.is_facing_away(hedef)))                                                                    :
            self.durum="takip"
        elif mesafe <= self.tespit_mesafesi and (self.alerted or (self.can_see_player(hedef) 
        and not self.is_facing_away(hedef))):
            self.durum = "takip"
        else:
            self.durum = "devriye"

        if self.durum == "devriye":
            self.devriye_et(collision_rects)
        elif self.durum == "takip":
            self.takip_et(hedef.x, hedef.y, collision_rects)
        elif self.durum == "saldiri":
            self.saldiri(hedef)
