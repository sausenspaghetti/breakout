import random

import pygame
from pygame import Vector2, Rect

from ..rect import DynamicRect, PhysicRect


def main():
    epsilon = 1e-10

    pygame.init()

    SCREEN_WIDTH = 800  # 20 * 40
    SCREEN_HEIGHT = 600 # 15 * 40
    STEP = 40

    N_X = SCREEN_WIDTH // STEP
    N_Y = SCREEN_HEIGHT // STEP

    FPS = 60




    # general stuffs
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dynamic Rect tests")
    clock = pygame.time.Clock()


    player = DynamicRect(30, 30, 0, 0)
    player.width, player.height = 15, 15
    player.vel = Vector2(-200, -200)





    left_border = PhysicRect(-20, 0, 20, SCREEN_HEIGHT)
    right_border = PhysicRect(SCREEN_WIDTH, 0, 20, SCREEN_HEIGHT)
    top_border = PhysicRect(-20, -20, SCREEN_WIDTH + 40, 20)
    bottom_border = PhysicRect(-20, SCREEN_HEIGHT, SCREEN_WIDTH + 40, 20)


    obstacles = [
        left_border,
        right_border,
        top_border,
        bottom_border,
    ]

    for j in range(30):
        x = random.randint(0, N_X)
        y = random.randint(0, N_Y)
        obstacles.append(PhysicRect(x * STEP, y * STEP, 40, 40))


    def resolve_collision(dynamic: DynamicRect, static_rect: PhysicRect, dt: float):
        resp = dynamic.collide_dynamic_rect(static_rect, dt)
        if not resp.is_hit:
            return
        
        print(resp, dynamic.vel)

        dynamic.vel -= 2 * (resp.norm * dynamic.vel) * resp.norm



    dt = clock.tick(FPS) / 1000
    run = True
    while run:
        clicked = False
        mousePos = Vector2(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player.center = mousePos
                


        step = player.vel * dt
        step.x, step.y = abs(step.x), abs(step.y)
        extended = player.copy()
        extended.scale_by_ip(2 * step)

        candidates = [ob for ob in obstacles if extended.colliderect(ob)]

        collided = []
        for num, ob in enumerate(candidates):
            result = player.collide_dynamic_rect(ob, dt)
            if result.is_hit:
                collided.append((num, result))
        
        if not collided:
            player.position += player.vel * dt
        else:
            # resolve all
            collided.sort(key=lambda x: x[1].t_hit_near)
            for ob in collided:
                resolve_collision(player, candidates[ob[0]], dt)


        screen.fill('black')
        # pygame.draw.rect(screen, 'green', player.get_pyrect())
        p_rect = player.get_pyrect()
        pygame.draw.circle(screen, 'red', p_rect.center, p_rect.width // 2)
        
        for ob in obstacles:
            pygame.draw.rect(screen, 'blue', ob.get_pyrect())


        pygame.display.flip()
        dt = clock.tick(FPS) * 1/1000


    pygame.quit()


