import pygame as pg
import time, sys

class Game:
    def __init__(self, resolution):
        pg.init()
        pg.display.set_caption('Raycaster')
        pg.mixer.music.load('./sound/music.wav')
        pg.mixer.music.play(-1)

        # Dimensões da janela e a surface
        self.resolution = resolution
        self.screen = pg.display.set_mode(resolution, 0, 32)

        pg.mouse.set_pos((resolution[0] // 2, resolution[1] // 2))
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Propriedades relacionadas ao tempo
        self.clock = pg.time.Clock()
        self.dt = 0
        self.last = time.time()

    def update(self, surface, framerate):
        """
        Realiza o blit de uma surface na janela do jogo, fazendo um
        resize para poder utilizar a resolução da janela completa
        """
        self.screen.blit(pg.transform.scale(surface, self.resolution), (0,0))
        pg.display.update()
        self.clock.tick(framerate)

    def quit(self):
        """
        Ações necessárias para finalizar corretamente o jogo
        """
        pg.quit()
        sys.exit()

    def update_time(self):
        """
        Atualiza o dt (delta time) para poder equilibrar os cálculos
        de distância do jogo caso haja queda de framerate
        """
        self.dt = time.time() - self.last
        self.last = time.time()