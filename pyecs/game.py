import pygame
from .typing import IGame, IEntityManager, ISystemManager


class Game(IGame):

    _playing = False

    def setup(self):
        ...

    def teardown(self):
        ...

    def play(self):
        self.setup()
        self._playing = True
        while self._playing:
            self.check_for_exit()
            frame_delta = self.clock.tick(60) / 1000
            self.system_manager.update(frame_delta)
        self.teardown()

    def check_for_exit(self):
        quit_event = pygame.event.get(pygame.QUIT)
        if quit_event:
            self._playing = False
            for e in quit_event:
                pygame.event.post(e)

    def __init__(self, entity_manager: IEntityManager, system_manager: ISystemManager):
        self.entity_manager = entity_manager
        self.system_manager = system_manager
        self.clock = pygame.time.Clock()

