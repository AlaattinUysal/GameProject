import pygame
import os
import random
import math

pygame.init()

# Pencere ayarları
genislik = 1600
yukseklik = 900
ekran = pygame.display.set_mode((genislik , yukseklik))

saat = pygame.time.Clock()
FPS=60

#durumlar
DEVRIYE="devriye"
TAKIP="takip"
SALDIRI="saldiri"
GERI_GIT="geri git"

class Karakter:
    def __init__(self, x, y, hiz, can,guc, sprite_klasoru, animasyonlar, sprite_soneki):
        self.x = x
        self.y = y
        self.hiz = hiz
        self.can = can
        self.maximum_can=can
        self.guc=guc
        self.sola_donuk = False
        self.animasyonlar = {} 
        self.mevcut_animasyon = "Idle"  
        self.kare_indeksi = 0
        self.sprite_soneki = sprite_soneki   
        
        
        self.temel_yol = os.path.dirname(os.path.abspath(__file__))  
        self.sprite_klasoru = os.path.abspath(os.path.join(self.temel_yol, "..", sprite_klasoru))
        
        self.animasyonlari_yukle(animasyonlar)
        self.animasyon_hizi=100
        self.son_animasyon_guncelleme=pygame.time.get_ticks()
        self.olum_animasyonu_tamamlandi=False
        self.vuruyor=False
        self.vuruldu=False
        self.vurma_zamani=0


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
                print(f"{animasyon_adi} animasyonu yüklendi: {len(kareler)} kare")
            except pygame.error as e:
                print(f"Hata: {resim_yolu} yüklenemedi!", e)


    def animasyonu_guncelle(self):
        simdiki_zaman = pygame.time.get_ticks()
        if simdiki_zaman - self.son_animasyon_guncelleme > self.animasyon_hizi:
            if self.mevcut_animasyon in self.animasyonlar:
                animasyon_kareleri = self.animasyonlar[self.mevcut_animasyon]
                if animasyon_kareleri:
                    if self.mevcut_animasyon=="Dead" and self.kare_indeksi==len(animasyon_kareleri)-1:
                        self.olum_animasyonu_tamamlandi=True
                    elif not(self.mevcut_animasyon=="Dead" and self.olum_animasyonu_tamamlandi):
                        self.kare_indeksi = (self.kare_indeksi + 1) % len(animasyon_kareleri)
                    
                    self.son_animasyon_guncelleme = simdiki_zaman

    def animasyonu_degistir(self, yeni_animasyon):
        if self.mevcut_animasyon != yeni_animasyon:
            self.mevcut_animasyon = yeni_animasyon
            self.kare_indeksi = 0

    def ciz(self, ekran):
        if self.mevcut_animasyon in self.animasyonlar:
            animasyon_kareleri = self.animasyonlar[self.mevcut_animasyon]
            if animasyon_kareleri and 0<=self.kare_indeksi<len(animasyon_kareleri):
                kare = animasyon_kareleri[self.kare_indeksi]
                if self.sola_donuk:
                    kare = pygame.transform.flip(kare, True, False)
                
                kare_genisligi = kare.get_width()
                kare_yuksekligi = kare.get_height()
                
                ekran.blit(kare, (self.x - kare_genisligi // 2, self.y - kare_yuksekligi // 2))

                can_cubugu_genislik=50
                can_cubugu_yukseklik=5
                can_cubugu_x=self.x-can_cubugu_genislik//2
                can_cubugu_y=self.y-kare_yuksekligi//2-10

                pygame.draw.rect(ekran,(255,0,0),(can_cubugu_x,can_cubugu_y,can_cubugu_genislik,can_cubugu_yukseklik))
                can_orani=self.can/self.maximum_can
                pygame.draw.rect(ekran,(0,255,0),(can_cubugu_x,can_cubugu_y,can_cubugu_genislik*can_orani,can_cubugu_yukseklik))

    def hasar_al(self,miktar,saldiran_x=None,saldiran_y=None):
        self.can-=miktar
        self.vuruldu=True
        self.mevcut_animasyon="Hurt"
        if self.can<=0:
            self.can=0
            self.mevcut_animasyon="Dead"
            self.olum_animasyonu_tamamlandi=False

    def canli_mi(self):
        return self.can>0
        
    def mesafe_hesapla(self, hedef_x, hedef_y):
        dx = hedef_x - self.x
        dy = hedef_y - self.y    
        return math.sqrt(dx ** 2 + dy ** 2)

class Dusman(Karakter):
    def __init__(self, x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki):
        super().__init__(x, y, hiz, can, guc, sprite_klasoru, animasyonlar, sprite_soneki)
        self.baslangic_x = self.x
        self.baslangic_y = self.y
        self.devriye_mesafesi=500
        self.tespit_mesafesi=300
        self.saldiri_mesafesi=100
        self.durum=DEVRIYE
        self.hedef_x,self.hedef_y=self.yeni_hedef_belirle()
        self.son_konum_degisimi=pygame.time.get_ticks()
        self.konum_degisim_suresi=3000
        self.geri_gitme_hizi=self.hiz*1.5
        self.geri_gitme_mesafesi=100
        self.geri_gitme_aktif=False
        self.geri_gitme_baslangic_x=0
        self.geri_gitme_baslangic_y=0
        self.saldiran_x=0
        self.saldiran_y=0

        self.hasar_zamani=0
        self.hasar_bekleme_suresi=800

    def yeni_hedef_belirle(self):
        hedef_x=self.baslangic_x+random.randint(-self.devriye_mesafesi,self.devriye_mesafesi)
        hedef_y=self.baslangic_y+random.randint(-self.devriye_mesafesi,self.devriye_mesafesi)

        hedef_x=max(50,min(hedef_x,genislik-50))
        hedef_y=max(50,min(hedef_y,yukseklik-50))

        return hedef_x,hedef_y
    
    def karakter_tespit_et(self,karakter):
        mesafe=self.mesafe_hesapla(karakter.x,karakter.y)
        if mesafe<=self.tespit_mesafesi:
            return True
        return False
    
    def hasar_al(self,miktar,saldiran_x=None,saldiran_y=None):
        super().hasar_al(miktar)

        self.hasar_zamani=pygame.time.get_ticks()

        if self.canli_mi() and saldiran_x is not None and saldiran_y is not None:
            self.geri_gitme_aktif=True
            self.geri_gitme_baslangic_x=self.x
            self.geri_gitme_baslangic_y=self.y
            self.saldiran_x=saldiran_x
            self.saldiran_y=saldiran_y
            
            self.sola_donuk=self.x>saldiran_x

            self.durum=GERI_GIT
    
    def geri_git(self):
        dx=self.x-self.saldiran_x
        dy=self.y-self.saldiran_y
        mesafe=math.sqrt(dx**2+dy**2)

        if mesafe>0:
            dx=dx/mesafe*self.geri_gitme_hizi
            dy=dy/mesafe*self.geri_gitme_hizi

            yeni_x=self.x+dx
            yeni_y=self.y+dy

            self.sola_donuk=self.x>self.saldiran_x

            self.x=max(50,min(yeni_x,genislik-50))
            self.y=max(50,min(yeni_y,yukseklik-50))

            if not self.vuruldu:
                self.mevcut_animasyon="Walk"

                baslangictan_mesafe=self.mesafe_hesapla(self.geri_gitme_baslangic_x,self.geri_gitme_baslangic_y)
                if baslangictan_mesafe>=self.geri_gitme_mesafesi:
                    self.geri_gitme_aktif=False
                    self.durum=DEVRIYE
    
    def guncelle(self):
        if not self.canli_mi():
            self.mevcut_animasyon="Dead"
            return
        
        simdiki_zaman=pygame.time.get_ticks()
        if self.durum==GERI_GIT:
            if self.geri_gitme_aktif:
                self.geri_git()

                if self.vuruldu and simdiki_zaman-self.hasar_zamani>self.hasar_bekleme_suresi:
                    self.vuruldu=False
                    self.animasyonu_degistir="Walk" 

                self.animasyonu_guncelle()

            else:
                self.durum=DEVRIYE
                if not self.vuruldu:
                    self.animasyonu_degistir("Idle")
            return

        if self.vuruldu and simdiki_zaman-self.hasar_zamani>self.hasar_bekleme_suresi:
            self.vuruldu=False
            self.canli_mi()
            self.animasyonu_degistir("Idle")

        if self.vuruyor and self.kare_indeksi>=len(self.animasyonlar["Attack_1"])-1:
            self.vuruyor=False
            self.animasyonu_degistir("Idle")

        if self.vuruldu:
            return
        
        if self.mesafe_hesapla(self.hedef_x, self.hedef_y) < self.hiz or \
        simdiki_zaman - self.son_konum_degisimi > self.konum_degisim_suresi:
            self.hedef_x, self.hedef_y = self.yeni_hedef_belirle()
            self.son_konum_degisimi = simdiki_zaman
        
        if self.durum == DEVRIYE:
            self.devriye_et()
        
    def devriye_et(self):
        dx = self.hedef_x - self.x
        dy = self.hedef_y - self.y
        mesafe = math.sqrt(dx**2 + dy**2)
    
        if mesafe > self.hiz:
            self.x += (dx / mesafe) * self.hiz
            self.y += (dy / mesafe) * self.hiz
            self.sola_donuk = dx < 0
        
            self.animasyonu_degistir("Walk")
        else:

            self.animasyonu_degistir("Idle")
    
    def saldiri(self, karakter=None):
        if not self.vuruyor:
            self.vuruyor = True
            self.mevcut_animasyon = "Attack_1"
            self.kare_indeksi = 0
            
            if karakter:
                karakter.hasar_al(self.guc)
                
                self.sola_donuk = karakter.x < self.x
        
class NinjaMonk(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":7,
            "Walk": 7,
            "Run": 8,
            "Jump":9,
            "Hurt":4,
            "Dead":5,
            "Cast":5,
            "Blade":6,
            "Attack_1":5,
            "Attack_2":5,     
        }
        super().__init__(x, y, hiz=3, can=50,guc=10, sprite_klasoru="ENEMIES/ninja/Ninja_Monk", animasyonlar=animasyonlar, sprite_soneki="Monk")

class NinjaPeasant(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":6,
            "Walk": 8,  
            "Run": 6,   
            "Jump":10,
            "Hurt":2,
            "Dead":4,
            "Disguise":9,
            "Attack_1":6,
            "Attack_2":4,
        }
        super().__init__(x, y, hiz=2, can=70,guc=5, sprite_klasoru="ENEMIES/ninja/Ninja_Peasant", animasyonlar=animasyonlar, sprite_soneki="Peasant")

class NinjaKunoichi(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":6,
            "Walk": 8,  
            "Run": 8,   
            "Jump":8,
            "Hurt":2,
            "Dead":4,
            "Cast":6,
            "Attack_1":6,
            "Attack_2":8,
        }
        super().__init__(x, y, hiz=1, can=40,guc=20, sprite_klasoru="ENEMIES/ninja/Ninja_Kunoichi", animasyonlar=animasyonlar, sprite_soneki="Kunoichi")

class WarriorMan3(Dusman):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle":6,
            "Idle_2":6,
            "Walk": 12,  
            "Run": 12,   
            "Jump":10,
            "Hurt":3,
            "Dead":5,
            "Run+Attack":5,
            "Attack_1":4,
            "Attack_2":5,
        }
        super().__init__(x, y, hiz=2, can=100,guc=10, sprite_klasoru="ENEMIES/warrior/Man_3", animasyonlar=animasyonlar, sprite_soneki="Man3")

pygame.font.init()
font = pygame.font.SysFont('Arial', 24)
npc_listesi = [
    NinjaMonk(100, 100),
    NinjaPeasant(300, 200), 
    NinjaKunoichi(500, 300), 
    WarriorMan3(700, 400),
]

durum = True
son_animasyon_zamani = pygame.time.get_ticks()
animasyon_gecikmesi = 100
while durum:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            durum = False

    simdiki_zaman = pygame.time.get_ticks()


    ekran.fill((30, 30, 30))  

    for npc in npc_listesi:
        npc.guncelle()
        npc.ciz(ekran)

        durum_rengi=(255,255,255)
        if npc.durum==DEVRIYE:
            durum_rengi=(0,255,0) #yeşil
        elif npc.durum==TAKIP:
            durum_rengi=(255,255,0) #sarı
        elif npc.durum==SALDIRI:
            durum_rengi=(255,0,0) #kırmızı
        elif npc.durum==GERI_GIT:
            durum_rengi=(0,0,0)

        pygame.draw.circle(ekran, durum_rengi, (int(npc.x), int(npc.y - 50)), 5)

        pygame.draw.circle(ekran, (255, 0, 0), (npc.hedef_x, npc.hedef_y), 5)

    if simdiki_zaman - son_animasyon_zamani > animasyon_gecikmesi:
        for npc in npc_listesi:
            npc.animasyonu_guncelle()
        son_animasyon_zamani = simdiki_zaman
        
    pygame.display.flip()
    saat.tick(FPS)  

pygame.quit()
