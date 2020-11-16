import pygame as pg

class Sprite:
    def __init__(self, path, durations, scale = 1):
        self.textures = {}
        self.durations = []

        name = path.split('/')[-1]
        for frame, n in zip(durations, range(len(durations))):
            frame_id = name + "_" + str(n)
            frame_image = pg.image.load(path + "/" + frame_id + ".png").convert_alpha()
            frame_image = pg.transform.scale(
                frame_image,
                (frame_image.get_width() * scale, frame_image.get_height() * scale)
            )
            self.textures[frame_id] = frame_image.copy()
            for i in range(frame):
                self.durations.append(frame_id)

    def next(self, frame):
        sprite = self.textures[self.durations[frame]]
        if frame >= len(self.durations) - 1:
            frame = 0
        else:
            frame += 1
        return sprite, frame