import pygame as pg
from projet_od.gui import Panel, Button, Label, THEME_WHITE
from projet_od.screen import BaseScreen

pg.init()

w, h = 720, 480

font = pg.font.SysFont("Comic Sans MS", 20, False, False)
large_font = pg.font.SysFont("Comic Sans MS", 30, True, False)

screen = BaseScreen(w, h)

def exit():
    global run
    run = False

class Win:
    def __init__(self) -> None:
        self.curr = None
        self.theme = THEME_WHITE
        self.home()
    
    def Panel(self):
        return Panel((0,0), (w,h), theme=self.theme)

    def Big_Label(self, pos, text, **kwargs):
        return Label(pos, text, large_font, theme=self.theme, **kwargs)
    
    def Label(self, pos, text, **kwargs):
        return Label(pos, text, font, theme=self.theme, **kwargs)
    
    def Button(self, pos, text, **kwargs):
        b = Button(pos, (150, 50), font, text, theme=self.theme, **kwargs)
        b.center_text()
        return b
    
    def home(self) -> Panel:
        bc = self.Panel()

        lb = self.Big_Label((0,50), "Wonderful home")
        lb.center_x(bc)

        bt1 = self.Button((0,150), "Go")
        bt1.center_x(bc)

        bt2 = self.Button((0,250), "Option")
        bt2.center_x(bc)

        bt3 = self.Button((0,350), "Quit")
        bt3.center_x(bc)

        bt1.on_click = self.go
        bt2.on_click = self.option
        bt3.on_click = exit

        bc.add(lb, bt1, bt2, bt3)
        self.curr = bc
        return bc
        
    def option(self) -> Panel:
        bc = self.Panel()

        lb = self.Big_Label((0, 50), "Options", text_color=(50,30,20))
        lb.center_x(bc)

        bt = self.Button((w/2, h/2), "BACK", on_click=self.home)
        bt.center(bc)
        bc.add(bt, lb)
        self.curr = bc
        return bc

    def go(self) -> Panel:
        bc = self.Panel()

        lb = self.Button((w/2, h/2), "BACK", on_click=self.home)
        lb.center(bc)
        bc.add(lb)

        self.curr = bc
        return bc
    
    def update(self):
        self.curr.update()
    
    def draw(self, screen):
        screen.fill((125,125,125))
        self.curr.draw(screen)

win = Win()

run = True
while run:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

    win.update()

    win.draw(screen)


    pg.display.update()

pg.quit()