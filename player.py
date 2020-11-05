import pygame as pg

class Player:
    def __init__(self, pos, direction, camera):
        self.x, self.y = pos
        self.dx, self.dy = direction
        self.px, self.py = camera

        self.speed = 5.0
        self.rot = 3.0

        self.inputs = {
            'up': False, 'down': False, 'left': False, 'right': False
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
