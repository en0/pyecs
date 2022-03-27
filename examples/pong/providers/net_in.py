import json
import socket
from threading import Thread, Event
from queue import Queue
from pyecs import Entity

from .opts import NetOpts
from ..components import flags, Transform, TextSprite


class NetworkListener(Thread):

    def run(self):
        srv = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        srv.bind(("0.0.0.0", self.port))
        srv.setblocking(False)
        while not self.event.is_set():
            try:
                d, _ = srv.recvfrom(1024)
                self.collect_entity(d)
            except BlockingIOError:
                ...

    def collect_entity(self, data):
        e = json.loads(data)
        self.q.put(e)

    def __init__(self, q: Queue, port: int):
        super().__init__()
        self.q = q
        self.port = port
        self.event = Event()


class NetworkInput:

    def shutdown(self):
        self.listener.event.set()

    def iter_entities(self):
        while not self.q.empty():
            val = self.q.get()
            yield val

    def __init__(self, opts: NetOpts):
        self.q = Queue()
        self.listener = NetworkListener(self.q, opts.listen_port)
        self.listener.start()

