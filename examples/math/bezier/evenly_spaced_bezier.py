import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.utils import bezier, bezier_cub_2d, bezier_cub_d, lerp, norm
from pygame import Vector2

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

point_1 = Vector2(start)
point_2 = Vector2(100, 100)
point_3 = Vector2(500, 300)
point_4 = Vector2(end)

class LUT:
    def __init__(self, granularity, *points) -> None:
        self.table = []
        tot = 0
        for i in range(granularity):
            t1 = i/granularity
            t2 = (i+1)/granularity
            point = bezier(t1, *points)
            second_point = bezier(t2, *points)
            segment = second_point - point
            self.table.append((t1, tot))
            tot += segment.length()
        self.table.append((t2, tot))
        self.length = tot
    
    def get(self, l):
        length = l * self.length
        prev_v = self.table[0][1]
        prev_x = self.table[0][0]
        for x, value in self.table:
            if value > length:
                break
            prev_v = value
            prev_x = x
        # print(l, length, self.length, x)
        return lerp(norm(length, prev_v, value), prev_x, x)


def courbe_length(*points, granularity=10):
    return sum((bezier((i+1)/granularity, *points) - bezier(i/granularity, *points)).length() for i in range(granularity))


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


    screen.draw_circle(point_1, 6, color=(255,)*3)
    screen.draw_circle(point_2, 6, color=(255,)*3)
    screen.draw_circle(point_3, 6, color=(255,)*3)
    screen.draw_circle(point_4, 6, color=(255,)*3)

    lut = LUT(10, point_1, point_2, point_3, point_4)

    for t in range(0,denominateur, nominateur):
        t /= denominateur

        t_p = lut.get(t)
        b = bezier(t_p, point_1, point_2, point_3, point_4)
        
        screen.draw_circle(b, 1, color=(255,)*3)

    pg.display.update()

    

pg.quit()