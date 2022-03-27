import pygame
import json
import socket
from dataclasses import asdict
from pyecs import Entity

from .opts import NetOpts


def make_safe(val):
    if isinstance(val, pygame.Vector2):
        return [val.x, val.y]
    elif isinstance(val, dict):
        for k, v in val.items():
            val[k] = make_safe(v)
        return val
    else:
        return val

class NetworkOutput:

    def send_entity(self, entity: Entity):
        d = {"identity": entity.identity, "data": {}}
        for k, v in entity.items():
            d["data"][k] = make_safe(asdict(v))
        data = json.dumps(d).encode("utf-8")
        try:
            self.socket.sendto(data, self.target)
        except:
            ...

    def __init__(self, opts: NetOpts):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.target = (opts.publish_addr, opts.publish_port)
