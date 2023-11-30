from pygame import Vector2, Rect

from typing import TYPE_CHECKING

from utils import get_normal

if TYPE_CHECKING:
    from units import Unit, Player, Ball
    from state import State



class Command:
    def run(self):
        raise NotImplementedError()
    

class CommandDestroy(Command):
    def __init__(self, obj_list: list["Unit"]):
        self.obj_list = obj_list

    def run(self):
        new_obj = []
        for ob in self.obj_list:
            if ob.status in ['alive', 'immortal']:
                new_obj.append(ob)
        
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

        # if self.gameState.is_inside(self.player):

        # TODO - balls ????



class CommandBallMove(Command):
    def __init__(self, gameState: "State", ball: "Ball", dt: float):
        self.gameState = gameState
        self.ball = ball
        self.dt = dt

    
    def run(self):
        # save old value
        old_ball_center = self.ball.center

        # calc step
        step = self.ball.velocity * self.dt
        step.x, step.y = int(step.x), int(step.y) 

        # 
        self.ball.center += step
        
        player = self.gameState.playerUnit

        norm_set = set()
        for ob in [*self.gameState.paddles, player]:
            if ob.colliderect(self.ball):
                norm = get_normal(self.ball, ob).normalize()
                self.ball.velocity -= (2 * norm.elementwise() * self.ball.velocity) * norm
                self.ball.center = old_ball_center
                if not ob is player:
                    ob.score -= 1
                break
                # norm_set.add(norm)
        

        # if not norm_set:
        #     return


        # self.ball.center = old_ball_center

        # final_norm: Vector2 = self._resolve_norm(step, norm_set)
        # self.ball.velocity -= 2 * final_norm.elementwise() * self.ball.velocity



    @staticmethod
    def _resolve_norm(step, norm_set) ->Vector2:
        all_x = set(map(lambda norm: norm.x, norm_set))
        all_y = set(map(lambda norm: norm.y, norm_set))
        all_x.discard(0)
        all_y.discard(0)
        return Vector2(0, 0)



