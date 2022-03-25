import pygame
from pyecs import Scene

from ..components import ball_sprite, paddle_sprite
from ..commands import (
    MovePlayerUpCommand,
    MovePlayerDownCommand,
    StopMovePlayerCommand,
)


class PlayScene(Scene):

    def setup(self) -> None:

        self.spawn(ball_sprite(
            position=(400, 300),
            vector=(1, 0),
        ))

        p1 = self.spawn(paddle_sprite((50, 300)))
        p2 = self.spawn(paddle_sprite((750, 300)))
        self.install_inputs(p1, pygame.K_w, pygame.K_s)
        self.install_inputs(p2, pygame.K_UP, pygame.K_DOWN)

    def install_inputs(self, player, up_key, down_key):
        entity = self.get_entity(player)
        self.install(pygame.KEYDOWN, MovePlayerUpCommand(entity), key=up_key)
        self.install(pygame.KEYUP, StopMovePlayerCommand(entity), key=up_key)
        self.install(pygame.KEYDOWN, MovePlayerDownCommand(entity), key=down_key)
        self.install(pygame.KEYUP, StopMovePlayerCommand(entity), key=down_key)
