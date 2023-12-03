from typing import Optional
from pygame import Vector2, Rect

# little helpers
epsilon = 1e-10
sign = lambda x: 1 if x >= 0 else -1 



class CollisionResponce:
    def __init__(
            self, 
            is_hit: bool = False, 
            norm: Optional[Vector2] = None, 
            t_hit_near: Optional[float] = None, 
            contact_points: Optional[list[Vector2]] = None):
        self.is_hit = is_hit
        self.norm = norm
        self.t_hit_near = t_hit_near
        self.contact_points = contact_points

    def __str__(self):
        return 'CollisionResponce<is_hit={}, norm={}, contact_points={}, t_hit_near={}>'.format(
            self.is_hit,
            self.norm,
            self.contact_points,
            self.t_hit_near
        )




class FloatRect:
    _classname = 'FloatRect'
    def __init__(self, left, top, width, height):
        self.left = float(left)
        self.top = float(top)
        self.width = float(width)
        self.height = float(height)
    
    @property
    def right(self):
        return self.left + self.width
    
    @right.setter
    def right(self, value):
        self.left = float(value) - self.width
    

    @property
    def bottom(self):
        return self.top + self.height
    
    @bottom.setter
    def bottom(self, value):
        self.top = float(value) - self.height

    
    @property
    def centerx(self):
        return self.left + self.width / 2
    
    @centerx.setter
    def centerx(self, value):
        self.left = float(value) - self.width / 2


    @property
    def centery(self):
        return self.top + self.height / 2
    
    @centery.setter
    def centery(self, value):
        self.top = float(value) - self.height / 2
        

    @property
    def center(self):
        return Vector2(self.centerx, self.centery)
    
    @center.setter
    def center(self, value):
        value = Vector2(value)
        self.centerx = value.x 
        self.centery = value.y


    @property
    def position(self):
        return Vector2(self.left, self.top)

    @position.setter
    def position(self, value):
        value = Vector2(value)
        self.left = value.x
        self.top = value.y


    @property
    def sizes(self):
        return Vector2(self.width, self.height)
    
    @sizes.setter
    def sizes(self, value):
        value = Vector2(value)
        self.width = value.x
        self.height = value.y


    def scale(self, alpha):
        old_center = self.center
        self.width *= alpha
        self.height *= alpha
        self.center = old_center


    def scale_by_ip(self, expand_factor: Vector2):
        old_center = self.center
        self.width += expand_factor.x
        self.height += expand_factor.y
        self.center = old_center


    def get_pyrect(self):
        return Rect(self.left, self.top, self.width, self.height)
    
    def copy(self):
        return type(self)(self.left, self.top, self.width, self.height)
    
    def __str__(self):
        return f'{self._classname}<{self.left}, {self.top}, {self.width}, {self.height}>'
    


class PhysicRect(FloatRect):
    _classname = 'PhysicRect'

    def colliderect(self, other_rect: "PhysicRect"):
        return all([
            self.left <= other_rect.left <= self.right or \
            other_rect.left <= self.left <= other_rect.right,

            self.top <= other_rect.top <= self.bottom or \
            other_rect.top <= self.top <= other_rect.bottom
        ])
    


    def collidepoint(self, point: Vector2):
        point = Vector2(point)
        return self.left <= point.x <= self.right and \
            self.top <= point.y <= self.bottom
    


    def clipline(self, start: Vector2, end: Vector2):
        """Interesting stuff:
            1) t_hit_near: float
            2) the norm: Vector2
            3) contact points: list[Vector2, Vector2]
            4) is_hit: bool
        """
        end = Vector2(end)
        start = Vector2(start)
        direction = end - start

        result = CollisionResponce()
        # result = {
        #     'is_hit': False,
        #     'norm': None,
        #     'contact_points': None,
        #     't_hit_near': None
        # }

        if abs(direction.x) < epsilon:
            direction.x = epsilon * sign(direction.x)
        if abs(direction.y) < epsilon:
            direction.y = epsilon * sign(direction.y)
    
        
        t_near = (self.position - start).elementwise() / direction
        t_far = (self.position + self.sizes - start).elementwise() / direction

        t_near.x, t_far.x = min(t_near.x, t_far.x), max(t_near.x, t_far.x)
        t_near.y, t_far.y = min(t_near.y, t_far.y), max(t_near.y, t_far.y) 

        if t_near.x > t_far.y or t_near.y > t_far.x:
            return result
        
        t_hit_near = max(t_near.x, t_near.y)
        t_hit_far = min(t_far.x, t_far.y)


        # TODO: добавить корректное условие 
        if t_hit_near < 0 or t_hit_near > 1:
            return result
        
        contact_point_near = start + (end - start) * t_hit_near
        if t_hit_near == t_near.x:
            if direction.x > 0:
                norm = Vector2(-1, 0)
            else:
                norm = Vector2(1, 0)
        elif t_hit_near == t_near.y:
            if direction.y > 0:
                norm = Vector2(0, -1)
            else:
                norm = Vector2(0, 1)

        result.is_hit = True
        result.norm = norm
        result.t_hit_near = t_hit_near

        if t_hit_far >= 1:
            contact_point_far = end
        else:
            contact_point_far = start + (end - start) * t_hit_far

        result.contact_points = [contact_point_near, contact_point_far]        
        return result




class DynamicRect(PhysicRect):
    _classname = 'DynamicRect'
    def __init__(self, left, top, width, height, vel: Vector2 = None):
        super().__init__(left, top, width, height)
        if not vel:
            vel = Vector2(0.0, 0.0)
        self.vel = vel


    def collide_dynamic_rect(self, other_rect: "PhysicRect", time_stop: float):
        if abs(self.vel.x) < epsilon and abs(self.vel.y) < epsilon:
            return CollisionResponce()
        
        expanded_rect = other_rect.copy()
        expanded_rect.scale_by_ip(self.sizes)

        step = self.vel * time_stop
        end_p = self.center + step

        result = expanded_rect.clipline(self.center, end_p)

        return result


