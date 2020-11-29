import math, random, tools

class Item:
    def __init__(self, pos, sprite, category):
        self.x, self.y = pos
        self.type = "item"
        self.distance = 0
        self.sprite = sprite
        self.category = category
        self.values = {
            "health": 50 if category == "health" else 0,
            "ammo": 50 if category == "ammo" else 0
        }

class Enemy:
    def __init__(self, pos, sprite, health = 100):
        self.x, self.y = pos
        self.distance = 0

        self.sprite = sprite
        self.state = "idle"
        self.frame = 0

        self.type = "enemy"
        self.health = health
        self.speed = 1.5
        self.delay = {
            'attack': 0,
            'damage': 0,
            'die': 0
        }

        self.angle = 0
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.rand_x = random.uniform(-0.5, 0.5)
        self.rand_y = random.uniform(-0.5, 0.5)
        self.step = 0
        self.distance = 0

    def next(self):
        sprite, self.frame = self.sprite.next(self.state, self.frame)
        return sprite

    def update_delta(self):
        self.dx = math.cos(self.angle) + self.rand_x
        self.dy = math.sin(self.angle) + self.rand_y

    def change_state(self, new, delay = 0):
        if self.state != new:
            self.frame = 0
        if delay != 0:
            self.delay[new] = delay
        self.state = new

    def damage(self, damage):
        self.health -= damage
        if self.health > 0:
            sprite = random.randint(1, 2)
            self.change_state('shot_' + str(sprite))
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

    def update(self, tiles, player, dt):
        self.angle = math.atan2(player.y - self.y, player.x - self.x)

        # Update delay
        if self.delay['attack'] > 0:
            self.delay['attack'] -= 1

        if self.delay['die'] > 0:
            self.delay['die'] -= 1
        elif self.delay['damage'] > 0:
            self.delay['damage'] -= 1
        else:
            if self.step > 9:
                self.step = 0
                self.rand_x = random.uniform(-0.5,0.5)
                self.rand_y = random.uniform(-0.5,0.5)
            else:
                self.step += 1

            self.update_delta()

            if self.distance >= 1.0:
                self.change_state('run')
                new_x = self.x + self.dx * dt * self.speed
                new_y = self.y + self.dy * dt * self.speed
            else:
                self.attack(player)
                if self.distance <= 0.5:
                    new_x = self.x - self.dx * dt * self.speed
                    new_y = self.y - self.dy * dt * self.speed
                else:
                    new_x = new_y = 0

            if tools.collide(tiles, (new_x, self.y)):
                self.x = new_x
            if tools.collide(tiles, (self.x, new_y)):
                self.y = new_y
