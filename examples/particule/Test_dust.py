import pygame as pg
import project_od.particule.particleEffect as pe
from project_od.screen import BaseScreen
import random

pg.init()

win = BaseScreen(600, 400)

pg.display.set_caption("ParticleSystems")

clock = pg.time.Clock()

background = pg.Surface([600, 400])
background.fill((200,200,200))

win.background = background

win.blit(background, (0,0))

pg.display.flip()

dusting = pe.Dust(0, 0, gravity=False)

run = True
while run:
    dt = clock.tick(30) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEMOTION:
            dusting.pos.x = event.pos[0]
            dusting.pos.y = event.pos[1]
            print(event.pos)

    dusting.update(dt)

    rects = dusting.draw(win)

    pg.display.update(rects)


pg.quit()
