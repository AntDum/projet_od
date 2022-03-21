import pygame as pg
from project_od.gui import *
from project_od.screen import SmartScreen

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)

font = pg.font.SysFont("Comic Sans MS", 26, False, False)

gc = GUIComponent((10, 10), (150, 150))

but = Button((170,10), (150, 50), font, "Button")

slider = Slider((170, 100), (270, 100), (25,50), (0,100), default=100)

it = InputText((350, 10), (180,50), font, text="Input")

# gc.on_click = lambda : print("Hello")
# it.on_change = lambda : print(it.get_text())
screen.make_background((120,0,0))
screen.draw_background()

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

    
    slider.draw(screen)
    screen.draw(but)
    gc.draw(screen)
    it.draw(screen)

    pg.display.update()

pg.quit()