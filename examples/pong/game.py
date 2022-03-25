import pygame
from pyecs import Game
from pyecs.typing import IGameContainer
from pyecs.systems import MessageSystem
from .systems import MoveSystem, DrawSystem
from .scenes import WelcomeScene, PlayScene


class Pong(Game):

    systems = [
        MessageSystem,
        MoveSystem,
        DrawSystem,
    ]

    scenes = [
        WelcomeScene,
        PlayScene,
    ]

    def setup(self, container: IGameContainer) -> None:
        pygame.init()
        surface = pygame.display.set_mode((800, 600))
        container.add_constant(pygame.Surface, surface)
