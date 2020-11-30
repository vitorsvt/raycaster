import pygame as pg

from Text import Font

class Menu:
    def __init__(self, size):
        self.size = size
        self.surface = pg.Surface(size)

        self.background = pg.Rect((0,0), size)
        self.font = Font('./sprites/font.png')
        self.play = pg.Rect(30, 160, 200, 50)
        self.exit = pg.Rect(30, 240, 200, 50)

    def draw(self):
        pg.draw.rect(self.surface, (15,15,15), self.background)
        pg.draw.rect(self.surface, (0,255,0), self.play)
        pg.draw.rect(self.surface, (255,0,0), self.exit)
        self.font.render(self.surface, 'PLAY',
            (45, 185 - self.font.height / 2)
        )
        self.font.render(self.surface, 'EXIT',
            (45, 265 - self.font.height / 2)
        )


    def click(self):
        pos = pg.mouse.get_pos()
        pos = int(pos[0] / 1.5), int(pos[1] / 1.5)
        if self.play.collidepoint(pos):
            return "play"
        elif self.exit.collidepoint(pos):
            return "quit"
        else:
            return False
