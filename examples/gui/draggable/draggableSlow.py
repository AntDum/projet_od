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

gc = GUIComponent((10, 10), (100, 100), image=image, draggable=True, drag_rate=0.1, drag_rotate=True, drag_point=(50,-10))


screen.make_background((20,120,120))
screen.draw_background()

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

    # pos = gc.rect.topleft
    gc.update()
    # movement : pg.Vector2 = (gc.rect.topleft - pg.Vector2(pos))
    # speed, angle = movement.as_polar()
    
    # vec = pg.Vector2(0,-1)

    # if speed != 0:    
    #     speed = clamp(abs(speed), 0, 50)/50
    #     rel_n = movement.normalize()
    #     rel_n *= speed
    #     vec += rel_n
    
    # _, angle = vec.as_polar()
    # angle += 90
    # angle *= -1
    # print(angle)
    # rotate_image = pg.transform.rotate(image, angle)
    # drag_point = (gc.rect.topleft + pg.Vector2(gc._drag_offset))
    # origin = rotate_pivot(drag_point, image.get_size(), gc._drag_offset, angle)

    # gc.image = rotate_image
    screen.draw_background()
    # screen.blit(rotate_image, origin)
    # screen.draw_circle(drag_point, 5, (255,)*3)
    gc.draw(screen)

    pg.display.update()

pg.quit()