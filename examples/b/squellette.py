import pygame as pg
from project_od.screen import SmartScreen

pg.init()
w,h = 720,480
FPS = 60
screen = SmartScreen(w, h)
clock = pg.time.Clock()

run = True
while run:
    dt = clock.tick(FPS) / 1000
    fps = round(1/dt)
    for event in pg.event.get():
        if event.type == pg.QUIT:
           run = False

    screen.display_update()

pg.quit()