class Entity:
    def __init__(self, pos, name, state = ""):
        self.x, self.y = pos
        self.name = name
        self.state = state
        self.frame = 0
        self.distance = 0

    def get_sprite(self):
        if self.state == "":
            return self.name
        else:
            return self.name + "_" + self.state

class Item(Entity):
    def __init__(self, pos, name):
        Entity.__init__(self, pos, name)

class Scenario(Entity):
    def __init__(self, pos, name):
        Entity.__init__(self, pos, name)

class Enemy(Entity):
    def __init__(self, pos, name):
        Entity.__init__(self, pos, name)