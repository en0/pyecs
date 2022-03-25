from pyecs import Vector2
from dataclasses import dataclass


@dataclass
class Movement:
    speed: float
    vector: Vector2 = Vector2.zero()
    bounce: bool = False

