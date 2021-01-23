from pygame import Color


class BaseTile:
    def __init__(self, move=True, useful=True, fill=False):
        self.can_move = move
        self.fill = fill
        self.useful = useful
        self.color = Color("white")
        self.resources = [0, 0, 0]

    def __str__(self):
        return self.__class__.__name__

    def __bool__(self):
        return self.__class__.__name__ == "BaseTile"

    def return_useful(self):
        for i in range(len(self.resources)):
            if self.resources[i]:
                return i

    def update(self):
        pass


class Mount(BaseTile):
    def __init__(self):
        super().__init__(False, False, True)
        self.player = -1


class Throne(BaseTile):
    def __init__(self, player):
        super().__init__(False, False, True)
        self.color = Color("yellow")
        self.player = player


class Field(BaseTile):
    def __init__(self, board, player):
        super().__init__(True, False, True)
        self.color = Color("orange")
        self.player = player
        self.board = board

    def update(self):
        pass

