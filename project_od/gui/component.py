import pygame as pg
from project_od.gui.theme import *
from project_od.utils import clamp, map

class Component:
    """Basic component for graphic, interactif component."""
    def __init__(self, pos : tuple, size : tuple, **kwargs):
        """Basic component use in every gui component.

        Args:
            pos (tuple): (x, y) position from top left
            size (tuple): (width, height) size of the component

        Kwargs:
            theme (theme) : Default WHITE
            color (Color) : Default theme.default_color
        """

        self.rect = pg.Rect(pos, size)

        def empty():
            pass
        def get(attr):
            g = None
            if attr in kwargs:
                g = kwargs[attr]
            elif hasattr(self, attr):
                g = getattr(self, attr)
            if g != None:
                return g
            return empty

        self.theme = kwargs.get("theme", THEME)

        self.on_click = get("on_click")
        self.on_left_click = get("on_left_click")
        self.on_right_click = get("on_right_click")
        self.on_middle_click = get("on_middle_click")
        self.on_hover_enter = get("on_hover_enter")
        self.on_hover = get("on_hover")
        self.on_hover_exit = get("on_hover_exit")
        self.on_press = get("on_press")
        self.on_drag = get("on_drag")
        self.on_change = get("on_change")
        self.on_press_left = get("on_press_left")
        self.on_press_right = get("on_press_right")
        self.on_press_middle = get("on_press_middle")
        self.on_focus_enter = get("on_focus_enter")
        self.on_focus_exit = get("on_focus_exit")
        self.on_pre_update = get("on_pre_update")
        self.on_post_update = get("on_post_update")
        self.pressed = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_middle = False
        self.hover = False
        self.focus = False
        self.dragging = False
        self.color = kwargs.get("color", self.theme.default_color)


    def update(self, scale=1) -> None:
        """Update the widget, call the registered event

        Args:
            scale (int, optional): Scale the widget. Defaults to 1.
        """
        self.on_pre_update()
        mouse = pg.mouse
        rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width*scale, self.rect.height*scale)
        if rect.collidepoint(mouse.get_pos()):
            self.on_hover()
            if not self.hover:
                self.on_hover_enter()
            self.hover = True
        else:
            self.on_hover_exit()
            self.hover = False
            self.pressed = False
            self.pressed_left = False
            self.pressed_right = False
            self.pressed_middle = False
        
        pressed = mouse.get_pressed()  
        if any(pressed):
            if self.hover:
                if not self.focus:
                    self.dragging = True
                    self.on_focus_enter()
                self.focus = True
                self.pressed = True
                self.on_press()
                if pressed[0]:
                    self.pressed_left = True
                    self.on_press_left()
                if pressed[1]:
                    self.pressed_middle = True
                    self.on_press_middle()
                if pressed[2]:
                    self.pressed_right = True
                    self.on_press_right()
            else:
                if self.focus:
                    self.on_focus_exit()
                self.focus = False

            if self.dragging:
                self.on_drag()
        else:
            if self.hover:
                if self.pressed:
                    self.on_click()
                    self.pressed = False
                if self.pressed_left:
                    self.on_left_click()
                    self.pressed_left = False
                if self.pressed_right:
                    self.on_right_click()
                    self.pressed_right = False
                if self.pressed_middle:
                    self.on_middle_click()
                    self.pressed_middle = False
            self.dragging = False

        self.on_post_update()

    def on_pre_update(self):
        self.color = (self.theme.default_color)

    def on_press(self):
        self.color = (self.theme.pressed_color)

    def on_hover(self):
        self.color = (self.theme.hover_color)

    def on_focus(self):
        self.color = (self.theme.focus_color)

    
    def move(self, offset : tuple):
        """Move the widget from an offset

        Args:
            offset (tuple): (x,y)
        """
        self.rect.move_ip(offset[0], offset[1])

    def move_to(self, pos : tuple):
        """Move the widget to a position

        Args:
            pos (tuple): (x,y)
        """
        horizontal_shift = pos[0]-self.rect.x
        vertical_shift = pos[1]-self.rect.y
        self.move((horizontal_shift,vertical_shift))
    
    def center_x(self, component):
        """Center the widget to the center x of the other component

        Args:
            component (Component): An other component
        """
        self.move_to((component.rect.centerx - self.rect.width/2, self.rect.y))

    def center_y(self, component):
        """Center the widget to the center y of the other component

        Args:
            component (Component): An other component
        """
        self.move_to((self.rect.x, component.rect.centery - self.rect.height/2))
    

    def center(self, component):
        """Center the widget to the center x and y of the other component

        Args:
            component (Component): An other component
        """
        self.move_to((component.rect.centerx - self.rect.width/2, component.rect.centery - self.rect.height/2))


