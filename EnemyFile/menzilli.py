import pygame
import math
import os
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
        self.mermi_menzili = 500
        self.saldiri_mesafesi = 300
        self.mermiler = []

    def saldiri(self, hedef):
        if not hedef.canli_mi() or not self.canli_mi():
            return
        simdiki_zaman = pygame.time.get_ticks()
        if not self.vuruyor and simdiki_zaman - self.son_saldiri_zamani >= self.saldiri_bekleme_suresi:
            self.vuruyor = True
            self.mevcut_animasyon = "Fireball"
            self.kare_indeksi = 0
            self.sola_donuk = hedef.x < self.x
            mermi = Mermi(
                self.x, self.y, hedef.x, hedef.y, self.mermi_hizi, self.guc,
                sprite_klasoru="ENEMIES/wizard/Fire vizard", sprite_soneki="fire", kare_sayisi=6
            )
            self.mermiler.append(mermi)
            self.son_saldiri_zamani = simdiki_zaman

    def guncelle(self, hedef, collision_rects):
        super().guncelle(hedef, collision_rects)
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
