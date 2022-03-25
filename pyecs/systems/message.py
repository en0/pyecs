import pygame
from ..typing import ISystem, IScene, CommandBinding


class MessageSystem(ISystem):
    """A message system used to relay events to scenes

    This system consumes the pygame event system and relays
    those events to commands installed on the active scene.
    """

    def setup(self) -> None:
        ...

    def teardown(self) -> None:
        ...

    def update(self, scene: IScene, frame_delay: float) -> None:
        for event in pygame.event.get():
            for i, command_binding in enumerate(scene.get_commands(event.type)):
                if self._match(event, command_binding):
                    command_binding.command.execute(event)

    def _match(self, event: pygame.event, binding: CommandBinding) -> bool:
        for key, value in binding.parameters.items():
            if not hasattr(event, key):
                return False
            if getattr(event, key) != value:
                return False
        return True
