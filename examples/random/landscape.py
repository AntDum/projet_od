from turtle import st
import pygame as pg
from project_od.utils import Perlin
from project_od.screen import DrawableScreen

import time

class Map:
    def __init__(self, w, h, conv) -> None:
        start_time = time.process_time()
        perlin = Perlin()
        end_time = time.process_time()
        
        self.conv = sorted(conv, key=lambda x: x[0])
        self.map = [[self.eval(perlin(x,y)) for x in range(w)] for y in range(h)]
        second_time = time.process_time()
        self.perlin = - start_time + end_time
        self.mapping =  - end_time + second_time
        self.tot = - start_time + second_time

        print(f"Init perlin : {self.perlin}\nCreating map : {self.mapping}\nMaking all : {self.tot}\nFor ({w},{h})")
    
    def eval(self, r_val):
        for val, ele in self.conv:
            if val > r_val:
                return ele

pg.init()

w, h = 720, 480

screen = DrawableScreen(w,h)

size = 30
conv = [(.3, (0,0,50)), (.7, (80,80,80)), (1, (125,125,125))]

def draw_map(k):
    for y, line in enumerate(k.map):
        for x, color in enumerate(line):
            screen.draw_rect((x*size,y*size,size,size), color)

map = Map(w//size, h//size, conv)
# map2 = Map(w, h, conv)

draw_map(map)

screen.display_update()

# toggle = True

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # if event.type == pg.KEYDOWN:
            # toggle = not toggle
            # print(toggle)
            # if toggle:
            # draw_map(map)
            # else:
            #     draw_map(map2)

            # pg.display.update()


pg.quit()