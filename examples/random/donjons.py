import pygame as pg
from project_od.screen import CameraScreen, DummyTarget
from project_od.utils import clamp

pg.init()
w,h = 720,480

screen = CameraScreen(w,h)

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

class RoomGenerator:
    def next(self, x : int, y : int, rules : list[bool|None], dir : int, *args, **kwargs) -> Room:
        return Room(x, y)

class Donjon:
    def __init__(self, generator : RoomGenerator) -> None:
        f = generator.next(x=0,y=0, rules=[None for _ in range(4)], dir=-1)
        self.rooms = {(0,0):f}
        stack = [f]
        while len(stack) != 0:
            room = stack.pop(0)
            x, y = room.x, room.y
            
            for i, (xr,yr) in enumerate(((x-1,y),(x, y-1),(x+1,y),(x,y+1))):
                if room.openning[i] and room.next_room[i] == None:
                    surrounding = [self.rooms.get(k, None) for k in ((xr-1,yr),(xr, yr-1),(xr+1,yr),(xr,yr+1))]
                    rules = [r.openning[(j+2)%4] if r != None else None for j, r in enumerate(surrounding)]

                    r = generator.next(x=xr, y=yr, dir=i, rules=rules)

                    self.rooms[(xr,yr)] = r

                    for j, sr in enumerate(surrounding):
                        if sr != None:
                            sr.next_room[(j+2)%4] = r
                            r.next_room[j] = sr
                    stack.append(r)

size = 30
factor = .4
from random import random

class DrawRoom(Room):
    def __init__(self, x, y, color, openning) -> None:
        super().__init__(x, y, openning)
        self.image = pg.Surface((30,30))
        self.image.fill((0,0,0))
        self.color = color
        pg.draw.rect(self.image, color, ((size/6, size/6),(size*2/3, size*2/3)))
    
    def render(self):
        halfi = size/2 - size/12
        ort = (0,halfi),(halfi, 0), (size-size/6, halfi), (halfi, size-size/6)
        for i, op in enumerate(self.openning):
            if op:
                pg.draw.rect(self.image, self.color, (ort[i],(size/6, size/6)))
    
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
        if dir == -1:
            r = DrawRoom(x,y, (255,)*3, openning=list((True,)*4))
            r.render()
            return r
        
        op = [random() < factor for _ in range(4)]

        r = DrawRoom(x,y,self.randomColor(), openning=op)
        for i, rule in enumerate(rules):
            if rule != None:
                r.openning[i] = rule

        r.render()
        return r
        

class DrawDonjon(Donjon):
    def __init__(self, generator: RoomGenerator) -> None:
        super().__init__(generator)
    
    def draw(self, screen):
        for room in self.rooms.values():
            room.draw(screen)

generator = ColorRoomGenerator()
target = DummyTarget(0, 0)
donjon = DrawDonjon(generator)


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                donjon.__init__(generator)
                target.move_to(0,0)

    target.update()
    screen.update_camera(target)
    
    screen.fill((25,25,25))
    donjon.draw(screen)

    pg.display.update()

pg.quit()