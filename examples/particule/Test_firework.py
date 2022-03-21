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

grp = []
fire = pe.FireWork(300,400)
grp.append(fire)

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN:
            color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            grp.append(pe.FireWork(event.pos[0], 400, timer=1+random.random()*1.5, amount=random.randint(10,30), missile_color=color))

    for firework in grp:
        firework.draw(win)

    grp = [item for item in grp if not item.has_finish]

    pg.display.update()

    clock.tick(30)

pg.quit()
