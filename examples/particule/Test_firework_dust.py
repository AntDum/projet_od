import pygame as pg
import project_od.particule.particleEffect as pe
from project_od.screen import BaseScreen
import random

pg.init()

FPS = 30

win = BaseScreen(600, 400)

pg.display.set_caption("ParticleSystems")

clock = pg.time.Clock()

background = pg.Surface([600, 400])
background.fill((200, 200, 200))

win.background = background

win.blit(background, (0, 0))

pg.display.flip()

dusting = pe.Dust(0, 0, gravity=True, FPS=FPS)

grp = []
fire = pe.FireWork(300, 400, FPS=FPS)
grp.append(fire)

run = True
while run:
    dt = clock.tick(FPS) / 1000
    pg.display.set_caption(f"{round(1/dt,2)}")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEMOTION:
            dusting.pos.x = event.pos[0]
            dusting.pos.y = event.pos[1]
        elif event.type == pg.MOUSEBUTTONDOWN:
            color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            grp.append(pe.FireWork(
                event.pos[0], 400, timer=1+random.random()*1.5, amount=random.randint(10, 30), missile_color=color))

    to_update = []

    for firework in grp:
        to_update.extend(firework.draw(win))

    grp = [item for item in grp if not item.has_finish]

    to_update.extend(dusting.draw(win))
    pg.display.update(to_update)

pg.quit()
