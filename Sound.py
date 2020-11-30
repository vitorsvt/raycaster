import pygame as pg

class Sound:
    def __init__(self, sounds):
        self.sounds = {}

        for key, value in sounds.items():
            self.sounds[key] = pg.mixer.Sound(value)

    def play(self, sound):
        self.sounds[sound].play()
        self.sounds[sound].fadeout(250) # Para previnir o ruído final