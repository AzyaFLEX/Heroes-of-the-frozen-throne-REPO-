from pygame import Color


class BaseTile:
    def __init__(self, move=True, useful=True, fill=False):
        self.can_move = move
        self.fill = fill
        self.useful = useful
        self.color = Color("white")
        self.resources = [0, 0, 0]
        self.can_be_attacked = False
        self.health = 0

    def __str__(self):
        return self.__class__.__name__

    def __bool__(self):
        return self.__class__.__name__ == "BaseTile"

    def return_useful(self):
        for i in range(len(self.resources)):
            if self.resources[i]:
                return i


class Mount(BaseTile):
    def __init__(self):
        super().__init__(False, False, True)
        self.player = -1


class Throne(BaseTile):
    def __init__(self, player):
        super().__init__(False, False, True)
        self.color = "red" if player else "blue"
        self.player = player
        self.can_be_attacked = True
        self.full_health = 300
        self.health = 300


class Field(BaseTile):
    def __init__(self, board, player):
        super().__init__(True, False, True)
        self.buff = [0, 0, 0]
        self.color = "#ff7373" if player else "#73fdff"
        self.player = player
        self.board = board
        self.can_be_attacked = True
        self.full_health = 50
        self.health = 50