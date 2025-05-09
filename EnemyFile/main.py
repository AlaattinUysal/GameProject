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
tmx_data, map_genislik, map_yukseklik = load_map('C:/Users/özer/Desktop/sw_eng_project/sw_eng_project/levels/village/village.tmx')
collision_rects = get_collision_rects(tmx_data)
player_spawn = get_player_spawn(tmx_data)

# Player character
ana_karakter = AnaKarakter(*player_spawn)

# Enemy list
dusman_listesi = [
    #enemy_types.NinjaMonk(300, 1200),
    #enemy_types.Wizard(400, 1200),
    #enemy_types.NinjaPeasant(500, 1200),
    #enemy_types.KarasuTengu(800, 1200),
    #enemy_types.Kitsune(1000, 1200),
    #enemy_types.YamabushiTengu(1200, 1200),
    #enemy_types.BlackWolf(1400, 1200),
    #enemy_types.RedWolf(1600, 1200),
    #enemy_types.WhiteWolf(1800, 1200),
    #enemy_types.Minotaur1(2000, 1200),
    #enemy_types.Minotaur2(2200, 1200),
    #enemy_types.Minotaur3(2400, 1200),
    #enemy_types.Copper(2600, 1200),
    #enemy_types.Lava(2800, 1200),
    #enemy_types.Stone(3000, 1200),
    #enemy_types.Gladiator1(3200, 1200),
    #enemy_types.Gladiator2(3400, 1200),
    #enemy_types.Gladiator3(3600, 1200),
]

# Camera settings
camera_x, camera_y = 0, 0
CAMERA_LERP = 0.05
animasyon_gecikmesi = 100
son_animasyon_zamani = pygame.time.get_ticks()

# Main loop
durum = True
while durum:
    for olay in pygame.event.get():
        if olay.type == pygame.QUIT:
            durum = False
        elif olay.type == pygame.KEYDOWN and ana_karakter.canli_mi():
            if olay.key == pygame.K_SPACE:
                ana_karakter.saldiri(dusman_listesi)

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
    anim_surface = FONT.render(animasyon_bilgisi, True, (255, 255, 0))
    ekran.blit(anim_surface, (10, 70))

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()
sys.exit()
