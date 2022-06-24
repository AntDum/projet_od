import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.utils import bezier, bezier_cub_d, bezier_cub_2d

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)
clock = pg.time.Clock()

screen.make_background((10,)*3)
screen.draw_background()
fps = 30
t=0
speed = 1

nominateur = 2
denominateur = 100

start = (0,200)
end = (720,200)



x = start[0]
y = start[1]

delta_x = end[0] - start[0]
delta_y = end[1] - start[1]

point_1 = (0, 300)
point_2 = (100, 100)
point_3 = (500, 300)
point_4 = (600, 400)
f = -1
run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False


    point_2 = pg.mouse.get_pos()

    screen.draw_background()


    screen.draw_circle(point_1, 6, color=(255,)*3)
    screen.draw_circle(point_2, 6, color=(255,)*3)
    screen.draw_circle(point_3, 6, color=(255,)*3)
    screen.draw_circle(point_4, 6, color=(255,)*3)

    for t in range(0,denominateur, nominateur):
        t /= denominateur
        x = bezier_cub_d(t, point_1[0]/100, point_2[0]/100, point_3[0]/100, point_4[0]/100)

        y = bezier_cub_d(t, point_1[1]/100, point_2[1]/100, point_3[1]/100, point_4[1]/100)

        screen.draw_circle((x*3+ 300, y*3 + 200), 1, color=(255,0,0))
    
    for t in range(0,denominateur, nominateur):
        t /= denominateur
        x = bezier_cub_2d(t, point_1[0]/100, point_2[0]/100, point_3[0]/100, point_4[0]/100)

        y = bezier_cub_2d(t, point_1[1]/100, point_2[1]/100, point_3[1]/100, point_4[1]/100)

        screen.draw_circle((x*2+ 500, y*2 + 200), 1, color=(0,255,0))

    for t in range(0,denominateur, nominateur):
        t /= denominateur
        x = bezier(t, point_1[0], point_2[0], point_3[0], point_4[0])

        y = bezier(t, point_1[1], point_2[1], point_3[1], point_4[1])

        screen.draw_circle((x, y), 1, color=(255,)*3)

    pg.display.update()

pg.quit()