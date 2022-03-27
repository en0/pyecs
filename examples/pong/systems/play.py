import pygame
from pyecs.typing import ISystem, IEntityManager
from ..components import flags, queries, ScoreHud, TextSprite, Transform, CircleSprite, Ballistic, RectCollider
from ..constants import SCREEN_WIDTH


class PlaySystem(ISystem):

    def update(self, frame_delta: float):

        left_point_increase, right_point_increase = 0, 0

        for entity in self.em.get_entities(queries.BALL):
            xfr: Transform = entity[flags.TRANSFORM]
            mov: Ballistic = entity[flags.BALLISTIC]
            if xfr.position.x < 0:
                right_point_increase += 1
                self.em.kill(entity)
                self.spawn_ball(mov.force * -1)

            elif xfr.position.x > SCREEN_WIDTH:
                left_point_increase += 1
                self.em.kill(entity)
                self.spawn_ball(mov.force * -1)

        for entity in self.em.get_entities(queries.HUD):
            text: TextSprite = entity[flags.TEXT_SPRITE]
            hud: ScoreHud = entity[flags.SCORE_HUD]
            hud.left_score += left_point_increase
            hud.right_score += right_point_increase
            text.value = f"{hud.left_score}   {hud.right_score}"

    def spawn_ball(self, vector: pygame.Vector2):
        self.em.spawn({
            flags.TRANSFORM: Transform(
                position=pygame.Vector2(400, 300)),
            flags.CIRCLE_SPRITE: CircleSprite(
                radius=10, thinkness=3),
            flags.BALLISTIC: Ballistic(
                force=vector),
            flags.RECT_COLLIDER: RectCollider(
                rect=pygame.Rect(0, 0, 15, 15)),
        })

    def __init__(self, em: IEntityManager):
        self.em = em

