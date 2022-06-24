import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.utils import norm, lerp

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)
clock = pg.time.Clock()

screen.make_background((20,120,120))
screen.draw_background()

run = True
while run:
    clock.tick(30)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    rel = pg.Vector2(pg.mouse.get_rel())
    rel *= -1
    speed, angle = rel.as_polar()
    pos = pg.Vector2(pg.mouse.get_pos())

    screen.draw_background()

    vec = pg.Vector2(0,1)
    if speed != 0:
        
        speed = clamp(abs(speed), 0, 50)/50
        rel_n = rel.normalize()
        rel_n *= speed
        vec += rel_n

        screen.draw_line(pos, pos+(rel * 5), (255,255,255), 5)
    vec.scale_to_length(50)
    screen.draw_line(pos, pos+vec, (255,0,0), 10)

    # screen.display_update()
    pg.display.update()

pg.quit()