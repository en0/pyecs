from pyecs import Vector2
from pyecs.typing import Entity
from typing import Tuple, TypeVar, Dict, Type

from .movement import Movement
from .shape import Shape
from .text import Text
from .transform import Transform


def text_sprite(
    value: str,
    position: Vector2,
    color: Tuple[int, int, int],
) -> Entity:
    return {
        Transform: Transform(Vector2(*position)),
        Text: Text(value, color)
    }

def ball_sprite(
    position: Vector2,
    vector: Tuple[float, float],
) -> Entity:
    return {
        Transform: Transform(Vector2(*position)),
        Movement: Movement(200, Vector2(*vector), True),
        Shape: Shape("circle", (255, 255, 255), 10)
    }

def paddle_sprite(
    position: Vector2,
) -> Entity:
    return {
        Transform: Transform(Vector2(*position)),
        Movement: Movement(200, Vector2.zero()),
        Shape: Shape("rect", (255, 255, 255), [20, 100]),
    }
