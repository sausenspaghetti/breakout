from typing import Optional
from pygame import Vector2, Rect

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .physic_rect import PhysicRect


class CollisionResponce:
    def __init__(
            self, 
            is_hit: bool = False, 
            norm: Optional[Vector2] = None, 
            t_hit_near: Optional[float] = None, 
            contact_points: Optional[list[Vector2]] = None,
            obstacle: "PhysicRect" = None):
        self.is_hit = is_hit
        self.norm = norm
        self.t_hit_near = t_hit_near
        self.contact_points = contact_points
        self.obstacle = obstacle

    def __str__(self):
        return 'CollisionResponce<is_hit={}, norm={}, contact_points={}, t_hit_near={}, obstacle={}>'.format(
            self.is_hit,
            self.norm,
            self.contact_points,
            self.t_hit_near,
            self.obstacle
        )
