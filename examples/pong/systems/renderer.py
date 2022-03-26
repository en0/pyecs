import pygame
from pyecs.typing import ISystem, IEntityManager

from ..components import BALL, BALLSPRITE, TRANSFORM, Transform, BallSprite


class RenderSystem(ISystem):

    def update(self, frame_delta: float):
        self.screen.fill((66, 66, 66))
        for entity in self.em.get_entities(BALL):
            xfr: Transform = entity[TRANSFORM]
            sprite: BallSprite = entity[BALLSPRITE]
            pygame.draw.circle(
                self.screen,
                sprite.color,
                xfr.position,
                sprite.radius
            )
        pygame.display.flip()

    def __init__(self, em: IEntityManager, screen: pygame.Surface):
        self.em = em
        self.screen = screen
