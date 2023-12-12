from typing import Optional
from pygame import Vector2, Rect


from .physic_rect import PhysicRect
from .collision_responce import CollisionResponce


# little helpers
epsilon = 1e-10
sign = lambda x: 1 if x >= 0 else -1 




class DynamicRect(PhysicRect):
    _classname = 'DynamicRect'
    def __init__(self, left: float, top: float, width: float, height: float, vel: Vector2 = None):
        super().__init__(left, top, width, height)
        if not vel:
            vel = Vector2(0.0, 0.0)
        self.vel = vel


    def collide_dynamic_rect(self, other_rect: "PhysicRect", time_stop: float) -> "CollisionResponce":
        if abs(self.vel.x) < epsilon and abs(self.vel.y) < epsilon:
            return CollisionResponce()
        
        expanded_rect = other_rect.copy()
        expanded_rect.scale_by_ip(self.sizes)

        step = self.vel * time_stop
        end_p = self.center + step

        result = expanded_rect.clipline(self.center, end_p)

        return result
    