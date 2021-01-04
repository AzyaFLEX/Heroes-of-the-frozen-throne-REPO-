from Cell.Tiles import Field


class Spell:
    def is_activated(self, board):
        """:return: bool. Показывает, можно ли использовать эту способность"""
        return True

    def cast(self, board):
        """:return: None. Использование способности"""
        pass


class Build(Spell):
    def is_activated(self, board):
        return bool(board.chosen_unit.tile) and any(board.chosen_unit.tile.resources)

    def cast(self, board):
        if self.is_activated(board):
            board.chosen_unit.tile = Field(board, board.chosen_unit.unit.player)