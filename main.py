import pygame as pg

from Player import Player
from Level import Level
from Entities import Enemy, Item
from Game import Game
from Menu import Menu
from Tileset import Tileset, AnimatedTileset
from Camera import Camera
from Sound import Sound

from pygame.locals import *

def main():
    game = Game((720, 480))
    data, sprites, sounds = game.load('game.json')

    menu = Menu((480, 320))
    level = Level(data["levels"][0], sprites)
    player = Player(sounds)
    camera = Camera((480, 320), sprites)

    level.play()
    player.x, player.y = level.spawn

    while True:
        game.update_time()
        game.inputs['mouse'] = pg.mouse.get_rel()

        if game.state == "play":
            camera.raycast(level, player)
            camera.spritecast(level, player)
            camera.draw_hud(player)

            player.move(game.inputs, level.map, camera.middle, game.dt)
            player.update()
            level.update(player, game.dt)
        
            game.update(camera.surface, 60)
        elif game.state == "menu":
            menu.draw()
            game.update(menu.surface, 60)

        for e in pg.event.get():
            if e.type == QUIT:
                game.quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    game.quit()
                if e.key == K_w: game.inputs['up'] = True
                if e.key == K_s: game.inputs['down'] = True
                if e.key == K_a: game.inputs['left'] = True
                if e.key == K_d: game.inputs['right'] = True
            if e.type == KEYUP:
                if e.key == K_w: game.inputs['up'] = False
                if e.key == K_s: game.inputs['down'] = False
                if e.key == K_a: game.inputs['left'] = False
                if e.key == K_d: game.inputs['right'] = False
            if e.type == MOUSEBUTTONDOWN:
                game.inputs['lmb'] = True
            if e.type == MOUSEBUTTONUP:
                game.inputs['lmb'] = False


if __name__ == "__main__":
    main()
