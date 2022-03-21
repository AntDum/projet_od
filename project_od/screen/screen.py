import pygame as pg

class BaseScreen:
    def __init__(self, w, h):
        self.surface = pg.display.set_mode((w,h))
        if not hasattr(self, "blit"):
            self.blit = self.surface.blit
        if not hasattr(self, "fill"):
            self.fill = self.surface.fill
        self.background = None
        self.width = w
        self.height = h

    def draw_background(self, rect=None):
        if self.background:
            if rect == None:
                rect = pg.Rect(0,0,self.width, self.height)
            return self.blit(self.background, rect, rect)

    def make_background(self, color):
        self.background = pg.Surface((self.width, self.height))
        self.background.fill(color)
    
    def draw(self, other):
        if hasattr(other, "draw"):
            other.draw(self)
        elif hasattr(other, "image") and hasattr(other, "rect"):
            self.blit(other.image, other.rect)
    
    def display_update(self, o=None):
        if o != None:
            pg.display.update(o)
        else:
            pg.display.update()

class CameraScreen(BaseScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.camera = pg.Rect(0,0,w,h)
        self.camera_border : tuple = None # left, top, right, bottom
    
    def background_cam(self, rect):
        return self.draw_background(self.from_cam(rect))

    def blit_cam(self, image, rect):
        return self.blit(image, self.from_cam(rect))
    
    def from_cam(self, rect):
        rect = pg.Rect(rect)
        return rect.move(self.camera.topleft)
    
    def set_camera_point(self, pos):
        x = -pos[0] + self.width//2
        y = -pos[1] + self.height//2

        if self.camera_border != None:
            xm, ym, xp, yp = self.camera_border
            x = min(xm, x)
            y = min(ym, y)

            x = max(-(xp - self.width), x)
            y = max(-(yp - self.height), y)

        self.camera.x = x
        self.camera.y = y

    def update_camera(self, target):
        """Set the vue of the camera to the target at the center

        Args:
            target : has a rect
        """
        self.set_camera_point((target.rect.x, target.rect.y))


class DummyTarget:
    def __init__(self, x, y, speed=1) -> None:
        self.rect = pg.Rect(x,y,0,0)
        self.speed = 1

    def update(self, dt=1):
        keys = pg.key.get_pressed()
        dx = keys[pg.K_RIGHT] - keys[pg.K_LEFT]
        dy = keys[pg.K_DOWN] - keys[pg.K_UP]
        s = dt * self.speed
        self.rect.move_ip(dx * s, dy * s)
    
    def move(self, x, y):
        self.rect.move_ip(x,y)
    
    def move_to(self, x, y):
        self.rect.x = x
        self.rect.y = y

class DrawableScreen(BaseScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
    
    def draw_rect(self, rect, color, *args, **kwargs):
        pg.draw.rect(self.surface, color=color, rect=rect, *args, **kwargs)
    
    def draw_line(self, start_pos, end_pos, color, width=1, *args, **kwargs):
        pg.draw.line(self.surface, color=color, start_pos=start_pos, end_pos=end_pos, width=width, *args, **kwargs)


class SmartScreen(CameraScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.to_update = []
        self.full_update = False

    def display_update(self, extend=[]):
        if self.full_update:
            pg.display.update()
        else:
            pg.display.update(self.to_update)
            if extend:
                pg.display.update(extend)
        self.full_update = False
        self.to_update = []

    def draw_background(self, rect=None):
        if rect != None:
            self.to_update.append(super().draw_background(rect))
        else:
            self.full_update = True
            super().draw_background(rect)

    def blit(self, image, rect, area=None):
        r = self.surface.blit(image, rect, area)
        self.to_update.append(r)
    
    def draw(self, other, area=None):
        if hasattr(other, "draw"):
            other.draw(self)
        elif hasattr(other, "rect"):
            rect = None
            prev_rect = None
            if hasattr(other, "prev_rect"):
                prev_rect = self.draw_background(other.prev_rect)
            if hasattr(other, "image"):
                rect = self.blit(other.image, other.rect, area=area)
            elif hasattr(other, "color"):
                rect = self.fill(other.color, rect)
            if prev_rect:
                if rect.colliderect(prev_rect):
                    self.to_update(rect.union(prev_rect))
                else:
                    self.to_update(rect)
                    self.to_update(prev_rect)
            else:
                self.to_update(rect)
            
    def draw_cam(self, other, area=None):
        if hasattr(other, "draw"):
            other.draw(self)
        elif hasattr(other, "rect"):
            rect = None
            prev_rect = None
            if hasattr(other, "prev_rect"):
                prev_rect = self.background_cam(other.prev_rect)
            if hasattr(other, "image"):
                rect = self.blit_cam(other.image, other.rect, area=area)
            elif hasattr(other, "color"):
                rect = self.fill(other.color, self.from_cam(rect))
            if prev_rect:
                if rect.colliderect(prev_rect):
                    self.to_update(rect.union(prev_rect))
                else:
                    self.to_update(rect)
                    self.to_update(prev_rect)
            else:
                self.to_update(rect)

    def fill(self, color, rect=None):
        if rect==None:
            self.surface.fill(color)
            self.full_update = True
        else:
            self.to_update.append(self.surface.fill(color, rect))
    
    def draw_rect(self, rect, color, *args, **kwargs):
        self.to_update.append(pg.draw.rect(self.surface, color=color, rect=rect, *args, **kwargs))
    
    def draw_line(self, start_pos, end_pos, color, width=1, *args, **kwargs):
        self.to_update.append(pg.draw.line(self.surface, color=color, start_pos=start_pos, end_pos=end_pos, width=width, *args, **kwargs))

    def draw_cross_center(self, color, width=1, *args, **kwargs):
        self.draw_line((self.width/2, 0),(self.width/2, self.height), color, width, *args, **kwargs)
        self.draw_line((0, self.height/2),(self.width, self.height/2), color, width, *args, **kwargs)