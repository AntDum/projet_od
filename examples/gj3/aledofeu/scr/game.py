import pygame as pg
from scr.map import map_from_file, stop_music
import os

def main(screen):
    clock = pg.time.Clock() 
    map = map_from_file(os.path.join("niveaux", "lvl4.csv"), tile_size=32)

    screen.set_size_tile(map.width_tile, map.height_tile)

    run = True
    while run:
        dt = clock.tick(30) / 1000 # connait le delta time entre les iterations
        fps = round(1/dt) # connait les fps

        quit = False
        for event in pg.event.get(): # Recupere les events
            if event.type == pg.QUIT: # Ferme le jeu quand on quitte
                run = False
                quit = True
        if quit:
            pg.event.post(pg.event.Event(pg.QUIT, {}))
            stop_music()
        
        map.update(screen, dt)

        screen.draw_background()
        map.draw(screen, dt)
        if map.countdown < 0:
            run = False
        
        screen.display_update()