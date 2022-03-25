import pygame
from pyecs import Scene
from pyecs.commands import DelegatedCommand
from ..components import text_sprite


class WelcomeScene(Scene):

    def setup(self) -> None:
        self.spawn(text_sprite(
            value="Press Enter to Play",
            position=(400, 300),
            color=(200, 200, 255)
        ))

        self.install(
            pygame.KEYDOWN,
            DelegatedCommand(lambda: self.game.push_scene("PlayScene")),
            key=pygame.K_RETURN)
