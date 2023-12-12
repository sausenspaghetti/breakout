from typing import Optional
from pygame import Vector2, Rect


# Base class
class FloatRect:
    _classname = 'FloatRect'
    def __init__(self, left: float, top: float, width: float, height: float):
        self.left = float(left)
        self.top = float(top)
        self.width = float(width)
        self.height = float(height)
    
    @property
    def right(self) -> float:
        return self.left + self.width
    
    @right.setter
    def right(self, value):
        self.left = float(value) - self.width
    

    @property
    def bottom(self) -> float:
        return self.top + self.height
    
    @bottom.setter
    def bottom(self, value: float):
        self.top = float(value) - self.height

    
    @property
    def centerx(self) -> float:
        return self.left + self.width / 2
    
    @centerx.setter
    def centerx(self, value: float):
        self.left = float(value) - self.width / 2


    @property
    def centery(self) -> float:
        return self.top + self.height / 2
    
    @centery.setter
    def centery(self, value: float):
        self.top = float(value) - self.height / 2
        

    @property
    def center(self) -> Vector2:
        return Vector2(self.centerx, self.centery)
    
    @center.setter
    def center(self, value: Vector2):
        value = Vector2(value)
        self.centerx = float(value.x) 
        self.centery = float(value.y)


    @property
    def position(self) -> Vector2:
        return Vector2(self.left, self.top)

    @position.setter
    def position(self, value: Vector2):
        value = Vector2(value)
        self.left = value.x
        self.top = value.y


    @property
    def sizes(self) -> Vector2:
        return Vector2(self.width, self.height)
    
    @sizes.setter
    def sizes(self, value: Vector2):
        value = Vector2(value)
        self.width = float(value.x)
        self.height = float(value.y)


    def scale(self, alpha: float):
        old_center = self.center
        self.width *= alpha
        self.height *= alpha
        self.center = old_center


    def scale_by_ip(self, expand_factor: Vector2):
        old_center = self.center
        self.width += expand_factor.x
        self.height += expand_factor.y
        self.center = old_center


    def get_pyrect(self) -> Rect:
        return Rect(self.left, self.top, self.width, self.height)
    
    def copy(self):
        return type(self)(self.left, self.top, self.width, self.height)
    
    def __str__(self):
        return f'{self._classname}<{self.left}, {self.top}, {self.width}, {self.height}>'
