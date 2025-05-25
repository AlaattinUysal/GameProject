import pygame
import os
import math
from utils import Spritesheet
class Dusman:
    def __init__(self, x, y, hiz, can, guc,  walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet):
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
        
        self.velocity_y = 0
        self.gravity = 0.5
        self.on_ground = False
        self.animasyon_hizi = 50
        self.son_animasyon_guncelleme = pygame.time.get_ticks()
        self.olum_animasyonu_tamamlandi = False
        self.vuruyor = False
        self.vuruldu = False
        self.vurma_zamani = 0
        self.update_hitbox()
        self.update_ground_check()

        walk_spritesheet = Spritesheet("ENEMIES/anime/Knight/Walk_AnimeKnight.png")
        idle_spritesheet = Spritesheet("ENEMIES/anime/Knight/Idle_AnimeKnight.png")
        jump_spritesheet = Spritesheet("ENEMIES/anime/Knight/Jump_AnimeKnight.png")
        run_spritesheet = Spritesheet("ENEMIES/anime/Knight/Run_AnimeKnight.png")
        attack1_spritesheet = Spritesheet("ENEMIES/anime/Knight/Attack_1_AnimeKnight.png")
        attack2_spritesheet = Spritesheet("ENEMIES/anime/Knight/Attack_2_AnimeKnight.png")
        attack3_spritesheet = Spritesheet("ENEMIES/anime/Knight/Attack_3_AnimeKnight.png")
        hurt_spritesheet = Spritesheet("ENEMIES/anime/Knight/Hurt_AnimeKnight.png")
        death_spritesheet = Spritesheet("ENEMIES/anime/Knight/Dead_AnimeKnight.png")

    # yakin.py içinde
    def animasyonlari_yukle(self, animasyonlar):
        for animasyon_adi, kare_sayisi in animasyonlar.items():
            formatli_isim = f"{animasyon_adi}_AnimeKnight.png"
            resim_yolu = os.path.join("ENEMIES/anime/Knight", formatli_isim)
            print(f"Yükleniyor: {resim_yolu}")
            try:
                sprite_sayfasi = Spritesheet(resim_yolu)
                kareler = sprite_sayfasi.get_animation_frames(frame_width=128, frame_height=128, scale=1, frame_count=kare_sayisi)
                self.animasyonlar[animasyon_adi] = kareler
            except pygame.error as e:
                print(f"Hata: {resim_yolu} yüklenemedi! Hata: {e}")
    
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

    # In yakin.py, in the Yakin class
    def animasyon_degistir(self, yeni_animasyon):
        if self.mevcut_animasyon != yeni_animasyon:
            # Only reset frame index for non-cyclic animations or significant state changes
            if yeni_animasyon in ["Attack_1", "Attack_2", "Attack_3", "Hurt", "Dead", "Jump"]:
                self.kare_indeksi = 0
            self.mevcut_animasyon = yeni_animasyon

    def ciz(self, ekran, camera_x, camera_y, zoom_factor):
        if self.mevcut_animasyon in self.animasyonlar:
            animation_frames = self.animasyonlar[self.mevcut_animasyon]
            if animation_frames and 0 <= self.kare_indeksi < len(animation_frames):
                kare = animation_frames[self.kare_indeksi]
                if self.sola_donuk:
                    kare = pygame.transform.flip(kare, True, False)
                
                # Sprite'ın ölçeklendirilmiş boyutlarını al
                kare_genisligi = int(kare.get_width() * zoom_factor)
                kare_yuksekligi = int(kare.get_height() * zoom_factor)
                kare = pygame.transform.scale(kare, (kare_genisligi, kare_yuksekligi))
                
                # 1. Dünya koordinatlarını ekran koordinatlarına çevir (zoom ve kamera etkisini uygula)
                hitbox_centerx_screen = (self.hitbox.centerx - camera_x) * zoom_factor
                hitbox_bottom_screen = (self.hitbox.bottom - camera_y) * zoom_factor
                
                # 2. Sprite'ın sol üst köşesini hesapla
                # Sprite'ın orta-alt noktası hitbox'ın orta-alt noktasına hizalanacak
                screen_x = hitbox_centerx_screen - (kare_genisligi // 2)
                screen_y = hitbox_bottom_screen - kare_yuksekligi
                
                ekran.blit(kare, (screen_x, screen_y))
                
                # Debug: Hitbox'ı çiz
                hitbox_x = (self.hitbox.x - camera_x) * zoom_factor
                hitbox_y = (self.hitbox.y - camera_y) * zoom_factor
                hitbox_width = self.hitbox.width * zoom_factor
                hitbox_height = self.hitbox.height * zoom_factor
                pygame.draw.rect(ekran, (255, 0, 0), (hitbox_x, hitbox_y, hitbox_width, hitbox_height), 2)
                
                # Can barı
                can_cubugu_genislik = 50 * zoom_factor
                can_cubugu_yukseklik = 5 * zoom_factor
                can_cubugu_x = (self.hitbox.centerx - can_cubugu_genislik // 2 - camera_x) * zoom_factor
                can_cubugu_y = (self.hitbox.top - 10 - camera_y) * zoom_factor
                pygame.draw.rect(ekran, (255, 0, 0), (can_cubugu_x, can_cubugu_y, can_cubugu_genislik, can_cubugu_yukseklik))
                can_orani = self.can / self.maksimum_can
                pygame.draw.rect(ekran, (0, 255, 0), (can_cubugu_x, can_cubugu_y, can_cubugu_genislik * can_orani, can_cubugu_yukseklik))
            else:
                print(f"Çizim hatası: {self.__class__.__name__}")
        else:
            print(f"Animasyon bulunamadı: {self.mevcut_animasyon}")

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
        return self.can >   0

    def mesafe_hesapla(self, hedef):
        if hasattr(hedef, 'rect'):
            dx = hedef.rect.centerx - self.x
            dy = hedef.rect.centery - self.y
        else:
            dx = hedef.x - self.x
            dy = hedef.y - self.y
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