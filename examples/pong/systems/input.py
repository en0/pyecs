import pygame
from pyecs.typing import ISystem, IEntityManager
from ..components import flags, queries, PlayerController, PaddleControl, SceneChangeTrigger


class InputSystem(ISystem):

    def update(self):
        pressed = pygame.key.get_pressed()

        for entity in self.em.get_entities(queries.SCENE_CHANGE_TRIGGER):
            trig: SceneChangeTrigger = entity[flags.SCENE_CHANGE_TRIGGER]
            if pressed[trig.key]:
                self.em.activate_world(trig.to_scene)

        for entity in self.em.get_entities(queries.PLAYER_PADDLE):
            player: PlayerController = entity[flags.PLAYER_CONTROLLER]
            ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]
            ctrl.moving_up = pressed[player.up]
            ctrl.moving_down = pressed[player.down]

    def __init__(self, em: IEntityManager):
        self.em = em
