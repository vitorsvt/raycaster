import math, random, tools

class Player:
    def __init__(self, sounds):
        self.x, self.y = (0,0)

        self.dx, self.dy = (-1, 0)
        self.px, self.py = (0, 0.66)

        self.health = 100
        self.ammo = 50
        self.speed = 5.0
        self.rot = 3.0
        self.moving = False

        self.offx = 0
        self.offx_inc = 1
        self.offy = 0
        self.offy_inc = 1

        self.shoot_delay = 0

        self.weapon_frame = 0
        self.weapon = 'pistol'
        self.state = 'idle'

        self.sounds = sounds

    def respawn(self, pos):
        self.x, self.y = pos
        self.ammo = max(20, self.ammo)
        self.state = 'idle'

    def update(self, game):
        if self.health <= 0:
            print('Você morreu...')
            game.quit()
        if self.moving:
            self.offx += self.offx_inc
            if self.offx > 10 or self.offx < -10:
                self.offx_inc = -self.offx_inc
            
            self.offy += self.offy_inc
            if self.offy > 5 or self.offy < -5:
                self.offy_inc = -self.offy_inc
        else:
            if self.offx > 0:
                self.offx -= abs(self.offx_inc)
            elif self.offx < 0:
                self.offx += abs(self.offx_inc)

            if self.offy > 0:
                self.offy -= abs(self.offy_inc)
            elif self.offy < 0:
                self.offy += abs(self.offy_inc)
        if self.shoot_delay == 0 and self.state == 'shoot':
            self.state = 'idle'
        elif self.shoot_delay > 0:
            self.shoot_delay -= 1

    def collide(self, tiles, delta):
        return tiles[int(delta[0])][int(delta[1])] == 0

    def move(self, game, tiles, middle):
        inputs = game.inputs
        dt = game.dt

        self.moving = False
        if inputs['up']:
            self.moving = True
            new_x = self.x + self.dx * self.speed * dt
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y + self.dy * self.speed * dt
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['down']:
            self.moving = True
            new_x = self.x - self.dx * self.speed * dt / 2
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y - self.dy * self.speed * dt / 2
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['left']:
            self.moving = True
            new_x = self.x - self.dy * self.speed * dt / 2
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y + self.dx * self.speed * dt / 2
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['right']:
            self.moving = True
            new_x = self.x + self.dy * self.speed * dt / 2
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y - self.dx * self.speed * dt / 2
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['mouse'][0] != 0:
            rotation = -(inputs['mouse'][0]) * 0.08 * dt
            old_dx = self.dx
            self.dx = self.dx * math.cos(rotation) - self.dy * math.sin(rotation)
            self.dy = old_dx * math.sin(rotation) + self.dy * math.cos(rotation)
            old_px = self.px
            self.px = self.px * math.cos(rotation) - self.py * math.sin(rotation)
            self.py = old_px * math.sin(rotation) + self.py * math.cos(rotation)
        if inputs['lmb']:
            self.shoot(middle)
        if inputs['esc']:
            game.change_state('menu')

    def damage(self, damage):
        self.health -= damage

    def shoot(self, target):
        if self.shoot_delay == 0 and self.ammo > 0:
            self.sounds.play('gunshot')
            if target != None and target.health > 0:
                target.damage(50)
                self.sounds.play('damage')
            self.shoot_delay = 25
            self.state = 'shoot'
            self.ammo -= 1

    def pickup(self, item):
        if item.x == int(self.x) and item.y == int(self.y):
            if item.category == "health":
                self.health = min(100, self.health + item.value)
                self.sounds.play('health')
            else:
                self.ammo += item.value
                self.sounds.play('ammo')
            return True

class Item:
    def __init__(self, pos, sprite, category):
        self.x, self.y = pos
        self.type = "item"
        self.distance = 0
        self.sprite = sprite
        self.category = category
        self.value = 50

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
            if self.step > 60:
                self.step = 0
                self.rand_x = random.uniform(-1,1)
                self.rand_y = random.uniform(-1,1)
            else:
                self.step += 1

            self.update_delta()

            if self.distance < 200:
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