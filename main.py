import pygame as pg
import sys, time, math

from player import Player
from level import Level

from pygame.locals import *

FRAMERATE = 60
WINDOW_SIZE = (480, 320)
DISPLAY_SIZE = (480, 320)

def main():
    screen, display = setup_pg()
    keys = {
        'up': False,
        'down': False,
        'left': False,
        'right': False,
    }
    clock = pg.time.Clock()
    last = time.time()

    player = Player((22,12), (-1,0), (0, 0.66))
    level = Level((24,24))
    colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,0,255)]

    while True:
        dt, last = update_time(last)

        display.fill((50,50,50))

        for i in range(DISPLAY_SIZE[0]):
            camera_x = 2 * i / DISPLAY_SIZE[0] - 1
            ray_dx = player.dx + player.px * camera_x
            ray_dy = player.dy + player.py * camera_x
            map_x = int(player.x)
            map_y = int(player.y)
            delta_x = 0 if ray_dy == 0 else (1 if ray_dx == 0 else abs(1 / ray_dx))
            delta_y = 0 if ray_dx == 0 else (1 if ray_dy == 0 else abs(1 / ray_dy))

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

            hit = 0
            while hit == 0:
                if side_x < side_y:
                    side_x += delta_x
                    map_x += step_x
                    side = 0
                else:
                    side_y += delta_y
                    map_y += step_y
                    side = 1
                if level.map[int(map_x)][int(map_y)] > 0:
                    hit = 1
            
            if side == 0:
                distance = (map_x - player.x + (1 - step_x) / 2) / ray_dx
            else:
                distance = (map_y - player.y + (1 - step_y) / 2) / ray_dy

            height = int(DISPLAY_SIZE[1] / distance) if distance != 0 else DISPLAY_SIZE[1]
            draw_start = max((-height + DISPLAY_SIZE[1])/2, 0)
            draw_end = min((height + DISPLAY_SIZE[1])/2, DISPLAY_SIZE[1] - 1)

            color = colors[level.map[int(map_x)][int(map_y)]]

            if side == 1:
                color = [c / 2 for c in color]

            pg.draw.line(display, color, (i, draw_start), (i, draw_end))

        speed = player.speed * dt
        rot = player.rot * dt
        if keys['up']:
            if level.map[int(player.x + player.dx * speed)][int(player.y)] == 0:
                player.x += player.dx * speed
            if level.map[int(player.x)][int(player.y + player.dy * speed)] == 0:
                player.y += player.dy * speed
        if keys['down']:
            if level.map[int(player.x - player.dx * speed)][int(player.y)] == 0:
                player.x -= player.dx * speed
            if level.map[int(player.x)][int(player.y - player.dy * speed)] == 0:
                player.y -= player.dy * speed
        if keys['right']:
            old_dx = player.dx
            player.dx = player.dx * math.cos(-rot) - player.dy * math.sin(-rot)
            player.dy = old_dx * math.sin(-rot) + player.dy * math.cos(-rot)
            old_px = player.px
            player.px = player.px * math.cos(-rot) - player.py * math.sin(-rot)
            player.py = old_px * math.sin(-rot) + player.py * math.cos(-rot)
        if keys['left']:
            old_dx = player.dx
            player.dx = player.dx * math.cos(rot) - player.dy * math.sin(rot)
            player.dy = old_dx * math.sin(rot) + player.dy * math.cos(rot)
            old_px = player.px
            player.px = player.px * math.cos(rot) - player.py * math.sin(rot)
            player.py = old_px * math.sin(rot) + player.py * math.cos(rot)

        for e in pg.event.get():
            if e.type == QUIT:
                pg.quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if e.key == K_w: keys['up'] = True
                if e.key == K_s: keys['down'] = True
                if e.key == K_a: keys['left'] = True
                if e.key == K_d: keys['right'] = True
            if e.type == KEYUP:
                if e.key == K_w: keys['up'] = False
                if e.key == K_s: keys['down'] = False
                if e.key == K_a: keys['left'] = False
                if e.key == K_d: keys['right'] = False

        screen.blit(display, (0, 0))

        pg.display.update()
        clock.tick(FRAMERATE)

def update_time(last):
    dt = (time.time() - last)
    return dt, time.time()

def setup_pg():
    pg.init()
    pg.display.set_caption("PyRaycaster")

    screen = pg.display.set_mode(WINDOW_SIZE, 0, 32)
    display = pg.Surface(DISPLAY_SIZE)

    return screen, display

if __name__ == "__main__":
    main()
