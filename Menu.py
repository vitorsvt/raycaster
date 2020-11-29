import pygame as pg

class Menu:
    def __init__(self, size):
        self.size = size
        self.surface = pg.Surface(size)

        self.background = pg.Rect((0,0), size)
        self.play = pg.Rect(0, 160, 240, 80)
        self.exit = pg.Rect(0, 240, 240, 80)

    def draw(self):
        pg.draw.rect(self.surface, (15,15,15), self.background)
        pg.draw.rect(self.surface, (0,255,0), self.play)
        pg.draw.rect(self.surface, (255,0,0), self.exit)