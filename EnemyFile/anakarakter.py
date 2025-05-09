from dusman import Dusman
import pygame

class AnaKarakter(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6,
            "Idle_2": 6,
            "Walk": 12, 
            "Run": 12, 
            "Jump": 10,
            "Hurt": 3, 
            "Dead": 5, 
            "Run+Attack": 5, 
            "Attack_1": 4, 
            "Attack_2": 5,
        }
        super().__init__(x, y - 50, hiz=5, can=100, guc=10, sprite_klasoru="ENEMIES/warrior/Man_3", animasyonlar=animasyonlar, sprite_soneki="Man3")
        self.saldiri_menzili = 100
        self.jump_power = -10

    def hareket_et(self, tuslar, collision_rects):
        if not self.canli_mi():
            return
        
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

        dx = 0
        hareket_var = False

        if tuslar[pygame.K_LEFT]:
            dx = -self.hiz
            self.sola_donuk = True
            hareket_var = True
        elif tuslar[pygame.K_RIGHT]:
            dx = self.hiz
            self.sola_donuk = False
            hareket_var = True

        if tuslar[pygame.K_UP] and self.on_ground:
            self.velocity_y = self.jump_power

        dx = handle_horizontal_collisions(dx)

        if hareket_var and not self.vuruldu:
            self.animasyon_degistir("Run")
        elif not self.vuruyor and not self.vuruldu and self.canli_mi():
            self.animasyon_degistir("Idle")

        self.x = self.rect.centerx
        self.y = self.rect.centery

    def saldiri(self, dusman_listesi):
        if not self.canli_mi():
            return
        if self.vuruyor:
            return
        
        self.vuruyor = True
        self.animasyon_degistir("Attack_1")
        self.vurma_zamani = pygame.time.get_ticks()
        for dusman in dusman_listesi:
            if dusman.canli_mi() and self.mesafe_hesapla(dusman.x, dusman.y) < self.saldiri_menzili:
                dusman.hasar_al(self.guc)

    def guncelle(self, collision_rects):
        if not self.canli_mi():
            if self.mevcut_animasyon != "Dead":
                self.mevcut_animasyon = "Dead"
                self.kare_indeksi = 0
            return
        self.update_physics(collision_rects)
        if self.vuruyor and self.kare_indeksi >= len(self.animasyonlar["Attack_1"]) - 1:
            self.vuruyor = False
            self.animasyon_degistir("Idle")
        if self.vuruldu and self.kare_indeksi >= len(self.animasyonlar["Hurt"]) - 1:
            self.vuruldu = False
            if self.canli_mi():
                self.animasyon_degistir("Idle")
