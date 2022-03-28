import pygame as pg
from project_od.screen import SmartScreen
from project_od.ia import GridAgent

pg.init()

w, h = 720, 480
FPS = 60
size = 20
screen = SmartScreen(w,h)
clock = pg.time.Clock()

screen.make_background((0,)*3)


class Pacman(pg.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.pos = pg.math.Vector2(x,y)
        self.dir = pg.math.Vector2(0,0)
    
    def update(self, dt):
        self.pos += self.dir * dt
        if self.dir.x != 0:
            self.pos.y = round(self.pos.y)
        else:
            self.pos.x = round(self.pos.x)
    
    def get_pos(self):
        return round(self.pos.x), round(self.pos.y)
    
    def draw(self, screen):
        screen.draw_circle((self.pos.x*size + size/2, self.pos.y*size + size/2), size/3,(255,255,0))

class Map:
    token = {"wall":"w",
            "pacman":"p",
            "power":"u",
            "empty":" ",
            "coin":"c"}

    def __init__(self) -> None:
        self.map = []
        self.pacman = None
        self.powerup = set()
        self.coins = set()
        with open("./examples/b/pacman/map") as f:
            for y, line in enumerate(f):
                lm = []
                for x, car in enumerate(line.strip()):
                    lm.append(car if car == self.token["wall"] else " ")
                    if car == self.token["coin"]:
                        self.coins.add((x,y))
                    elif car == self.token["pacman"]:
                        self.pacman = Pacman(x,y)
                    elif car == self.token["power"]:
                        self.powerup.add((x,y))
                self.map.append(lm)

        self.agent = GridAgent(self.map, [self.token["wall"]])

    def draw(self, screen : SmartScreen):
        for y, line in enumerate(self.map):
            for x, ele in enumerate(line):
                if ele == self.token['wall']:
                    screen.draw_rect((x*size, y*size, size, size), (0,20,100))
        
        for x,y in self.coins:
            screen.draw_circle((x*size + size/2, y*size + size/2), size/6, (255,255,255))

        for x,y in self.powerup:
            screen.draw_circle((x*size + size/2, y*size + size/2), size/4, (255,255,255))

        self.pacman.draw(screen)
    
    def can_go(self, x, y):
        return (0 <= y < len(self.map)) and (0 <= x < len(self.map[y])) and self.map[y][x] != self.token["wall"]
            

    def update(self, dt):
        self.pacman.update(dt)
        self.pacman.pos += self.pacman.dir
        x,y = self.pacman.get_pos()
        self.pacman.pos -= self.pacman.dir
        if not self.can_go(x,y):
           pass
        

    def key_pressed(self, key):
        x,y = self.pacman.get_pos()
        if key == "left":
            if (self.can_go(x-1, y)):
                self.pacman.dir = pg.math.Vector2(-1,0)
        elif key == "right":
            if (self.can_go(x+1, y)):
                self.pacman.dir = pg.math.Vector2(1,0)
        elif key == "up":
            if (self.can_go(x, y-1)):
                self.pacman.dir = pg.math.Vector2(0,-1)
        elif key == "down":
            if (self.can_go(x, y+1)):
                self.pacman.dir = pg.math.Vector2(0,1)

map = Map()

run = True
while run:
    dt = clock.tick(FPS) / 1000
    fps = round(1/dt)
    pg.display.set_caption(f"Pacman    (FPS : {FPS})")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                map.key_pressed("left")
            elif event.key == pg.K_RIGHT:
                map.key_pressed("right")
            elif event.key == pg.K_UP:
                map.key_pressed("up")
            elif event.key == pg.K_DOWN:
                map.key_pressed("down")

    screen.draw_background()

    map.update(dt)

    map.draw(screen)

    screen.display_update()

pg.quit()