import pygame as pg
import math

class Player:
    def __init__(self, pos, direction, camera):
        self.x, self.y = pos
        self.dx, self.dy = direction
        self.px, self.py = camera

        self.speed = 5.0
        self.rot = 3.0

        self.inputs = {
            'up': False, 'down': False, 'left': False, 'right': False,
            'mouse': [0,0]
        }

    def collide(self, tiles, delta):
        return tiles[int(delta[0])][int(delta[1])] == 0

    def move(self, tiles, dt):
        if self.inputs['up']:
            new_x = self.x + self.dx * self.speed * dt
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y + self.dy * self.speed * dt
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if self.inputs['down']:
            new_x = self.x - self.dx * self.speed * dt
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y - self.dy * self.speed * dt
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if self.inputs['left']:
            new_x = self.x - self.dy * self.speed * dt
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y + self.dx * self.speed * dt
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if self.inputs['right']:
            new_x = self.x + self.dy * self.speed * dt
            if self.collide(tiles, (new_x, self.y)):
                self.x = new_x
            new_y = self.y - self.dx * self.speed * dt
            if self.collide(tiles, (self.x, new_y)):
                self.y = new_y
        if self.inputs['mouse'][0] != 0:
            rotation = -(self.inputs['mouse'][0]) * 0.08 * dt

            old_dx = self.dx
            self.dx = self.dx * math.cos(rotation) - self.dy * math.sin(rotation)
            self.dy = old_dx * math.sin(rotation) + self.dy * math.cos(rotation)
            old_px = self.px
            self.px = self.px * math.cos(rotation) - self.py * math.sin(rotation)
            self.py = old_px * math.sin(rotation) + self.py * math.cos(rotation)