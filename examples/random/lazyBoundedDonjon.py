import pygame as pg
from project_od.screen import SmartScreen, DummyTarget
from project_od.utils import clamp
from project_od.gui import Label, Panel
from random import random


class LazyRoom:
    def __init__(self, x, y, openning=None) -> None:
        if openning == None:
            # left, top, right, bottom
            # True is a door, False a wall
            self.openning = [True, True, True, True]
        else:
            self.openning = openning
        self.next_room = [None for _ in range(4)]
        self.x = x
        self.y = y
        self.loaded = False
    
    def __hash__(self) -> int:
        return hash((self.x,self.y))
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, LazyRoom):
            return (self.x, self.y) == (__o.x, __o.y)
        return False

    def on_load(self):
        pass

    
class RoomGenerator:
    def next(self, x : int, y : int, rules : list[bool], dir : int, *args, **kwargs) -> LazyRoom:
        """Give an instance of a child of LazyRoom

            rules describe the shape of the room, it has a length of 4,
            where:
                0 is left,
                1 is top,
                2 is right,
                3 is bottom
            it can have 3 possibility :
                True there is a door,
                False there is a wall,
                None it's up to the generator to choose

        Args:
            x (int): the room is at x
            y (int): the room is at y
            rules (list[bool]): shape that the room can take
            dir (int): dir from where it come

        Returns:
            LazyRoom: The room instantiate
        """
        return LazyRoom(x, y)

class LazyBoundedDonjon:
    def __init__(self, generator : RoomGenerator) -> None:
        self.generator = generator
        self.min_rooms = minimum_rooms
        self.max_rooms = maximum_rooms
        self.rooms = {}
        self.to_create = {(0,0)}
        self.loaded = 0
        self.get(0,0)
    
    def get(self, x : int, y : int) -> LazyRoom:
        """Get the room at the coordinate, load it if it's not already

        Args:
            x (int): x coord
            y (int): y coord

        Returns:
            LazyRoom: The room asked
        """
        room = self.rooms.get((x,y), None)
        if room == None or room.loaded == False:
            self.load(x,y)
        return room
    
    def load(self, x : int, y: int) -> None:
        """Load the room at x, y and create it's neighboors

        Args:
            x (int): x coord
            y (int): y coord
        """
        if (x,y) not in self.rooms: # Not created
            # Neighbors coordinate
            neighborhood = (x-1,y),(x, y-1),(x+1,y),(x,y+1)
            # Neighbor room
            neighbors = [self.rooms.get(k, None) for k in neighborhood]
            # Can have a room in the direction
            rules = [r.openning[(j+2)%4] if r != None else None for j, r in enumerate(neighbors)]
            # Create the room
            room = generator.next(x,y, rules=rules, dir=-1)

            # Add the neighbor to the set (for counting purpose)
            for j, ope in enumerate(room.openning):
                if ope and neighborhood[j] not in self.rooms:
                    self.to_create.add(neighborhood[j])
            self.rooms[(x,y)] = room
        else: # Already created
            room = self.rooms[(x,y)]

        x, y = room.x, room.y

        room.loaded = True
        room.on_load()
        self.loaded += 1

        self.to_create.remove((x,y))

        # Create the next room
        for i, (xr,yr) in enumerate(((x-1,y),(x, y-1),(x+1,y),(x,y+1))):
            # If there is a door and the neighbor doesn't exist
            if room.openning[i] and room.next_room[i] == None and (xr,yr) not in self.rooms:

                neighborhood = (xr-1,yr),(xr, yr-1),(xr+1,yr),(xr,yr+1)
                neighbors = []
                rules = []
                authorized_door =  self.max_rooms - self.get_num_estimate_size()
                for j, k in enumerate(neighborhood):
                    r = self.rooms.get(k, None)
                    neighbors.append(r)
                    if r != None:
                        # There is a neighbor, make a wall if he has, or a door, be like him !
                        # Why would you have a personality ?
                        rules.append(r.openning[(j+2)%4])
                    else:
                        rule = False
                        
                        if authorized_door > 0: #Can generate more
                            if self.get_num_estimate_size() < self.min_rooms and self.get_num_border() == 1: #Have to generate more
                                    rule = True
                            else:
                                rule = None
                            authorized_door -= 1
                        rules.append(rule)

                # Create the room
                r = generator.next(x=xr, y=yr, dir=i, rules=rules)

                # Add the neighbor to the set (for counting purpose)
                for j, ope in enumerate(r.openning):
                    if ope and neighborhood[j] not in self.rooms:
                        self.to_create.add(neighborhood[j])
                

                self.rooms[(xr,yr)] = r
                
                # Link the room
                for j, sr in enumerate(neighbors):
                    if sr != None:
                        sr.next_room[(j+2)%4] = r
                        r.next_room[j] = sr

    def get_num_loaded(self):
        return self.loaded
    
    def get_num_created(self):
        return len(self.rooms)

    def get_num_to_create(self):
        return len(self.to_create)
    
    def get_num_unloaded(self):
        return self.get_num_created()-self.get_num_loaded()

    def get_num_border(self):
        return self.get_num_to_create()-self.get_num_unloaded()

    def get_num_estimate_size(self):
        return self.get_num_loaded() + self.get_num_to_create()




class DrawRoom(LazyRoom):
    def __init__(self, x, y, color, openning) -> None:
        super().__init__(x, y, openning)
        self.image = pg.Surface((size,size))
        self.image.fill((200,200,200))
        self.realColor = color
        self.color = (20,20,20)
        self.render()
    
    def render(self):
        pg.draw.rect(self.image, self.color, ((size/5, size/5),(size*6/10, size*6/10)))
        halfi = size/2 - size/10
        ort = (0,halfi),(halfi, 0), (size-size/5, halfi), (halfi, size-size/5)
        for i, op in enumerate(self.openning):
            if op:
                pg.draw.rect(self.image, self.color, (ort[i],(size/5, size/5)))
    
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
        #If has full choice (no neighbors) (new or tp)
        if all(i==None for i in rules):
            return DrawRoom(x,y, (255,)*3, openning=list((True,)*4))
        
        # Make the choice for empty space
        op = [random() < factor if rule == None else rule for rule in rules]

        return DrawRoom(x,y,self.randomColor(), openning=op)
        
class DrawDonjon(LazyBoundedDonjon):
    def __init__(self, generator: RoomGenerator) -> None:
        super().__init__(generator)
    
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

generator = ColorRoomGenerator()
target = DummyTarget(size/2, size/2)
donjon = DrawDonjon(generator)
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