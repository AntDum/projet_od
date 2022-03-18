import pygame as pg
from projet_od.gui import *

pg.init()
pg.display.init()
h = 480
w = 720
screen = pg.display.set_mode((w,h))

font = pg.font.SysFont("Comic Sans MS", 26, False, False)

gc = GUIComponent((10, 10), (150, 150))

but = Button((170,10), (150, 50), font, "Button")

slider = Slider((170, 100), (270, 100), (25,50), (0,100))

it = InputText((350, 10), (180,50), font, text="Input")

# gc.on_click = lambda : print("Hello")
# it.on_change = lambda : print(it.get_text())

run = True
while run:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False
    
    slider.update()
    but.update()
    gc.update()
    it.update(events)

    screen.fill((20,20,20))
    
    slider.draw(screen)
    but.draw(screen)
    gc.draw(screen)
    it.draw(screen)

    pg.display.update()

pg.quit()