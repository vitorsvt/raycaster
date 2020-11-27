import pygame as pg
import math, json
import numpy as np

from tools import *
from entity import Enemy

class Level:
    def __init__(self, file):
        with open(file) as f:
            data = json.load(f)
        
        self.map = data["map"]
        self.nmap = np.array(data["map"])
        self.width, self.height = len(data["map"][0]), len(data["map"])
        self.color = tuple(data["floor_color"]), tuple(data["ceil_color"])
        self.entities = [Enemy(pos) for pos in data["enemies"]]

        self.tex_width, self.tex_height = (64, 64)

    def update(self, player, dt):
        for entity in self.entities:
            if entity.health <= 0 and entity.delay['die'] == 0:
                self.entities.remove(entity)
            else:
                entity.update(self.map, player, dt)

    