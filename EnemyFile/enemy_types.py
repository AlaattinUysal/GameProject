from yakin import Yakin
from menzilli import Menzilli

class NinjaMonk(Yakin):
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
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class NinjaPeasant(Yakin):
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
        super().__init__(x, y, hiz=2, can=100, guc=10, sprite_klasoru="ENEMIES/ninja/Ninja_Peasant", animasyonlar=animasyonlar, sprite_soneki="Peasant")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class KarasuTengu(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class YamabushiTengu(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class BlackWolf(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class RedWolf(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class WhiteWolf(Yakin):
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
        self.devriye_noktasi_1 = (x - 120, y)
        self.devriye_noktasi_2 = (x + 120, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Minotaur1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack_1": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_1", animasyonlar=animasyonlar, sprite_soneki="Minotaur1")
        self.devriye_noktasi_1 = (x - 50, y)
        self.devriye_noktasi_2 = (x + 50, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Minotaur2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack_1": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_2", animasyonlar=animasyonlar, sprite_soneki="Minotaur2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Minotaur3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack_1": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_3", animasyonlar=animasyonlar, sprite_soneki="Minotaur3")
        self.devriye_noktasi_1 = (x - 150, y)
        self.devriye_noktasi_2 = (x + 150, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1
    
class Copper(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Lava(Yakin):
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
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Stone(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3
    
class Gladiator1(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Gladiator2(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Gladiator3(Yakin):
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Amazon1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 10, 
            "Run": 10, 
            "Jump": 11, 
            "Hurt": 4,
            "Dead": 4,  
            "Attack_1": 5, 
            "Attack_2": 3,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/amazon/Amazon_1", animasyonlar=animasyonlar, sprite_soneki="Amazon1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Amazon2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 10, 
            "Run": 10, 
            "Jump": 11, 
            "Hurt": 5,
            "Dead": 4,  
            "Attack_1": 5, 
            "Attack_2": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/amazon/Amazon_2", animasyonlar=animasyonlar, sprite_soneki="Amazon2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Amazon3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 10, 
            "Run": 10, 
            "Jump": 11, 
            "Hurt": 3,
            "Dead": 4,  
            "Attack_1": 6, 
            "Attack_2": 3,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/amazon/Amazon_3", animasyonlar=animasyonlar, sprite_soneki="Amazon3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Berserk(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8, 
            "Run": 8, 
            "Jump": 12, 
            "Hurt": 2,
            "Dead": 3,  
            "Attack_1": 4, 
            "Attack_2": 4,
            "Attack_3": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime/Berserk", animasyonlar=animasyonlar, sprite_soneki="Berserk")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class AnimeKnight(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 7, 
            "Run": 8, 
            "Jump": 12, 
            "Hurt": 2,
            "Dead": 3,    
            "Attack_1": 4, 
            "Attack_2": 7,
            "Attack_3": 3,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime/Knight", animasyonlar=animasyonlar, sprite_soneki="AnimeKnight")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Enchantress(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8, 
            "Run": 8, 
            "Jump": 12, 
            "Hurt": 2,
            "Dead": 4,
            "Charge": 7,    
            "Attack_1": 4, 
            "Fire":6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime/Enchantress", animasyonlar=animasyonlar, sprite_soneki="Enchantress")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Demon1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8, 
            "Walk": 10,   
            "Hurt": 6,
            "Dead": 11, 
            "Attack_1": 6, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime_demon/Demon_1", animasyonlar=animasyonlar, sprite_soneki="Demon1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Demon3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 8, 
            "Attack_1": 9, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime_demon/Demon_3", animasyonlar=animasyonlar, sprite_soneki="Demon3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class HugeMushroom(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 6,
            "Hurt": 4,
            "Dead": 4, 
            "Attack_1": 4,
            "Attack_2": 4,
            "Attack_3": 6,
            "Attack_4": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/cave bosses/1 Huge Mushroom", animasyonlar=animasyonlar, sprite_soneki="HugeMushroom")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.sola_donuk=True
        self.attack_count=4

class VampireBat(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 6,
            "Hurt": 4,
            "Dead": 4, 
            "Attack_1": 4,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/cave bosses/3 Vampire Bat", animasyonlar=animasyonlar, sprite_soneki="VampireBat")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=4

class CityMan1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 10,
            "Run": 10,   
            "Hurt": 3,
            "Dead": 4, 
            "Attack_1": 5, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/cityMen/City_men_1", animasyonlar=animasyonlar, sprite_soneki="CityMan1")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class CityMan2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 10,
            "Run": 10,   
            "Hurt": 3,
            "Dead": 4, 
            "Attack_1": 4, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/cityMen/City_men_2", animasyonlar=animasyonlar, sprite_soneki="CityMan2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class CityMan3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 10,
            "Run": 10,   
            "Hurt": 3,
            "Dead": 5, 
            "Attack_1": 4, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/cityMen/City_men_3", animasyonlar=animasyonlar, sprite_soneki="CityMan3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Demon5(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 3, 
            "Attack_1": 5, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/demon/Demon_2", animasyonlar=animasyonlar, sprite_soneki="Demon2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Demon6(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5, 
            "Attack_1": 5, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/demon/Demon_3", animasyonlar=animasyonlar, sprite_soneki="Demon3")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=1

class Goblin1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8,
            "Run": 8,
            "Jump": 11,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 5,
            "Attack_2": 6,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/goblin/Goblin_1", animasyonlar=animasyonlar, sprite_soneki="Goblin1")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Goblin2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 9,
            "Run": 8,
            "Jump": 12,
            "Hurt": 3,
            "Dead": 6,
            "Attack_1": 5,
            "Attack_2": 8,
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/goblin/Goblin_2", animasyonlar=animasyonlar, sprite_soneki="Goblin2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Goblin3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 13,
            "Run": 7,
            "Hurt": 3,
            "Dead": 3,
            "Attack_1": 16,
            "Attack_2": 7,
            "Attack_3": 10,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/goblin/Goblin_3", animasyonlar=animasyonlar, sprite_soneki="Goblin3")
        self.devriye_noktasi_1 = (x - 50, y)
        self.devriye_noktasi_2 = (x + 50, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Gorgon2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 13,
            "Run": 7,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 16,
            "Attack_2": 7,
            "Attack_3": 10,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/gorgon/Gorgon_2", animasyonlar=animasyonlar, sprite_soneki="Gorgon2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Gorgon1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 8,
            "Run": 8,
            "Jump": 11,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 5,
            "Attack_2": 6,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/gorgon/Gorgon_1", animasyonlar=animasyonlar, sprite_soneki="Gorgon1")
        self.devriye_noktasi_1 = (x - 250, y)
        self.devriye_noktasi_2 = (x + 250, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Gorgon3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 13,
            "Run": 7,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 16,
            "Attack_2": 10,
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/gorgon/Gorgon_3", animasyonlar=animasyonlar, sprite_soneki="Gorgon3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Hellhound1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 9,
            "Run": 6,
            "Jump": 10,
            "Hurt": 4,
            "Dead": 6,
            "Attack_1": 5,
            "Attack_2": 4,
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/hellhound/Hellhound_1", animasyonlar=animasyonlar, sprite_soneki="Hellhound1")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Hellhound2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 9,
            "Run": 6,
            "Jump": 10,
            "Hurt": 3,
            "Dead": 6,
            "Attack_1": 6,
            "Attack_2": 3,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/hellhound/Hellhound_2", animasyonlar=animasyonlar, sprite_soneki="Hellhound2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Hellhound3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 9,
            "Run": 6,
            "Jump": 10,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 6,
            "Attack_2": 4,
            "Attack_3": 3,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/hellhound/Hellhound_3", animasyonlar=animasyonlar, sprite_soneki="Hellhound3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Knight1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 8,
            "Run": 7,
            "Jump": 6,
            "Hurt": 2,
            "Dead": 6,
            "Attack_1": 5,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/knight/Knight_1", animasyonlar=animasyonlar, sprite_soneki="Knight1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=4

class Knight2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 8,
            "Run": 7,
            "Jump": 6,
            "Hurt": 2,
            "Dead": 6,
            "Attack_1": 5,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/knight/Knight_2", animasyonlar=animasyonlar, sprite_soneki="Knight2")
        self.devriye_noktasi_1 = (x - 250, y)
        self.devriye_noktasi_2 = (x + 250, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=4

class Knight3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 8,
            "Run": 7,
            "Jump": 6,
            "Hurt": 2,
            "Dead": 6,
            "Attack_1": 5,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/knight/Knight_3", animasyonlar=animasyonlar, sprite_soneki="Knight3")
        self.devriye_noktasi_1 = (x - 75, y)
        self.devriye_noktasi_2 = (x + 75, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=4

class Mutant1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 9,
            "Run": 7,
            "Jump": 11,
            "Hurt": 5,
            "Dead": 5,
            "Attack_1": 5,
            "Attack_2": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/mutant/Mutant_1", animasyonlar=animasyonlar, sprite_soneki="Mutant1")
        self.devriye_noktasi_1 = (x - 50, y)
        self.devriye_noktasi_2 = (x + 50, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class Mutant2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 7,
            "Run": 8,
            "Jump": 10,
            "Hurt": 4,
            "Dead": 6,
            "Attack_1": 6,
            "Attack_2": 6,
            "Attack_3": 14,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/mutant/Mutant_2", animasyonlar=animasyonlar, sprite_soneki="Mutant2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 75, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Mutant3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 7,
            "Run": 8,
            "Jump": 10,
            "Hurt": 4,
            "Dead": 6,
            "Attack_1": 6,
            "Attack_2": 6,
            "Attack_3": 14,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/mutant/Mutant_3", animasyonlar=animasyonlar, sprite_soneki="Mutant3")
        self.devriye_noktasi_1 = (x - 50, y)
        self.devriye_noktasi_2 = (x + 50, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class BrownOrc(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 8,
            "Run": 8,
            "Jump": 13,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 5,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/orc/Orc_Warrior_Brown", animasyonlar=animasyonlar, sprite_soneki="Brown")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=4

class GreenOrc(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 8,
            "Run": 8,
            "Jump": 13,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 5,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/orc/Orc_Warrior_Green", animasyonlar=animasyonlar, sprite_soneki="Green")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=4

class WomanOrc(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 6, 
            "Walk": 8,
            "Run": 8,
            "Jump": 11,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 6,
            "Attack_2": 4,
            "Attack_3": 4,
            "Attack_4": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/orc/Orc_Warrior_Brown", animasyonlar=animasyonlar, sprite_soneki="Brown")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class Pyromancer2(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 8,
            "Run": 8,
            "Jump": 13,
            "Hurt": 4,
            "Dead": 5,
            "Attack_1": 4,
            "Attack_2": 5,
            "Attack_3": 13,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/pyromancer/Pyromancer_2", animasyonlar=animasyonlar, sprite_soneki="Pyromancer2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Pyromancer3(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 7,
            "Walk": 8,
            "Run": 8,
            "Jump": 13,
            "Hurt": 5,
            "Dead": 4,
            "Attack_1": 6,
            "Attack_2": 5,
            "Attack_3": 11,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/pyromancer/Pyromancer_3", animasyonlar=animasyonlar, sprite_soneki="Pyromancer3")
        self.devriye_noktasi_1 = (x - 350, y)
        self.devriye_noktasi_2 = (x + 350, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Raider1(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 8,
            "Run": 8,
            "Jump": 11,
            "Hurt": 2,
            "Dead": 4,
            "Attack_1": 6,
            "Attack_2": 3,
            "Attack_3": 12,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/raider/Raider_1", animasyonlar=animasyonlar, sprite_soneki="Raider1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Raider3(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 7,
            "Run": 8,
            "Jump": 8,
            "Hurt": 2,
            "Dead": 4,
            "Attack_1": 5,
            "Attack_2": 5,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/raider/Raider_3", animasyonlar=animasyonlar, sprite_soneki="Raider3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Samurai(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 9,
            "Run": 8,
            "Jump": 9,
            "Hurt": 3,
            "Dead": 6,
            "Attack_1": 4,
            "Attack_2": 5,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/samuray/Samurai", animasyonlar=animasyonlar, sprite_soneki="Samurai")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class SamuraiCommander(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 5,
            "Walk": 9,
            "Run": 8,
            "Jump": 7,
            "Hurt": 2,
            "Dead": 6,
            "Attack_1": 4,
            "Attack_2": 5,
            "Attack_3": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/samuray/Samurai_Commander", animasyonlar=animasyonlar, sprite_soneki="SamuraiCommander")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Man1(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 12,
            "Run": 12,
            "Jump": 10,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 5,
            "Attack_2": 3,
            "Attack_3": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/warrior/Man_1", animasyonlar=animasyonlar, sprite_soneki="Man1")
        self.devriye_noktasi_1 = (x - 150, y)
        self.devriye_noktasi_2 = (x + 150, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Man2(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 12,
            "Run": 12,
            "Jump": 10,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 4,
            "Attack_2": 4,
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/warrior/Man_2", animasyonlar=animasyonlar, sprite_soneki="Man2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Man3(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 12,
            "Run": 12,
            "Jump": 10,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 4,
            "Attack_2": 5,
            "Attack_3": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/warrior/Man_3", animasyonlar=animasyonlar, sprite_soneki="Man3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Witch1(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 10,
            "Run": 10,
            "Jump": 11,
            "Hurt": 5,
            "Dead": 6,
            "Attack_1": 8,
            "Attack_2": 3,
            "Attack_3": 13,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/witch/Witch_1", animasyonlar=animasyonlar, sprite_soneki="witch1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=3

class Witch2(Menzilli):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 8,
            "Walk": 10,
            "Run": 10,
            "Jump": 13,
            "Hurt": 5,
            "Dead": 4,
            "Attack_1": 5,
            "Attack_2": 4,
            "Charge": 10,
            "Fire": 8,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/witch/Witch_2", animasyonlar=animasyonlar, sprite_soneki="witch2",)
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=2

class Witch3(Menzilli):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 10,
            "Run": 10,
            "Jump": 11,
            "Hurt": 4,
            "Dead": 4,
            "Attack_1": 8,
            "Attack_2": 3,
            "Charge": 9,
            "Fire": 14,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/witch/Witch_3", animasyonlar=animasyonlar, sprite_soneki="witch3")
        self.devriye_noktasi_1 = (x - 300, y)
        self.devriye_noktasi_2 = (x + 300, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=2

class Pyromancer1(Yakin):
    def __init__(self, x, y):
        animasyonlar={
            "Idle": 6,
            "Walk": 8,
            "Run": 10,
            "Jump": 12,
            "Hurt": 4,
            "Dead": 4,
            "Attack_1": 14,
            "Attack_2": 6,
            "Fire": 9,
            "Charge": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/pyromancer/Pyromancer_1", animasyonlar=animasyonlar, sprite_soneki="Pyromancer1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count=2

class GoblinKing(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 6,
            "Hurt": 4,
            "Dead": 4, 
            "Attack_1": 4,
            "Attack_2": 6,
            "Attack_3": 4,
            "Charge": 1,
            "Fire": 4,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/cave bosses/2 Goblin King", animasyonlar=animasyonlar, sprite_soneki="GoblinKing")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=3

class BattleMecha1(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 6,  
            "Hurt": 2,
            "Dead": 6, 
            "Charge": 6,
            "Fire": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/battlemecha/1", animasyonlar=animasyonlar, sprite_soneki="BattleMecha1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=0

class BattleMecha2(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 6,  
            "Hurt": 2,
            "Dead": 6, 
            "Charge": 6,
            "Fire": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/battlemecha/2", animasyonlar=animasyonlar, sprite_soneki="BattleMecha2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=0

class BattleMecha3(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 4, 
            "Walk": 6,  
            "Hurt": 2,
            "Dead": 6, 
            "Charge": 1,
            "Fire": 6,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/battlemecha/3", animasyonlar=animasyonlar, sprite_soneki="BattleMecha3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=0

class Demon4(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7, 
            "Walk": 1,  
            "Hurt": 3,
            "Dead": 3, 
            "Charge": 5,
            "Fire": 12,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime_demon/Demon_4", animasyonlar=animasyonlar, sprite_soneki="Demon4")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=0

class Demon2(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8, 
            "Walk": 10,  
            "Hurt": 6,
            "Dead": 11, 
            "Charge": 7,
            "Fire": 7, 
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/anime_demon/Demon_2", animasyonlar=animasyonlar, sprite_soneki="Demon2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=0

class Wizard(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7,
            "Walk": 6,
            "Run": 8,
            "Jump": 9,
            "Attack_1": 4,
            "Attack_2": 4,
            "Attack_3": 14,
            "Fire": 8,
            "Charge": 12,
            "Hurt": 3,
            "Dead": 6,
        }
        super().__init__(x, y, hiz=2, can=50, guc=15, sprite_klasoru="ENEMIES/wizard/Fire vizard", animasyonlar=animasyonlar, sprite_soneki="fire")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.attack_count=3

class Lightning(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 7,
            "Walk": 7,
            "Run": 8,
            "Jump": 8,
            "Hurt": 3,
            "Dead": 5,
            "Attack_1": 10,
            "Attack_2": 4,
            "Attack_3": 12,
            "Fire": 7,
            "Charge": 9, 
        }
        super().__init__(x, y, hiz=2, can=50, guc=15, sprite_klasoru="ENEMIES/wizard/Lightning Mage", animasyonlar=animasyonlar, sprite_soneki="lightning")
        self.devriye_noktasi_1 = (x - 400, y)
        self.devriye_noktasi_2 = (x + 400, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.attack_count=3

class Wanderer(Menzilli):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 8,
            "Walk": 7,
            "Run": 8,
            "Jump": 8,
            "Hurt": 4,
            "Dead": 4,
            "Attack_1": 7,
            "Attack_2": 9,
            "Fire": 16,
            "Charge": 9,
        }
        super().__init__(x, y, hiz=2, can=50, guc=15, sprite_klasoru="ENEMIES/wizard/Wanderer Magican", animasyonlar=animasyonlar, sprite_soneki="wanderer")
        self.devriye_noktasi_1 = (x - 250, y)
        self.devriye_noktasi_2 = (x + 250, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=2

class Kitsune(Menzilli):
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
            "Fire": 7,
            "Charge": 11,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/yokai/Kitsune", animasyonlar=animasyonlar, sprite_soneki="Kitsune")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
        self.attack_count=2
