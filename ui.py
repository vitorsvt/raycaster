import pygame as pg
import math, tools

class Menu:
    def __init__(self, size):
        self.size = size
        self.surface = pg.Surface(size)

        self.background = pg.Rect((0,0), size)
        self.font = Font('./sprites/font.png')
        self.play = pg.Rect(30, 160, 200, 50)
        self.exit = pg.Rect(30, 240, 200, 50)

    def draw(self):
        pg.draw.rect(self.surface, (15,15,15), self.background)
        pg.draw.rect(self.surface, (0,255,0), self.play)
        pg.draw.rect(self.surface, (255,0,0), self.exit)
        self.font.render(self.surface, 'PLAY',
            (45, 185 - self.font.height / 2)
        )
        self.font.render(self.surface, 'EXIT',
            (45, 265 - self.font.height / 2)
        )

    def click(self):
        pos = pg.mouse.get_pos()
        pos = int(pos[0] / 1.5), int(pos[1] / 1.5)
        if self.play.collidepoint(pos):
            return "play"
        elif self.exit.collidepoint(pos):
            return "quit"
        else:
            return False

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
                char_img = tools.clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
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

class Camera:
    def __init__(self, size, sprites):
        self.font = Font('./sprites/font.png')
        self.size = size
        self.surface = pg.Surface(size)
        self.sprites = sprites
        self.middle = None
        self.zbuffer = []

    def draw_hud(self, player):
        w, h = self.size
        # Health
        self.font.render(self.surface, 'HEALTH', (10, h - 2*(self.font.height + 10)))
        self.font.render(self.surface, str(player.health) + "%", (10, h - (self.font.height + 10)))
        # Ammo
        self.font.render(self.surface, 'AMMO', (w - 4*self.font.space_width - 10, h - 2*(self.font.height + 10)))
        ammo = str(player.ammo)
        self.font.render(self.surface, ammo,
            (w - len(ammo) * self.font.space_width - 10, h - (self.font.height + 10))
        )
        # Viewmodel
        self.draw_weapon(player)

    def draw_weapon(self, player):
        sprite, player.weapon_frame = self.sprites[player.weapon].next(player.state, player.weapon_frame)
        w, h = self.size
        sw, sh = sprite.get_size()

        self.surface.blit(
            sprite,
            (
                (w - sw)/2 + player.offx,
                h - sh + player.offy + 6
            )
        )

    def raycast(self, level, player):
        """
        Algoritmo de raycast foi retirado do site (aplicação em C++):
        https://lodev.org/cgtutor/raycasting.html
        """
        w, h = self.size # Dimensões da tela

        # if self.zbuffer != []:
        #     print(min(self.zbuffer), max(self.zbuffer))

        self.zbuffer = []

        # Cores do chão e do teto
        self.surface.fill(level.color[0], pg.Rect(0,h/2,w,h/2))
        self.surface.fill(level.color[1], pg.Rect(0,0,w,h/2))

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
                if level.map[map_x][map_y] > 0:
                    hit = True
            
            # Checa se é horizontal ou vertical
            if horizontal:
                distance = (map_x - player.x + (1 - step_x) / 2) / ray_dx
            else:
                distance = (map_y - player.y + (1 - step_y) / 2) / ray_dy
            distance += 0.1

            self.zbuffer.append(distance)

            line_height = int(h / distance)

            if line_height > 2000: line_height = 2000

            # Definimos o começo e fim da parede (y)
            draw_start = -line_height/2 + h/2
            draw_end = line_height/2 + h/2
            # Salvamos a altura da parede, com base na diferença
            draw_height = int(draw_end - 1) - int(draw_start)

            # Definimos qual a textura da parede que atingimos
            tex_image = self.sprites['walls'].sprites[level.map[map_x][map_y] - 1]

            # Definimos qual o "ponto x" que atingimos da parede
            if horizontal:
                wall_x = player.y + distance * ray_dy
            else:
                wall_x = player.x + distance * ray_dx
            # Após isso, "wall_x" será entre 0 e 1
            wall_x -= math.floor(wall_x)

            # Qual o "ponto x" da textura que utilizaremos
            tex_x = int(wall_x * level.tex_width)
            if (horizontal and ray_dx > 0) or (not horizontal and ray_dy < 0):
                tex_x = level.tex_width - tex_x - 1

            # Definimos o step, para descobrirmos a altura da textura
            step = level.tex_height / line_height

            # Início da textura (y)
            tex_pos = (draw_start + line_height/2 - h/2) * step
            # Usamos "and" para caso de overflow
            tex_y = int(tex_pos) & (level.tex_height - 1)
            # Definimos a altura da textura (h)
            tex_height = step * draw_height

            # Recortamos a linha vertical da textura, e aumentamos a altura
            vline = pg.transform.scale(tools.clip(
                tex_image,
                tex_x,
                tex_y,
                1,
                tex_height
            ), (1, draw_height))

            # Sombra
            if level.dark:
                shadow = pg.Surface(vline.get_size())
                shadow.set_alpha(max(min(235 - 255/distance, 255), 0))
                vline.blit(shadow, (0, 0))
            elif horizontal:
                shadow = pg.Surface(vline.get_size())
                shadow.set_alpha(100)
                vline.blit(shadow, (0, 0))

            # Blit da linha vertical na surface
            self.surface.blit(
                vline,
                (x, draw_start)
            )

    def spritecast(self, level, player):
        w, h = self.size
        self.middle = None

        for e in level.entities:
            e.distance = tools.basic_distance((e.x, e.y), (player.x, player.y))

        level.entities.sort(key=lambda e: e.distance, reverse=True)

        for entity in level.entities:
            if entity.type == "enemy":
                sprite = entity.next()
            else:
                sprite = entity.sprite

            tex_width, tex_height = sprite.get_size()
            sprite_x = entity.x - player.x
            sprite_y = entity.y - player.y

            inv_det = 1 / (player.px * player.dy - player.dx * player.py)

            transform_x = inv_det * (player.dy * sprite_x - player.dx * sprite_y)
            transform_y = inv_det * (-player.py * sprite_x + player.px * sprite_y)

            sprite_screen_x = int((w/2) * (1 + transform_x / transform_y))

            sprite_height = min(abs(int(h / transform_y)), 500) # Limite para não deixar o jogo lento

            draw_start_y = int(-sprite_height/2 + h/2)
            draw_end_y = int(sprite_height/2 + h/2)

            sprite_width = min(abs(int(h / transform_y)), 500) # Limite para não deixar o jogo lento
            draw_start_x = int(-sprite_width/2 + sprite_screen_x)
            draw_end_x = int(sprite_width/2 + sprite_screen_x)
            
            if draw_start_x < w/2 < draw_end_x and 0 < transform_y < self.zbuffer[int(w/2)] and entity.type == "enemy" and entity.health > 0:
                self.middle = entity

            if draw_start_x < w and draw_end_x > 0:
                for stripe in range(max(draw_start_x, 0), min(draw_end_x, w)):
                    if (transform_y > 0 and stripe > 0 and stripe < w and transform_y < self.zbuffer[stripe]):
                        tex_x = int(
                            (stripe - (-sprite_width / 2 + sprite_screen_x)) * tex_width / sprite_width
                        )
                        tex_y = ((draw_end_y - 1) - h/2 + sprite_height/2) * tex_height / sprite_height

                        vline = pg.transform.scale(tools.clip(
                            sprite,
                            tex_x,
                            0,
                            1,
                            tex_y
                        ), (1, sprite_height))

                        self.surface.blit(
                            vline,
                            (stripe, draw_start_y)
                        )