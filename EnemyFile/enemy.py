import pygame
import os
import random
import math
import pytmx
import sys

pygame.init()

# Pencere ayarları
genislik = 1600
yukseklik = 900
ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("Ninja Savaşı")

saat = pygame.time.Clock()
FPS = 60

# Durum sabitleri
DEVRIYE = "devriye"

# Harita yükleme
tmx_data = pytmx.load_pygame('C:/Users/özer/Desktop/sw_eng_project/sw_eng_project/levels/village/village.tmx')
map_genislik = tmx_data.width * tmx_data.tilewidth
map_yukseklik = tmx_data.height * tmx_data.tileheight

# Çarpışma objeleri
collision_rects = []
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "collision":
        for nesne in layer:
            if hasattr(nesne, 'x') and hasattr(nesne, 'y'):
                rect = pygame.Rect(nesne.x, nesne.y, nesne.width, nesne.height)
                collision_rects.append(rect)

# Kamera ayarları
camera_x, camera_y = 0, 0

class Karakter:
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        self.rect = pygame.Rect(x - 50, y - 50, 100, 100)  # Çarpışma için dikdörtgen
        self.x = x  # Görsel pozisyon
        self.y = y
        self.hiz = hiz
        self.can = can
        self.maximum_can = can
        self.guc = guc
        self.sola_donuk = False
        self.animasyonlar = {}
        self.mevcut_animasyon = "Idle"
        self.kare_indeksi = 0
        self.sprite_soneki = sprite_soneki
        self.velocity_y = 0  # Dikey hız 
        self.gravity = 0.5  # Yerçekimi
        self.on_ground = False
        
        self.temel_yol = os.path.dirname(os.path.abspath(__file__))
        self.sprite_klasoru = os.path.abspath(os.path.join(self.temel_yol, "..", sprite_klasoru))
        
        self.animasyonlari_yukle(animasyonlar)
        
        if "Idle" in self.animasyonlar and self.animasyonlar["Idle"]:
            kare = self.animasyonlar["Idle"][0]
            self.rect = pygame.Rect(x - kare.get_width() // 2, y - kare.get_height() // 2, kare.get_width(), kare.get_height())
        self.animasyon_hizi = 100
        self.son_animasyon_guncelleme = pygame.time.get_ticks()
        self.olum_animasyonu_tamamlandi = False
        self.vuruyor = False
        self.vuruldu = False
        self.vurma_zamani = 0

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

    def animasyonu_guncelle(self):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_animasyon_guncelleme > self.animasyon_hizi:
            if self.mevcut_animasyon in self.animasyonlar:
                animation_frames = self.animasyonlar.get(self.mevcut_animasyon, [])
                if animation_frames:
                    if self.mevcut_animasyon == "Dead" and self.kare_indeksi >= len(animation_frames) - 1:
                        self.kare_indeksi = len(animation_frames) - 1
                        self.olum_animasyonu_tamamlandi = True
                    elif not (self.mevcut_animasyon == "Dead" and self.olum_animasyonu_tamamlandi):
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
                screen_y = self.rect.centery - kare_yuksekligi // 2 - camera_y
                ekran.blit(kare, (screen_x, screen_y))
                
                # Can çubuğu
                can_cubugu_genislik = 50
                can_cubugu_yukseklik = 5
                can_cubugu_x = screen_x + kare_genisligi // 2 - can_cubugu_genislik // 2
                can_cubugu_y = screen_y - 10
                pygame.draw.rect(ekran, (255, 0, 0), (can_cubugu_x, can_cubugu_y, can_cubugu_genislik, can_cubugu_yukseklik))
                can_orani = self.can / self.maximum_can
                pygame.draw.rect(ekran, (0, 255, 0), (can_cubugu_x, can_cubugu_y, can_cubugu_genislik * can_orani, can_cubugu_yukseklik))

    def hasar_al(self, miktar):
        if not self.canli_mi():
            return
        self.can -= miktar
        self.vuruldu = True
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
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self.on_ground = False

        # Dikey çarpışma kontrolü
        for rect in collision_rects:
            if self.rect.colliderect(rect):
                if self.velocity_y > 0:
                    self.rect.bottom = rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = rect.bottom
                    self.velocity_y = 0

        # Görsel pozisyonu günceller
        self.x = self.rect.centerx
        self.y = self.rect.centery

class Dusman(Karakter):
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        super().__init__(x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki)
        self.baslangic_x = x
        self.baslangic_y = y
        self.durum = DEVRIYE
        self.devriye_noktasi_1 = (x - 150, y)
        self.devriye_noktasi_2 = (x + 150, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.jump_power = -10
        self.son_ziplama_zamani = 0
        self.ziplama_bekleme_suresi = 500

    def platform_kontrolu(self, collision_rects, hedef_x, hedef_y):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_ziplama_zamani < self.ziplama_bekleme_suresi:
            return
        
        yon = 1 if hedef_x > self.x else -1
        kontrol_noktasi_x = self.rect.centerx + yon * (self.rect.width // 2 + 10)
        kontrol_noktasi_y = self.rect.bottom

        for rect in collision_rects:
            if rect.collidepoint(kontrol_noktasi_x, kontrol_noktasi_y - 10):
                self.velocity_y = self.jump_power
                self.animasyon_degistir("Jump")
                self.son_ziplama_zamani = simdiki_zaman
                break

    def guncelle(self, collision_rects):
        self.update_physics(collision_rects)
        if not self.canli_mi():
            if self.mevcut_animasyon != "Dead":
                self.mevcut_animasyon = "Dead"
                self.kare_indeksi = 0
            return

        if self.vuruldu and self.kare_indeksi >= len(self.animasyonlar["Hurt"]) - 1:
            self.vuruldu = False
            if self.canli_mi():
                self.animasyon_degistir("Idle")

        if self.mevcut_animasyon == "Jump" and self.on_ground and \
        self.kare_indeksi >= len(self.animasyonlar["Jump"]) - 1:
            self.animasyon_degistir("Idle")

        if self.durum == DEVRIYE:
            self.devriye_et(collision_rects)

    def devriye_et(self, collision_rects):
        dx = self.hedef_x - self.x
        mesafe = abs(dx)
        
        if mesafe > self.hiz:
            self.rect.x += (dx / mesafe) * self.hiz
            for rect in collision_rects:
                if self.rect.colliderect(rect):
                    if dx > 0:
                        self.rect.right = rect.left
                        self.platform_kontrolu(collision_rects, self.hedef_x, self.hedef_y)
                    elif dx < 0:
                        self.rect.left = rect.right
                        self.platform_kontrolu(collision_rects, self.hedef_x, self.hedef_y)
            self.sola_donuk = dx < 0
            if self.velocity_y == 0:
                self.animasyon_degistir("Walk")
        else:
            if (self.hedef_x, self.hedef_y) == self.devriye_noktasi_1:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_2
            else:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_1
            self.animasyon_degistir("Idle")

        self.x = self.rect.centerx
        self.y = self.rect.bottom

class NinjaMonk(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7,
            "Walk": 7,
            "Run": 8,
            "Jump": 9,
            "Hurt": 4,
            "Dead": 5,
            "Cast": 5,
            "Blade": 6,
            "Attack_1": 5,
            "Attack_2": 5,
        }
        super().__init__(x, y, hiz=3, can=50, guc=10, sprite_klasoru="ENEMIES/ninja/Ninja_Monk", animasyonlar=animasyonlar, sprite_soneki="Monk")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 500, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class NinjaPeasant(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6,
            "Walk": 8,
            "Run": 6,
            "Jump": 10,
            "Hurt": 2,
            "Dead": 4,
            "Disguise": 9,
            "Attack_1": 6,
            "Attack_2": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=5, sprite_klasoru="ENEMIES/ninja/Ninja_Peasant", animasyonlar=animasyonlar, sprite_soneki="Peasant")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class NinjaKunoichi(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6,
            "Walk": 8,
            "Run": 8,
            "Jump": 8,
            "Hurt": 2,
            "Dead": 4,
            "Cast": 6,
            "Attack_1": 6,
            "Attack_2": 8,
        }
        super().__init__(x, y, hiz=1, can=40, guc=20, sprite_klasoru="ENEMIES/ninja/Ninja_Kunoichi", animasyonlar=animasyonlar, sprite_soneki="Kunoichi")
        self.devriye_noktasi_1 = (x - 150, y)
        self.devriye_noktasi_2 = (x + 150, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class WarriorMan3(Dusman):
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
        super().__init__(x, y, hiz=2, can=100, guc=10, sprite_klasoru="ENEMIES/warrior/Man_3", animasyonlar=animasyonlar, sprite_soneki="Man3")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1


def draw_map(tmx_data, surface, camera_x, camera_y):
    surface.fill((0, 0, 0))
    start_x = max(0, int(camera_x / tmx_data.tilewidth))
    end_x = min(tmx_data.width, int((camera_x + genislik) / tmx_data.tilewidth) + 2)
    start_y = max(0, int(camera_y / tmx_data.tileheight))
    end_y = min(tmx_data.height, int((camera_y + yukseklik) / tmx_data.tileheight) + 2)
    offset_x = -(camera_x % tmx_data.tilewidth)
    offset_y = -(camera_y % tmx_data.tileheight)

    current_time = pygame.time.get_ticks()
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    gid = layer.data[y][x]
                    if gid:
                        tile_properties = tmx_data.get_tile_properties_by_gid(gid)
                        if tile_properties and 'frames' in tile_properties:
                            frames = tile_properties['frames']
                            total_duration = sum(frame[1] for frame in frames)
                            if not frames or total_duration <= 0:
                                tile_image = tmx_data.get_tile_image_by_gid(gid)
                            else:
                                elapsed_time = current_time % total_duration
                                frame_time = 0
                                for frame in frames:
                                    frame_time += frame[1]
                                    if elapsed_time <= frame_time:
                                        tile_image = tmx_data.get_tile_image_by_gid(frame[0])
                                        break
                        else:
                            tile_image = tmx_data.get_tile_image_by_gid(gid)
                        if tile_image:
                            screen_x = (x - start_x) * tmx_data.tilewidth + offset_x
                            screen_y = (y - start_y) * tmx_data.tileheight + offset_y
                            surface.blit(tile_image, (screen_x, screen_y))


npc_listesi = [
    NinjaMonk(300, 1200),
    NinjaPeasant(400, 1200),
    NinjaKunoichi(500, 1200),
    WarriorMan3(700, 1200),
]

# Font
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# Ana döngü
durum = True
son_animasyon_zamani = pygame.time.get_ticks()
animasyon_gecikmesi = 100

while durum:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            durum = False

    # Kamera sabit 
    camera_x = max(0, min(500 - genislik // 2, map_genislik - genislik))
    camera_y = max(0, min(1200 - yukseklik // 2, map_yukseklik - yukseklik))

    # Güncelleme
    for npc in npc_listesi:
        npc.guncelle(collision_rects)

    if pygame.time.get_ticks() - son_animasyon_zamani > animasyon_gecikmesi:
        for npc in npc_listesi:
            npc.animasyonu_guncelle()
        son_animasyon_zamani = pygame.time.get_ticks()

    # Çizim
    draw_map(tmx_data, ekran, camera_x, camera_y)
    for npc in npc_listesi:
        npc.ciz(ekran, camera_x, camera_y)
        durum_rengi = (0, 255, 0) if npc.durum == DEVRIYE else (255, 255, 255)
        pygame.draw.circle(ekran, durum_rengi, (int(npc.x - camera_x), int(npc.y - camera_y - 50)), 5)
        pygame.draw.circle(ekran, (255, 0, 0), (int(npc.hedef_x - camera_x), int(npc.hedef_y - camera_y)), 5)

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
