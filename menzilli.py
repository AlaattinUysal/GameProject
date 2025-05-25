import pygame
import math
import os
import random
from yakin import Yakin
import game_state

class Mermi:
    def __init__(self, x, y, hedef_x, hedef_y, hiz, guc, sprite_klasoru, sprite_soneki, kare_sayisi):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.hiz = hiz
        self.guc = guc
        self.hedef_x = hedef_x
        self.hedef_y = hedef_y
        dx = hedef_x - x
        dy = hedef_y - y
        mesafe = math.sqrt(dx**2 + dy**2)
        self.vx = (dx / mesafe) * hiz if mesafe != 0 else hiz
        self.vy = (dy / mesafe) * hiz if mesafe != 0 else 0
        self.animasyonlar = {}
        try:
            resim_yolu = f"{sprite_klasoru}/Charge{sprite_soneki}.png"
            sprite_sayfasi = pygame.image.load(resim_yolu).convert_alpha()
            # Ensure kare_sayisi is at least 1 to avoid division by zero
            kare_sayisi = max(1, kare_sayisi)
            kare_genisligi = sprite_sayfasi.get_width() // kare_sayisi
            kare_yuksekligi = sprite_sayfasi.get_height()
            self.animasyonlar["Charge"] = []
            for i in range(kare_sayisi):
                kare = sprite_sayfasi.subsurface((i * kare_genisligi, 0, kare_genisligi, kare_yuksekligi))
                self.animasyonlar["Charge"].append(kare)
        except FileNotFoundError:
            print(f"Warning: Mermi sprite not found at {resim_yolu}. Using default red circle.")
            self.animasyonlar["Charge"] = [pygame.Surface((30, 30))]
            self.animasyonlar["Charge"][0].fill((255, 0, 0))
        except ZeroDivisionError:
            print(f"Warning: Invalid kare_sayisi ({kare_sayisi}) for Mermi sprite. Using default red circle.")
            self.animasyonlar["Charge"] = [pygame.Surface((30, 30))]
            self.animasyonlar["Charge"][0].fill((255, 0, 0))
        self.mevcut_animasyon = "Charge"
        self.kare_indeksi = 0
        self.animasyon_hizi = 0.2

    def animasyonu_guncelle(self):
        if not self.animasyonlar:
            return
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_animasyon_guncelleme > self.animasyon_hizi:
            self.kare_indeksi = (self.kare_indeksi + 1) % len(self.animasyonlar)
            self.son_animasyon_guncelleme = simdiki_zaman

    def guncelle(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        dx = self.hedef_x - self.rect.x
        dy = self.hedef_y - self.rect.y
        mesafe = math.sqrt(dx**2 + dy**2)
        if mesafe > self.hiz * 50:
            self.canli = False
        self.kare_indeksi += self.animasyon_hizi
        if self.kare_indeksi >= len(self.animasyonlar[self.mevcut_animasyon]):
            self.kare_indeksi = 0

    def ciz(self, ekran, camera_x, camera_y):
        if self.animasyonlar:
            kare = self.animasyonlar[self.kare_indeksi]
            dondurulmus_kare = pygame.transform.rotate(kare, self.aci)
            dondurulmus_rect = dondurulmus_kare.get_rect(center=(self.x - camera_x, self.y - camera_y))
            ekran.blit(dondurulmus_kare, dondurulmus_rect)
        else:
            pygame.draw.circle(ekran, (255, 0, 0), (int(self.x - camera_x), int(self.y - camera_y)), 5)

    def carpisma_kontrolu(self, hedef):
        if self.rect.colliderect(hedef.rect):
            hedef.hasar_al(self.hasar)
            return True
        return False

class Menzilli(Yakin):
    def __init__(self, x, y, hiz, can, guc, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet, charge_spritesheet, fire_spritesheet, sprite_klasoru="ENEMIES/wizard/Fire vizard", sprite_soneki="_fire"):
        super().__init__(x, y, hiz, can, guc, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet)
        self.mermi_hizi = 4
        self.mermi_menzili = 200
        self.menzilli_saldiri_mesafesi = 200
        self.mermiler = []
        self.charge_spritesheet = charge_spritesheet
        self.fire_spritesheet = fire_spritesheet
        self.sprite_klasoru = sprite_klasoru  # Initialize sprite_klasoru
        self.sprite_soneki = sprite_soneki    # Initialize sprite_soneki

    # In menzilli.py
    def saldiri(self, hedef):
    # Check if target and self are alive
        if hasattr(hedef, 'canli_mi'):
            target_alive = hedef.canli_mi()
        else:
            target_alive = hedef.alive if hasattr(hedef, 'alive') else True  # Default to True if no alive check
        if not target_alive or not self.canli_mi():
            return
        simdiki_zaman = pygame.time.get_ticks()

        if simdiki_zaman - self.son_saldiri_zamani < self.saldiri_bekleme_suresi:
            if not self.vuruyor and self.on_ground and not self.vuruldu:
                self.animasyon_degistir("Idle")
            return
        
        mesafe = self.mesafe_hesapla(hedef)
        target_x = hedef.rect.centerx if hasattr(hedef, 'rect') else hedef.x
        target_y = hedef.rect.centery if hasattr(hedef, 'rect') else hedef.y
        self.sola_donuk = target_x < self.x

        if mesafe <= self.saldiri_mesafesi:
            self.vuruyor = True
            self.mevcut_animasyon = "Attack_3"
            self.kare_indeksi = 0
            hedef.hasar_al(self.guc)
            self.son_saldiri_zamani = simdiki_zaman
        elif mesafe <= self.menzilli_saldiri_mesafesi:
            self.vuruyor = True
            self.mevcut_animasyon = "Fire"
            self.kare_indeksi = 0
            mermi_kare_sayisi = len(self.animasyonlar.get("Charge", []))
            mermi = Mermi(
                self.x, self.y, target_x, target_y, self.mermi_hizi, self.guc,
                sprite_klasoru=self.sprite_klasoru,
                sprite_soneki=self.sprite_soneki,
                kare_sayisi=mermi_kare_sayisi
            )
            self.mermiler.append(mermi)
            self.son_saldiri_zamani = simdiki_zaman
        elif mesafe <= self.tespit_mesafesi:
            self.vuruyor = True
            if self.on_ground and not self.vuruldu:
                self.animasyon_degistir("Walk")
            self.takip_et(hedef, None, game_state.collision_rects)  # Pass hedef object
        else:
            self.vuruyor = False
            if self.on_ground and not self.vuruldu:
                self.animasyon_degistir("Idle")
            self.devriye_et([])

    # In menzilli.py
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
        elif mesafe <= self.saldiri_mesafesi and (self.alerted or (self.can_see_player(hedef) and not self.is_facing_away(hedef))):
            self.durum = "saldiri"
        elif isinstance(self, Menzilli) and mesafe <= self.menzilli_saldiri_mesafesi and (self.alerted or (self.can_see_player(hedef) and not self.is_facing_away(hedef))):
            self.durum = "saldiri"
        elif mesafe <= self.tespit_mesafesi and (self.alerted or (self.can_see_player(hedef) and not self.is_facing_away(hedef))):
            self.durum = "takip"
        else:
            self.durum = "devriye"

        if self.durum == "devriye":
            self.devriye_et(collision_rects)
        elif self.durum == "takip":
            self.takip_et(hedef, None, collision_rects if collision_rects is not None else [])
        elif self.durum == "saldiri":
            self.saldiri(hedef)

        for mermi in self.mermiler[:]:
            mermi.guncelle()
            if mermi.carpisma_kontrolu(hedef):
                self.mermiler.remove(mermi)
            elif self.mesafe_hesapla(mermi) > self.mermi_menzili:
                self.mermiler.remove(mermi)
        

    def ciz(self, ekran, camera_x, camera_y):
        super().ciz(ekran, camera_x, camera_y)
        for mermi in self.mermiler:
            mermi.ciz(ekran, camera_x, camera_y)