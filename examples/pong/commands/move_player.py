from pyecs import Vector2
from pyecs.typing import ICommand
from ..components import Movement


class PlayerCommandBase(ICommand):
    def __init__(self, entity: dict) -> None:
        self.entity = entity

class MovePlayerUpCommand(PlayerCommandBase):
    def execute(self, event) -> None:
        self.entity[Movement].vector += Vector2(0, -1)

class MovePlayerDownCommand(PlayerCommandBase):
    def execute(self, event) -> None:
        self.entity[Movement].vector += Vector2(0, 1)

class StopMovePlayerCommand(PlayerCommandBase):
    def execute(self, event) -> None:
        self.entity[Movement].vector = Vector2.zero()
