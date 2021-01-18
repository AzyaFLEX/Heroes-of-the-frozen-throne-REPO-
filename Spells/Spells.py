from Units.Units import *
from Cell.Tiles import Field


class Spell:
    def __init__(self):
        self.casting = False
        self.use_on_himself = False
        self.range = 0

    def is_activated(self, board):
        """:return: bool. Показывает, можно ли использовать эту способность"""
        return True

    def can_cast(self, board, unit):
        """:return: bool. Показывает, можно ли ghbvtybnm эту способность на выбраном юните"""
        return True

    def cast(self, board, unit=None):
        """:return: None. Использование способности"""
        pass


class Build(Spell):
    def is_activated(self, board):
        return bool(board.chosen_unit.tile) and any(board.chosen_unit.tile.resources)

    def cast(self, board, unit=None):
        if self.is_activated(board):
            board.chosen_unit.tile = Field(board, board.chosen_unit.unit.player)


class Heal(Spell):
    def __init__(self):
        super().__init__()
        self.casting = True
        self.use_on_himself = True
        self.range = 3

    def can_cast(self, board, unit):
        if board.turn == unit.player:
            return True
        return False

    def cast(self, board, unit=None):
        if self.is_activated(board) and unit:
            unit.unit.health += 15 if not unit.unit.health + 15 > unit.unit.full_health \
                else unit.unit.full_health - unit.unit.health
