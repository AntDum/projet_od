import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)

gc = GUIComponent((10, 10), (150, 150), draggable=True)

screen.make_background((120,0,0))
screen.draw_background()

run = True
while run:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    gc.update()

    screen.draw_background()
    gc.draw(screen)

    # screen.display_update()
    pg.display.update()

pg.quit()