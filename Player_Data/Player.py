class PlayerData:
    def __init__(self):
        self.resources = [0, 0, 0]
        self.buff = [0, 0, 0]

    def wood(self):
        return self.resources[0]

    def iron(self):
        return self.resources[1]

    def gold(self):
        return self.resources[2]

    def update(self):
        for i in range(3):
            self.resources[i] += self.buff[i]
