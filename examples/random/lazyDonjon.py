import pygame as pg
from project_od.screen import SmartScreen, DummyTarget
from project_od.utils import clamp
from project_od.gui import Label

pg.init()
w,h = 720,480

screen = SmartScreen(w,h)

class Room:
    def __init__(self, x, y, openning=None) -> None:
        if openning == None:
            self.openning = [True, True, True, True] # left, top, right, bottom
        else:
            self.openning = openning
        self.next_room = [None for _ in range(4)]
        self.x = x
        self.y = y
    
    def __hash__(self) -> int:
        return hash((self.x,self.y))
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Room):
            return (self.x, self.y) == (__o.x, __o.y)
        return False

class LazyRoom(Room):
    def __init__(self, x, y, openning=None) -> None:
        super().__init__(x, y, openning)
        self.loaded = False
    
    def on_load(self):
        pass

class RoomGenerator:
    def next(self, x : int, y : int, rules : list[bool|None], dir : int, *args, **kwargs) -> Room:
        return Room(x, y)

class LazyDonjon:
    def __init__(self, generator : RoomGenerator) -> None:
        self.generator = generator
        self.rooms = {}
        self.load(0,0)
    
    def get(self, x, y):
        room = self.rooms.get((x,y), None)
        if room == None or room.loaded == False:
            self.load(x,y)
        return room
    
    def load(self, x, y):
        if (x,y) not in self.rooms:
            surrounding = [self.rooms.get(k, None) for k in ((x-1,y),(x, y-1),(x+1,y),(x,y+1))]
            rules = [r.openning[(j+2)%4] if r != None else None for j, r in enumerate(surrounding)]
            room = generator.next(x,y, rules=rules, dir=-1)
            self.rooms[(x,y)] = room
        else:
            room = self.rooms[(x,y)]
        x, y = room.x, room.y
        room.loaded = True
        room.on_load()


        # Pre load the next room
        for i, (xr,yr) in enumerate(((x-1,y),(x, y-1),(x+1,y),(x,y+1))):
            if room.openning[i] and room.next_room[i] == None and (xr,yr) not in self.rooms:
                surrounding = [self.rooms.get(k, None) for k in ((xr-1,yr),(xr, yr-1),(xr+1,yr),(xr,yr+1))]
                rules = [r.openning[(j+2)%4] if r != None else None for j, r in enumerate(surrounding)]

                r = generator.next(x=xr, y=yr, dir=i, rules=rules)

                self.rooms[(xr,yr)] = r

                for j, sr in enumerate(surrounding):
                    if sr != None:
                        sr.next_room[(j+2)%4] = r
                        r.next_room[j] = sr

size = 30
factor = .4
from random import random

class DrawRoom(LazyRoom):
    def __init__(self, x, y, color, openning) -> None:
        super().__init__(x, y, openning)
        self.image = pg.Surface((30,30))
        self.image.fill((200,200,200))
        self.realColor = color
        self.color = (20,20,20)
    
    def render(self):
        pg.draw.rect(self.image, self.color, ((size/6, size/6),(size*2/3, size*2/3)))
        halfi = size/2 - size/12
        ort = (0,halfi),(halfi, 0), (size-size/6, halfi), (halfi, size-size/6)
        for i, op in enumerate(self.openning):
            if op:
                pg.draw.rect(self.image, self.color, (ort[i],(size/6, size/6)))
    
    def on_load(self):
        self.color = self.realColor
        self.render()

    def draw(self, screen):
        screen.blit_cam(self.image, pg.Rect(self.x*size, self.y*size,0,0))
    
    def __str__(self) -> str:
        return f"{self.x,self.y} - {self.openning}"
    
    def __repr__(self) -> str:
        return str(self)

class ColorRoomGenerator(RoomGenerator):
    def randomColor(self):
        return tuple(int(clamp(random()*255, 30, 230)) for _ in range(3))

    def next(self, x, y, rules, dir=-1 , **kwargs):
        if all(i==None for i in rules):
            r = DrawRoom(x,y, (255,)*3, openning=list((True,)*4))
            r.render()
            return r
        
        op = [random() < factor for _ in range(4)]
        if not any(op):
            op = [True for _ in op]
        r = DrawRoom(x,y,self.randomColor(), openning=op)
        for i, rule in enumerate(rules):
            if rule != None:
                r.openning[i] = rule

        r.render()
        return r
        

class DrawDonjon(LazyDonjon):
    def __init__(self, generator: RoomGenerator) -> None:
        super().__init__(generator)
    
    def draw(self, screen):
        for room in self.rooms.values():
            room.draw(screen)

generator = ColorRoomGenerator()
target = DummyTarget(0, 0)
donjon = DrawDonjon(generator)
x, y = 0,0

font = pg.font.SysFont("Comic Sans Ms", 26)

lb = Label((10, 10), f"{x}, {y}", font, text_color=(255,255,255))

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                donjon.__init__(generator)
                target.move_to(0,0)
            r = donjon.get(x,y)
            if event.key == pg.K_LEFT:
                if r.openning[0]:
                    x -= 1
            if event.key == pg.K_UP:
                if r.openning[1]:
                    y -= 1
            if event.key == pg.K_RIGHT:
                if r.openning[2]:
                    x += 1
            if event.key == pg.K_DOWN:
                if r.openning[3]:
                    y += 1

            donjon.load(x,y)
            target.move_to(x*size,y*size)
            lb.set_text(f"{x}, {y}")


    screen.update_camera(target)
    lb.update()
    screen.fill((25,25,25))
    
    donjon.draw(screen)
    pg.draw.rect(screen.surface, (255,0,0), screen.from_cam(((x*size + size/4, y*size + size/4),(size/2,size/2))))
    lb.draw(screen)

    screen.display_update()

pg.quit()