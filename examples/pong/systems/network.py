import pygame
from pyecs.typing import ISystem, IEntityManager
from pyecs import Entity
from ..components import flags, queries, NetSyncIn, NetSyncOut
from ..providers import NetworkInput, NetworkOutput


class NetworkSystem(ISystem):

    def update(self, frame_delta):
        self.counter += 1
        for net_entity in self.net_in.iter_entities():
            entity = self.em.get_entity(net_entity["identity"])
            if entity is None:
                continue
            for k, v in net_entity["data"].items():
                if int(k) == flags.TRANSFORM:
                    entity[flags.TRANSFORM].position = pygame.Vector2(*v["position"])
                elif int(k) == flags.TEXT_SPRITE:
                    entity[flags.TEXT_SPRITE].value = v["value"]

        if self.counter % 2 == 0:
            for entity in self.em.get_entities(queries.NETSYNC_OUT):
                net: NetSyncOut = entity[flags.NETSYNC_OUT]
                out_entity = Entity()
                out_entity.identity = entity.identity
                for flag in net.components:
                    out_entity[flag] = entity[flag]
                self.net_out.send_entity(out_entity)

    def __init__(self, em: IEntityManager, net_in: NetworkInput, net_out: NetworkOutput):
        self.em = em
        self.net_in = net_in
        self.net_out = net_out
        self.counter = 0
