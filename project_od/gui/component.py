from cmath import rect
from operator import length_hint
import pygame as pg
from project_od.gui.theme import *
from project_od.physics.animator import Follow
from project_od.physics.transform import rotate_pivot
from project_od.screen.screen import BaseScreen, DrawableScreen, SmartScreen
from project_od.utils import clamp, translate


def empty():
    pass

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
        self.on_drag_enter = get("on_drag_enter")
        self.on_drag = get("on_drag")
        self.on_drag_exit = get("on_drag_exit")
        self.on_change = get("on_change")
        self.on_press_left = get("on_press_left")
        self.on_press_right = get("on_press_right")
        self.on_press_middle = get("on_press_middle")
        self.on_focus_enter = get("on_focus_enter")
        self.on_focus_exit = get("on_focus_exit")
        self.on_pre_update = get("on_pre_update")
        self.on_post_update = get("on_post_update")
        self.draggable = kwargs.get("draggable", False)
        self.drag_rate = kwargs.get("drag_rate", 1)
        self.drag_min_dist = kwargs.get("drag_min_dist", 0.01)
        self.drag_rotate = kwargs.get("drag_rotate", False)
        self.drag_point = kwargs.get("drag_point", "auto")

        self._drag_offset = (0,0)
        self.follower = Follow(self.drag_rate, self.drag_min_dist)
        self.pressed = False
        self.newly_pressed = False
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_middle = False
        self.hover = False
        self.focus = False
        self.dragging = False
        self.global_mouse_pressed = False
        self.color = kwargs.get("color", self.theme.default_color)
        self.prev_pos = self.rect.topleft


    def update(self, scale=1) -> None:
        """Update the widget, call the registered event

        Args:
            scale (int, optional): Scale the widget. Defaults to 1.
        """
        
        self.on_pre_update()
        mouse = pg.mouse
        mouse_pos = mouse.get_pos()
        rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width*scale, self.rect.height*scale)
        if rect.collidepoint(mouse_pos):
            self.on_hover()
            if not self.hover:
                self.on_hover_enter()
            self.hover = True
        else:
            self.on_hover_exit()
            self.hover = False
            self.newly_pressed = False
            self.pressed = False
            self.pressed_left = False
            self.pressed_right = False
            self.pressed_middle = False
        
        pressed = mouse.get_pressed()  
        if any(pressed):
            
            if self.hover:
                if self.newly_pressed:
                    if not self.dragging:
                        self._on_drag_enter()
                        self.on_drag_enter()
                    if not self.focus:
                        self.on_focus_enter()
                    self.dragging = True
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
                if not self.global_mouse_pressed:
                    if self.focus:
                        self.on_focus_exit()
                        self.focus = False

            self.global_mouse_pressed = True
            if self.dragging:
                self._on_drag()
                self.on_drag()
        else:
            if self.hover and self.newly_pressed:
                if self.pressed:
                    self.on_click()
                if self.pressed_left:
                    self.on_left_click()
                if self.pressed_right:
                    self.on_right_click()
                if self.pressed_middle:
                    self.on_middle_click()
            if self.dragging:
                self._on_drag_exit()
                self.on_drag_exit()
            self.global_mouse_pressed = False
            self.pressed = False
            self.pressed_left = False
            self.pressed_right = False
            self.pressed_middle = False
            self.dragging = False
        
        if self.hover and not self.pressed:
            self.newly_pressed = True

        if self.focus:
            self.on_focus()

        self.on_post_update()
        self.rel_pos = self.rect.left - self.prev_pos[0], self.rect.top - self.prev_pos[1] 
        self.prev_pos = self.rect.topleft
        

    def on_pre_update(self):
        self.color = (self.theme.default_color)

    def on_press(self):
        self.color = (self.theme.pressed_color)

    def on_hover(self):
        self.color = (self.theme.hover_color)

    def on_focus(self):
        self.color = (self.theme.focus_color)

    def _on_drag_enter(self):
        if self.draggable:
            if self.drag_point == "auto":
                pos = pg.mouse.get_pos()
                off_x = pos[0] - self.rect.x
                off_y = pos[1] - self.rect.y
                self._drag_offset = off_x, off_y
            else:
                self._drag_offset = self.drag_point
            self.follower.set_current(self.rect.topleft)

    def _on_drag(self):
        if self.draggable:
            pos = pg.mouse.get_pos()
            self.follower.set_objectif((pos[0] - self._drag_offset[0], pos[1] - self._drag_offset[1]))
            self.move_to(self.follower.next())

    def _on_drag_exit(self):
        if self.draggable:
            self._drag_offset = (0,0)
    
    def move(self, offset : tuple):
        """Move the widget from an offset

        Args:
            offset (tuple): (x,y)
        """
        self.rect.move_ip(offset[0], offset[1])
        return self

    def move_to(self, pos : tuple):
        """Move the widget to a position

        Args:
            pos (tuple): (x,y)
        """
        horizontal_shift = pos[0]-self.rect.x
        vertical_shift = pos[1]-self.rect.y
        self.move((horizontal_shift,vertical_shift))
        return self
    
    def center_x(self, component):
        """Center the widget to the center x of the other component

        Args:
            component (Component): An other component
        """
        self.move_to((component.rect.centerx - self.rect.width/2, self.rect.y))
        return self

    def center_y(self, component):
        """Center the widget to the center y of the other component

        Args:
            component (Component): An other component
        """
        self.move_to((self.rect.x, component.rect.centery - self.rect.height/2))
        return self
    

    def center(self, component):
        """Center the widget to the center x and y of the other component

        Args:
            component (Component): An other component
        """
        self.move_to((component.rect.centerx - self.rect.width/2, component.rect.centery - self.rect.height/2))
        return self
    
    def set_color(self, color):
        self.color = color


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
            if self.theme.border_radius > 0:
                self.image = pg.Surface(self.rect.size, flags=pg.SRCALPHA)
            else:
                self.image = pg.Surface(self.rect.size)
                
            self._render(self.image)
        else:
            self.has_image = True
            self.image = image
    
    def _render(self, surf, pos=(0,0)):
        pg.draw.rect(surface=surf, 
                    color=self.color, 
                    rect=(pos,self.rect.size),
                    width=0,
                    border_radius=self.theme.border_radius)


    def draw(self, screen) -> None:
        """Draw the image, to the rect on the screen.

        Args:
            screen (Surface | Screen): a surface to draw to.
        """
        if self.draggable and self.drag_rotate and self.dragging:
            mouvement : pg.Vector2 = pg.Vector2(self.rel_pos)
            length = mouvement.length()
            if length > 0:
                mouvement.scale_to_length(clamp(abs(length), 0, 50)/50)
                vec : pg.Vector2 = (0,-1) + mouvement
                _, angle = vec.as_polar()
                angle = (angle + 90) * -1
                rotate_image = pg.transform.rotate(self.image, angle)
                drag_point = (self.rect.topleft + pg.Vector2(self._drag_offset))
                
                origin = rotate_pivot(drag_point, self.image.get_size(), self._drag_offset, angle)
                screen.blit(rotate_image, origin)
                return

        screen.blit(self.image, self.rect)

    def update(self):
        if not self.has_image:
            self._render(self.image)
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
        self.on_hover = empty
        self.on_press = empty
        self.on_focus = empty
        self.on_pre_update = empty
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
        return self


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
        self.on_focus = empty
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
        return self

    def set_text(self, text):
        self.label.set_text(text)
        return self
    
    def center_text(self):
        self.label.center(self)
        return self


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
        self.prev_rect = self.rect.copy()

    def move(self, pos):
        GUIComponent.move(self, pos)
        self.pos_min = self.pos_min[0] + pos[0], self.pos_min[1] + pos[1]
        self.pos_max = self.pos_max[0] + pos[0], self.pos_max[1] + pos[1]
        self.place_slider()
        return self
    
    
    def place_slider(self) -> None:
        self.prev_rect = self.rect.copy()
        if self.pos_min[0] == self.pos_max[0]:
            self.rect.centery = translate(self.value, self.range[0], self.range[1], self.pos_min[1], self.pos_max[1])
        else:
            self.rect.centerx = translate(self.value, self.range[0], self.range[1], self.pos_min[0], self.pos_max[0])
        
    
    def on_drag(self) -> None:
        pos = pg.mouse.get_pos()
        self.prev_rect = self.rect.copy()
        pos_min = self.pos_min
        pos_max = self.pos_max
        self.rect.centerx = clamp(pos[0], pos_min[0], pos_max[0])
        self.rect.centery = clamp(pos[1], pos_min[1], pos_max[1])
        prev = self.value
        if pos_min[0] == pos_max[0]:
            self.value = translate(self.rect.centery, pos_min[1], pos_max[1], self.range[0], self.range[1])
        else:
            self.value = translate(self.rect.centerx, pos_min[0], pos_max[0], self.range[0], self.range[1])
        if prev != self.value:
            self.on_change()
        
        
    def draw(self, screen):
        if isinstance(screen, pg.Surface):
            pg.draw.line(screen, self.theme.default_color, self.pos_min, self.pos_max)
            screen.blit(self.image, self.rect)
        elif isinstance(screen, (SmartScreen, DrawableScreen)):
            if self.prev_rect != self.rect:
                screen.draw_background(self.prev_rect)
            screen.draw_line(self.pos_min, self.pos_max, self.theme.default_color)
            screen.blit(self.image, self.rect)
        else:
            pg.draw.line(screen.surface, self.theme.default_color, self.pos_min, self.pos_max)
            screen.blit(self.image, self.rect)

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
        return self

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
        return self
        
    def set_text(self, text):
        self.text = str(text)
        self.imePos = len(self.text)
        return self
    
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
        return self
    
    def draw(self, screen):
        for child in self.sprites():
            child.draw(screen)

    def move_to(self, pos):
        horizontal_shift = pos[0]-self.rect.x
        vertical_shift = pos[1]-self.rect.y
        self.move((horizontal_shift,vertical_shift))
        return self