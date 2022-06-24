import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.utils import bezier, lerp, norm

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
point_3 = (720, 300)
f = -1
run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    # t += speed/fps
    # if t > 1:
    #     t = 1
    #     speed *= -1
    # if t < 0:
    #     t = 0
    #     speed *= -1

    # pos = bezier(t, 1, 0.3, 0, 0)

    point_2 = pg.mouse.get_pos()

    screen.draw_background()
    # screen.draw_circle(start, 6, color=(255,)*3)
    # screen.draw_circle(end, 6, color=(255,)*3)

    # screen.draw_circle((x + delta_x * pos,y + delta_y * pos), 9, color=(255,0,0))

    screen.draw_circle(point_1, 6, color=(255,)*3)
    screen.draw_circle(point_2, 6, color=(255,)*3)
    screen.draw_circle(point_3, 6, color=(255,)*3)
    pf = f
    f = norm(point_2[0], point_1[0], point_3[0])
    if pf != f:
        print(round(f,2))
    for t in range(0,denominateur, nominateur):
        t /= denominateur
        x1 = lerp(t, 0, f)
        x2 = lerp(t, f, 1)
        x3 = lerp(t, x1, x2)
        x3 *= point_3[0]

        y1 = lerp(t, point_1[1], point_2[1])
        y2 = lerp(t, point_2[1], point_3[1])
        y3 = lerp(t, y1, y2)

        screen.draw_circle((x3, y3), 1, color=(255,)*3)
        # screen.draw_circle((x3, 300), 1, color=(255,)*3)


    pg.display.update()

pg.quit()