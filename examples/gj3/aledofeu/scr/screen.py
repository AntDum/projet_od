from project_od.screen import SmartScreen
import random as R

class Screen(SmartScreen):
    def __init__(self, w, h, tile_size=32, *args, **kwargs):
        super().__init__(w, h, *args, **kwargs)
        self.tile_size = tile_size
        self.amount_x_tile = 0
        self.amount_y_tile = 0
        
    
    def draw_grid(self):
        for x in range(0, self.width, self.tile_size):
            self.draw_line((x,0), (x,self.height), (181,181,181))
        for y in range(0, self.height, self.tile_size):
            self.draw_line((0,y), (self.width,y), (181,181,181))

    def set_size_tile(self, w, h):
        self.amount_x_tile = w
        self.amount_y_tile = h
        
    def shake(self):
        if R.random() > 0.5:
            self.camera.x += 5
        else:
            self.camera.x -= 5
        if R.random() > 0.5:
            self.camera.y += 5
        else:
            self.camera.y -= 5
