import pygame
import os
import math

class Dusman:
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        self.rect = pygame.Rect(x - 50, y - 50, 100, 100)
        self.hitbox = pygame.Rect(0, 0, 30, 60)
        self.ground_check = pygame.Rect(0, 0, 24, 5)
        self.x = x
        self.y = y
        self.hiz = hiz
        self.can = can
        self.maksimum_can = can
        self.guc = guc
        self.sola_donuk = False
        self.animasyonlar = {}
        self.mevcut_animasyon = "Idle"
        self.kare_indeksi = 0
        self.sprite_soneki = sprite_soneki
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.temel_yol = os.path.dirname(os.path.abspath(__file__))
        self.sprite_klasoru = os.path.abspath(os.path.join(self.temel_yol, "..", sprite_klasoru))
        self.animasyonlari_yukle(animasyonlar)
        self.animasyon_hizi = 100
        self.son_animasyon_guncelleme = pygame.time.get_ticks()
        self.olum_animasyonu_tamamlandi = False
        self.vuruyor = False
        self.vuruldu = False
        self.vurma_zamani = 0
        self.update_hitbox()
        self.update_ground_check()

    def animasyonlari_yukle(self, animasyonlar):
        for animasyon_adi, kare_sayisi in animasyonlar.items():
            formatli_isim = f"{animasyon_adi}_{self.sprite_soneki}.png"
            resim_yolu = os.path.join(self.sprite_klasoru, formatli_isim)
            try:
                sprite_sayfasi = pygame.image.load(resim_yolu).convert_alpha()
                kare_genisligi = sprite_sayfasi.get_width() // kare_sayisi
                kare_yuksekligi = sprite_sayfasi.get_height()
                kareler = []
                for i in range(kare_sayisi):
                    kare = sprite_sayfasi.subsurface(pygame.Rect(i * kare_genisligi, 0, kare_genisligi, kare_yuksekligi))
                    kareler.append(kare)
                self.animasyonlar[animasyon_adi] = kareler
            except pygame.error as e:
                print(f"Hata: {resim_yolu} yüklenemedi!", e)
        
        if "Idle" in self.animasyonlar and self.animasyonlar["Idle"]:
            kare = self.animasyonlar["Idle"][0]
            self.rect.width = kare.get_width()
            self.rect.height = kare.get_height()
            self.rect.center = (self.x, self.y)
            self.update_hitbox()
    
    def update_hitbox(self):
        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def update_ground_check(self):
        self.ground_check.centerx = self.hitbox.centerx
        self.ground_check.top = self.hitbox.bottom

    def check_on_ground(self, collision_rects):
        self.on_ground = False
        self.update_ground_check()
        for rect in collision_rects:
            if self.ground_check.colliderect(rect):
                self.on_ground = True
                return

    def animasyonu_guncelle(self):
        if not self.canli_mi() and self.mevcut_animasyon != "Dead" and self.olum_animasyonu_tamamlandi:
            return
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_animasyon_guncelleme > self.animasyon_hizi:
            if self.mevcut_animasyon in self.animasyonlar:
                animation_frames = self.animasyonlar.get(self.mevcut_animasyon, [])
                if animation_frames:
                    if self.mevcut_animasyon == "Dead":
                        if self.kare_indeksi >= len(animation_frames) - 1:
                            self.kare_indeksi = len(animation_frames) - 1
                            self.olum_animasyonu_tamamlandi = True
                        else:
                            self.kare_indeksi += 1
                    elif self.mevcut_animasyon == "Hurt":
                        if self.kare_indeksi >= len(animation_frames) - 1:
                            self.vuruldu = False
                            self.vuruyor = False
                            self.mevcut_animasyon = "Idle"
                            self.kare_indeksi = 0
                        else:
                            self.kare_indeksi += 1
                    elif self.mevcut_animasyon == "Jump":
                        if self.on_ground:
                            self.mevcut_animasyon = "Idle"
                            self.kare_indeksi = 0
                        else:
                            self.kare_indeksi = (self.kare_indeksi + 1) % len(animation_frames)
                    elif self.mevcut_animasyon in ["Attack_1", "Attack_2", "Attack_3","Attack_4","Fire"]:
                        if self.kare_indeksi >= len(animation_frames) - 1:
                            self.vuruyor = False
                            self.mevcut_animasyon = "Idle"
                            self.kare_indeksi = 0
                        else:
                            self.kare_indeksi += 1
                    else:
                        self.kare_indeksi = (self.kare_indeksi + 1) % len(animation_frames)
                    self.son_animasyon_guncelleme = simdiki_zaman

    def animasyon_degistir(self, yeni_animasyon):
        if self.mevcut_animasyon != yeni_animasyon:
            self.mevcut_animasyon = yeni_animasyon
            self.kare_indeksi = 0

    def ciz(self, ekran, camera_x, camera_y):
        if self.mevcut_animasyon in self.animasyonlar:
            animation_frames = self.animasyonlar[self.mevcut_animasyon]
            if animation_frames and 0 <= self.kare_indeksi < len(animation_frames):
                kare = animation_frames[self.kare_indeksi]
                if self.sola_donuk:
                    kare = pygame.transform.flip(kare, True, False)
                
                kare_genisligi = kare.get_width()
                kare_yuksekligi = kare.get_height()
                screen_x = self.rect.centerx - kare_genisligi // 2 - camera_x
                screen_y = self.rect.bottom - kare_yuksekligi - camera_y
                ekran.blit(kare, (screen_x, screen_y))
                
                can_cubugu_genislik = 50
                can_cubugu_yukseklik = 5
                can_cubugu_x = screen_x + kare_genisligi // 2 - can_cubugu_genislik // 2
                can_cubugu_y = screen_y - 10
                pygame.draw.rect(ekran, (255, 0, 0), (can_cubugu_x, can_cubugu_y, can_cubugu_genislik, can_cubugu_yukseklik))
                can_orani = self.can / self.maksimum_can
                pygame.draw.rect(ekran, (0, 255, 0), (can_cubugu_x, can_cubugu_y, can_cubugu_genislik * can_orani, can_cubugu_yukseklik))

    def hasar_al(self, miktar):
        if not self.canli_mi():
            return
        self.can -= miktar
        self.vuruldu = True
        self.alerted=True
        self.mevcut_animasyon = "Hurt"
        self.kare_indeksi = 0
        if self.can <= 0:
            self.can = 0
            self.mevcut_animasyon = "Dead"
            self.olum_animasyonu_tamamlandi = False

    def canli_mi(self):
        return self.can > 0

    def mesafe_hesapla(self, hedef_x, hedef_y):
        dx = hedef_x - self.x
        dy = hedef_y - self.y
        return math.sqrt(dx**2 + dy**2)

    def update_physics(self, collision_rects):
        self.check_on_ground(collision_rects)


        self.velocity_y += self.gravity
        if self.velocity_y > 10:
            self.velocity_y = 10

        self.rect.y += self.velocity_y
        self.update_hitbox()

        for rect in collision_rects:
            if self.hitbox.colliderect(rect):
                if self.velocity_y > 0:
                    self.hitbox.bottom = rect.top
                    self.rect.bottom = self.hitbox.bottom
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.hitbox.top = rect.bottom
                    self.rect.bottom = self.hitbox.bottom
                    self.velocity_y = 0

        if self.on_ground and self.velocity_y >= 0:
            self.velocity_y = 0

        self.x = self.rect.centerx
        self.y = self.rect.centery
