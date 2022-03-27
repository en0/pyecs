from pygame import Vector2, Color, Rect
from typing import Tuple
from dataclasses import dataclass


@dataclass
class PlayerController:
    up: int
    down: int


@dataclass
class PaddleControl:
    moving_up: bool = False
    moving_down: bool = False


@dataclass
class Transform:
    position: Vector2


@dataclass
class CircleSprite:
    radius: float
    thinkness: float = 0
    color: Tuple[int, int, int] = (255, 255, 255)


@dataclass
class RectSprite:
    height: float
    width: float
    thinkness: int = 0
    color: Tuple[int, int, int] = (255, 255, 255)


@dataclass
class TextSprite:
    value: str


@dataclass
class ScoreHud:
    left_score: int
    right_score: int


@dataclass
class RectCollider:
    rect: Rect


@dataclass
class Ballistic:
    force: Vector2


@dataclass
class AiController:
    reaction_time: int
    phase: int = 0
    wait_until: int = 0
    target: float = 0
    prediction: float = 0


@dataclass
class Temporial:
    kill_at: int

