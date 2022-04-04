# pyecs

Yet another ECS pygame framework.

# Quick Start

Install pyecs

```
pip install pyecs
```

Create a System or two.

```
from pygame import draw, display
from pyecs.typing import ISystem, IEntityManager


class RenderSystem(ISystem):

    def update(self) -> None:
        self.screen.fill((0, 0, 255))
        draw.circle(self.screen, (0, 0, 0), (400, 300), 5)
        display.flip()

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
```

Create the game using the game builder.

```
from pyecs import GameBuilder


if __name__ == "__main__":
    game = GameBuilder(init=True)
    game.using_screen_mode((800, 600))
    game.using_system(RenderSystem)
    game.play()
```
