import pygame
import os
import random
import math
import pytmx
import sys

pygame.init()

# Pencereyi açma
genislik = 1600
yukseklik = 900
ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("Ninja Savaşi")

saat = pygame.time.Clock()
FPS = 60

# Durum sabitleri
DEVRIYE = "devriye"
TAKIP = "takip"
SALDIRI = "saldiri"


# Harita yükleme
tmx_data = pytmx.load_pygame('C:/Users/özer/Desktop/sw_eng_project/sw_eng_project/levels/village/village.tmx')  
#tmx_data = pytmx.load_pygame('C:/Users/özer/Desktop/sw_eng_project/sw_eng_project/levels/frozen_cave/frozen cave.tmx')  
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

# Başlangıç pozisyonu
player_spawn = (200, 100)
for layer in tmx_data.layers:
    if isinstance(layer, pytmx.TiledObjectGroup) and layer.name.lower() == "spawn":
        for nesne in layer:
            if nesne.name.lower() == "spawn_point":
                player_spawn = (nesne.x, nesne.y)

# Kamera ayarları
camera_x, camera_y = 0, 0

class Karakter:
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        self.rect = pygame.Rect(x - 50, y - 50, 100, 100)  # Çarpışma için dikdörtgen
        self.hitbox=pygame.Rect(0,0,30,60)
        self.ground_check=pygame.Rect(0,0,24,5)
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
        self.velocity_y = 0  # Dikey hız (yerçekimi için)
        self.gravity = 0.5  # Yerçekimi
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

class AnaKarakter(Karakter):
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
        super().__init__(x, y-50, hiz=5, can=100, guc=10, sprite_klasoru="ENEMIES/warrior/Man_3", animasyonlar=animasyonlar, sprite_soneki="Man3")
        self.saldiri_menzili = 100
        self.jump_power = -10

    def hareket_et(self, tuslar, collision_rects):
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

        # Animasyon belirleme
        if hareket_var and not self.vuruldu:
            self.animasyon_degistir("Run")
        elif not self.vuruyor and not self.vuruldu and self.canli_mi():
            self.animasyon_degistir("Idle")

        self.x = self.rect.centerx
        self.y = self.rect.centery

    def saldiri(self, dusman_listesi):
        if not self.canli_mi() or self.vuruyor:
            return
        self.vuruyor = True
        self.animasyon_degistir("Attack_1")
        self.vurma_zamani = pygame.time.get_ticks()
        for dusman in dusman_listesi:
            if dusman.canli_mi() and self.mesafe_hesapla(dusman.x, dusman.y) < self.saldiri_menzili:
                dusman.hasar_al(self.guc)

    def guncelle(self, collision_rects):
        self.update_physics(collision_rects)
        if self.vuruyor and self.kare_indeksi >= len(self.animasyonlar["Attack_1"]) - 1:
            self.vuruyor = False
            self.animasyon_degistir("Idle")
        if self.vuruldu and self.kare_indeksi >= len(self.animasyonlar["Hurt"]) - 1:
            self.vuruldu = False
            if self.canli_mi():
                self.animasyon_degistir("Idle")

