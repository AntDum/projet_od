import pygame as pg
from scr.menu import Menu
from scr.screen import Screen
from scr.game import main

pg.init()

w, h = 720, 480
FPS = 60
screen = Screen(w, h, 32, "Aledofeu Remastered")
screen.make_background((135,206,235))

menu = Menu(w,h)

clock = pg.time.Clock()

menu.home()

menu.play_btn.on_click = lambda : main(screen)

menu.start(screen)


pg.quit()