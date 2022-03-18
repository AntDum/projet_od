import pygame as pg

class BaseScreen:
    def __init__(self, w, h):
        self.surface = pg.display.set_mode((w,h))
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

    def update_camera(self, target):
        x = -target.rect.x + self.width//2
        y = -target.rect.y + self.height//2

        if self.border != None:
            xm, ym, xp, yp = self.border
            x = min(xm, x)
            y = min(ym, y)

            x = max(-(xp - self.width), x)
            y = max(-(yp - self.height), y)

        self.camera.x = x
        self.camera.y = y