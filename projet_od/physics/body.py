import pygame as pg

class Body(pg.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        
        self.image = pg.Surface((64,64))
        self.image.fill((48,212,32))
        
        self.rect = self.image.get_rect()
        self.prev_rect = self.rect
        
        self.pos = pg.Vector2(x, y)
        self.vel = pg.Vector2(0,0)

    
    def update(self, dt):
        self.prev_rect = pg.Rect(self.rect)
        
        self.pos += self.vel * dt
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
    def draw(self, screen):
        rect = [screen.draw_background(self.prev_rect)]
        rect.append(screen.blit(self.image, self.rect))
        pg.display.update(rect)
        
