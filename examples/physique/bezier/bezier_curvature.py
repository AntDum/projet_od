import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.utils import *
from pygame import Vector2, Vector3

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

point_1 = Vector2(100, 300)
point_2 = Vector2(100, 100)
point_3 = Vector2(500, 300)
point_4 = Vector2(600, 300)



f = -1
run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False


    point_2 = Vector2(pg.mouse.get_pos())

    screen.draw_background()


    # screen.draw_circle(point_1, 6, color=(255,)*3)
    screen.draw_circle(point_2, 6, color=(255,)*3)
    # screen.draw_circle(point_3, 6, color=(255,)*3)
    # screen.draw_circle(point_4, 6, color=(255,)*3)

    for t in range(0,denominateur, nominateur):
        t /= denominateur
        b = bezier(t, point_1, point_2, point_4)
        der = bezier_quad_d(t, point_1, point_2, point_4)
        der2 = bezier_quad_2d(t, point_1, point_2, point_4)
        k = abs(curvature_parametrize(der, der2)) * 100
        # if k != 0:
        #     r = 1/k
        #     nder = der.normalize().rotate(90)
        #     nder.scale_to_length(r)
        #     no = nder + b
        #     screen.draw_circle(no, r, (200,150,150), width=1)
        color = tuple(clamp(c, 0, 255) for c in  bezier(k, Vector3(0,255,255),Vector3(0,255,0), Vector3(255,255,0)))
        screen.draw_circle(b, 1, color=color)

    pg.display.update()

pg.quit()