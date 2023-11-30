import pygame
from pygame import Vector2, Rect


from state import State
from commands import CommandBallMove, CommandDestroy, CommandPlayerMove

import config

FPS = 60


class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption('best game ever')
        self.screen = pygame.display.set_mode((config.HEIGHT, config.WIDTH))

        self.state = State(self)

        self.running = True
        self.clock = pygame.time.Clock()
        self.mousePos = Vector2(0, 0)

        self.commands = []
        self.pause = False
        self.dt = self.clock.tick(config.FPS) / 1000


    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause = not self.pause

        if not self.pause:
            self.mode_move = True
            mousePos = Vector2(pygame.mouse.get_pos())
            mousePos.x, mousePos.y = int(mousePos.x), int(mousePos.y)
            if mousePos != self.mousePos:
                self.mousePos = mousePos
                self.commands.append(
                    CommandPlayerMove(self.state, self.state.playerUnit, self.mousePos)
                )

            self.commands.append(
                CommandBallMove(self.state, self.state.ballUnit, self.dt)
            )
            self.commands.append(
                CommandDestroy(self.state.paddles)
            )

    
    def update(self):
        for cmd in self.commands:
            cmd.run()

        self.commands.clear()
        # self.state.update(self.mousePos.x)


    def render(self):
        self.screen.fill('black')
        for paddle in self.state.paddles:
            color = config.PADDLE_COLORS.get(paddle.score)
            if not color:
                color = 'yellow'
            pygame.draw.rect(self.screen, color, paddle)
        
        ball = self.state.ballUnit
        player = self.state.playerUnit
        pygame.draw.circle(self.screen, 'white', ball.center, ball.radius)
        pygame.draw.rect(self.screen, 'white', player)

        # pygame.draw.rect(self.screen, 'white', self.state.playerUnit.get_rect())
        # pygame.draw.circle(self.screen, 'lime', self.state.ballUnit.position, self.state.ballUnit.radius)
        # print(self.state.ballUnit.position, self.state.ballUnit.radius)
        pygame.display.update()



    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(config.FPS) / 1000



if __name__ == '__main__':
    g = Game()
    g.run()
