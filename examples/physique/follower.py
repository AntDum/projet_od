import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.physics.animator import Follow

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)
clock = pg.time.Clock()

screen.make_background((10,)*3)
screen.draw_background()
fps = 30

follow = Follow(rate=0.3, min_dist=10)

start = (300,300)

x = start[0]
y = start[1]

follow.set_current(start)

run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False


    mouse = pg.mouse.get_pos()
    follow.set_objectif(mouse)

    x,y = follow.next()

    screen.draw_background()

    screen.draw_circle((x,y), 6, color=(255,)*3)

    pg.display.update()

pg.quit()