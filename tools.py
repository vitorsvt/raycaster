import pygame as pg
import math

def clip(surface, x, y, w, h):
    handle = surface.copy()
    clip_rect = pg.Rect(x, y, w, h)
    handle.set_clip(clip_rect)
    image = surface.subsurface(handle.get_clip())
    return image.copy()