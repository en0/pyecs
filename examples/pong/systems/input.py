import pygame
from pyecs.typing import ISystem, IEntityManager
from ..components import flags, queries, PlayerController, PaddleControl


class InputSystem(ISystem):

    def update(self, frame_delta):
        pressed = pygame.key.get_pressed()
        for entity in self.em.get_entities(queries.PLAYER_PADDLE):
            player: PlayerController = entity[flags.PLAYER_CONTROLLER]
            ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]
            ctrl.moving_up = pressed[player.up]
            ctrl.moving_down = pressed[player.down]

    def __init__(self, em: IEntityManager):
        self.em = em
