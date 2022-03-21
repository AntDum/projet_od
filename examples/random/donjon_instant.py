import pygame as pg
from project_od.screen import SmartScreen, DummyTarget
from project_od.utils import clamp
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
    
    def generate(self, x):
        while x > 0:
            for next in list(self.to_create):
                self.load_room(*next)
                x-=1
                if x <= 0:
                    break
            if len(self.to_create) == 0:
                break
        
        print(self.get_size())


# =============== Init ===================
pg.init()
w,h = 720,480

screen = SmartScreen(w,h)
size = 10
factor = .6
minimum_rooms = 20
maximum_rooms = 10000
step = 500

FPS = 60
clock = pg.time.Clock()

screen.make_background((25,25,25))

generator = ColorRoomGenerator(factor)
target = DummyTarget(size/2, size/2, 2)
donjon = DrawDonjon(generator, minimum_rooms, maximum_rooms)


# =============== Main Loop ===============
run = True
while run:
    dt = clock.tick(FPS) / 1000
    pg.display.set_caption(f"FPS : {round(1/dt)}")
    for event in pg.event.get():
        if event.type == pg.QUIT:
           run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE: # Reset the donjon
                donjon.__init__(generator)

            if event.key == pg.K_RETURN:
                donjon.generate(step)

    
    # Move the camera
    target.update(dt)
    screen.update_camera(target)

    # == Draw ==
    # Draw background
    screen.draw_background()
    # Draw the donjon
    donjon.draw(screen)

    # screen.draw_cross_center((255,0,0))

    # Update the screen
    screen.display_update()

pg.quit()