import pygame
from pygame import Vector2, Rect


from state import State
from commands import CommandBallMove

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
        self.dt = self.clock.tick(config.FPS) / 1000


    def processInput(self):
        self.mode_move = True
        self.mousePos = Vector2(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_m:
                    self.mode_move = not self.mode_move
                if event.key == pygame.K_s:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode_move:
                    vel = -(self.state.ballUnit.center - self.mousePos).normalize() * 50
                    vel.x, vel.y = int(vel.x), int(vel.y)
                    self.state.ballUnit.velocity = vel
                else:
                    self.state.ballUnit.center = self.mousePos

        self.commands.append(
            CommandBallMove(self.state, self.state.ballUnit, self.dt)
        )

    
    def update(self):
        for cmd in self.commands:
            cmd.run()

        self.commands.clear()
        # self.state.update(self.mousePos.x)


    def render(self):
        self.screen.fill('black')
        for paddle in self.state.paddles:
            pygame.draw.rect(self.screen, 'medium spring green', paddle)
        
        ball = self.state.ballUnit
        pygame.draw.circle(self.screen, 'red', ball.center, ball.radius)


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
