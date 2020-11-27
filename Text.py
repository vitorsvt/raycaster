import pygame as pg

def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pg.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!\"#$%&'()*+,-./"
        font_img = pg.image.load(path).convert()
        font_img.set_colorkey((0,0,0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()
        self.height = self.characters['A'].get_height()

    def render(self, surf, text, loc, change = (0,0)):
        length = len(text)

        x_offset = y_offset = 0
        for i in range(length):
            char = text[i]
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1] + y_offset))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

            if i < int(length / 2) - 1:
                y_offset += change[0]
            else:
                y_offset -= change[1]