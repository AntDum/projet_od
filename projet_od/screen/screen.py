import pygame as pg

class BaseScreen:
    def __init__(self, w, h):
        self.surface = pg.display.set_mode((w,h))
        if not hasattr(self, "blit"):
            self.blit = self.surface.blit
        self.fill = self.surface.fill
        self.background = None
        self.width = w
        self.height = h

    def draw_background(self, rect):
        return self.blit(self.background, rect, rect)

    def make_background(self, color):
        self.background = pg.Surface((self.width, self.height))
        self.background.fill(color)

class CameraScreen(BaseScreen):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.camera = pg.Rect(0,0,w,h)
        self.border : tuple = None # left, top, right, bottom
    
    def background_cam(self, rect):
        return self.draw_background(rect.move(self.camera.topleft))

    def blit_cam(self, image, rect):
        return self.blit(image, rect.move(self.camera.topleft))
    
    def from_cam(self, rect):
        rect = pg.Rect(rect)
        return rect.move(self.camera.topleft)
    
    def set_camera_point(self, pos):
        x = -pos[0] + self.width//2
        y = -pos[1] + self.height//2

        if self.border != None:
            xm, ym, xp, yp = self.border
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
    
    def draw_rect(self, rect, color):
        pg.draw.rect(self.surface, color=color, rect=rect)
    
    def draw_line(self, start_pos, end_pos, color, width=1):
        pg.draw.line(self.surface, color=color, start_pos=start_pos, end_pos=end_pos, width=width)