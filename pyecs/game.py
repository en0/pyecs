import pygame
from .typing import (
    IGame,
    IEntityManager,
    ISystemManager,
    IObjectFactory,
)


class Game(IGame):

    _playing = False

    def setup(self) -> None:
        ...

    def teardown(self) -> None:
        ...

    def update(self) -> None:
        ...

    def play(self) -> None:
        self.setup()
        self._playing = True
        while self._playing:
            self._check_for_exit()
            self.update()
            self.system_manager.update()
        self.teardown()

    def _check_for_exit(self) -> None:
        quit_event = pygame.event.get(pygame.QUIT)
        if quit_event:
            self._playing = False
            for e in quit_event:
                pygame.event.post(e)

    def stop(self) -> None:
        self._playing = False

    def __init__(self, entity_manager: IEntityManager, system_manager: ISystemManager, factory: IObjectFactory):
        self.entity_manager = entity_manager
        self.system_manager = system_manager
        self.factory = factory

