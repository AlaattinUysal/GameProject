from yakin import Yakin
from menzilli import Menzilli
from utils import Spritesheet

class AnimeKnight(Yakin):
    def __init__(self, x, y, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet):
        super().__init__(x, y, 2, 70, 20, walk_spritesheet, idle_spritesheet, jump_spritesheet, run_spritesheet, attack1_spritesheet, attack2_spritesheet, attack3_spritesheet, hurt_spritesheet, death_spritesheet)
        self.devriye_noktasi_1 = (x - 100, y)
        self.devriye_noktasi_2 = (x + 100, y)
        self.hedef_x, self.hedef_y = self.devriye_noktasi_1
        self.attack_count = 3
        self.available_attacks = self.attacks[:self.attack_count]
        
class Wizard(Menzilli):
    def __init__(self, x, y, game_state, sprite_klasoru="ENEMIES/wizard/Fire vizard", sprite_soneki="_fire"):
        # Define sprite sheets for Wizard
        walk_spritesheet = Spritesheet(f"{sprite_klasoru}/Walk{sprite_soneki}.png")
        idle_spritesheet = Spritesheet(f"{sprite_klasoru}/Idle{sprite_soneki}.png")
        jump_spritesheet = Spritesheet(f"{sprite_klasoru}/Jump{sprite_soneki}.png")
        run_spritesheet = Spritesheet(f"{sprite_klasoru}/Run{sprite_soneki}.png")
        attack1_spritesheet = Spritesheet(f"{sprite_klasoru}/Attack_1{sprite_soneki}.png")
        attack2_spritesheet = Spritesheet(f"{sprite_klasoru}/Attack_2{sprite_soneki}.png")
        attack3_spritesheet = Spritesheet(f"{sprite_klasoru}/Attack_3{sprite_soneki}.png")
        hurt_spritesheet = Spritesheet(f"{sprite_klasoru}/Hurt{sprite_soneki}.png")
        death_spritesheet = Spritesheet(f"{sprite_klasoru}/Dead{sprite_soneki}.png")
        charge_spritesheet = Spritesheet(f"{sprite_klasoru}/Charge{sprite_soneki}.png")
        fire_spritesheet = Spritesheet(f"{sprite_klasoru}/Fire{sprite_soneki}.png")

        # Pass all required arguments to Menzilli's __init__, including sprite_klasoru and sprite_soneki
        super().__init__(
            x, y, 
            hiz=2, can=70, guc=5,
            walk_spritesheet=walk_spritesheet,
            idle_spritesheet=idle_spritesheet,
            jump_spritesheet=jump_spritesheet,
            run_spritesheet=run_spritesheet,
            attack1_spritesheet=attack1_spritesheet,
            attack2_spritesheet=attack2_spritesheet,
            attack3_spritesheet=attack3_spritesheet,
            hurt_spritesheet=hurt_spritesheet,
            death_spritesheet=death_spritesheet,
            charge_spritesheet=charge_spritesheet,
            fire_spritesheet=fire_spritesheet,
            sprite_klasoru=sprite_klasoru,
            sprite_soneki=sprite_soneki
        )
        self.saldiri_mesafesi = 50
        self.menzilli_saldiri_mesafesi = 200
        self.tespit_mesafesi = 300
        self.saldiri_bekleme_suresi = 1000
        self.mermi_hizi = 5
        self.mermi_menzili = 400
        self.jump_power = -12
        self.available_attacks = ["Attack_1", "Attack_2", "Attack_3"]
