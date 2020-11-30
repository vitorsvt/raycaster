import pygame as pg
import time, json, sys
from loaders import Sound, Tileset, AnimatedTileset
from entities import Player
from ui import Menu, Camera, Loading
from level import Level

class Game:
    def __init__(self, resolution):
        pg.mixer.pre_init(44100, -16, 2, 512)
        pg.init()
        pg.display.set_caption('Raycaster')
        # Dimensões da janela e a surface
        self.resolution = resolution
        self.screen = pg.display.set_mode(resolution, 0, 32)
        # Configurações do mouse
        pg.mouse.set_pos((resolution[0] // 2, resolution[1] // 2))
        # Propriedades relacionadas ao tempo
        self.clock = pg.time.Clock()
        self.dt = 0
        self.last = time.time()
        # Entradas
        self.inputs = {
            'up': False, 'down': False, 'left': False, 'right': False,
            'mouse': [0,0], 'lmb': False, 'rmb': False,
            'esc': False
        }
        # Estado do jogo
        self.state = "menu"
        # Fases
        self.level = None
        self.levels = None
        self.loading = 0

    def next_level(self, player):
        if self.state != "loading":
            self.level = next(self.levels, False)
            if self.level == False:
                print('Você ganhou!')
                self.quit()
            else:
                self.change_state("loading")
                self.loading = 120
        else:
            self.change_state("play")
            self.level.play()
            player.respawn(self.level.spawn)

    def change_state(self, new):
        self.inputs['lmb'] = False
        if new == "quit":
            self.quit()
        elif new in ["menu", "loading"]:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
            self.state = new
        elif new != False:
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
            self.state = new
    
    def load(self, file):
        """
        Carrega o arquivo json com as configurações e níveis
        """
        with open(file) as f:
            data = json.load(f)

        sounds = Sound(data["sounds"])
        sprites = { 
            k:(
                AnimatedTileset(*v) if isinstance(v[2], dict) else Tileset(*v)
            ) for k,v in data["sprites"].items()
        }
        self.levels = iter(Level(level, sprites) for level in data["levels"])
        self.level = next(self.levels)
        surface = int(self.resolution[0] / 1.5), int(self.resolution[1] / 1.5)
        camera = Camera(surface, sprites)
        loading = Loading(surface)
        menu = Menu(surface)
        player = Player(sounds)
        return player, camera, menu, loading

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
