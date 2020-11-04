import pygame as pg
import sys, time

from pygame.locals import *

FRAMERATE = 60
WINDOW_SIZE = (1024, 512)
DISPLAY_SIZE = (512, 512)

def main():
    screen, display_2d, display_3d = setup_pg()
    keys = {
        'up': False,
        'down': False,
        'left': False,
        'right': False,
    }
    clock = pg.time.Clock()
    last = time.time()

    while True:
        dt, last = update_time(last)
        display_2d.fill((15,15,15))
        display_3d.fill((50,50,50))

        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()

    screen.blit(display_2d, (0, 0))
    screen.blit(display_3d, (512, 0))

    pg.display.update()
    clock.tick(FRAMERATE)

def update_time(last):
    return (time.time() - last)*60, time.time()

def setup_pg():
    pg.init()
    pg.display.set_caption("PyRaycaster")

    screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
    display1 = pg.Surface(DISPLAY_SIZE)
    display2 = pg.Surface(DISPLAY_SIZE)

    return screen, display1, display2

if __name__ == "__main__":
    main()
