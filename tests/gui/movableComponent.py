import pygame as pg
from projet_od.gui.component import *

pg.init()
pg.display.init()
h = 480
w = 720
screen = pg.display.set_mode((w,h))

font = pg.font.SysFont("Comic Sans MS", 26, False, False)

gc = GUIComponent((10, 10), (150, 150))

lb = Label((20,300), "Mais non", font)

but = Button((170,10), (150, 50), font, "Button", theme=WHITE)

slider = Slider((180, 100), (300, 100), (25,50), (0,100), theme=WHITE)

pn = Panel((0,0), (480,720))

pn.add(gc, but, slider, lb)

gc.on_click = lambda : pn.move((50,0))
but.on_click = lambda : pn.move_to((30,30))
# it.on_change = lambda : print(it.get_text())

run = True
while run:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            print(but.label.rect)

    pn.update()
    
    screen.fill((125,125,125))
    pn.draw(screen)

    pg.display.update()

pg.quit()