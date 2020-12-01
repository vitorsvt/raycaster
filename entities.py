"""Módulo de entidades do jogo"""

import math
import random
import tools

class Player:
    """
    Classe do player, conforme o tutorial de raycasting,
    ela possui atributos dx/dy e px/py que são a direção e o
    plano da câmera
    """
    def __init__(self, sounds):
        self.x, self.y = (0,0)
        # Direção e plano da câmera
        self.dx, self.dy = (-1, 0)
        self.px, self.py = (0, 0.66)
        # Algumas informações para o jogo
        self.health = 100
        self.ammo = 50
        self.speed = 5.0
        self.rot = 3.0
        self.moving = False
        # Para balançar o viewmodel quando andamos
        self.offx = 0
        self.offx_inc = 1
        self.offy = 0
        self.offy_inc = 1
        # Delay para cada tiro
        self.shoot_delay = 0
        # O frame de animação da arma e o estado do jogador
        self.weapon_frame = 0
        self.weapon = 'pistol'
        self.state = 'idle'
        # Objeto de Sounds
        self.sounds = sounds

    def update(self):
        """Atualiza algumas informações periódicas do player"""
        if self.health <= 0:
            print('Você morreu...')
            tools.end()
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

    def move(self, game, tiles, middle, dt):
        """
        Move o player e atualiza outros inputs, como por
        exemplo 'atirar', e testa as colisões do player com o mapa
        """
        inputs = game.inputs

        self.moving = False
        if inputs['up']:
            self.moving = True
            new_x = self.x + self.dx * self.speed * dt
            if tools.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y + self.dy * self.speed * dt
            if tools.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['down']:
            self.moving = True
            new_x = self.x - self.dx * self.speed * dt / 2
            if tools.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y - self.dy * self.speed * dt / 2
            if tools.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['left']:
            self.moving = True
            new_x = self.x - self.dy * self.speed * dt / 2
            if tools.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y + self.dx * self.speed * dt / 2
            if tools.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['right']:
            self.moving = True
            new_x = self.x + self.dy * self.speed * dt / 2
            if tools.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y - self.dx * self.speed * dt / 2
            if tools.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if inputs['mouse'][0] != 0: # Movimentação do mouse
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
            game.state.change_state('menu')

    def damage(self, damage):
        """Dá dano ao player"""
        self.health -= damage

    def shoot(self, target):
        """Atira, e testa se acertou alguém"""
        if self.shoot_delay == 0 and self.ammo > 0:
            self.sounds.play('gunshot')
            if target is not None and target.health > 0: # Se temos alvo e ele não está morto
                target.damage(50)
                self.sounds.play('damage')
            self.shoot_delay = 25
            self.state = 'shoot'
            self.ammo -= 1

    def pickup(self, item):
        """Testa se há colisão com um item, e atualiza os valores se sim"""
        if item.x == int(self.x) and item.y == int(self.y):
            if item.category == "health":
                self.health = min(100, self.health + item.value)
                self.sounds.play('health')
            else:
                self.ammo += item.value
                self.sounds.play('ammo')
            return True
        else:
            return False

class Item:
    """Classe para armazenar as informações de um item"""
    def __init__(self, pos, sprite, category):
        self.x, self.y = pos
        self.type = "item"
        self.distance = 0
        self.sprite = sprite
        self.category = category
        self.value = 50

class Enemy:
    """Classe para armazenar e atualizar um inimigo"""
    def __init__(self, pos, sprite, boss):
        # Posição
        self.x, self.y = pos
        # Distância do player
        self.distance = 0
        # Spritesheet
        self.sprite = sprite
        self.state = "idle"
        self.frame = 0
        # Algumas informações
        self.type = "enemy"
        self.boss = boss
        self.health = 100 if not boss else 1000
        self.attack_value = 25 if not boss else 50
        self.speed = 2
        # Delay de ações
        self.delay = {
            'attack': 0,
            'attack_max': 36 if not boss else 40,
            'attack_idle': 24 if not boss else 20,
            'damage': 0,
            'die': 0
        }
        # Movimentação
        self.angle = 0
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        # Aleatoriedade na movimentação
        self.rand_x = random.uniform(-0.5, 0.5)
        self.rand_y = random.uniform(-0.5, 0.5)
        self.step = 0

    def next(self):
        """Atualiza o frame a retorna o sprite"""
        sprite, self.frame = self.sprite.next(self.state, self.frame)
        return sprite

    def change_state(self, new, delay = 0):
        """Atualiza o estado, com um delay opcional"""
        if self.state != new:
            self.frame = 0
        if delay != 0:
            self.delay[new] = delay
        self.state = new

    def damage(self, damage):
        """Dá dano ao inimigo, e atualiza o estado"""
        self.health -= damage
        if self.health > 0:
            sprite = random.randint(1, 2) # Temos dois sprites para o dano
            self.change_state(('shot_' + str(sprite)) if not self.boss else 'shot')
            self.delay['damage'] = 10
        elif self.state != 'die':
            self.change_state('die', 80)

    def attack(self, player):
        """Ataca o player"""
        if self.delay['attack'] == 0:
            player.damage(self.attack_value)
            self.change_state('attack', self.delay['attack_max'])
            self.frame = 0
        elif self.delay['attack'] <= self.delay['attack_idle']:
            self.state = 'idle'
            self.frame = 0

    def update(self, tiles, player, dt):
        """
        Atualiza os delays e a posição.
        O inimigo apenas segue a direção do player,
        utilizando a função arctan2 para descobrir o ângulo
        """
        self.angle = math.atan2(player.y - self.y, player.x - self.x)

        if self.delay['attack'] > 0:
            self.delay['attack'] -= 1
        if self.delay['die'] > 0:
            self.delay['die'] -= 1
        elif self.delay['damage'] > 0:
            self.delay['damage'] -= 1
        else:
            # A cada 60 frames trocamos a aleatoriedade
            if self.step > 60:
                self.step = 0
                self.rand_x = random.uniform(-1,1)
                self.rand_y = random.uniform(-1,1)
            else:
                self.step += 1

            # Atualizamos a direção
            self.dx = math.cos(self.angle) + self.rand_x
            self.dy = math.sin(self.angle) + self.rand_y

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
