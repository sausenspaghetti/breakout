import random

from pygame import Vector2, Rect
from pygame import Vector2, Rect

from units import Unit, Player, Ball, Paddle
import config

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
        p_pos = Vector2(self.width // 2, self.height * 0.8) - Vector2(p_width, p_height) // 2
        self.playerUnit = Player(
            p_pos.x, p_pos.y,
            p_width, p_height
        )

        # ball
        velocity = Vector2(0.5, -1.5).normalize() * config.SPEED
        velocity.x, velocity.y =  int(velocity.x), int(velocity.y)
        self.ballUnit = Ball(
            position=Vector2(self.width / 2, self.height / 2),
            radius=10,
            velocity=velocity
        )

        # paddles 
        upperBorder = Paddle(-100, -100, self.width + 200, 100)
        upperBorder.set_immortal()

        bottomBorder = Paddle(-100, self.height, self.width, 100)
        bottomBorder.set_immortal()

        leftBorder = Paddle(-100, 0, 100, self.height)
        leftBorder.set_immortal()


        rightBorder = Paddle(self.width, 0, 100, self.height)
        rightBorder.set_immortal()

        # read level <-- ??


        self.paddles: list[Paddle] = [
            upperBorder, bottomBorder, leftBorder, rightBorder
        ]

        field = self.generate_random_field()
        for x in range(config.N_X):
            for y in range(config.N_Y):
                if field[x][y]:
                    new_block = Paddle(
                        x * config.STEP_X + 5, 
                        y * config.STEP_Y + 5, 
                        config.STEP_X - 10, 
                        config.STEP_Y - 10,
                        score=1)
                    # new_block.set_immortal()
                    self.paddles.append(new_block)



    @staticmethod
    def generate_random_field():
        field = [[0,] * config.N_Y for x in range(config.N_X)]
        for x in range(config.N_X):
            for y in range(config.N_Y // 2):
                field[x][y] = 1 if random.random() > 0.5 else 0

        
        return field
