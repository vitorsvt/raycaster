"""Módulo para a classe de um nível"""

import pygame as pg
from entities import Enemy, Item

class Level:
    """Classe de um nível, carregado a partir de um dict e sprites já carregados"""
    def __init__(self, data, sprites):
        # Localização inicial do jogador
        self.spawn = data["player"]
        # Tiles do mapa
        self.map = data["map"]
        self.width, self.height = len(data["map"][0]), len(data["map"])
        self.tex = 64
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

    def respawn(self, player):
        """Move o player e reseta alguns de seus stats"""
        player.x, player.y = self.spawn
        player.ammo = max(20, player.ammo)
        player.state = 'idle'
        player.weapon_frame = 0 # Caso houve troca de nível durante um tiro

    def play_music(self):
        """Toca a música deste nível"""
        pg.mixer.music.stop()
        pg.mixer.music.load(self.music)
        pg.mixer.music.play(-1)

    def update(self, player, game, dt):
        """Atualiza todas as entidades"""
        done = True # Se ainda há alguma entidade neste nível
        for entity in self.entities:
            if entity.type == "enemy":
                done = False
                if entity.health <= 0 and entity.delay['die'] == 0:
                    self.entities.remove(entity)
                else:
                    entity.update(self.map, player, dt)
            else:
                if player.pickup(entity):
                    self.entities.remove(entity)
        if done:
            game.state.next_level(player)
