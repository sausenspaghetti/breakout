from pygame import Vector2, Rect

from units import Unit, Ball, Paddle, Player


def get_normal(a: Rect, b: Rect):
    if not a.colliderect(b):
        return Vector2(0, 0)
    
    diff = Vector2(a.center) - Vector2(b.center)
    height_inter = (a.height + b.height) // 2 - abs(diff.y)
    height_inter = min(height_inter, a.height, b.height)

    width_inter = (a.width + b.width) // 2 - abs(diff.x)
    width_inter = min(width_inter, a.width, b.width)

    # if width_inter > height_inter:
    #     sign_y = 1 if diff.y > 0 else -1
    #     return Vector2(0, 1) * sign_y
    # elif width_inter < height_inter:
    #     sign_x = 1 if diff.x > 0 else -1
    #     return Vector2(1, 0) * sign_x
    # else:
    #     sign_y = 1 if diff.y > 0 else -1
    #     sign_x = 1 if diff.x > 0 else -1
    #     return Vector2(sign_x, sign_y)
    

    flag_x = (width_inter <= height_inter)
    flag_y = (width_inter >= height_inter)
    sign_x = 1 if diff.x > 0 else -1
    sign_y = 1 if diff.y > 0 else -1
    return Vector2(0, 1) * sign_y * flag_y  +  Vector2(1, 0) * sign_x * flag_x



# collisions --> ball VS rect

