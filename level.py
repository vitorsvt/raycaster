import pygame as pg
import math

from tools import *

class Level:
    def __init__(self, size, colors, textures, sprites, entities):
        self.width, self.height = size
        self.tex_width, self.tex_height = (64, 64)
        self.middle = None
        self.textures = textures
        self.color = colors
        self.entities = entities
        self.sprites = sprites
        self.map = [
            [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,7,7,7,7,7,7,7,7],
            [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,7],
            [4,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [4,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7],
            [4,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,7],
            [4,0,4,0,0,0,0,5,5,5,5,5,5,5,5,5,7,7,0,7,7,7,7,7],
            [4,0,5,0,0,0,0,5,0,5,0,5,0,5,0,5,7,0,0,0,7,7,7,1],
            [4,0,6,0,0,0,0,5,0,0,0,0,0,0,0,5,7,0,0,0,0,0,0,8],
            [4,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,1],
            [4,0,8,0,0,0,0,5,0,0,0,0,0,0,0,5,7,0,0,0,0,0,0,8],
            [4,0,0,0,0,0,0,5,0,0,0,0,0,0,0,5,7,0,0,0,7,7,7,1],
            [4,0,0,0,0,0,0,5,5,5,5,0,5,5,5,5,7,7,7,7,7,7,7,1],
            [6,6,6,6,6,6,6,6,6,6,6,0,6,6,6,6,6,6,6,6,6,6,6,6],
            [8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
            [6,6,6,6,6,6,0,6,6,6,6,0,6,6,6,6,6,6,6,6,6,6,6,6],
            [4,4,4,4,4,4,0,4,4,4,6,0,6,2,2,2,2,2,2,2,3,3,3,3],
            [4,0,0,0,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,0,0,0,2],
            [4,0,0,0,0,0,0,0,0,0,0,0,6,2,0,0,5,0,0,2,0,0,0,2],
            [4,0,0,0,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,2,0,2,2],
            [4,0,6,0,6,0,0,0,0,4,6,0,0,0,0,0,5,0,0,0,0,0,0,2],
            [4,0,0,5,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,2,0,2,2],
            [4,0,6,0,6,0,0,0,0,4,6,0,6,2,0,0,5,0,0,2,0,0,0,2],
            [4,0,0,0,0,0,0,0,0,4,6,0,6,2,0,0,0,0,0,2,0,0,0,2],
            [4,4,4,4,4,4,4,4,4,4,1,1,1,2,2,2,2,2,2,3,3,3,3,3]
        ]
        self.zbuffer = []

    def raycast(self, surface, player):
        """
        Algoritmo de raycast (e a aplicação em C++) foi retirado do site:
        https://lodev.org/cgtutor/raycasting.html
        """
        w, h = surface.get_size() # Dimensões da tela

        self.zbuffer = [0] * w

        # Cores do chão e do teto
        surface.fill(self.color['floor'], pg.Rect(0,h/2,w,h/2))
        surface.fill(self.color['ceil'], pg.Rect(0,0,w,h/2))

        for x in range(w):
            camera_x = 2 * x / w - 1

            # Definindo direção do raio
            ray_dx = player.dx + player.px * camera_x
            ray_dy = player.dy + player.py * camera_x

            # Salvando a posição atual do player (estimada com int)
            map_x = int(player.x)
            map_y = int(player.y)

            # Definindo os deltas
            """
            Deltas são a distância que um ponto precisa para chegar
            até a próxima linha horizontal ou vertical (x ou y)
            """
            delta_x = 0 if ray_dy == 0 else (1 if ray_dx == 0 else abs(1 / ray_dx))
            delta_y = 0 if ray_dx == 0 else (1 if ray_dy == 0 else abs(1 / ray_dy))

            # Definindo os valores que utilizaremos nos raios no raycasting
            if ray_dx < 0:
                step_x = -1
                side_x = (player.x - map_x) * delta_x
            else:
                step_x = 1
                side_x = (1 + map_x - player.x) * delta_x
            if ray_dy < 0:
                step_y = -1
                side_y = (player.y - map_y) * delta_y
            else:
                step_y = 1
                side_y = (1 + map_y - player.y) * delta_y


            # Enquanto não atingirmos uma parede
            hit = False
            while not hit:
                if side_x < side_y:
                    side_x += delta_x
                    map_x += step_x
                    horizontal = True
                else:
                    side_y += delta_y
                    map_y += step_y
                    horizontal = False
                if self.map[map_x][map_y] > 0:
                    hit = True
            
            # Checa se é horizontal ou vertical
            if horizontal:
                distance = (map_x - player.x + (1 - step_x) / 2) / ray_dx
            else:
                distance = (map_y - player.y + (1 - step_y) / 2) / ray_dy
            distance += 0.1

            self.zbuffer[x] = distance

            line_height = int(h / distance)

            if line_height > 2000: line_height = 2000

            # Definimos o começo e fim da parede (y)
            draw_start = -line_height/2 + h/2
            draw_end = line_height/2 + h/2
            # Salvamos a altura da parede, com base na diferença
            draw_height = int(draw_end - 1) - int(draw_start)

            # Definimos qual a textura da parede que atingimos
            tex_image = self.textures[self.map[map_x][map_y] - 1]

            # Definimos qual o "ponto x" que atingimos da parede
            if horizontal:
                wall_x = player.y + distance * ray_dy
            else:
                wall_x = player.x + distance * ray_dx
            # Após isso, "wall_x" será entre 0 e 1
            wall_x -= math.floor(wall_x)

            # Qual o "ponto x" da textura que utilizaremos
            tex_x = int(wall_x * self.tex_width)
            if (horizontal and ray_dx > 0) or (not horizontal and ray_dy < 0):
                tex_x = self.tex_width - tex_x - 1

            # Definimos o step, para descobrirmos a altura da textura
            step = self.tex_height / line_height

            # Início da textura (y)
            tex_pos = (draw_start + line_height/2 - h/2) * step
            # Usamos "and" para caso de overflow
            tex_y = int(tex_pos) & (self.tex_height - 1)
            # Definimos a altura da textura (h)
            tex_height = step * draw_height

            # Recortamos a linha vertical da textura, e aumentamos a altura
            vline = pg.transform.scale(clip(
                tex_image,
                tex_x,
                tex_y,
                1,
                tex_height
            ), (1, draw_height))

            # Sombra
            if horizontal:
                shadow = pg.Surface(vline.get_size())
                shadow.set_alpha(150)
                vline.blit(shadow, (0, 0))

            # Blit da linha vertical na surface
            surface.blit(
                vline,
                (x, draw_start)
            )

    def spritecast(self, surface, player):
        w, h = surface.get_size() # Dimensões da tela
        self.middle = None

        for e in self.entities:
            e.distance = basic_distance((e.x, e.y), (player.x, player.y))

        self.entities.sort(key=lambda e: e.distance, reverse=True)

        for entity in self.entities:
            sprite, entity.frame = self.sprites[entity.get_sprite()].next(entity.frame)
            tex_width, tex_height = sprite.get_size()

            sprite_x = entity.x - player.x
            sprite_y = entity.y - player.y

            inv_det = 1 / (player.px * player.dy - player.dx * player.py)

            transform_x = inv_det * (player.dy * sprite_x - player.dx * sprite_y)
            transform_y = inv_det * (-player.py * sprite_x + player.px * sprite_y)

            sprite_screen_x = int((w/2) * (1 + transform_x / transform_y))

            sprite_height = abs(int(h / transform_y))
            if sprite_height > 1000: sprite_height = 1000

            draw_start_y = int(-sprite_height/2 + h/2)
            draw_end_y = int(sprite_height/2 + h/2)

            sprite_width = abs(int(h / transform_y))
            draw_start_x = int(-sprite_width/2 + sprite_screen_x)
            draw_end_x = int(sprite_width/2 + sprite_screen_x)
            
            if draw_start_x < w/2 < draw_end_x and 0 < transform_y < self.zbuffer[int(w/2)]:
                self.middle = entity

            for stripe in range(draw_start_x, draw_end_x):
                if (transform_y > 0 and stripe > 0 and stripe < w and transform_y < self.zbuffer[stripe]):
                    tex_x = int(
                        (stripe - (-sprite_width / 2 + sprite_screen_x)) * tex_width / sprite_width
                    )
                    tex_y = ((draw_end_y - 1) - h/2 + sprite_height/2) * tex_height / sprite_height
                    vline = pg.transform.scale(clip(
                        sprite,
                        tex_x,
                        0,
                        1,
                        tex_y
                    ), (1, draw_end_y - draw_start_y))

                    surface.blit(
                        vline,
                        (stripe, draw_start_y)
                    )