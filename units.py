from pygame import Rect, Vector2
# import pygame


class Item:
    def __init__(self):
        self.status = 'alive'

    def kill(self):
        if self.status != 'immortal':
            self.status = 'delete'

    def set_immortal(self):
        self.status = 'immortal'



class Unit(Rect, Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # Rect.__init__
        super(Rect, self).__init__()        # Item.__init__


    # def render(self, screen):
    #     raise NotImplementedError()
    



class Ball(Unit):
    def __init__(self, position: Vector2, radius: int, velocity: Vector2):
        self.velocity = velocity
        super().__init__(position, (int(radius), int(radius)))


    # def render(self, screen):
    #     pygame.draw.circle(screen, 'green', self.center, self.radius)
        

    @property
    def radius(self):
        return (self.width + self.height) // 4
    

    @radius.setter
    def set_radius(self, value):
        self.width = self.height = 2 * int(value)




class Paddle(Unit):
    def __init__(self, *args, **kwargs):
        score = 1
        if 'score' in kwargs:
            score = kwargs['score']
            kwargs.pop('score')
        self._score = score
        super().__init__(*args, **kwargs)


    # def render(self, screen):
    #     pygame.draw.rect(screen, 'white', self)

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
    pass
    # def render(self, screen):
    #     pygame.draw.rect(screen, 'white', self)

