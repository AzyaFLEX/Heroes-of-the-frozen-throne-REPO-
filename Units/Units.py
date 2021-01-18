from pygame import draw, Color
from Spells.Spells import *


class BaseUnit:
    def __init__(self, player, hexagon, move_per_round=200, attack_range=0):
        self.damage = 999
        self.health = 99
        self.mana = 999
        self.full_mana = 999
        self.full_health = 999
        self.player = player
        self.spells = [None for _ in range(4)]
        self.hexagon = hexagon
        self.attacked = False
        self.attack_range = attack_range
        self.moves_per_round = move_per_round
        self.moved = move_per_round
        self.color = Color("red")

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def get_full(self):
        self.full_health = self.health
        self.full_mana = self.mana

    def move(self, move):
        self.moved -= move

    def draw(self, screen, tile, cell_size, diagonal):
        draw.rect(screen, self.color, (
                            tile.center[0] - cell_size // 2,
                            tile.center[1] - diagonal // 2,
                            cell_size,
                            diagonal))

    def attack(self, range_, enemy_unit):
        if not self.attacked and range_ <= self.attack_range and self.player != enemy_unit.player:
            enemy_unit.health -= self.damage
            self.moved = 0
            self.attacked = True
            self.health -= round(enemy_unit.damage / 3)
            return True, enemy_unit.health <= 0
        return False, False

    def update(self):
        # Проверка на активность скиллов у всех персонажей
        pass

    def refresh(self):
        self.moved = self.moves_per_round
        self.attacked = False


class Worker(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 20, 0)
        self.health = 50
        self.mana = 0
        self.spells[0] = Build()
        self.get_full()
        self.color = Color("white")

    def spell_1(self):
        pass


class Warrior(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 4, 1)
        self.health = 50
        self.mana = 0
        self.damage = 25
        self.get_full()
        self.color = Color("blue")


class Wizard(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 3, 3)
        self.spells[0] = Heal()
        self.health = 30
        self.mana = 20
        self.damage = 30
        self.get_full()
        self.color = Color("pink")
