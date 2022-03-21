import pygame as pg
import project_od.particule.particleEffect as pe
from project_od.screen import SmartScreen
import random

pg.init()

FPS = 30

win = SmartScreen(600, 400)

pg.display.set_caption("ParticleSystems")

clock = pg.time.Clock()

win.make_background((200,200,200))

win.draw_background()

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


    # win.draw_background()
    for firework in grp:
        firework.draw(win)

    grp = [item for item in grp if not item.has_finish]

    dusting.draw(win)

    win.display_update()

pg.quit()
