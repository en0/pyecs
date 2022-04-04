from ..typing import ISystem
from ..services import ClockService


class ClockSystem(ISystem):

    def update(self) -> None:
        self.clock.tick()

    def __init__(self, clock: ClockService) -> None:
        self.clock = clock
