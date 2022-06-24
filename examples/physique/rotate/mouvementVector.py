import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen

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
    speed, angle = rel.as_polar()
    pos = pg.Vector2(pg.mouse.get_pos())

    screen.draw_background()

    vec = pg.Vector2(1,0)
    vec.scale_to_length(speed * 4)
    # vec.scale_to_length(50)
    vec.rotate_ip(angle)
    vec *= -1
    screen.draw_line(pos, pos+vec, (255,0,0), 5)

    # screen.display_update()
    pg.display.update()

pg.quit()