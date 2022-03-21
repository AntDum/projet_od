import pygame as pg
from projet_od.screen import CameraScreen
from projet_od.physics.body import DummyTarget

pg.init()
w,h = 720,480

screen = CameraScreen(w,h)

class Room:
    def __init__(self, x, y) -> None:
        self.openning = [True, True, True, True] # left, top, right, bottom
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
    def next(self, x=0, y=0, *args, **kwargs) -> Room:
        return Room(x, y)

class Donjon:
    def __init__(self, generator : RoomGenerator) -> None:
        self.rooms = []
        self.krooms = {}
        stack = [generator.next(0,0, key=self.krooms)]
        while len(stack) != 0:
            room = stack.pop(0)
            print(room)
            x, y = room.x, room.y
            self.rooms.append(room)
            for i, (xr,yr) in enumerate(((x-1,y),(x, y-1),(x+1,y),(x,y+1))):
                if room.openning[i] and room.next_room[i] == None:
                    stack.append(generator.next(xr, yr, prev=room, dir=i, key=self.krooms))

size = 30
factor = .1
from random import random

class DrawRoom(Room):
    def __init__(self, x, y, color, openning) -> None:
        super().__init__(x, y)
        self.openning = openning
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

class ColorRoomGenerator(RoomGenerator):
    def randomColor(self):
        return tuple(int(random()*255) for _ in range(3))

    def next(self, x, y, prev=None, dir=-1, key={}, **kwargs):
        if prev == None:
            return DrawRoom(x,y, (255,)*3, openning=list((True,)*4))
        
        op = [random() < factor for _ in range(4)]

        r = DrawRoom(x,y,self.randomColor(), openning=op)
        for i, coor in enumerate(((x-1,y),(x, y-1),(x+1,y),(x,y+1))):
            if coor in key:
                opposite = (i+2)%4
                ele = key[coor]
                r.openning[i] = ele.openning[opposite]
                ele.next_room[opposite] = r
                r.next_room[i] = ele

        key[(x,y)] = r
        r.render()
        return r
        

class DrawDonjon(Donjon):
    def __init__(self, generator: RoomGenerator) -> None:
        super().__init__(generator)
    
    def draw(self, screen):
        for room in self.rooms:
            room.draw(screen)


target = DummyTarget(0, 0)
donjon = DrawDonjon(ColorRoomGenerator())


run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
           run = False
        

    target.update()
    screen.update_camera(target)
    
    screen.fill((25,25,25))
    donjon.draw(screen)

    pg.display.update()

pg.quit()