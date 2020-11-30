import pygame as pg
from game import Game
from ui import Menu, Camera
from entities import Player

from pygame.locals import *

def main():
    game = Game((720, 480))
    data, sprites, sounds = game.load('game.json')

    menu = Menu((480, 320))
    player = Player(sounds)
    camera = Camera((480, 320), sprites)

    game.levels[game.level].play()
    player.x, player.y = game.levels[game.level].spawn

    while True:
        game.update_time()
        game.inputs['mouse'] = pg.mouse.get_rel()

        if game.state == "play":
            camera.raycast(game.levels[game.level], player)
            camera.spritecast(game.levels[game.level], player)
            camera.draw_hud(player)
            player.move(game, game.levels[game.level].map, camera.middle)
            player.update(game)
            game.levels[game.level].update(player, game)
            game.update(camera.surface, 60)
        elif game.state == "menu":
            menu.draw()
            if game.inputs['lmb']:
                new = menu.click()
                game.change_state(new)
            game.update(menu.surface, 60)

        for e in pg.event.get():
            if e.type == QUIT:
                game.quit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE: game.inputs['esc'] = True
                if e.key == K_w: game.inputs['up'] = True
                if e.key == K_s: game.inputs['down'] = True
                if e.key == K_a: game.inputs['left'] = True
                if e.key == K_d: game.inputs['right'] = True
            if e.type == KEYUP:
                if e.key == K_ESCAPE: game.inputs['esc'] = False
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
