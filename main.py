import pygame
from pygame import Vector2, Rect


FPS = 60




class Unit:
    def __init__(self, position: Vector2, sizes: Vector2):
        self.position = position
        self.sizes = sizes

    def get_rect(self):
        return Rect(*self.position, *self.sizes)
    

    def set_rect(self, new_rect: Rect):
        self.position = Vector2(new_rect.left, new_rect.top)
        self.sizes = Vector2(new_rect.width, new_rect.height)
    

    
class Player(Unit):
    # def __init__(self, position: Vector2, sizes: Vector2):
    #     super().__init__(position, sizes)
    pass
     


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

    



class State:
    def __init__(self, game: "Game"):
        self.screen = game.screen
        self.size = game.screen.get_size()
        self.width = self.size[0]
        self.height = self.size[1]

        # player
        p_width, p_height = self.width // 6, self.height // 40
        self.playerUnit = Player(
            sizes=Vector2(p_width, p_height),
            position=Vector2(self.width / 2, self.height * 0.8) - Vector2(p_width, p_height) // 2
        )

        # ball
        self.ball_pos = Vector2(self.width // 2, self.height // 2)
        self.ball_radius = 10
        self.ball_rect = Rect(0, 0, 0, 0)
        self.ball_rect.center = self.ball_pos
        self.ball_rect.width = self.ball_rect.height = self.ball_radius * 2
        self.ball_speed = 5
        self.ball_direction = Vector2(1, -1).normalize()


        self.ballUnit = Ball(
            position=Vector2(self.width / 2, self.height / 2),
            radius=10,
            speed=5,
            direction=Vector2(1, -1).normalize()
        )

    
    def update(self, playerPosX: int):
        # player is not out of screen
        new_player = self.playerUnit.get_rect()
        new_player.centerx = playerPosX
        if self.is_inside(new_player):
            self.playerUnit.set_rect(new_player)



        # ball
        # newBallRect = Rect(self.ball_rect)
        ball = self.ballUnit
        newBallRect = ball.get_rect()
        newBallPos = ball.position + ball.direction * ball.speed
        # newBallPos.x, newBallPos.y = int(newBallPos.x), int(newBallPos.y)  
        newBallRect.center = newBallPos

        if self.is_collided(newBallRect, self.playerUnit.get_rect()):
            print('sus')

        coeff = Vector2(1, 1)
        coeff = coeff.elementwise() * self.board_direction(newBallRect)
        coeff = coeff.elementwise() * self.collision_direction(newBallRect, self.playerUnit.get_rect())
        # print(coeff, self.ball_direction)
        if coeff != Vector2(1, 1):
            # self.ball_direction = (self.ball_direction.elementwise() * coeff).normalize()
            self.ballUnit.direction = (ball.direction.elementwise() * coeff).normalize()
        else:
            # self.ball_pos = newBallPos
            # self.ball_rect = newBallRect
            self.ballUnit.position = newBallPos

        


    def is_inside(self, obj: Rect):
        return all([
            obj.top >= 0,
            obj.bottom <= self.height,
            obj.left >= 0,
            obj.right <= self.width
        ])
    
    def board_direction(self, obj: Rect):
        direction = Vector2(1, 1)

        if not obj.top >= 0 or not obj.bottom <= self.height:
            direction.y *= -1
        if not obj.left >= 0 or not obj.right <= self.width:
            direction.x *= -1

        return direction


    # TODO: check later
    def is_collided(self, a: Rect, b: Rect):
        return all([
                any([
                    a.left <= b.left <= a.right, 
                    b.left <= a.right <= b.right
                ]),
                any([
                    a.top <= b.top <= a.bottom, 
                    b.top <= a.top <= b.bottom
                ])
            ])
    

    def collision_direction(self, a: Rect, b: Rect):
        diff = Vector2(a.center) - Vector2(b.center)
        del_h = (a.height + b.height) / 2 - abs(diff.y)
        del_w = (a.width + b.width) / 2 - abs(diff.x)

        del_h = min(a.height, b.height, del_h)
        del_w = min(a.width, b.width, del_w)

        coeff = Vector2(1, 1)
        # if there is collision.
        if del_h >= 0 and del_w >= 0:
            if del_h > del_w:
                coeff = Vector2(-1, 1)
            elif del_h < del_w:
                coeff = Vector2(1, -1)
            else:
                coeff = Vector2(-1, -1)
        
        return coeff




class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption('best game ever')
        self.screen = pygame.display.set_mode((480, 360))

        self.state = State(self)

        self.running = True
        self.clock = pygame.time.Clock()
        self.mousePos = Vector2(0, 0)


    def processInput(self):
        self.mousePos = Vector2(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    
    def update(self):
        self.state.update(self.mousePos.x)


    def render(self):
        self.screen.fill('black')
        pygame.draw.rect(self.screen, 'white', self.state.playerUnit.get_rect())
        # pygame.draw.rect(self.screen, 'red', self.state.ball_rect)
        pygame.draw.circle(self.screen, 'lime', self.state.ballUnit.position, self.state.ballUnit.radius)

        pygame.display.update()



    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            dt = self.clock.tick(FPS)
        



if __name__ == '__main__':
    g = Game()
    g.run()
