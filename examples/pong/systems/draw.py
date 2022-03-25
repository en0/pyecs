import pygame
from pyecs.typing import ISystem, IScene
from ..components import Transform, Text, Shape


class DrawSystem(ISystem):

    _font: pygame.font.Font

    def setup(self) -> None:
        sys_font = pygame.font.get_default_font()
        self._font = pygame.font.Font(sys_font, 75)

    def teardown(self) -> None:
        ...

    def update(self, scene: IScene, frame_delay: float) -> None:
        self.screen.fill((0, 0, 0))

        self.draw_text(scene)
        self.draw_shapes(scene)

        pygame.display.flip()

    def draw_text(self, scene: IScene) -> None:
        for entity in scene.get_entities(Text):
            transform: Transform = entity[Transform]
            text: Text = entity[Text]
            sprite = self._font.render(text.text, False, text.color)
            loc = sprite.get_rect()
            loc.center = transform.position
            self.screen.blit(sprite, loc)

    def draw_shapes(self, scene: IScene) -> None:
        for entity in scene.get_entities(Shape):
            if entity[Shape].shape == "circle":
                pygame.draw.circle(
                    self.screen,
                    entity[Shape].color,
                    entity[Transform].position,
                    entity[Shape].value,
                )
            if entity[Shape].shape == "rect":
                rect = pygame.Rect((0, 0), entity[Shape].value)
                rect.center = entity[Transform].position
                pygame.draw.rect(
                    self.screen,
                    entity[Shape].color,
                    rect,
                )

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
