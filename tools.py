import pygame as pg
import math

def clip(surface, x, y, w, h):
    handle = surface.copy()
    clip_rect = pg.Rect(x, y, w, h)
    handle.set_clip(clip_rect)
    image = surface.subsurface(handle.get_clip())
    return image.copy()

def basic_distance(a, b):
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)