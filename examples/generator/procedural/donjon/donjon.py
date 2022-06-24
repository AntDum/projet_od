import pygame as pg
from project_od.screen import SmartScreen, DummyTarget
from project_od.utils import clamp
from project_od.gui import Label, Panel
from project_od.map.donjon import Donjon, DonjonRoom, RoomGenerator
from random import random


class DrawRoom(DonjonRoom):
    def __init__(self, x, y, color, shape) -> None:
        super().__init__(x, y, shape)
        self.image = pg.Surface((size,size))
        self.image.fill((200,200,200))
        self.realColor = color
        self.color = (20,20,20)
        self.render()
    
    def render(self):
        pg.draw.rect(self.image, self.color, ((size/5, size/5),(size*6/10, size*6/10)))
        halfi = size/2 - size/10
        ort = (0,halfi),(halfi, 0), (size-size/5, halfi), (halfi, size-size/5)
        for i, op in enumerate(self.shape):
            if op:
                pg.draw.rect(self.image, self.color, (ort[i],(size/5, size/5)))
    
    def on_load(self):
        self.color = self.realColor
        self.render()

    def draw(self, screen):
        screen.blit_cam(self.image, pg.Rect(self.x*size, self.y*size,0,0))
    
    def __str__(self) -> str:
        return f"{self.x,self.y} - {self.shape}"
    
    def __repr__(self) -> str:
        return str(self)

class ColorRoomGenerator(RoomGenerator):
    def __init__(self, factor) -> None:
        super().__init__()
        self.factor = factor

    @staticmethod
    def randomColor():
        return tuple(int(clamp(random()*255, 30, 230)) for _ in range(3))

    def next(self, x, y, rules, dir=-1 , **kwargs):
        #If has full choice (no neighbors) (new or tp)
        if all(i==None for i in rules):
            return DrawRoom(x,y, (255,)*3, shape=list((True,)*4))
        
        # Make the choice for empty space
        op = [random() < self.factor if rule == None else rule for rule in rules]

        return DrawRoom(x,y,self.randomColor(), shape=op)
        
class DrawDonjon(Donjon):
    def __init__(self, generator: RoomGenerator, *args) -> None:
        super().__init__(generator, *args)
    
    def draw(self, screen):
        for room in self.rooms.values():
            room.draw(screen)


# =============== Init ===================
pg.init()
w,h = 720,480

screen = SmartScreen(w,h)
size = 30
factor = .4
minimum_rooms = 20
maximum_rooms = 50

screen.make_background((25,25,25))

generator = ColorRoomGenerator(factor)
target = DummyTarget(size/2, size/2)
donjon = DrawDonjon(generator, minimum_rooms, maximum_rooms)
x, y = 0,0

#  =============== GUI =================
font = pg.font.SysFont("Comic Sans Ms", 26)
small_font = pg.font.SysFont("Arial", 15)

pn = Panel((0,0), (w,h))
lb_coor = Label((10, 10), f"{x}, {y}", font, text_color=(255,255,255))

pn_info = Panel((0,0), (0,0))
lb_pendant = Label((0, 0), f"To explore : {donjon.get_num_to_create()}", small_font, text_color=(200,200,20))
lb_border = Label((0, 15), f"Border : {donjon.get_num_border()}", small_font, text_color=(200,200,20))
lb_tot = Label((0, 30), f"Tot : {donjon.get_num_created()}", small_font, text_color=(200,200,20))
lb_loaded = Label((0, 45), f"Loaded : {donjon.get_num_loaded()}", small_font, text_color=(200,200,20))
lb_unloaded = Label((0, 60), f"Unloaded : {donjon.get_num_unloaded()}", small_font, text_color=(200,200,20))
lb_size = Label((0, 80), f"Estimate size : {donjon.get_num_estimate_size()}", small_font, text_color=(200,200,20))

pn_info.add(lb_border, lb_tot, lb_loaded, lb_unloaded, lb_pendant, lb_size)

pn_info.move_to((w-100, 10))

pn.add(lb_coor, pn_info)


# =============== Main Loop ===============
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: # Reset the donjon
                donjon.__init__(generator)
                target.move_to(size/2,size/2)
                x, y = 0, 0

            r = donjon.get(x,y) # Get the current room

            if event.key == pg.K_LEFT:
                if r.shape[0]:
                    x -= 1
            if event.key == pg.K_UP:
                if r.shape[1]:
                    y -= 1
            if event.key == pg.K_RIGHT:
                if r.shape[2]:
                    x += 1
            if event.key == pg.K_DOWN:
                if r.shape[3]:
                    y += 1

            donjon.get(x,y) # Load the next room

            target.move_to(x*size + size/2,y*size + size/2) # Move the camera

            # == Update gui ==
            lb_coor.set_text(f"{x}, {y}")
            lb_border.set_text(f"Border : {donjon.get_num_border()}")
            lb_tot.set_text(f"Tot : {donjon.get_num_created()}")
            lb_loaded.set_text(f"Loaded : {donjon.get_num_loaded()}")
            lb_unloaded.set_text(f"Unloaded : {donjon.get_num_unloaded()}")
            lb_pendant.set_text(f"To explore : {donjon.get_num_to_create()}")
            lb_size.set_text(f"Estimate size : {donjon.get_num_estimate_size()}")

    
    # Move the camera
    screen.update_camera(target)

    # == Draw ==
    # Draw background
    screen.draw_background()
    # Draw the donjon
    donjon.draw(screen)
    # Draw the cursor
    pg.draw.rect(screen.surface, (255,0,0), screen.from_cam(((x*size + size/3, y*size + size/3),(size/3,size/3))))
    # Draw the gui
    pn.draw(screen)

    # screen.draw_cross_center((255,0,0))

    # Update the screen
    screen.display_update()

pg.quit()