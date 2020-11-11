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

    sprites['zombie_idle'] = Sprite('assets/zombie_idle', [1])
    sprites['zombie_run'] = Sprite('assets/zombie_run', [5]*4)
    sprites['zombie_attack'] = Sprite('assets/zombie_attack', [2,2,2,2,2,2])
    sprites['zombie_shot_1'] = Sprite('assets/zombie_shot_1', [10])
    sprites['zombie_shot_2'] = Sprite('assets/zombie_shot_2', [10])
    sprites['zombie_die'] = Sprite('assets/zombie_die', [5]*4 + [60])

    player = Player((22,11.5), (-1,0), (0, 0.66))
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
            Enemy((20.5, 11.5), 'zombie'),
            # Enemy((10.5, 11.5), 'zombie'),
            # Enemy((10.5, 10.5), 'zombie'),
            # Enemy((10.5, 9.5), 'zombie')
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

        player.move(level.map, level.middle, dt)
        player.update()

        level.update(player, dt)
        
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
            if e.type == MOUSEBUTTONDOWN:
                player.inputs['lmb'] = True
            if e.type == MOUSEBUTTONUP:
                player.inputs['lmb'] = False

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
