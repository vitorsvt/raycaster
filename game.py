"""Módulo de setup do jogo, com a classe para a inicialização"""

import time
import json
import pygame as pg
import tools
from loaders import Sound, Spritesheet, AnimatedSpritesheet
from entities import Player
from ui import Camera, Interface
from level import Level

class State:
    """Gerencia o estado do jogo"""
    def __init__(self, levels):
        # Estado do jogo
        self.current = "menu"
        # Fases
        self.levels = levels
        self.level = next(self.levels)

    def next_level(self, player):
        """Muda de nível, ativa a loading screen e respawna o player"""
        if self.current != "loading":
            self.level = next(self.levels, False)
            if not self.level:
                self.change_state("victory")
            else:
                self.change_state("loading")
        else:
            self.change_state("play")
            self.level.play_music()
            self.level.respawn(player)

    def change_state(self, new):
        """Atualiza o estado e faz mudanças necessárias"""
        if new == "quit":
            tools.end()
        elif new == "play":
            pg.event.set_grab(True)
            pg.mouse.set_visible(False)
        else:
            pg.event.set_grab(False)
            pg.mouse.set_visible(True)
        self.current = new

class Game:
    """
    Classe de setup do jogo, inicializa funções do pygame,
    as classes e armazena utilidades, como o estado e os inputs
    """
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
        self.last = time.time()
        # Entradas
        self.mappings = {
            pg.K_w: 'up',
            pg.K_s: 'down',
            pg.K_a: 'left',
            pg.K_d: 'right',
            pg.K_ESCAPE: 'esc'
        }
        self.inputs = {
            'up': False, 'down': False, 'left': False, 'right': False,
            'mouse': [0,0], 'lmb': False, 'esc': False, 0: False
        }
        # Estado
        self.state = None

    def load(self, file):
        """
        Carrega o arquivo json com as configurações e níveis
        """
        with open(file) as f:
            data = json.load(f)
        sounds = Sound(data["sounds"])
        sprites = {
            k:(AnimatedSpritesheet(*v) if isinstance(v[2], dict) else Spritesheet(*v))
            for k, v in data["sprites"].items()
        }
        levels = iter(Level(level, sprites) for level in data["levels"])
        self.state = State(levels)
        surface = int(self.resolution[0] / 1.5), int(self.resolution[1] / 1.5)
        camera = Camera(surface, sprites)
        interface = Interface(surface, data["music"]["victory"])
        player = Player(sounds)
        return player, camera, interface

    def update(self, surface, framerate):
        """
        Realiza o blit de uma surface na janela do jogo, fazendo um
        resize para poder utilizar a resolução da janela completa
        """
        self.screen.blit(pg.transform.scale(surface, self.resolution), (0,0))
        pg.display.update()
        self.clock.tick(framerate)

    def update_time(self):
        """
        Atualiza o dt (delta time) para poder equilibrar os cálculos
        de distância do jogo caso haja queda de framerate
        """
        dt = time.time() - self.last
        self.last = time.time()
        return dt
