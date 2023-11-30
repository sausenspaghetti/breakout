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

        # # player
        # p_width, p_height = self.width // 6, self.height // 40
        # self.playerUnit = Player(
        #     sizes=Vector2(p_width, p_height),
        #     position=Vector2(self.width // 2, self.height * 0.8) - Vector2(p_width, p_height) // 2
        # )

        # ball
        self.ballUnit = Ball(
            position=Vector2(self.width / 2, self.height / 2),
            radius=10,
            velocity=Vector2(50, 50)
        )

        # paddles 
        upperBorder = Paddle(0, 0, self.width, 20)
        upperBorder.bottomleft = Vector2(0, 0)
        upperBorder.set_immortal()

        bottomBorder = Paddle(0, 0, self.width, 20)
        bottomBorder.topleft = Vector2(0, self.height)
        bottomBorder.set_immortal()

        leftBorder = Paddle(0, 0, 20, self.height)
        leftBorder.topright = Vector2(0, 0)
        leftBorder.set_immortal()


        rightBorder = Paddle(0, 0, 20, self.height)
        rightBorder.topleft = Vector2(self.width, 0)
        print(rightBorder)  # <rect(0, 475, 20, 360)>
        # Rect()
        rightBorder.set_immortal()

        # read level <-- ??


        self.paddles: list[Rect] = [
            upperBorder, bottomBorder, leftBorder, rightBorder
        ]

        field = self.generate_random_field()
        for x in range(config.N_X):
            for y in range(config.N_Y):
                if field[x][y]:
                    new_block = Paddle(
                        x * config.STEP_X, 
                        y * config.STEP_Y, 
                        config.STEP_X, 
                        config.STEP_Y)
                    new_block.set_immortal()
                    self.paddles.append(new_block)



    @staticmethod
    def generate_random_field():
        field = [[0,] * config.N_Y for x in range(config.N_X)]
        for x in range(config.N_X):
            for y in range(config.N_Y):
                field[x][y] = 1 if random.random() > 0.8 else 0

        
        return field
