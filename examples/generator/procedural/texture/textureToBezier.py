import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen
from project_od.utils import bezier, bezier_cub_2d, bezier_cub_d, lerp, norm
from project_od.physics.transform import rotate_pivot
from pygame import Vector2

from os.path import join

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)
clock = pg.time.Clock()

road_size = 40

road = pg.transform.rotate(pg.transform.scale(pg.image.load(join("examples","generator","procedural","texture","road.png"), "road"), (road_size, road_size)), 90)

screen.make_background((10,)*3)
screen.draw_background()
fps = 30
t=0
speed = 1

nominateur = 2
denominateur = 100

start = (50,200)
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
        if l == 1 or l == 0:
            return l
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
        t1 = t / denominateur
        t2 = (t + nominateur) / denominateur 
        
        l1 = lut.get(t1)
        l2 = lut.get(t2)

        # l1 = t1
        # l2 = t2

        b = bezier(l1, point_1, point_2, point_3, point_4)

        b2 = bezier(l2, point_1, point_2, point_3, point_4)

        diff = b2 - b
        length, angle = diff.as_polar()
        angle *= -1
        pivot_point = rotate_pivot(b, (road_size, road_size), (road_size/2, 0), angle)
        rotate_image = pg.transform.rotate(pg.transform.scale(road, (length * 1.2, road_size)), angle)

        screen.blit(rotate_image, pivot_point)


    screen.blit(road, (0,0))

    pg.display.update()

pg.quit()