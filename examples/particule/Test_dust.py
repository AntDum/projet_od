import pygame as pg
import projet_od.particule.particleEffect as pe
from projet_od.screen import BaseScreen
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
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEMOTION:
            dusting.pos.x = event.pos[0]
            dusting.pos.y = event.pos[1]

    rects = dusting.draw(win)
    pg.display.update(rects)

    clock.tick(30)

pg.quit()