class GUIComponent(Component, pg.sprite.Sprite):
    """Blank graphical component."""
    def __init__(self, pos : tuple, size : tuple, **kwargs):
        """A first use of an component.

        Args:
            pos (tuple): (x, y) position.
            size (tuple): (width, height) size of the component.
        
        Kwargs:
            image (Surface): an image for the component.
            theme (theme) : Default WHITE
            color (Color) : Default theme['default_color']
        """
        pg.sprite.Sprite.__init__(self)
        Component.__init__(self, pos, size, **kwargs)

        image = kwargs.get("image", None)
        if image == None:
            self.has_image = False
            self.image = pg.Surface(size)
            self.image.fill((123,30,73))
        else:
            self.has_image = True
            self.image = image


    def draw(self, screen) -> None:
        """Draw the image, to the rect on the screen.

        Args:
            screen (Surface | Screen): a surface to draw to.
        """
        screen.blit(self.image, self.rect)

    def update(self):
        if not self.has_image:
            self.image.fill(self.color)
        Component.update(self)


class Label(GUIComponent):
    """A label widget"""
    def __init__(self, pos : tuple, text : str, font, **kwargs):
        """A basic widget to show text

        Args:
            pos (tuple): (x, y) position from top left
            text (str): text of the label
            font (font): the font of the text
        
        Kwargs:
            padding (int) : padding from left
            theme (theme) : Default WHITE
            text_color (Color) : color of the text
            color (Color) : Default theme['default_color']
        """
        pg.sprite.Sprite.__init__(self)
        self.font = font
        self.text : str = text
        self.text_size : tuple = font.size(text)
        self.padding : int = kwargs.get("padding", 0)
        self.on_hover = None
        self.on_press = None
        self.on_focus = None
        self.on_pre_update = None
        GUIComponent.__init__(self, (pos[0] + self.padding, pos[1]), self.text_size, **kwargs)
        self.text_color = kwargs.get("text_color", self.theme.text_color)
        self.render()
        self.has_image = True

    def render(self) -> None:
        self.image = self.font.render(self.text, True, self.text_color)
    
    def set_text(self, text : str):
        """Set text
        """
        prev = self.text
        self.text = str(text)
        if self.text != prev:
            self.render()


class Button(GUIComponent):
    """A button widget"""
    def __init__(self, pos : tuple, size : tuple, font, text="", **kwargs):
        """

        Args:
            pos (tuple): (x, y) position from top left
            size (tuple): (width, height) size of the component
            font (font): the font of the text
            text (str, optional): text on the button. Defaults to "".
        
        Kwargs:
            padding (int) : padding from left
            theme (theme) : Default WHITE
            text_color (Color) : color of the text
            color (Color) : Default theme['default_color']
        """
        self.on_focus = None
        GUIComponent.__init__(self, pos, size, **kwargs)
        kwargs.setdefault("padding", self.theme.padding)
        self.label = Label(pos, text, font, **kwargs)
        self.label.rect.centery = self.rect.centery
        
    def update(self):
        GUIComponent.update(self)
        self.label.update()
    

    def draw(self, screen) -> None:
        GUIComponent.draw(self, screen)
        self.label.draw(screen)
    
    def move(self, pos):
        GUIComponent.move(self, pos)
        self.label.move(pos)

    def set_text(self, text):
        self.label.set_text(text)
    
    def center_text(self):
        self.label.center(self)


class Slider(GUIComponent):
    """A slider widget"""
    def __init__(self, pos_min : tuple, pos_max : tuple, size : tuple, value_range : tuple, **kwargs):
        """_summary_

        Args:
            pos_min (tuple): _description_
            pos_max (tuple): _description_
            size (tuple): _description_
            value_range (tuple): _description_

        Kwargs:
            default (float) : default value of the slide
            theme (theme) : Default WHITE
            color (Color) : Default theme['default_color']

        Raises:
            ValueError: can't be diagonale
        """
        if (pos_min[0] != pos_max[0]) and (pos_min[1] != pos_max[1]):
            raise ValueError("Need to be vertical or horizontal, not diagonal")

        self.pos_min = pos_min
        self.pos_max = pos_max
        
        GUIComponent.__init__(self, ((pos_min[0]+pos_max[0])/2-size[0]/2, (pos_min[1]+pos_max[1])/2-size[1]/2), size, **kwargs)
        self.range : tuple = value_range
        self.value : float = kwargs.get("default",(value_range[0] + value_range[1]) / 2)
        self.place_slider()

    def move(self, pos):
        GUIComponent.move(self, pos)
        self.pos_min = self.pos_min[0] + pos[0], self.pos_min[1] + pos[1]
        self.pos_max = self.pos_max[0] + pos[0], self.pos_max[1] + pos[1]
        self.place_slider()
    
    
    def place_slider(self) -> None:
        if self.pos_min[0] == self.pos_max[0]:
            self.rect.centery = map(self.value, self.range[0], self.range[1], self.pos_min[1], self.pos_max[1])
        else:
            self.rect.centerx = map(self.value, self.range[0], self.range[1], self.pos_min[0], self.pos_max[0])
    
    def on_drag(self) -> None:
        pos = pg.mouse.get_pos()
        pos_min = self.pos_min
        pos_max = self.pos_max
        self.rect.centerx = clamp(pos[0], pos_min[0], pos_max[0])
        self.rect.centery = clamp(pos[1], pos_min[1], pos_max[1])
        prev = self.value
        if pos_min[0] == pos_max[0]:
            self.value = map(self.rect.centery, pos_min[1], pos_max[1], self.range[0], self.range[1])
        else:
            self.value = map(self.rect.centerx, pos_min[0], pos_max[0], self.range[0], self.range[1])
        if prev != self.value:
            self.on_change()
        
        
    def draw(self, screen):
        if isinstance(screen, pg.Surface):
            pg.draw.line(screen, self.theme.default_color, self.pos_min, self.pos_max)
            pg.draw.rect(screen, self.color, self.rect)
        else:
            pg.draw.line(screen.surface, self.theme.default_color, self.pos_min, self.pos_max)
            pg.draw.rect(screen.surface, self.color, self.rect)

    def get_value(self):
        """Return the value of the slide
        """
        return round(self.value, 3)


