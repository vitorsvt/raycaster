import pygame as pg
import numpy as np

import tools

class Tileset:
    def __init__(self, path, tile, data, scale = 1):
        self.image = pg.image.load(path).convert_alpha()
        self.tile = tile

        if isinstance(data, list):
            self.sprites = {}
            for x in range(len(data)):
                sprite = pg.transform.scale(tools.clip(
                    self.image,
                    x * self.tile, 0,
                    self.tile, self.tile
                ), (self.tile * scale, self.tile * scale))
                self.sprites[data[x]] = sprite.copy()
        else:
            self.sprites = []
            for x in range(data):
                sprite = pg.transform.scale(tools.clip(
                    self.image,
                    x * self.tile, 0,
                    self.tile, self.tile
                ), (self.tile * scale, self.tile * scale))
                self.sprites.append(sprite.copy())

class AnimatedTileset:
    def __init__(self, path, tile, data, scale = 1):
        self.image = pg.image.load(path).convert_alpha()
        self.tile = tile
        self.sprites = {}
        self.durations = {}
        y = 0 # Deslocamento vertical (linhas)
        for animation, y in zip(data.items(), range(len(data))): # {'animation_name': [frames...]}
            name = animation[0]
            self.sprites[name] = []
            self.durations[name] = []
            for frame, x in zip(animation[1], range(len(animation[1]))):
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
                for i in range(frame):
                    self.durations[name].append(x)

    def next(self, state, frame):
        sprite = self.sprites[state][self.durations[state][frame]]
        if frame >= len(self.durations[state]) - 1:
            frame = 0
        else:
            frame += 1
        return sprite, frame
