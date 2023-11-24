from pygame import Vector2, Rect

from units import Unit, Player, Ball, Paddle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Game


class State:
    def __init__(self, game: "Game"):
        self.screen = game.screen
        self.size = game.screen.get_size()
        self.width, self.height = self.size

        # player
        p_width, p_height = self.width // 6, self.height // 40
        self.playerUnit = Player(
            sizes=Vector2(p_width, p_height),
            position=Vector2(self.width // 2, self.height * 0.8) - Vector2(p_width, p_height) // 2
        )

        # ball
        self.ballUnit = Ball(
            position=Vector2(self.width / 2, self.height / 2),
            radius=10,
            speed=5,
            direction=Vector2(1, -1).normalize()
        )

        # paddles 
        self.paddles = []

    
    def update(self, playerPosX: int):
        # player is not out of screen
        new_player = self.playerUnit.get_rect()
        new_player.centerx = playerPosX
        if self.is_inside(new_player):
            self.playerUnit.set_rect(new_player)

        # ball
        # set new ball's position
        ball = self.ballUnit
        newBallRect = ball.get_rect()
        newBallPos = ball.position + ball.direction * ball.speed
        newBallRect.center = newBallPos

        # check collision
        coeff = Vector2(1, 1)
        coeff = coeff.elementwise() * self.board_direction(newBallRect, ball.direction)
        coeff = coeff.elementwise() * self.collision_direction(newBallRect, self.playerUnit.get_rect())
        if coeff != Vector2(1, 1):
            self.ballUnit.direction = (ball.direction.elementwise() * coeff).normalize()
        else:
            self.ballUnit.position = newBallPos


    def update_new(self, playerPosX: int):
        pass
        
    def is_inside(self, obj: Rect):
        return all([
            obj.top >= 0,
            obj.bottom <= self.height,
            obj.left >= 0,
            obj.right <= self.width
        ])
    
    def board_direction(self, obj: Rect, direction):
        coeff = Vector2(1, 1)

        if obj.top <= 0 and direction.y < 0:
            coeff.y *= -1
        if obj.bottom >= self.height and direction.y > 0:
            coeff.y *= -1
        if obj.left <= 0 and direction.x < 0:
            coeff.x *= -1
        if obj.right >= self.width and direction.x > 0:
            coeff.x *= -1

        return coeff


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