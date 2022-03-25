from typing import Tuple, Any
from dataclasses import dataclass


@dataclass
class Shape:
    shape: str
    color: Tuple[int, int, int]
    value: Any