class InputText(GUIComponent):
    """A inputtext widget"""
    def __init__(self, pos : tuple, size : tuple, font,**kwargs):
        """
        Args:
            pos (tuple): (x, y) position from top left
            size (tuple): (width, height) size of the component
            font (font): the font of the text
        
        Kwargs:
            padding (int) : padding from left
            text (str) : default text
            theme (theme) : Default WHITE
            color (Color) : Default theme['default_color']
            text_color (Color) : color of the text
        """
        GUIComponent.__init__(self, pos, size, **kwargs)
        pg.key.set_text_input_rect(self.rect)
        self.font = font
        self.font_height = self.font.get_height()
        self.set_text(kwargs.get("text", ""))
        self.padding : int = kwargs.get("padding", self.theme.padding)
        self.text_color = kwargs.get("text_color", self.theme.text_color)
        self.render(self.text)
        self.text_pos = (self.rect.x + self.padding, self.rect.y + self.rect.height/2 - self.font_height/2)
    
    def move(self, pos):
        GUIComponent.move(self, pos)
        self.text_pos = (self.rect.x + self.padding, self.rect.y + self.rect.height/2 - self.font_height/2)

    def render(self, text) -> None:
        self.text_image = self.font.render(text, True, self.text_color)
        self.prev_text = text
    
    def on_focus_enter(self):
        pg.key.start_text_input()
    
    def on_focus_exit(self):
        pg.key.stop_text_input()
    
    def update(self, events) -> None:
        GUIComponent.update(self)
        if self.focus:
            for event in events:
                if event.type == pg.KEYDOWN:
                    change = True
                    if event.key == pg.K_BACKSPACE:
                        self.text = self.text[0:self.imePos-1] + self.text[self.imePos:]
                        self.imePos = max(0, self.imePos-1)
                    elif event.key == pg.K_DELETE:
                        self.text = self.text[0:self.imePos] + self.text[self.imePos+1:]
                    elif event.key == pg.K_LEFT:
                        self.imePos = max(0,self.imePos-1)
                    elif event.key == pg.K_RIGHT:
                        self.imePos = min(len(self.text),self.imePos+1)
                    else:
                        change = False

                    if change:
                        self.on_change()  
                        
                elif event.type == pg.TEXTINPUT:
                    self.text = self.text[:self.imePos] + event.text + self.text[self.imePos:]
                    self.imePos += len(event.text)
                    self.on_change()
                
                elif event.type == pg.TEXTEDITING:
                    self.text = event.text
                    self.imePos = event.start
                    self.on_change()
                    
    def draw(self, screen):
        GUIComponent.draw(self, screen)
        if self.focus:
            text = self.text[: self.imePos] + '|' + self.text[self.imePos:]
        else:
            text = self.text
        

        index_max = max(1,round((self.rect.width-self.padding)/(self.font_height/2.7)))
        if len(text) > index_max:
            text = text[min(self.imePos, len(text)-index_max): (self.imePos+index_max)]

        if text != self.prev_text:
            self.render(text)

        screen.blit(self.text_image, self.text_pos)
    
    def set_padding(self, padding):
        self.padding = padding
        self.text_pos = (self.rect.x + self.padding, self.rect.y + self.rect.height/2 - self.font_height/2)
        
    def set_text(self, text):
        self.text = str(text)
        self.imePos = len(self.text)
    
    def get_text(self) -> str:
        return self.text


class Panel(pg.sprite.Group, Component):
    """A panel widget"""
    def __init__(self, pos: tuple, size: tuple, **kwargs):
        """

        Args:
            pos (tuple): (x, y) position from top left
            size (tuple): (width, height) size of the component

        Kwargs:
            theme (theme) : Default WHITE
            color (Color) : Default theme['default_color']
        """
        Component.__init__(self, pos, size, **kwargs)
        pg.sprite.Group.__init__(self)
    
    def update(self, *args, **kwargs):
        Component.update(self, *args, **kwargs)
        pg.sprite.Group.update(self, *args, **kwargs)
    
    def move(self, pos):
        Component.move(self, pos)
        for child in self.sprites():
            child.move(pos)
    
    def draw(self, screen):
        for child in self.sprites():
            child.draw(screen)

    def move_to(self, pos):
        horizontal_shift = pos[0]-self.rect.x
        vertical_shift = pos[1]-self.rect.y
        self.move((horizontal_shift,vertical_shift))