import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)
screen.make_background((125,125,125))

font = pg.font.SysFont("Comic Sans MS", 26, False, False)

gc = GUIComponent((10, 10), (150, 150))

lb = Label((20,300), "Mais non", font)

but = Button((170,10), (150, 50), font, "Button")

slider = Slider((180, 100), (300, 100), (25,50), (0,100))

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

    pn.update()
    
    screen.draw_background()
    screen.draw(pn)

    screen.display_update()

pg.quit()