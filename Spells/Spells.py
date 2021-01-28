from Cell.Tiles import Field


class Spell:
    def __init__(self):
        self.casting = False
        self.use_on_himself = False
        self.range = 0
        self.casted = -1
        self.max_cast = self.casted
        self.mana_cost = False

    def is_activated(self, board):
        """:return: bool. Показывает, можно ли использовать эту способность"""
        return True

    def can_cast(self, board, unit):
        """:return: bool. Показывает, можно ли ghbvtybnm эту способность на выбраном юните"""
        return True

    def cast(self, board, unit=None):
        """:return: None. Использование способности"""
        pass

    def update(self):
        self.casted = self.max_cast


class Build(Spell):
    def is_activated(self, board):
        return bool(board.chosen_unit.tile) and any(board.chosen_unit.tile.resources)

    def cast(self, board, unit=None):
        if self.is_activated(board):
            board.players[board.turn].buff[board.chosen_unit.tile.return_useful()]\
                += board.chosen_unit.tile.resources[board.chosen_unit.tile.return_useful()]
            res = [0, 0, 0]
            res[board.chosen_unit.tile.return_useful()]\
                = board.chosen_unit.tile.resources[board.chosen_unit.tile.return_useful()]
            board.chosen_unit.tile = Field(board, board.chosen_unit.unit.player)
            board.chosen_unit.tile.buff = res
            board.chosen_unit.unit.moved = 0


class Heal(Spell):
    def __init__(self):
        super().__init__()
        self.casting = True
        self.use_on_himself = True
        self.range = 3
        self.casted = 2
        self.max_cast = self.casted
        self.mana_cost = True

    def can_cast(self, board, unit):
        if board.turn == unit.player:
            return True
        return False

    def cast(self, board, unit=None):
        if self.is_activated(board) and unit and self.casted and board.chosen_unit.unit.mana >= 4:
            unit.unit.health += 15 if not unit.unit.health + 15 > unit.unit.full_health \
                else unit.unit.full_health - unit.unit.health
            board.chosen_unit.unit.mana -= 4
            if self.casted != -1:
                self.casted -= 1


class Mana_regen(Spell):
    def __init__(self):
        super().__init__()
        self.casting = True
        self.use_on_himself = True
        self.range = 4
        self.casted = 1
        self.max_cast = self.casted
        self.mana_cost = True

    def can_cast(self, board, unit):
        if board.turn == unit.player:
            return True
        return False

    def cast(self, board, unit=None):
        if self.is_activated(board) and unit and self.casted and board.chosen_unit.unit.mana >= 4:
            board.chosen_unit.unit.mana -= 4
            unit.unit.mana += 5 if not unit.unit.mana + 5 > unit.unit.full_mana \
                else unit.unit.full_mana - unit.unit.mana
            if self.casted != -1:
                self.casted -= 1


class Genjitsu(Spell):
    def __init__(self):
        super().__init__()
        self.casting = True
        self.use_on_himself = True
        self.range = 4
        self.casted = 1
        self.max_cast = self.casted
        self.mana_cost = True

    def can_cast(self, board, unit):
        if board.turn != unit.player:
            return True
        return False

    def cast(self, board, unit=None):
        if self.is_activated(board) and unit and self.casted and board.chosen_unit.unit.mana >= 80:
            unit.unit.player = 0 if unit.unit.player else 1
            board.chosen_unit.unit.mana -= 80
            if self.casted != -1:
                self.casted -= 1