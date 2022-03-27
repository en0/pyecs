import pygame
from pyecs.typing import ISystem, IEntityManager

from ..components import flags, queries, Transform, CircleSprite, RectSprite, TextSprite


class RenderSystem(ISystem):

    def update(self, frame_delta: float):

        self.screen.fill((66, 66, 66))
        self.render_circles()
        self.render_rects()
        self.render_text()
        pygame.display.flip()

    def render_circles(self):
        for entity in self.em.get_entities(queries.CIRCLE):
            xfr: Transform = entity[flags.TRANSFORM]
            sprite: CircleSprite = entity[flags.CIRCLE_SPRITE]
            pygame.draw.circle(
                self.screen,
                sprite.color,
                xfr.position,
                sprite.radius,
                sprite.thinkness,
            )

    def render_rects(self):
        for entity in self.em.get_entities(queries.RECT):
            xfr: Transform = entity[flags.TRANSFORM]
            sprite: RectSprite = entity[flags.RECT_SPRITE]
            rect = pygame.Rect(0, 0, sprite.width, sprite.height)
            rect.center = xfr.position
            pygame.draw.rect(
                self.screen,
                sprite.color,
                rect,
                sprite.thinkness,
            )

    def render_text(self):
        for entity in self.em.get_entities(queries.TEXT):
            text: TextSprite = entity[flags.TEXT_SPRITE]
            xfr: Transform = entity[flags.TRANSFORM]
            sprite = self.font.render(text.value, True, (255, 255, 255))
            rect = sprite.get_rect(center=xfr.position)
            self.screen.blit(sprite, rect)

    def __init__(self, em: IEntityManager, screen: pygame.Surface):
        self.em = em
        self.screen = screen
        self.font = pygame.sysfont.Font(pygame.font.get_default_font(), 72)
