import pygame as pg
import math, json

from Entities import Enemy, Item

class Level:
    def __init__(self, data, sprites):
        # Localização inicial do jogador
        self.spawn = data["player"]
        # Tiles do mapa
        self.map = data["map"]
        self.width, self.height = len(data["map"][0]), len(data["map"])
        self.tex_width, self.tex_height = 64, 64
        # Cores
        self.color = tuple(data["colors"]["floor"]), data["colors"]["ceil"]
        self.dark = data["colors"]["dark"]
        # Música de fundo
        self.music = data["music"]
        # Inimigos e itens
        self.entities = [
            Enemy(pos, sprites["enemy"]) for pos in data["enemies"]
        ] + [
            Item(pos, sprites["items"].sprites[item], item) for item, pos in data["items"]
        ]

    def play(self):
        pg.mixer.music.stop()
        pg.mixer.music.load(self.music)
        pg.mixer.music.play(-1)

    def update(self, player, dt):
        for entity in self.entities:
            if entity.type == "enemy":
                if entity.health <= 0 and entity.delay['die'] == 0:
                    self.entities.remove(entity)
                else:
                    entity.update(self.map, player, dt)
            else:
                if entity.x == int(player.x) and entity.y == int(player.y):
                    player.health = min(100, player.health + entity.values["health"])
                    player.ammo += entity.values["ammo"]
                    self.entities.remove(entity)
    