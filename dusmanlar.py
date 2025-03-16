import pygame
import os
import random
import math

pygame.init()

# Pencereyi aç
os.environ["SDL_VIDEO_CENTERED"]="1"
info=pygame.display.Info()
genislik,yukseklik=info.current_w,info.current_h
ekran=pygame.display.set_mode((genislik,yukseklik-50),pygame.RESIZABLE)

saat = pygame.time.Clock()
FPS=10

class Dusman:
    def __init__(self, x, y, hiz, guc, sprite_klasoru, animasyonlar, sprite_soneki="Monk"):
        self.x = x
        self.y = y
        self.hiz = hiz
        self.guc=guc
        self.hedef_x, self.hedef_y = self.yeni_hedef_belirle()
        self.sola_donuk = False
        self.animasyonlar = {} 
        self.mevcut_animasyon = "walk"  
        self.kare_indeksi = 0
        self.sprite_soneki = sprite_soneki   
        
        
        self.temel_yol = os.path.dirname(os.path.abspath(__file__))  
        self.sprite_klasoru = os.path.abspath(os.path.join(self.temel_yol, "..", sprite_klasoru))
        
        
        self.animasyonlari_yukle(animasyonlar)

    def yeni_hedef_belirle(self):
        hedef_x = random.randint(100, genislik - 100)
        hedef_y = random.randint(100, yukseklik - 100)

        return hedef_x, hedef_y

    def animasyonlari_yukle(self, animasyonlar):
        for animasyon_adi, kare_sayisi in animasyonlar.items():
            formatli_isim = f"{animasyon_adi.capitalize()}_{self.sprite_soneki}.png"  
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
                print(f"{animasyon_adi} animasyonu yüklendi: {len(kareler)} kare")
            except pygame.error as e:
                print(f"Hata: {resim_yolu} yüklenemedi!", e)

    def hedefe_dogru_hareket_et(self):
        dx = self.hedef_x - self.x
        dy = self.hedef_y - self.y
        mesafe = math.sqrt(dx**2 + dy**2)

        if mesafe > self.hiz:
            self.x += (dx / mesafe) * self.hiz
            self.y += (dy / mesafe) * self.hiz
        else:
            self.hedef_x, self.hedef_y = self.yeni_hedef_belirle()

        
        self.sola_donuk = dx < 0

    def animasyonu_guncelle(self):
        if self.mevcut_animasyon in self.animasyonlar:
            self.kare_indeksi = (self.kare_indeksi + 1) % len(self.animasyonlar[self.mevcut_animasyon])

    def ciz(self, ekran):
        if self.mevcut_animasyon in self.animasyonlar and len(self.animasyonlar[self.mevcut_animasyon]) > 0:
            kare = self.animasyonlar[self.mevcut_animasyon][self.kare_indeksi]
            if self.sola_donuk:
                kare = pygame.transform.flip(kare, True, False)
            
            
            kare_genisligi = kare.get_width()
            kare_yuksekligi = kare.get_height()
            
            
            ekran.blit(kare, (self.x - kare_genisligi // 2, self.y - kare_yuksekligi // 2))

class NinjaMonk(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":7,
            "walk": 7,
            "run": 8,
            "Jump":9,
            "Hurt":4,
            "Dead":5,
            "Cast":5,
            "Blade":6,
            "Attack_1":5,
            "Attack_2":5,     
        }
        super().__init__(x, y, hiz=3, guc=10, sprite_klasoru="ENEMIES/ninja/Ninja_Monk", animasyonlar=animasyonlar, sprite_soneki="Monk")

class NinjaPeasant(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":9,
            "walk": 8,  
            "run": 8,   
            "Jump":10,
            "Hurt":2,
            "Dead":4,
            "Disguise":9,
            "Attack_1":6,
            "Attack_2":4,
        }
        super().__init__(x, y, hiz=2, guc=15, sprite_klasoru="ENEMIES/ninja/Ninja_Peasant", animasyonlar=animasyonlar, sprite_soneki="Peasant")

class NinjaKunoichi(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":6,
            "walk": 8,  
            "run": 6,   
            "Jump":8,
            "Hurt":2,
            "Dead":4,
            "Cast":6,
            "Attack_1":6,
            "Attack_2":8,
        }
        super().__init__(x, y, hiz=4, guc=5, sprite_klasoru="ENEMIES/ninja/Ninja_Kunoichi", animasyonlar=animasyonlar, sprite_soneki="Kunoichi")

class WarriorMan3(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":6,
            "Idle_2":6,
            "walk": 12,  
            "run": 12,   
            "Jump":10,
            "Hurt":3,
            "Dead":5,
            "Run+Attack":5,
            "Attack_1":4,
            "Attack_2":5,
        }
        super().__init__(x, y, hiz=3, guc=10, sprite_klasoru="ENEMIES/warrior/Man_3", animasyonlar=animasyonlar, sprite_soneki="Man3")

npc_listesi = [
    NinjaMonk(100, 100),
    NinjaPeasant(300, 200), 
    NinjaKunoichi(500, 300), 
    WarriorMan3(700, 400),
]

durum = True
while durum:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            durum = False

    ekran.fill((30, 30, 30))  

    for npc in npc_listesi:
        npc.hedefe_dogru_hareket_et()
        npc.animasyonu_guncelle()
        npc.ciz(ekran)

        
        pygame.draw.circle(ekran, (255, 0, 0), (npc.hedef_x, npc.hedef_y), 10)  

    pygame.display.flip()
    saat.tick(FPS)  

pygame.quit()