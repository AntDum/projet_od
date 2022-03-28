from project_od.ia import GridAgent
from project_od.screen import SmartScreen
import pygame as pg

pg.init()

w, h = 720, 480

screen = SmartScreen(w,h)

grid = []
with open('./examples/ia/map01') as f:
    for line in f:
        if line:
            grid.append(list(line.strip()))
wall = ['#']

agent = GridAgent(grid, wall)

size = 30
mouse = 3,1
cat = 12, 11
empty = (0,0,0)
wall_color = (175, 200, 35)

def can_go(x,y):
    return grid[y][x] not in wall

def draw_map():
    for y, line in enumerate(grid):
        for x, case in enumerate(line):
            screen.draw_rect((x*size, y*size, size, size), empty if case == " " else wall_color)

    screen.draw_rect((mouse[0] *size, mouse[1] * size, size, size), (125,125,125))
    screen.draw_rect((cat[0] *size, cat[1] * size, size, size), (255,125,125))

def draw_path(path):
    for i in range(len(path)-1):
        screen.draw_line((path[i][0]*size+size/2, path[i][1]*size+size/2),
                        (path[i+1][0]*size+size/2, path[i+1][1]*size+size/2),
                        (255,0,0), width=3)

path = agent.shortest_path(cat, mouse)

draw_map()
draw_path(path)

screen.display_update()



run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            path = agent.shortest_path(cat, mouse)
            # print(cat,path)
            cat = path[0]
            if cat == mouse:
                run = False
                print("You lose")
            if event.key == pg.K_LEFT:
                if can_go(mouse[0]-1, mouse[1]):
                    mouse = mouse[0]-1, mouse[1]
            if event.key == pg.K_UP:
                if can_go(mouse[0], mouse[1]-1):
                    mouse = mouse[0], mouse[1]-1
            if event.key == pg.K_RIGHT:
                if can_go(mouse[0]+1, mouse[1]):
                    mouse = mouse[0]+1, mouse[1]
            if event.key == pg.K_DOWN:
                if can_go(mouse[0], mouse[1]+1):
                    mouse = mouse[0], mouse[1]+1

            draw_map()
            draw_path(path)

            screen.display_update()

pg.quit()