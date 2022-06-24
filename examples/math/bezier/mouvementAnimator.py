import pygame as pg
from project_od.screen import SmartScreen
from project_od.physics.animator import AnimateValue


pg.init()

h = 480
w = 720
fps = 30
screen = SmartScreen(w,h)
clock = pg.time.Clock()
screen.make_background((125,)*3)
image = pg.Surface((50,50))

start = 200,100
dest = 400,300


pos2 = dest

anim1 = AnimateValue((0,255,0), (245,25,16), keys=[0,0.2,1], fps=fps, time=2)
anim2 = AnimateValue(dest, start, keys=[0,-1,2,1], fps=fps, time=2)

run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    color = anim1.next()
    pos2 = anim2.next()

    if anim2.has_finish():
        anim2.reset()
    if anim1.has_finish():
        anim1.reset()

    screen.draw_background()
    image.fill(color)
    screen.blit(image, pos2)

    # screen.display_update()
    pg.display.update()

pg.quit()