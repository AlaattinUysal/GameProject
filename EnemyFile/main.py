import pygame
import sys
from config import GENISLIK, YUKSEKLIK, FPS, FONT, DEVRIYE, TAKIP, SALDIRI
from map_utils import load_map, get_collision_rects, get_player_spawn, draw_map
import enemy_types
from anakarakter import AnaKarakter

pygame.init()

# Window setup
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Ninja Savasi")
saat = pygame.time.Clock()

# Map loading
#tmx_data, map_genislik, map_yukseklik = load_map('C:/Users/özer/Desktop/GameProject-feature-player/levels/village/village.tmx')
tmx_data, map_genislik, map_yukseklik = load_map('C:/Users/özer/Desktop/GameProject-feature-player/levels/cyberpunk/cyberpunk.tmx')
#tmx_data,map_genislik,map_yukseklik=load_map('C:/Users/özer/Desktop/GameProject-feature-player/levels/frozen_cave/frozen_cave.tmx')
#tmx_data, map_genislik, map_yukseklik=load_map('C:/Users/özer/Desktop/GameProject-feature-player/levels/castle/castle.tmx')
#tmx_data, map_genislik, map_yukseklik=load_map('C:/Users/özer/Desktop/GameProject-feature-player/levels/lab/lab.tmx')
collision_rects = get_collision_rects(tmx_data)
player_spawn = get_player_spawn(tmx_data)

# Player character
ana_karakter = AnaKarakter(*player_spawn)

# Enemy list
#frozen cave düşmanları
""" enemy_types.NinjaMonk(1798, 1184),
    enemy_types.Wizard(1550, 192),
    enemy_types.KarasuTengu(1530, 544),
    enemy_types.BlackWolf(1180, 1152),
    enemy_types.RedWolf(650, 1120),
    enemy_types.WhiteWolf(2320, 832),
    enemy_types.Stone(1260, 896),
    enemy_types.BrownOrc(704,704),
    enemy_types.Knight1(2000,576),
    enemy_types.Hellhound3(200,1088),
    enemy_types.Witch2(593,288),
    enemy_types.NinjaPeasant(1200,1200),"""
#cyberpunk düşmanları
"""enemy_types.Minotaur1(653, 736),
    enemy_types.Minotaur2(3300, 864),
    enemy_types.Lava(2080, 352),
    enemy_types.Amazon1(1320,896),
    enemy_types.Amazon2(2950,128),
    enemy_types.CityMan1(900,896),
    enemy_types.Demon5(8400,256),
    enemy_types.Demon6(1930,480),
    enemy_types.Goblin1(2080,608),
    enemy_types.Goblin2(5200,288),
    enemy_types.Goblin3(8825,96),
    enemy_types.GreenOrc(7300,128),
    enemy_types.Hellhound1(400,1152),
    enemy_types.Knight2(2000,896),
    enemy_types.Knight3(9225,96),
    enemy_types.Lightning(1000,1152),
    enemy_types.Man1(6200,416),
    enemy_types.Man2(9625,96),
    enemy_types.Pyromancer2(4300,257),
    enemy_types.Pyromancer3(2050,1056),
    enemy_types.BattleMecha1(4800,736),
    enemy_types.Witch1(3900,992),"""
#lab düşmanları
""" enemy_types.Minotaur3(250, 160),
    enemy_types.GoblinKing(1800,672),
    enemy_types.Demon4(500,288),
    enemy_types.Mutant1(1207,288),
    enemy_types.Mutant2(1300,448),
    enemy_types.Mutant3(1875,352),
    enemy_types.Wanderer(950,672),"""
#castle düşmanları
"""enemy_types.Kitsune(1000, 752),
    enemy_types.Gladiator1(200, 176),
    enemy_types.Gladiator3(1700, 416),
    enemy_types.Man3(200,416),
    enemy_types.Pyromancer1(1700,752),
    enemy_types.VampireBat(1700,176),
    enemy_types.SamuraiCommander(1200,752),"""
