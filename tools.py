"""Módulo de ferramentas que não necessitam estar contidas em uma classe"""

import math
import sys
import pygame as pg

def end():
    """Finalizar o jogo"""
    pg.quit()
    sys.exit()

def clip(surface, x, y, w, h):
    """Recorta um retângulo de uma superfície"""
    handle = surface.copy()
    clip_rect = pg.Rect(x, y, w, h)
    handle.set_clip(clip_rect)
    image = surface.subsurface(handle.get_clip())
    return image

def basic_distance(a, b):
    """Calcula uma distância entre dois pontos, sem calcular a raiz"""
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

def collide(tiles, pos):
    """Checa se determinado ponto em uma matriz é 0"""
    return tiles[int(pos[0])][int(pos[1])] == 0

def distance(a, b):
    """Distância utilizando o teorema de pitágoras completo"""
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def wrap_angle(a):
    """Ajeita o ângulo ao passarmos de 2pi ou de 0 (wrap around)"""
    if a > 2 * math.pi:
        a -= 2 * math.pi
    elif a < 0:
        a += 2 * math.pi
    return a
