import pygame


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, length, width=0, height=0, color=(255,255,255), image=None, gravity=True):
        """Init

        Args:\n
            x : pos x
            y : pos y
            angle : angle where the particle will go
            length : speed vector
            width (int, optional): width of the particle. Defaults to 0.
            height (int, optional): height of the particle. Defaults to 0.
            color (tuple, optional): color of the particle. Defaults to (255,255,255).
            image (pygame.Surface, optional): image of the particle. Defaults to None.
            gravity (bool, optional): is the particle has gravity. Defaults to True.
        """
        
        super().__init__()

        if image == None:
            self.image = pygame.Surface([width, height])
            self.image.fill(color)
        else:
            self.image = image

        self.rect = self.image.get_rect()
        self.prev_rect = self.rect

        self.pos = pygame.math.Vector2(x, y)

        self.speed = pygame.math.Vector2(0,0)
        self.speed.from_polar((length, angle))

        self.acceleration = pygame.math.Vector2(0,0)

        if gravity:
            self.gravity = pygame.math.Vector2(0, 0.1)
        else:
            self.gravity = pygame.math.Vector2(0, 0)

    def set_color(self, color):
       self.image.fill(color)

    def update(self):
        self.prev_rect = pygame.Rect(self.rect)

        self.speed += self.acceleration
        self.speed += self.gravity

        self.pos += self.speed

        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def draw_background(self, screen):
        return screen.draw_background(self.prev_rect)

    def clean(self, screen):
        return screen.draw_background(self.rect)

    def get_pos(self):
        return (self.pos.x, self.pos.y)


class ParticleSystem(pygame.sprite.RenderUpdates):
    def __init__(self):
        super().__init__()

    def draw(self, screen):
        self.update()
        rect_list = [sprite.draw_background(screen) for sprite in self.sprites()]
        rect_list.extend(super().draw(screen))
        return rect_list
        #Ici il faudrais mettre un return et gerer ça plus globalement

    def cleanEmpty(self, screen):
        rect_list = [sprite.clean(screen) for sprite in self.sprites()]
        pygame.display.update(rect_list)
        self.empty()

    def remove_first(self, screen):
        if (len(self.sprites()) > 0):
            s = self.sprites()[0]
            s.kill()
            r = s.clean(screen)
            pygame.display.update(r)