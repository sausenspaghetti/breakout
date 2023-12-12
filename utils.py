from pygame import Vector2, Rect

from units import Unit, Ball, Paddle, Player



def get_intersect_area(a: Rect, b: Rect):
    if not a.colliderect(b):
        return 0, 0, Vector2(0, 0)
    
    diff = Vector2(a.center) - Vector2(b.center)
    height_inter = (a.height + b.height) // 2 - abs(diff.y)
    height_inter = min(height_inter, a.height, b.height)

    width_inter = (a.width + b.width) // 2 - abs(diff.x)
    width_inter = min(width_inter, a.width, b.width)

    return width_inter, height_inter, diff



def get_normal(a: Rect, b: Rect, intersect_info=None):
    if not intersect_info:
        intersect_info = get_intersect_area(a, b)
    
    width_inter, height_inter, diff = intersect_info

    flag_x = (width_inter <= height_inter)
    flag_y = (width_inter >= height_inter)
    sign_x = 1 if diff.x > 0 else -1
    sign_y = 1 if diff.y > 0 else -1
    return Vector2(0, 1) * sign_y * flag_y  +  Vector2(1, 0) * sign_x * flag_x
