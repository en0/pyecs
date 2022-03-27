import pygame
from random import uniform
from pyecs.typing import ISystem, IEntityManager
from ..components import flags, queries, PaddleControl, Ballistic, Transform, AiController
from ..components import CircleSprite, Temporial, RectSprite
from ..constants import SCREEN_HEIGHT


DETECT = 0
WAIT = 1
PREDICT = 2
MOVE = 3


class AiSystem(ISystem):

    def update(self, frame_delta):
        for entity in self.em.get_entities(queries.NPC_PADDLE):

            ai: AiController = entity[flags.AI_CONTROLLER]
            ball = self.em.get_entity(ai.target)
            if ball is None or ball[flags.BALLISTIC].force.x < 0:
                ai.phase = DETECT

            if ai.phase == DETECT:
                self.update_detect(entity)
            if ai.phase == WAIT:
                self.update_wait(entity)
            if ai.phase == PREDICT:
                self.update_predict(entity)
            if ai.phase == MOVE:
                self.update_move(entity)


    def update_detect(self, entity):
        ai: AiController = entity[flags.AI_CONTROLLER]
        ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]

        ctrl.moving_down = False
        ctrl.moving_up = False

        poi, dist = None, 0
        for ball in self.em.get_entities(queries.BALL):
            _xfr: Transform = ball[flags.TRANSFORM]
            _mov: Ballistic = ball[flags.BALLISTIC]
            if _mov.force.x > 0:
                if _xfr.position.x > dist:
                    dist = _xfr.position.x
                    poi = ball.identity
        if not poi:
            return

        ai.phase = WAIT
        ai.wait_until = pygame.time.get_ticks() + ai.reaction_time
        ai.target = poi

    def update_wait(self, entity):
        ai: AiController = entity[flags.AI_CONTROLLER]
        ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]
        if ai.wait_until <= pygame.time.get_ticks():
            ai.phase = PREDICT

    def update_predict(self, entity):
        ai: AiController = entity[flags.AI_CONTROLLER]
        ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]
        xfr: Transform = entity[flags.TRANSFORM]
        ball = self.em.get_entity(ai.target)
        position: pygame.Vector2 = ball[flags.TRANSFORM].position
        force: pygame.Vector2 = ball[flags.BALLISTIC].force

        # Some really crummery perdiction
        dist = xfr.position.x - position.x
        reflect = dist - position.y
        ai.prediction = max((xfr.position.y + dist) * -1, 0) + reflect
        # add some error
        ai.prediction += ai.prediction * uniform(0.10, -0.10)

        self.em.spawn({
            flags.TRANSFORM: Transform(
                position=pygame.Vector2(700, ai.prediction)),
            flags.CIRCLE_SPRITE: CircleSprite(
                radius=10, thinkness=1, color=(255, 0, 0)),
            flags.TEMPORIAL: Temporial(
                kill_at=pygame.time.get_ticks()+3000),
        })

        self.em.spawn({
            flags.TRANSFORM: Transform(
                position=position.copy()),
            flags.CIRCLE_SPRITE: CircleSprite(
                radius=10, thinkness=1, color=(255, 0, 255)),
            flags.TEMPORIAL: Temporial(
                kill_at=pygame.time.get_ticks()+3000),
        })

        self.em.spawn({
            flags.TRANSFORM: Transform(
                position=xfr.position.copy()),
            flags.RECT_SPRITE: RectSprite(
                height=100, width=25, thinkness=2, color=(255, 0, 0)),
            flags.TEMPORIAL: Temporial(
                kill_at=pygame.time.get_ticks()+3000),
        })

        ai.phase = MOVE

    def update_move(self, entity):
        ai: AiController = entity[flags.AI_CONTROLLER]
        xfr: Transform = entity[flags.TRANSFORM]
        ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]
        if abs(xfr.position.y - ai.prediction) < 10:
            ctrl.moving_down = False
            ctrl.moving_up = False
        else:
            ctrl.moving_down = xfr.position.y < ai.prediction
            ctrl.moving_up = xfr.position.y > ai.prediction

    def __init__(self, em: IEntityManager, screen: pygame.Surface):
        self.em = em
        self.screen = screen
        self._prediction = None

