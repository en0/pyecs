from pygame import Vector2, Color
from dataclasses import dataclass


# Component Flags
TRANSFORM = 1 << 0
BALLSPRITE = 1 << 1


# Component Groups
BALL = TRANSFORM | BALLSPRITE


component_groups = [
    BALL
]


@dataclass
class Transform:
    position: Vector2


@dataclass
class BallSprite:
    radius: float
    color: Color
