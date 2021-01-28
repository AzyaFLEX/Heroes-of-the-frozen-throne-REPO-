from pygame import draw, Color
from Spells.Spells import *


class BaseUnit:
    def __init__(self, player, hexagon, move_per_round=200, attack_range=0):
        self.damage = 999
        self.health = 99
        self.mana = 999
        self.full_mana = 999
        self.full_health = 999
        self.cost = [0, 0, 0]
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

    def change_color(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Worker(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 5, 0)
        self.health = 35
        self.damage = 0
        self.mana = 0
        self.cost = [20, 0, 0]
        self.spells[0] = Build()
        self.get_full()
        self.color = "#89a7e2" if not player else "#e289b5"

    def spell_1(self):
        pass


class Warrior(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 4, 1)
        self.health = 50
        self.mana = 0
        self.cost = [20, 10, 0]
        self.damage = 25
        self.get_full()
        self.color = "#344570" if not player else "#703444"


class Archer(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 5, 4)
        self.health = 10
        self.mana = 0
        self.cost = [15, 15, 0]
        self.damage = 15
        self.get_full()
        self.color = "#B9F73E" if not player else "#9F3ED5"


class Morphling(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 3, 4)
        self.spells[0] = Mana_regen()
        self.health = 25
        self.mana = 10
        self.cost = [15, 15, 2]
        self.damage = 15
        self.get_full()
        self.color = "#37DA7E" if not player else "#FF6B40"


class Wizard(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 3, 3)
        self.spells[0] = Heal()
        self.health = 40
        self.mana = 20
        self.cost = [25, 30, 5]
        self.damage = 30
        self.get_full()
        self.color = "#22d5ba" if not player else "#d522a5"


class Tank(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 3, 1)
        self.health = 100
        self.mana = 0
        self.cost = [10, 40, 3]
        self.damage = 20
        self.get_full()
        self.color = "#A69F00" if not player else "#3F046F"


class Hunter(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 5, 2)
        self.health = 20
        self.damage = 35
        self.cost = [20, 20, 30]
        self.mana = 0
        self.get_full()
        self.color = "#002761" if not player else "#610017"

    def attack(self, range_, enemy_unit):
        if not self.attacked and range_ <= self.attack_range and self.player != enemy_unit.player:
            enemy_unit.health -= self.damage
            self.moved = 0
            self.attacked = True
            self.health -= round(enemy_unit.damage / 3)
            if enemy_unit.health <= 0:
                self.full_health += 10
                self.damage += 5
            return True, enemy_unit.health <= 0
        return False, False


class Itachi(BaseUnit):
    def __init__(self, player, hexagon):
        super().__init__(player, hexagon, 3, 1)
        self.health = 20
        self.mana = 80
        self.cost = [40, 40, 40]
        self.spells[0] = Genjitsu()
        self.damage = 10
        self.get_full()
        self.color = "#1D8C00" if not player else "#9F0013"