class YakinDusman(Karakter):
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        super().__init__(x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki)
        self.baslangic_x = x
        self.baslangic_y = y
        self.tespit_mesafesi = 300
        self.saldiri_mesafesi = 100
        self.durum = DEVRIYE
        self.devriye_noktasi_1=(x-150,y)
        self.devriye_noktasi_2=(x+150,y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.son_konum_degisimi = pygame.time.get_ticks()
        self.son_saldiri_zamani = 0
        self.saldiri_bekleme_suresi = 1000
        self.jump_power = -10
        self.son_ziplama_zamani = 0
        self.ziplama_bekleme_suresi = 500
    
    def platform_kontrolu(self, collision_rects,hedef_x,hedef_y):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_ziplama_zamani < self.ziplama_bekleme_suresi or not self.on_ground:
            return
        
        yon = 1 if hedef_x >self.x else -1
        kontrol_rect = pygame.Rect(0, 0, 20, self.hitbox.height + 10)
        kontrol_rect.centerx = self.hitbox.centerx + yon * (self.hitbox.width // 2 + 15)
        kontrol_rect.bottom = self.hitbox.bottom

        for rect in collision_rects:
            if kontrol_rect.colliderect(rect):
                # Engel varsa ve yerdeysek zıplar
                self.velocity_y = self.jump_power
                self.animasyon_degistir("Jump")
                self.son_ziplama_zamani = simdiki_zaman
                break
            zemin_kontrol_rect = pygame.Rect(0, 0, 10, 10)
            zemin_kontrol_rect.centerx = self.hitbox.centerx + yon * (self.hitbox.width // 2 + 10)
            zemin_kontrol_rect.top = self.hitbox.bottom
            if not any(zemin_kontrol_rect.colliderect(r) for r in collision_rects):
                self.velocity_y = self.jump_power
                self.animasyon_degistir("Jump")
                self.son_ziplama_zamani = simdiki_zaman
                break

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
        
        self.platform_kontrolu(collision_rects,self.hedef_x,self.hedef_y)
        
        if mesafe > self.hiz:
            move_dx=(dx / mesafe) * self.hiz
            move_dx=handle_horizontal_collision(move_dx)
            self.sola_donuk = dx < 0
            if self.velocity_y==0:
                self.animasyon_degistir("Walk")
        else:
            if (self.hedef_x, self.hedef_y) == self.devriye_noktasi_1:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_2
            else:
                self.hedef_x, self.hedef_y = self.devriye_noktasi_1
            self.animasyon_degistir("Idle")

        self.x = self.rect.centerx
        self.y = self.rect.bottom

    def takip_et(self, karakter, collision_rects):
        dx = karakter.x - self.x
        dy = karakter.y - self.y
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
        
        if abs(dy) > 50 and self.on_ground:
            self.platform_kontrolu(collision_rects,karakter.x,karakter.y)

        if mesafe > self.hiz:
            move_dx = (dx / mesafe) * self.hiz * 1.5
            move_dx = handle_horizontal_collisions(move_dx)
            self.sola_donuk = dx < 0
            if move_dx != 0 and self.on_ground and not self.vuruyor and not self.vuruldu:
                self.animasyon_degistir("Run")
        self.x = self.rect.centerx
        self.y = self.rect.bottom

    def saldiri(self, karakter):
        if not karakter.canli_mi() or not self.canli_mi():
            return
        simdiki_zaman = pygame.time.get_ticks()
        if not self.vuruyor and simdiki_zaman - self.son_saldiri_zamani >= self.saldiri_bekleme_suresi:
            self.vuruyor = True
            self.mevcut_animasyon = random.choice(["Attack_1", "Attack_2"])
            self.kare_indeksi = 0
            self.son_saldiri_zamani = simdiki_zaman
            self.sola_donuk = karakter.x < self.x
        
            if self.mesafe_hesapla(karakter.x, karakter.y) <= self.saldiri_mesafesi:
                karakter.hasar_al(self.guc)
                print(f"Düşman vurdu! Ana karakter can: {karakter.can}")  
        elif not self.vuruyor and self.on_ground:
            self.animasyon_degistir("Idle")
    
    def guncelle(self, karakter, collision_rects):
        self.update_physics(collision_rects)
        if not self.canli_mi():
            if self.mevcut_animasyon != "Dead":
                self.mevcut_animasyon = "Dead"
                self.kare_indeksi = 0
            return

        mesafe = self.mesafe_hesapla(karakter.x, karakter.y)
        if not karakter.canli_mi():
            self.durum = DEVRIYE
        elif mesafe <= self.saldiri_mesafesi:
            self.durum = SALDIRI
        elif mesafe <= self.tespit_mesafesi:
            self.durum = TAKIP
        else:
            self.durum = DEVRIYE

        if self.vuruldu and self.mevcut_animasyon == "Hurt":
            if self.kare_indeksi >= len(self.animasyonlar["Hurt"]) - 1:
                self.vuruldu = False
                if self.canli_mi():
                    if not self.on_ground:
                        self.animasyon_degistir("Jump")
                    elif self.durum == DEVRIYE:
                        if abs(self.hedef_x - self.x) > self.hiz:
                            self.animasyon_degistir("Walk")
                        else:
                            self.animasyon_degistir("Idle")
                    elif self.durum == TAKIP:
                        if abs(karakter.x - self.x) > self.hiz:
                            self.animasyon_degistir("Run")
                        else:
                            self.animasyon_degistir("Idle")
                    elif self.durum == SALDIRI:
                        self.animasyon_degistir("Idle")  
                print(f"Hurt animasyonu bitti, yeni animasyon: {self.mevcut_animasyon}")

        elif self.vuruyor:
            if self.mevcut_animasyon in ["Attack_1", "Attack_2", "Attack_3"] and self.kare_indeksi >= len(self.animasyonlar[self.mevcut_animasyon]) - 1:
                self.vuruyor = False
                if self.canli_mi():
                    self.animasyon_degistir("Idle")

        elif self.mevcut_animasyon == "Jump" and self.on_ground and self.kare_indeksi >= len(self.animasyonlar["Jump"]) - 1:
            self.animasyon_degistir("Idle")

        elif self.velocity_y != 0 and not self.on_ground and self.mevcut_animasyon not in ["Hurt", "Jump"]:
            self.animasyon_degistir("Jump")

        if not self.vuruldu and not self.vuruyor:  
            if self.durum == DEVRIYE:
                self.devriye_et(collision_rects)
            elif self.durum == TAKIP:
                self.takip_et(karakter, collision_rects)
            elif self.durum == SALDIRI:
                self.saldiri(karakter)

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
        
        # Charge animasyonu
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

        # Hedefe doğru yön vektörü ve açı hesaplama
        dx = hedef_x - x
        dy = hedef_y - y
        mesafe = math.sqrt(dx**2 + dy**2)
        if mesafe > 0:
            self.vx = (dx / mesafe) * hiz
            self.vy = (dy / mesafe) * hiz
            # Merminin yönüne göre açı hesaplama
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

class DusmanMenzilli(YakinDusman):
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        super().__init__(x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki)
        self.mermi_hizi = 4
        self.mermi_menzili = 500
        self.saldiri_mesafesi = 300
        self.mermiler = []

    def saldiri(self, karakter):
        if not karakter.canli_mi() or not self.canli_mi():
            return
        simdiki_zaman = pygame.time.get_ticks()
        if not self.vuruyor and simdiki_zaman - self.son_saldiri_zamani >= self.saldiri_bekleme_suresi:
            self.vuruyor = True
            self.mevcut_animasyon = "Fireball"
            self.kare_indeksi = 0
            self.sola_donuk = karakter.x < self.x
            
            mermi = Mermi(
                self.x, self.y, karakter.x, karakter.y, self.mermi_hizi, self.guc,
                sprite_klasoru="ENEMIES/wizard/Fire vizard", sprite_soneki="fire", kare_sayisi=6
            )
            self.mermiler.append(mermi)
            self.son_saldiri_zamani = simdiki_zaman

    def guncelle(self, karakter, collision_rects):
        super().guncelle(karakter, collision_rects)
        for mermi in self.mermiler[:]:
            mermi.guncelle()
            if mermi.carpisma_kontrolu(karakter):
                self.mermiler.remove(mermi)
            elif self.mesafe_hesapla(mermi.x, mermi.y) > self.mermi_menzili:
                self.mermiler.remove(mermi)

    def ciz(self, ekran, camera_x, camera_y):
        super().ciz(ekran, camera_x, camera_y)
        for mermi in self.mermiler:
            mermi.ciz(ekran, camera_x, camera_y)

class NinjaMonk(YakinDusman):
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
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class NinjaPeasant(YakinDusman):
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
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/ninja/Ninja_Peasant", animasyonlar=animasyonlar, sprite_soneki="Peasant")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class KarasuTengu(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8, 
            "Run": 8, 
            "Jump": 15, 
            "Hurt": 3,
            "Dead": 6,  
            "Attack_1": 6, 
            "Attack_2": 4,
            "Attack_3": 3,
        }
        super().__init__(x, y, hiz=2, can=100, guc=20, sprite_klasoru="ENEMIES/yokai/Karasu_tengu", animasyonlar=animasyonlar, sprite_soneki="Karasu")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Kitsune(DusmanMenzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8, 
            "Walk": 8, 
            "Run": 8, 
            "Jump": 10, 
            "Hurt": 2,
            "Dead": 10, 
            "Attack_1": 10, 
            "Attack_2": 10,
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/yokai/Kitsune", animasyonlar=animasyonlar, sprite_soneki="Kitsune")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300

class YamabushiTengu(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8, 
            "Run": 8, 
            "Jump": 15, 
            "Hurt": 3,
            "Dead": 6,  
            "Attack_1": 3, 
            "Attack_2": 6,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/yokai/Yamabushi_tengu", animasyonlar=animasyonlar, sprite_soneki="Yamabushi")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class BlackWolf(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8, 
            "Walk": 11, 
            "Run": 9, 
            "Jump": 11, 
            "Hurt": 2,
            "Dead": 2,  
            "Attack_1": 6, 
            "Attack_2": 4,
            "Attack_3": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/werewolf/Black_Werewolf", animasyonlar=animasyonlar, sprite_soneki="black")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class RedWolf(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8, 
            "Walk": 11, 
            "Run": 9, 
            "Jump": 11, 
            "Hurt": 2,
            "Dead": 2,  
            "Attack_1": 6, 
            "Attack_2": 4,
            "Attack_3": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/werewolf/Red_Werewolf", animasyonlar=animasyonlar, sprite_soneki="red")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class WhiteWolf(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8, 
            "Walk": 11, 
            "Run": 9, 
            "Jump": 11, 
            "Hurt": 2,
            "Dead": 2,  
            "Attack_1": 6, 
            "Attack_2": 4,
            "Attack_3": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/werewolf/White_Werewolf", animasyonlar=animasyonlar, sprite_soneki="white")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Minotaur1(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_1", animasyonlar=animasyonlar, sprite_soneki="Minotaur1")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Minotaur2(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_2", animasyonlar=animasyonlar, sprite_soneki="Minotaur2")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Minotaur3(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_3", animasyonlar=animasyonlar, sprite_soneki="Minotaur3")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1
    
class Copper(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8, 
            "Run": 8, 
            "Jump": 16, 
            "Hurt": 4,
            "Dead": 6,  
            "Attack_1": 6, 
            "Attack_2": 7,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/golem/Copper_Golem", animasyonlar=animasyonlar, sprite_soneki="Copper")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Lava(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8, 
            "Run": 10, 
            "Jump": 12, 
            "Hurt": 4,
            "Dead": 7,  
            "Attack_1": 5, 
            "Attack_2": 4,
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/golem/Lava_golem", animasyonlar=animasyonlar, sprite_soneki="Lava")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Stone(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 7, 
            "Run": 6, 
            "Jump": 13, 
            "Hurt": 4,
            "Dead": 9,  
            "Attack_1": 5, 
            "Attack_2": 4,
            "Attack_3": 2,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/golem/Stone_Golem", animasyonlar=animasyonlar, sprite_soneki="Stone")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1
    
class Gladiator1(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 10, 
            "Run": 10, 
            "Jump": 10, 
            "Hurt": 4,
            "Dead": 3,  
            "Attack_1": 5, 
            "Attack_2": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/gladiator/Gladiator_1", animasyonlar=animasyonlar, sprite_soneki="Gladiator1")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Gladiator2(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 10, 
            "Run": 10, 
            "Jump": 10, 
            "Hurt": 4,
            "Dead": 5,  
            "Attack_1": 5, 
            "Attack_2": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/gladiator/Gladiator_2", animasyonlar=animasyonlar, sprite_soneki="Gladiator2")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Gladiator3(YakinDusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 10, 
            "Run": 10, 
            "Jump": 10, 
            "Hurt": 4,
            "Dead": 5,  
            "Attack_1": 5, 
            "Attack_2": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/gladiator/Gladiator_3", animasyonlar=animasyonlar, sprite_soneki="Gladiator3")
        self.devriye_noktasi_1=(x-100,y)
        self.devriye_noktasi_2=(x+100,y)
        self.hedef_x,self.hedef_y=self.devriye_noktasi_1

class Wizard(DusmanMenzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7,
            "Walk": 6,
            "Run": 8,
            "Jump": 9,
            "Attack_1": 4,
            "Attack_2": 4,
            "Fireball": 8,
            "Flame_jet": 14,
            "Charge": 12,
            "Hurt": 3,
            "Dead": 6,
        }
        super().__init__(x, y, hiz=2, can=50, guc=15, sprite_klasoru="ENEMIES/wizard/Fire vizard", animasyonlar=animasyonlar, sprite_soneki="fire")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300


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


ana_karakter = AnaKarakter(*player_spawn)
dusman_listesi = [
    NinjaMonk(300, 1200),
    #Wizard(400, 1200),
    NinjaPeasant(500, 1200),
    KarasuTengu(800, 1200),
    #Kitsune(1000, 1200),
    YamabushiTengu(1200, 1200),
    BlackWolf(1400, 1200),
    RedWolf(1600, 1200),
    WhiteWolf(1800, 1200),
    #Minotaur1(2000, 1200),
    #Minotaur2(2200, 1200),
    #Minotaur3(2400, 1200),
    Copper(2600, 1200),
    Lava(2800, 1200),
    Stone(3000, 1200),
    Gladiator1(3200, 1200),
    Gladiator2(3400, 1200),
    Gladiator3(3600, 1200),
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
        elif olay.type == pygame.KEYDOWN:
            if olay.key == pygame.K_SPACE:
                ana_karakter.saldiri(dusman_listesi)

    tuslar = pygame.key.get_pressed()
    ana_karakter.hareket_et(tuslar, collision_rects)
    ana_karakter.guncelle(collision_rects)

    if pygame.time.get_ticks() - son_animasyon_zamani > animasyon_gecikmesi:
        ana_karakter.animasyonu_guncelle()
        for dusman in dusman_listesi:
            dusman.animasyonu_guncelle()
        son_animasyon_zamani = pygame.time.get_ticks()

    for dusman in dusman_listesi[:]:
        dusman.guncelle(ana_karakter, collision_rects)

    # Kamera güncellemesi
    CAMERA_LERP = 0.05  
    target_x = ana_karakter.x - genislik // 2
    target_y = ana_karakter.y - yukseklik // 2
    camera_x += (target_x - camera_x) * CAMERA_LERP
    camera_y += (target_y - camera_y) * CAMERA_LERP
    camera_x = max(0, min(camera_x, map_genislik - genislik))
    camera_y = max(0, min(camera_y, map_yukseklik - yukseklik))

    # Çizim
    draw_map(tmx_data, ekran, camera_x, camera_y)
    for dusman in dusman_listesi:
        dusman.ciz(ekran, camera_x, camera_y)
        durum_rengi = (255, 255, 255)
        if dusman.durum == DEVRIYE:
            durum_rengi = (0, 255, 0)
        elif dusman.durum == TAKIP:
            durum_rengi = (255, 255, 0)
        elif dusman.durum == SALDIRI:
            durum_rengi = (255, 0, 0)
        pygame.draw.circle(ekran, durum_rengi, (int(dusman.x - camera_x), int(dusman.y - camera_y - 50)), 5)

    ana_karakter.ciz(ekran, camera_x, camera_y)
    animasyon_bilgisi = f"Animasyon: {ana_karakter.mevcut_animasyon}, Kare: {ana_karakter.kare_indeksi}"
    anim_surface = font.render(animasyon_bilgisi, True, (255, 255, 0))
    ekran.blit(anim_surface, (10, 70))

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
