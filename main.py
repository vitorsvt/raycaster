import pygame as pg
import sys, time, math

from player import Player
from level import Level

from pygame.locals import *

FRAMERATE = 60
WINDOW_SIZE = (640, 480)
DISPLAY_SIZE = (640, 480)

def main():
    screen, display = setup_pg()
    inputs = {
        'up': False,
        'down': False,
        'left': False,
        'right': False,
    }
    clock = pg.time.Clock()
    last = time.time()

    player = Player((22,12), (-1,0), (0, 0.66))
    level = Level((24,24))
    colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,0,255)]

    while True:
        dt, last = update_time(last)

        display.fill((50,50,50))

        level.raycast(display, player)

        player.move(level.map, dt)
        
        # rot = player.rot * dt
        # if keys['right']:
        #     old_dx = player.dx
        #     player.dx = player.dx * math.cos(-rot) - player.dy * math.sin(-rot)
        #     player.dy = old_dx * math.sin(-rot) + player.dy * math.cos(-rot)
        #     old_px = player.px
        #     player.px = player.px * math.cos(-rot) - player.py * math.sin(-rot)
        #     player.py = old_px * math.sin(-rot) + player.py * math.cos(-rot)
        # if keys['left']:
        #     old_dx = player.dx
        #     player.dx = player.dx * math.cos(rot) - player.dy * math.sin(rot)
        #     player.dy = old_dx * math.sin(rot) + player.dy * math.cos(rot)
        #     old_px = player.px
        #     player.px = player.px * math.cos(rot) - player.py * math.sin(rot)
        #     player.py = old_px * math.sin(rot) + player.py * math.cos(rot)

        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if e.key == K_w: player.inputs['up'] = True
                if e.key == K_s: player.inputs['down'] = True
                if e.key == K_a: player.inputs['left'] = True
                if e.key == K_d: player.inputs['right'] = True
            if e.type == KEYUP:
                if e.key == K_w: player.inputs['up'] = False
                if e.key == K_s: player.inputs['down'] = False
                if e.key == K_a: player.inputs['left'] = False
                if e.key == K_d: player.inputs['right'] = False

        screen.blit(display, (0, 0))

        pg.display.update()
        clock.tick(FRAMERATE)

def update_time(last):
    dt = (time.time() - last)
    return dt, time.time()

def setup_pg():
    pg.init()
    pg.display.set_caption("PyRaycaster")

    screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pg.Surface(DISPLAY_SIZE)

    return screen, display

if __name__ == "__main__":
    main()
