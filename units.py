from pygame import Vector2, Rect

class Item:
    def __init__(self):
        self.status = 'alive'

    def kill(self):
        self.status = 'delete'



class Unit(Item):
    def __init__(self, position: Vector2, sizes: Vector2):
        super().__init__()
        self.position = position
        self.sizes = sizes

    def get_rect(self):
        return Rect(*self.position, *self.sizes)
    

    def set_rect(self, new_rect: Rect):
        self.position = Vector2(new_rect.left, new_rect.top)
        self.sizes = Vector2(new_rect.width, new_rect.height)
    

    
class Player(Unit):
    pass


class Paddle(Unit):
    def __init__(self, position: Vector2, sizes: Vector2, scores=1):
        super().__init__(position, sizes)
        self.scores = scores



class Ball(Unit):
    def __init__(self, position: Vector2, radius: int, speed: int, direction: Vector2):
        """position is the center of the circle."""
        sizes = Vector2(2 * radius, 2 * radius)
        self.direction = direction.normalize()
        self.speed = speed
        self.radius = radius
        super().__init__(position, sizes)


    def get_rect(self):
        edge = self.position - self.sizes / 2
        return Rect(*edge, *self.sizes)
    
    def set_rect(self, new_rect):
        self.position = new_rect.center
        self.sizes = Vector2(new_rect.width, new_rect.height)
