import pygame as pg

class Player:
    def __init__(self, pos, direction, camera):
        self.x, self.y = pos
        self.dx, self.dy = direction
        self.px, self.py = camera

        self.speed = 10
        self.rot = 3