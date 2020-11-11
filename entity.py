import math, random

from tools import basic_distance

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
        Entity.__init__(self, pos, name, 'idle')

        self.health = 100
        self.speed = 1.5
        self.delay = {
            'attack': 0,
            'damage': 0,
            'die': 0
        }

        # Propriedades de movimentação
        self.new_x, self.new_y = pos
        self.angle = 0
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.rand_x = random.uniform(-0.5, 0.5)
        self.rand_y = random.uniform(-0.5, 0.5)
        self.step = 0

    def collide(self, tiles, delta):
        return tiles[int(delta[0])][int(delta[1])] == 0

    def damage(self, damage):
        self.health -= damage
        if self.health > 0:
            sprite_number = random.randint(1, 2)
            self.change_state('shot_' + str(sprite_number))
            self.delay['damage'] = 10
        elif self.state != 'die':
            self.change_state('die', 80)

    def attack(self, player):
        if self.delay['attack'] == 0:
            player.damage(10)
            self.change_state('attack', 36)
            self.frame = 0
        elif self.delay['attack'] <= 24:
            self.state = 'idle'
            self.frame = 0

    def change_state(self, new, delay = 0):
        if self.state != new:
            self.frame = 0
        if delay != 0:
            self.delay[new] = delay
        self.state = new

    def update(self, tiles, player, dt):
        self.angle = math.atan2(player.y - self.y, player.x - self.x)
        d = basic_distance((player.x, player.y),(self.x, self.y))

        # Update delay
        if self.delay['attack'] > 0:
            self.delay['attack'] -= 1

        if self.delay['die'] > 0:
            self.delay['die'] -= 1
        elif self.delay['damage'] > 0:
            self.delay['damage'] -= 1
        elif d > 0.5:
            self.change_state('run')

            if self.step > 9:
                self.step = 0
                self.rand_x = random.uniform(-0.5,0.5)
                self.rand_y = random.uniform(-0.5,0.5)
            else:
                self.step += 1

            self.dx = math.cos(self.angle) + self.rand_x
            self.dy = math.sin(self.angle) + self.rand_y

            new_x = self.x + self.dx * dt * self.speed
            new_y = self.y + self.dy * dt * self.speed

            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        elif d <= 0.5:
            self.attack(player)