dusman_listesi = [  
    #enemy_types.YamabushiTengu(1200, 1200),
    #enemy_types.Copper(2600, 1200),
    #enemy_types.Gladiator2(3400, 1200),
    #enemy_types.Amazon3(3000,1200),
    #enemy_types.AnimeKnight(2000,1200),
    #enemy_types.BattleMecha2(1000,1200),
    #enemy_types.BattleMecha3(1200,1200),
    #enemy_types.Berserk(1000,1200),
    #enemy_types.CityMan2(700,1200),
    #enemy_types.CityMan3(800,1200),
    #enemy_types.Demon1(670,1120),
    #enemy_types.Demon2(670,1120),
    #enemy_types.Demon3(2000,1200),
    #enemy_types.Enchantress(2900,1200),
    #enemy_types.Gorgon1(950,672),
    #enemy_types.Gorgon2(2300,1200),
    #enemy_types.Gorgon3(3100,1200),
    #enemy_types.Hellhound2(3200,1200),
    #enemy_types.HugeMushroom(1550,192),
    #enemy_types.Raider1(3500,1200),
    #enemy_types.Raider3(3200,1200),
    #enemy_types.Samurai(700,752),
    #enemy_types.Witch3(2600,1200),
    #enemy_types.WomanOrc(2600,1200),
]

# Camera settings
camera_x, camera_y = 0, 0
CAMERA_LERP = 0.05
animasyon_gecikmesi = 100
son_animasyon_zamani = pygame.time.get_ticks()

# Main loop
running = True
while running:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            running = False
        elif olay.type == pygame.KEYDOWN and ana_karakter.canli_mi():
            if olay.key == pygame.K_j:
                ana_karakter.saldiri(dusman_listesi, animasyon="Attack_1")
            elif olay.key == pygame.K_k:
                ana_karakter.saldiri(dusman_listesi, animasyon="Attack_2")
            elif olay.key == pygame.K_l:
                ana_karakter.saldiri(dusman_listesi, animasyon="Attack_3")   
    tuslar = pygame.key.get_pressed()
    if ana_karakter.canli_mi():
        ana_karakter.hareket_et(tuslar, collision_rects)
    
    ana_karakter.guncelle(collision_rects)

    # Update animations
    if pygame.time.get_ticks() - son_animasyon_zamani > animasyon_gecikmesi:
        ana_karakter.animasyonu_guncelle()
        for dusman in dusman_listesi:
            dusman.animasyonu_guncelle()
        son_animasyon_zamani = pygame.time.get_ticks()

    # Update enemies
    for dusman in dusman_listesi[:]:
        dusman.guncelle(ana_karakter, collision_rects)

    # Update camera
    target_x = ana_karakter.x - GENISLIK // 2
    target_y = ana_karakter.y - YUKSEKLIK // 2
    camera_x += (target_x - camera_x) * CAMERA_LERP
    camera_y += (target_y - camera_y) * CAMERA_LERP
    camera_x = max(0, min(camera_x, map_genislik - GENISLIK))
    camera_y = max(0, min(camera_y, map_yukseklik - YUKSEKLIK))

    # Draw
    draw_map(tmx_data, ekran, camera_x, camera_y, GENISLIK, YUKSEKLIK)
    for dusman in dusman_listesi:
        dusman.ciz(ekran, camera_x, camera_y)
        """durum_rengi = (255, 255, 255)
        if dusman.durum == DEVRIYE:
            durum_rengi = (0, 255, 0)
        elif dusman.durum == TAKIP:
            durum_rengi = (255, 255, 0)
        elif dusman.durum == SALDIRI:
            durum_rengi = (255, 0, 0)
        pygame.draw.circle(ekran, durum_rengi, (int(dusman.x - camera_x), int(dusman.y - camera_y - 50)), 5)"""

    ana_karakter.ciz(ekran, camera_x, camera_y)
    animasyon_bilgisi = f"Animasyon: {ana_karakter.mevcut_animasyon}, Kare: {ana_karakter.kare_indeksi}"
    anim_surface = FONT.render(animasyon_bilgisi, True, (255, 255, 0))
    ekran.blit(anim_surface, (10, 70))
    koordinat_bilgisi = f"X: {ana_karakter.x:.2f}, Y: {ana_karakter.y:.2f}"
    koordinat_surface = FONT.render(koordinat_bilgisi, True, (255, 255, 0))
    ekran.blit(koordinat_surface, (10, 100))

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
