import pygame as pg
from project_od.gui import *
from project_od.physics.transform import rotate_pivot
from project_od.screen import SmartScreen

pg.init()

h = 480
w = 720
screen = SmartScreen(w,h)
clock = pg.time.Clock()
image = pg.Surface((100, 100))
pg.draw.line(image, (255,0,0), (0,0), (100,100))
pg.draw.line(image, (255,0,0), (100,0), (50,50))
screen.make_background((20,120,120))
screen.draw_background()
angle = 0
"""
        use 
        rotated_image = pygame.transform.rotate(image, angle)

        and 
        blit(rotated_image, origin)
"""

run = True
while run:
    clock.tick(30)
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    angle += 1

    rotate_image = pg.transform.rotate(image, angle)


    origin_topleft = rotate_pivot((400, 200), (100,100), (0,0), angle)

    origin_center = rotate_pivot((200,400), (100, 100), (50,50), angle)
    
    screen.draw_background()
    screen.blit(rotate_image, (100,100))
    screen.blit(rotate_image, origin_topleft)
    screen.blit(rotate_image, origin_center)
    screen.draw_circle((400,200), 3, (255,255,255))
    screen.draw_circle((200,400), 3, (255,255,255))

    # screen.display_update()
    pg.display.update()

pg.quit()