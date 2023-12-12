import math
from typing import TYPE_CHECKING

from pygame import Vector2, Rect

from utils import get_normal, get_intersect_area

if TYPE_CHECKING:
    from units import Unit, Player, Ball
    from state import State
    from physic.rect import PhysicRect, DynamicRect



class Command:
    def run(self):
        raise NotImplementedError()
    

class CommandDestroy(Command):
    def __init__(self, obj_list: list["Unit"], state: "State"):
        self.obj_list = obj_list
        self.state = state

    def run(self):
        new_obj = []
        for ob in self.obj_list:
            if ob.status in ['alive', 'immortal']:
                new_obj.append(ob)
        
        self.state.scores += len(self.obj_list) - len(new_obj)
        self.obj_list[:] = new_obj



class CommandPlayerMove(Command):
    def __init__(self, gameState: "State", player: "Player", mouse_pos: Vector2):
        self.player = player
        self.mouser_pos = mouse_pos
        self.gameState = gameState


    # TODO: collision with balls!
    def run(self):
        # old_pos = self.player.center

        # set left and right borders
        indent = self.player.width // 2
        left_border = indent
        right_border = self.gameState.width - indent
        
        new_x = self.mouser_pos.x
        new_x = min(max(left_border, new_x), right_border)

        new_center = Vector2(self.player.center)
        new_center.x = new_x
        self.player.center = new_center



class CommandBallMove(Command):
    def __init__(self, gameState: "State", ball: "Ball", dt: float):
        self.gameState = gameState
        self.ball = ball
        self.dt = dt
        self.player = self.gameState.playerUnit


    def _deprecated_run(self):
        # save old value
        old_ball_center = self.ball.center

        # calc step
        step = self.ball.velocity * self.dt
        step.x, step.y = int(step.x), int(step.y) 

        # 
        self.ball.center += step
        
        ball = self.ball
        player = self.gameState.playerUnit

        if player.colliderect(ball):
            norm = get_normal(ball, player).normalize()
            if norm.y:
                ball.velocity = self.get_pb_velocity(player, ball)
            else:
                ball.velocity -= (2 * norm.elementwise() * ball.velocity) * norm

            old_ball_center = self.ball.center
            return 




        for ob in self.gameState.paddles:
            if ob.colliderect(ball):
                norm = get_normal(ball, ob).normalize()
                ball.velocity -= (2 * norm.elementwise() * ball.velocity) * norm
                ball.center = old_ball_center
                if not ob is player:
                    ob.score -= 1
                break


    @staticmethod
    def get_pb_velocity(player: "Player", ball: "Ball"):
        diff = Vector2(ball.center) - Vector2(player.center)
        alpha = math.pi / 3 * (2 * diff.x) / (player.width + ball.width)
        speed = (ball.velocity* ball.velocity) ** 0.5
        new_velocity = Vector2(math.sin(alpha), -math.cos(alpha)) * speed
        new_velocity.x, new_velocity.y = int(new_velocity.x), int(new_velocity.y)

        print(alpha, diff, new_velocity)
        return new_velocity
    



    def resolve_collision(self, ball: "DynamicRect", static_rect: "PhysicRect", dt: float):
        resp = ball.collide_dynamic_rect(static_rect, dt)
        if not resp.is_hit:
            return
        
        # print(resp, dynamic.vel)
        ball.vel -= 2 * (resp.norm * ball.vel) * resp.norm
    

    def resolve_collision_player(self, ball: "DynamicRect", player: "DynamicRect", dt: float):
        resp = ball.collide_dynamic_rect(player, dt)
        if not resp.is_hit:
            return
        
        nearest_point = resp.contact_points[0]
        coeff = 2 * (nearest_point.x - resp.obstacle.left) / resp.obstacle.width - 1

        alpha = math.pi / 3 * coeff
        speed = (ball.vel * ball.vel) ** 0.5
        new_velocity = Vector2(speed * math.sin(alpha), - speed * math.cos(alpha))
        ball.vel = new_velocity




    def run(self):
        # 1. выбираем кандидатов для столкновения
        candidates = self.choose_candidates()
        
        # 2. Ищем тех, с кем столкнемся через self.dt
        collided = []
        for num, ob in enumerate(candidates):
            result = self.ball.collide_dynamic_rect(ob, self.dt)
            if result.is_hit:
                collided.append((num, result))
        
        if not collided:
            self.ball.center += self.ball.vel * self.dt
            return
        
        # 3. сортируем по порядку столкновения и разрешаем коллизии
        collided.sort(key=lambda x: x[1].t_hit_near)
        num_first = collided[0][0]
        candidates[num_first].kill()

        for ob in collided:
            if candidates[ob[0]] is self.gameState.bottomBorder:
                self.gameState.status = 'lose'
                break
            if candidates[ob[0]] is self.player:
                self.resolve_collision_player(self.ball, self.player, self.dt)
                continue
            self.resolve_collision(self.ball, candidates[ob[0]], self.dt)

        
    
    def choose_candidates(self):
        step = self.ball.vel * self.dt
        step.x, step.y = abs(step.x), abs(step.y)
        extended = self.ball.copy()
        extended.scale_by_ip(2 * step)

        candidates = [ 
            ob for ob in 
            self.gameState.paddles 
            if extended.colliderect(ob)
        ]
        if extended.colliderect(self.player):
            candidates.append(self.player)
        
        return candidates





# class CommandMusic(Command):
#     def __init__(self, sound):
#         self.sound = sound
    
#     def run(self):
#         self.sound.play()




