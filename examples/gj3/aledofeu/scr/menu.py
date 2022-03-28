from project_od.gui import Panel, Button, Label, THEME_WHITE
import pygame as pg

class Menu:
    def __init__(self, w, h) -> None:
        self.curr = None
        self.theme = THEME_WHITE
        self.w = w
        self.h = h
        self.large_font = pg.font.SysFont('arial', 24)
        self.font = pg.font.SysFont('arial', 16)
        self.go = lambda x : x
    
    def Panel(self):
        return Panel((0,0), (self.w,self.h), theme=self.theme)

    def Big_Label(self, pos, text, **kwargs):
        return Label(pos, text, self.large_font, theme=self.theme, **kwargs)
    
    def Label(self, pos, text, **kwargs):
        return Label(pos, text, self.font, theme=self.theme, **kwargs)
    
    def Button(self, pos, text, **kwargs):
        b = Button(pos, (150, 50), self.font, text, theme=self.theme, **kwargs)
        b.center_text()
        return b
    
    def home(self) -> Panel:
        bc = self.Panel()

        lb = self.Big_Label((0,50), "Aledofeu Remaster")
        lb.center_x(bc)
        
        bt1 = self.Button((0,150), "Go")
        bt1.center_x(bc)

        bt3 = self.Button((0,350), "Quit")
        bt3.center_x(bc)

        bt1.on_click = self.go
        bt3.on_click = exit

        bc.add(lb, bt1, bt3)
        self.curr = bc
        self.play_btn = bt1
        return bc
    
    def start(self, screen):
        self.run = True

        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            
            self.update()
        
            self.draw(screen)

            screen.display_update()

    
    def update(self):
        self.curr.update()
    
    def draw(self, screen):
        screen.fill((125,125,125))
        self.curr.draw(screen)
    
    def stop(self):
        self.run = False