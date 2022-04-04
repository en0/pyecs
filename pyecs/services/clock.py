from pygame.time import Clock
from time import time
from typing import NamedTuple


class ClockServiceOpts(NamedTuple):
    framerate: int


class ClockService:

    @property
    def frame_delta(self) -> float:
        return self._tick_ms / 1000

    @property
    def frame_delta_ms(self) -> int:
        return self._tick_ms

    def tick(self) -> float:
        self._tick_ms = self._clock.tick(self._framerate)
        return self.frame_delta

    def get_fps(self) -> float:
        return self._clock.get_fps()

    def get_now(self) -> float:
        return time()

    def __init__(self, opts: ClockServiceOpts):
        self._tick_ms = 0
        self._framerate = opts.framerate
        self._clock = Clock()
