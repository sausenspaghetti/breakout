import pygame
from pygame import Vector2, Rect


from state import State

FPS = 60


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
        pygame.draw.circle(self.screen, 'lime', self.state.ballUnit.position, self.state.ballUnit.radius)
        print(self.state.ballUnit.position, self.state.ballUnit.radius)
        pygame.display.update()



    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.dt = self.clock.tick(FPS)



if __name__ == '__main__':
    g = Game()
    g.run()
