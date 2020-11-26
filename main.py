import pygame as pg
import sys, time, math

from player import Player
from level import Level
from entity import Enemy, Item, Scenario
from Game import Game
from Tileset import Tileset, AnimatedTileset
from Camera import Camera

from pygame.locals import *

def main():
    game = Game((480, 320))
    sprites = {
        'enemy': AnimatedTileset('./sprites/enemy.png', 64, {
            'idle': [1],
            'run': [5,5,5,5],
            'attack': [2,2,2,2,2,2],
            'shot_1': [10],
            'shot_2': [10],
            'die': [5,5,5,5,80]
        }),
        'pistol': AnimatedTileset('./sprites/pistol.png', 32, {
            'idle': [1],
            'shoot': [5,5,5,5,5]
        }, 5),
        'walls': Tileset('./sprites/walls.png', 64, 9)
    }
    player = Player((2,2))
    level = Level('./map.json')
    camera = Camera((480, 320), sprites)

    while True:
        game.update_time()
        player.inputs['mouse'] = pg.mouse.get_rel()
        camera.raycast(level, player)
        camera.spritecast(level, player)
        player.draw_weapon(camera.surface, sprites)
        player.move(level.map, camera.middle, game.dt)
        player.update()
        level.update(player, game.dt)
        
        for e in pg.event.get():
            if e.type == QUIT:
                game.quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    game.quit()
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

        game.update(camera.surface, 60)

if __name__ == "__main__":
    main()
