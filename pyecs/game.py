import pygame
from collections import deque
from pyioc3 import ScopeEnum
from typing import List, Type, Deque, Union

from .typing import IGame, IScene, ISystem, IGameContainer
from .container import GameContainer
from .systems import MessageSystem


SCENE_PUSH = 1
SCENE_POP = 2


def _setup(comp):
    comp.setup()
    return comp

class Game(IGame):

    framerate: float = 60
    systems: List[Type[ISystem]] = []
    scenes: List[Type[IScene]] = []

    def setup(self, container: IGameContainer) -> None:
        ...

    def teardown(self) -> None:
        ...

    def run(self) -> None:

        self._setup()

        delay = self._get_frame_delay()
        self._is_running = True
        while self._is_running:
            self._check_for_exit()
            scene = self._get_current_scene()
            scene.update(delay)
            for system in self._loaded_systems:
                system.update(scene, delay)
            delay = self._get_frame_delay()

        self._teardown()

    def push_scene(self, scene_t: Type[Union[IScene, str]]) -> None:
        if isinstance(scene_t, str):
            scene_t = next(filter(lambda x: x.__name__ == scene_t, self.scenes))
        self._scene_actions.appendleft((SCENE_PUSH, scene_t))

    def pop_scene(self) -> IScene:
        self._scene_actions.appendleft((SCENE_POP, None))

    def quit(self) -> None:
        self._is_running = False

    def _setup(self) -> None:

        pygame.init()

        self.setup(self._container)

        # Bind all scenes
        for scene_t in self.scenes:
            self._container.add_provider(
                provider=scene_t,
                scope=ScopeEnum.TRANSIENT,
                on_activate=_setup)

        # Bind all systems
        for system_t in self.systems:
            self._container.add_provider(
                provider=system_t,
                scope=ScopeEnum.SINGLETON,
                on_activate=_setup)

        self.push_scene(self.scenes[0])

        self._loaded_systems = [
            self._container.get_provider(s)
            for s in self.systems
        ]

    def _teardown(self) -> None:

        self._loaded_scenes.pop().teardown()

        for system in self._loaded_systems:
            system.teardown()

        self.teardown()

    def _get_current_scene(self) -> IScene:
        action: int
        scene_t: Type[IScene]
        while self._scene_actions:
            action, scene_t = self._scene_actions.pop()
            if action == SCENE_POP:
                self._loaded_scenes.pop().teardown()
            elif action == SCENE_PUSH:
                scene = self._container.get_provider(scene_t)
                self._loaded_scenes.appendleft(scene)
        return self._loaded_scenes[0]

    def _check_for_exit(self):
        quit_event = pygame.event.get(pygame.QUIT)
        if quit_event:
            # Push the quit event back in so other
            # components can react
            pygame.event.post(quit_event[0])
            self._is_running = False

    def _get_frame_delay(self):
        return self._clock.tick(self.framerate) / 1000

    def __init__(self):

        self._is_running: bool = False
        self._container: GameContainer = GameContainer(self)
        self._scene_actions: Deque[SceneChangeRecord] = deque()
        self._loaded_scenes: Deque[IScene] = deque()
        self._loaded_systems: List[ISystem] = list()
        self._clock = pygame.time.Clock()
