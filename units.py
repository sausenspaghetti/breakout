from pygame import Rect, Vector2
# import pygame

from physic.rect import DynamicRect, PhysicRect


class Item:
    def __init__(self):
        self.status = 'alive'

    def kill(self):
        if self.status != 'immortal':
            self.status = 'delete'

    def set_immortal(self):
        self.status = 'immortal'



class Unit(Item, DynamicRect):
    _classname = 'Unit'
    def __init__(self, left: float, top: float, width: float, height: float):
        super().__init__()        # Item.__init__
        super(Item, self).__init__(float(left), float(top), float(width), float(height))   # RhysicRect.__init__



class Ball(Unit):
    _classname = 'Ball'
    def __init__(self, position: Vector2, radius: int, velocity: Vector2):
        self.velocity = Vector2(velocity)
        position =Vector2(position)
        super().__init__(float(position.x), float(position.y), int(radius), int(radius))


    @property
    def radius(self):
        return (self.width + self.height) // 4
    

    @radius.setter
    def set_radius(self, value):
        self.width = self.height = 2 * int(value)
    



class Paddle(Unit):
    _classname = 'Paddle'
    def __init__(self, left: float, top: float, width: float, height: float, score: int=1):
        super().__init__(left, top, width, height)
        self._score = score


    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if self.status == 'immortal':
            return
        self._score =  max(0, int(value))
        if self._score == 0:
            self.kill()

    def set_immortal(self):
        super().set_immortal()
        self._score = -1



class Player(Unit):
    _classname = 'Player'
    def __init__(self, left: float, top: float, width: float, height: float):
        super().__init__(left, top, width, height)
        self.set_immortal()



if __name__ == '__main__':
    # print(Player.mro())
    u = Unit(1, 1, 1, 1)
    pp = Player(1, 2, 3, 4)
    p = Paddle(1, 2, 3, 4)
    b = Ball((1, 2), 5, (1,1))
    print(u)
    print(p)
    print(pp)
    print(b)