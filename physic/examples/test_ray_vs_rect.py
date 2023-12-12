import pygame
from pygame import Vector2

from ..physic_rect import PhysicRect


def main():
    pygame.init()

    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    FPS = 60

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Collision")
    clock = pygame.time.Clock()


    obstacles: list[PhysicRect] = [
        PhysicRect(100, 200, 80, 50),
        PhysicRect(280, 150, 20, 110),
        PhysicRect(400, 50, 40, 40),
        PhysicRect(500, 290, 70, 90),
    ]

    start_p = Vector2(0, 0)
    end_p = Vector2(0, 0)


    dt = clock.tick(FPS)
    run = True
    while run:
        end_p = Vector2(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                start_p = end_p
        
        
        screen.fill('grey')
        for num, ob in enumerate(obstacles):
            result = ob.clipline(start_p, end_p)  
            if result.is_hit:
                norm = result.norm
                contact_point_near, contact_point_far = result.contact_points
                pygame.draw.line(screen, '#FFFF66',  contact_point_near,  contact_point_near + 20 * norm, width=2)
                pygame.draw.circle(screen,  '#FF3399',  contact_point_near, 4)
                pygame.draw.circle(screen,  '#FF3399',  contact_point_far, 4)
                pygame.draw.rect(screen, '#33FF99', ob.get_pyrect())
            else:
                pygame.draw.rect(screen, 'blue', ob.get_pyrect())


        pygame.draw.line(screen, 'black', start_p, end_p, width=2)
        
        pygame.display.flip()
        dt = clock.tick(FPS) * 1/1000

    pygame.quit()

