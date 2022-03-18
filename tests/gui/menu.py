import pygame as pg
from projet_od.gui import *

pg.init()
pg.display.init()
h = 480
w = 720
screen = pg.display.set_mode((w,h))

font = pg.font.SysFont("Comic Sans MS", 26, False, False)

theme = WHITE
name = "MENU"
b1_name = "Play"
b2_name = "Quit"

p_menu = Panel((0,0), (w,h), theme=theme)

l_title = Label((0,50), name, font, theme=theme)
l_title.center_x(p_menu)

b_play = Button((0,150), (150, 50), font, b1_name, theme=theme)
b_play.label.center(b_play)
b_play.center_x(p_menu)

b_quit = Button((0,250), (150, 50), font, b2_name, theme=theme)
b_quit.label.center(b_quit)
b_quit.center_x(p_menu)

p_menu.add(l_title, b_play, b_quit)

run = True
while run:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    p_menu.update()
    
    screen.fill((125,125,125))

    p_menu.draw(screen)

    # pg.draw.line(screen, (255,0,0), (w/2, 0), (w/2, h))
    # pg.draw.line(screen, (255,0,0), (0, h/2), (w, h/2))

    pg.display.update()

pg.quit()