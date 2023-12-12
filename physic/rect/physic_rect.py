from typing import Optional
from pygame import Vector2, Rect

from .float_rect import FloatRect
from .collision_responce import CollisionResponce


# little helpers
epsilon = 1e-10
sign = lambda x: 1 if x >= 0 else -1 



class PhysicRect(FloatRect):
    _classname = 'PhysicRect'

    def copy(self):
        return PhysicRect(self.left, self.top, self.width, self.height)


    def colliderect(self, other_rect: "PhysicRect") -> bool:
        return all([
            self.left <= other_rect.left <= self.right or \
            other_rect.left <= self.left <= other_rect.right,

            self.top <= other_rect.top <= self.bottom or \
            other_rect.top <= self.top <= other_rect.bottom
        ])
    


    def collidepoint(self, point: Vector2) -> bool:
        point = Vector2(point)
        return self.left <= point.x <= self.right and \
            self.top <= point.y <= self.bottom
    


    def clipline(self, start: Vector2, end: Vector2) -> "CollisionResponce":
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
        result.obstacle = self

        return result

