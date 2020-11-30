"""
Módulo de utilitários para o
carregamento de sons e spritesheets
"""

import pygame as pg
import tools

class Sound:
    """Carrega arquivos .wav e permite tocá-los"""
    def __init__(self, sounds):
        self.sounds = {}

        for key, value in sounds.items():
            self.sounds[key] = pg.mixer.Sound(value)

    def play(self, sound):
        """Toca o arquivo de som desejado"""
        self.sounds[sound].play()
        self.sounds[sound].fadeout(250) # Para previnir o ruído final

class Spritesheet:
    """
    Carrega uma spritesheet estática horizontal
    Permite tanto índices numéricos quanto strings
    """
    def __init__(self, path, tile, data, scale = 1):
        self.image = pg.image.load(path).convert_alpha()
        self.tile = tile

        if isinstance(data, list):
            # Se for uma lista, será um dicionário
            self.sprites = {}
            for x, name in enumerate(data):
                sprite = pg.transform.scale(tools.clip(
                    self.image,
                    x * self.tile, 0,
                    self.tile, self.tile
                ), (self.tile * scale, self.tile * scale))
                self.sprites[name] = sprite.copy()
        else:
            # Caso contrário apenas uma lista
            self.sprites = []
            for x in range(data):
                sprite = pg.transform.scale(tools.clip(
                    self.image,
                    x * self.tile, 0,
                    self.tile, self.tile
                ), (self.tile * scale, self.tile * scale))
                self.sprites.append(sprite.copy())

class AnimatedSpritesheet:
    """
    Carrega uma spritesheet animada, com base na entrada 'data'
    que indica o que cada linha da spritesheet significa e quantos
    quadros cada ação possui. Ver 'game.json' para um exemplo...

    'durations' é um dict de listas, sendo elas '[1,1,1,1,2,2,2...]'
    diversos frames representando qual sprite é com base em um determinado
    frame de animação
    """
    def __init__(self, path, tile, data, scale = 1):
        self.image = pg.image.load(path).convert_alpha()
        self.tile = tile
        self.sprites = {}
        self.durations = {}
        y = 0 # Deslocamento vertical (linhas)
        #for animation, y in zip(data.items(), range(len(data))): # {'animation_name': [frames...]}
        for y, animation in enumerate(data.items()):
            name = animation[0]
            frames = animation[1]
            self.sprites[name] = []
            self.durations[name] = []
            for x, frame in enumerate(frames):
                frame_image = tools.clip(
                    self.image,
                    x * self.tile, y * self.tile,
                    self.tile, self.tile
                )
                frame_image = pg.transform.scale(
                    frame_image,
                    (self.tile * scale, self.tile * scale)
                )
                self.sprites[name].append(frame_image.copy())
                for _ in range(frame):
                    self.durations[name].append(x)

    def next(self, state, frame):
        """Retorna o próximo quadro com base no estado e no quadro atual"""
        sprite = self.sprites[state][self.durations[state][frame]]
        if frame >= len(self.durations[state]) - 1:
            frame = 0
        else:
            frame += 1
        return sprite, frame
