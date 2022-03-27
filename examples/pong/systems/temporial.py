import pygame
from pyecs.typing import ISystem, IEntityManager
from ..components import flags, queries, PlayerController, PaddleControl, Temporial


class TemporialSystem(ISystem):

    def update(self, frame_delta):
        for entity in self.em.get_entities(queries.TEMPORIAL):
            life: Temporial = entity[flags.TEMPORIAL]
            if pygame.time.get_ticks() >= life.kill_at:
                self.em.kill(entity)

    def __init__(self, em: IEntityManager):
        self.em = em
