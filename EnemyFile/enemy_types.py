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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 500, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

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
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/ninja/Ninja_Peasant", animasyonlar=animasyonlar, sprite_soneki="Peasant")
        self.devriye_noktasi_1 = (x - 200, y)
        self.devriye_noktasi_2 = (x + 200, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class Minotaur1(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_1", animasyonlar=animasyonlar, sprite_soneki="Minotaur1")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class Minotaur2(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_2", animasyonlar=animasyonlar, sprite_soneki="Minotaur2")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

class Minotaur3(Yakin):
    def __init__(self, x, y):
        animasyonlar = {
            "Idle": 10, 
            "Walk": 12,  
            "Hurt": 3,
            "Dead": 5,  
            "Attack": 5,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/minatour/Minotaur_3", animasyonlar=animasyonlar, sprite_soneki="Minotaur3")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
    
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
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1

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

class Wizard(Menzilli):
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
            "Attack_3": 7,
        }
        super().__init__(x, y, hiz=2, can=70, guc=20, sprite_klasoru="ENEMIES/yokai/Kitsune", animasyonlar=animasyonlar, sprite_soneki="Kitsune")
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.tespit_mesafesi = 400
        self.saldiri_mesafesi = 300
