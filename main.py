import pygame
from os.path import join
from pygame import Vector2, Rect


from state import State
from commands import CommandBallMove, CommandDestroy, CommandPlayerMove

import config

FPS = 60



class Game:

    def __init__(self):
        pygame.init()

        pygame.display.set_caption('best game ever')
        self.main_screen = pygame.display.set_mode((config.MAIN_WIDTH, config.MAIN_HEIGHT))
        self.screen = pygame.Surface((config.WIDTH, config.HEIGHT))
        self.screen_pos = (config.BORDERS['BORDER_FRAME_BARELL'], config.BORDERS['BORDER_FRAME_TOP'])


        self.font = pygame.font.Font(join('font', 'big-shot.ttf'), 20)


        self.state = State(self)

        self.running = True
        self.clock = pygame.time.Clock()
        self.mousePos = Vector2(0, 0)

        self.commands = []
        self.pause = False
        self.dt = self.clock.tick(config.FPS) / 1000
        
        self.score = 0



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
                CommandDestroy(self.state.paddles, self.state)
            )

    
    def update(self):
        for cmd in self.commands:
            cmd.run()

        self.commands.clear()


    def draw_frame_borders(self):
        sizes = self.screen.get_size()
        top_left = self.screen_pos
        top_right = (sizes[0] + self.screen_pos[0], self.screen_pos[1])
        bottom_left = (self.screen_pos[0], self.screen_pos[1] + sizes[1]) #(0, sizes[1])
        bottom_right = (sizes[0] + self.screen_pos[0], self.screen_pos[1] + sizes[1]) 

        pygame.draw.line(self.main_screen, 'white', top_left, top_right, width=3)
        pygame.draw.line(self.main_screen, 'white', bottom_right, bottom_left, width=3)
        pygame.draw.line(self.main_screen, 'white', top_left, bottom_left, width=3)
        pygame.draw.line(self.main_screen, 'white', top_right, bottom_right, width=3)

    def draw_score(self):
        text = f'Scores: {str(self.state.scores).zfill(3)}'

        textSurface = self.font.render(text, False, 'lime')
        textRect = textSurface.get_rect()
        textRect.centerx = self.main_screen.get_width() // 2
        textRect.top = 10

        self.main_screen.blit(textSurface, textRect)
        


    def render(self):
        # render game screen
        self.screen.fill('black')
        for paddle in self.state.paddles:
            color = config.PADDLE_COLORS.get(paddle.score) or 'yellow'
            pygame.draw.rect(self.screen, color, paddle.get_pyrect())
        
        ball = self.state.ballUnit
        player = self.state.playerUnit
        pygame.draw.circle(self.screen, 'white', ball.center, ball.radius)
        pygame.draw.rect(self.screen, 'white', player.get_pyrect())


        self.main_screen.fill('black')
        self.main_screen.blit(self.screen, self.screen_pos)
        self.draw_score()
        self.draw_frame_borders()

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
