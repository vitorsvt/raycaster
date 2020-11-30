"""Arquivo principal do jogo"""

import pygame as pg
import tools
from game import Game

def main():
    """Inicializa a classe do jogo e realiza o loop principal"""
    game = Game((720, 480))
    player, camera, menu, loading = game.load('game.json')
    level = game.state.level
    level.play_music()
    level.respawn(player)
    while True: # Loop principal
        dt = game.update_time() # Calcula o delta time
        game.inputs['mouse'] = pg.mouse.get_rel() # Armazena se houve movimentação do mouse
        if game.state.current == "play": # Se estivermos jogando
            camera.raycast(level, player)
            camera.spritecast(level, player)
            camera.draw_hud(player)
            player.move(game, level.map, camera.middle, dt)
            player.update(game)
            level.update(player, game, dt)
            game.update(camera.surface, 60) # Desenha tudo
        elif game.state.current == "menu": # Se estiver pausado / menu
            menu.draw()
            if game.inputs['lmb']:
                game.inputs['lmb'] = False
                new = menu.click()
                if new:
                    game.state.change_state(new)
            game.update(menu.surface, 60) # Desenha tudo
        elif game.state.current == "loading": # Se estiver carregando
            loading.draw()
            if game.state.loading == 0:
                game.state.next_level(player)
                level = game.state.level
            else:
                game.state.loading -= 1
            game.update(loading.surface, 60) # Desenha tudo

        for event in pg.event.get():
            # Atualiza os inputs
            if event.type == pg.QUIT:
                tools.end()
            elif event.type in [pg.KEYDOWN, pg.KEYUP]:
                game.inputs[game.mappings.get(event.key, 0)] = event.type == pg.KEYDOWN
            elif event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                game.inputs['lmb'] = event.type == pg.MOUSEBUTTONDOWN

if __name__ == "__main__":
    main()
