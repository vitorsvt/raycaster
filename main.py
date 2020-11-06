import pygame as pg
import sys, time, math

from player import Player
from level import Level
from sprite import Sprite
from entity import Enemy, Item, Scenario

from pygame.locals import *

FRAMERATE = 60
WINDOW_SIZE = (480, 320)
DISPLAY_SIZE = (480, 320)
WINDOW_CENTER = (240, 160)

def main():
    screen, display = setup_pg()

    sprites = {}
    sprites['pistol_idle'] = Sprite('pistol', [1], 5)
    sprites['pistol_shoot'] = Sprite('pistol', [5]*5, 5)
    sprites['lamp'] = Sprite('lamp', [1])

    player = Player((22,11.5), (-1,0), (0, 0.66))
    inputs = {
        'up': False,
        'down': False,
        'left': False,
        'right': False,
    }
    textures = [
            'walls/eagle.png',
            'walls/redbrick.png',
            'walls/purplestone.png',
            'walls/greystone.png',
            'walls/bluestone.png',
            'walls/mossy.png',
            'walls/wood.png',
            'walls/colorstone.png'
    ]
    level = Level(
        (24,24),
        {'floor': (15,5,5), 'ceil': (35,5,5)}, 
        [pg.image.load(i).convert_alpha() for i in textures],
        sprites,
        [
            Scenario((20.5, 11.5), 'lamp')
            # Sprite((20.5, 11.5), 8),
            # Sprite((15.5, 11.5), 8),
            # Sprite((10.5, 11.5), 8),
            # Sprite((8.5, 11.5), 9)
        ]
    )

    clock = pg.time.Clock()
    last = time.time()
    while True:
        dt, last = update_time(last)
        player.inputs['mouse'] = pg.mouse.get_rel()

        level.raycast(display, player)
        level.spritecast(display, player)
        player.draw_weapon(display, sprites)
        player.move(level.map, dt)
        
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

        screen.blit(pg.transform.scale(display, WINDOW_SIZE), (0, 0))

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

    pg.mouse.set_pos(WINDOW_CENTER)
    pg.event.set_grab(True)
    pg.mouse.set_visible(False)

    return screen, display

if __name__ == "__main__":
    main()
