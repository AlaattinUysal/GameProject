import pygame
import math
import os
import random
from yakin import Yakin

class Mermi:
    def __init__(self, x, y, hedef_x, hedef_y, hiz, hasar, sprite_klasoru, sprite_soneki, kare_sayisi):
        self.x = x
        self.y = y
        self.hiz = hiz
        self.hasar = hasar
        self.kare_indeksi = 0
        self.animasyon_hizi = 100
        self.son_animasyon_guncelleme = pygame.time.get_ticks()
        self.animasyonlar = []
        temel_yol = os.path.dirname(os.path.abspath(__file__))
        sprite_klasoru = os.path.abspath(os.path.join(temel_yol, "..", sprite_klasoru))
        formatli_isim = f"Charge_{sprite_soneki}.png"
        resim_yolu = os.path.join(sprite_klasoru, formatli_isim)
        try:
            sprite_sayfasi = pygame.image.load(resim_yolu).convert_alpha()
            kare_genisligi = sprite_sayfasi.get_width() // kare_sayisi
            kare_yuksekligi = sprite_sayfasi.get_height()
            for i in range(kare_sayisi):
                kare = sprite_sayfasi.subsurface(pygame.Rect(i * kare_genisligi, 0, kare_genisligi, kare_yuksekligi))
                self.animasyonlar.append(kare)
            self.rect = pygame.Rect(x - kare_genisligi // 2, y - kare_yuksekligi // 2, kare_genisligi, kare_yuksekligi)
        except pygame.error as e:
            print(f"Hata: {resim_yolu} yüklenemedi!", e)
            self.animasyonlar = []
            self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
        dx = hedef_x - x
        dy = hedef_y - y
        mesafe = math.sqrt(dx**2 + dy**2)
        if mesafe > 0:
            self.vx = (dx / mesafe) * hiz
            self.vy = (dy / mesafe) * hiz
            self.aci = math.degrees(math.atan2(-dy, dx))
        else:
            self.vx = hiz
            self.vy = 0
            self.aci = 0

    def animasyonu_guncelle(self):
        if not self.animasyonlar:
            return
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_animasyon_guncelleme > self.animasyon_hizi:
            self.kare_indeksi = (self.kare_indeksi + 1) % len(self.animasyonlar)
            self.son_animasyon_guncelleme = simdiki_zaman

    def guncelle(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)
        self.animasyonu_guncelle()

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
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        super().__init__(x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki)
        self.mermi_hizi = 4
        self.mermi_menzili = 200
        self.menzilli_saldiri_mesafesi = 200
        self.mermiler = []

    def saldiri(self, hedef):
        if not hedef.canli_mi() or not self.canli_mi():
            return
        simdiki_zaman = pygame.time.get_ticks()

        if simdiki_zaman - self.son_saldiri_zamani < self.saldiri_bekleme_suresi:
            if not self.vuruyor and self.on_ground and not self.vuruldu:
                self.animasyon_degistir("Idle")
            return
        
        mesafe = self.mesafe_hesapla(hedef.x, hedef.y)
        self.sola_donuk = hedef.x < self.x

        if mesafe<=self.saldiri_mesafesi:
            self.vuruyor=True
            self.mevcut_animasyon="Attack_3"
            self.kare_indeksi=0
            hedef.hasar_al(self.guc)
            self.son_saldiri_zamani=simdiki_zaman

        elif mesafe <=self.menzilli_saldiri_mesafesi:
            self.vuruyor=True
            self.mevcut_animasyon="Fire"
            self.kare_indeksi=0
            mermi_kare_sayisi=len(self.animasyonlar.get("Charge", []))
            mermi = Mermi(
                self.x, self.y, hedef.x, hedef.y, self.mermi_hizi, self.guc,
                sprite_klasoru=self.sprite_klasoru,
                sprite_soneki=self.sprite_soneki,
                kare_sayisi=mermi_kare_sayisi
            )
            self.mermiler.append(mermi)
            self.son_saldiri_zamani=simdiki_zaman
        
        elif mesafe<=self.tespit_mesafesi:
            self.vuruyor=True
            if self.on_ground and not self.vuruldu:
                self.animasyon_degistir("Walk")
            self.takip_et(hedef.x,hedef.y, [])
        
        else:
            self.vuruyor=False
            if self.on_ground and not self.vuruldu:
                self.animasyon_degistir("Idle")
            self.devriye_et([])

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
            self.takip_et(hedef.x, hedef.y, collision_rects)
        elif self.durum == "saldiri":
            self.saldiri(hedef)

        for mermi in self.mermiler[:]:
            mermi.guncelle()
            if mermi.carpisma_kontrolu(hedef):
                self.mermiler.remove(mermi)
            elif self.mesafe_hesapla(mermi.x, mermi.y) > self.mermi_menzili:
                self.mermiler.remove(mermi)
        

    def ciz(self, ekran, camera_x, camera_y):
        super().ciz(ekran, camera_x, camera_y)
        for mermi in self.mermiler:
            mermi.ciz(ekran, camera_x, camera_y)
