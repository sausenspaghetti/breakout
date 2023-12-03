import pygame
from pygame import Vector2, Rect

from physic_rect import DynamicRect, PhysicRect


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30


# general stuffs
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dynamic Rect tests")
clock = pygame.time.Clock()


player = DynamicRect(30, 30, 0, 0)
player.width, player.height = 50, 30


dt = clock.tick(FPS) * 1000
run = True

one_obstacle = PhysicRect(100, 200, 150, 200)
one_obstacle.center  = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

while run:
    clicked = False
    mousePos = Vector2(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.center = mousePos
            

    velocity = (mousePos - player.center)
    player.vel = velocity


    res = player.collide_dynamic_rect(one_obstacle, dt)
    if res.is_hit:
        player.center += player.vel * res.t_hit_near * dt
        player.vel -= Vector2((res.norm * player.vel) * res.norm)
        player.center += player.vel * (1 - res.t_hit_near) * dt
    else:
        player.center += player.vel * dt


    screen.fill('grey')
    
    pygame.draw.rect(screen, 'blue', one_obstacle.get_pyrect(), width=3)
    pygame.draw.rect(screen, 'green', player.get_pyrect(), width=3)
    

    pygame.display.flip()
    dt = clock.tick(FPS) * 1/1000


pygame.quit()


