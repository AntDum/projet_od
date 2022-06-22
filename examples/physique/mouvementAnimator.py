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

start = 0,0
dest = 600,400

# pos1 = start
pos2 = dest

# anim1 = AnimateValue(start, dest, mode="linear", fps=fps, time=5)
anim2 = AnimateValue(dest, start, mode="linear", fps=fps, time=2)

run = True
while run:
    clock.tick(fps)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    # pos1 = anim1.next(pos1)
    pos2 = anim2.next(pos2)

    if anim2.has_finish():
        anim2.reset()

    screen.draw_background()
    # screen.blit(image, pos1)
    screen.blit(image, pos2)

    # screen.display_update()
    pg.display.update()

pg.quit()