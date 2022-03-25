from typing import Tuple
from dataclasses import dataclass


@dataclass
class Text:
    text: str
    color: Tuple[int, int, int]

