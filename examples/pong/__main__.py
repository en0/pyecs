import pygame
from pyecs import GameBuilder

from .systems import RenderSystem
from . import components as c


def main():
    game = GameBuilder()
    game.using_screen_mode((800, 600))
    game.using_component_groups({c.BALL})
    game.using_system(RenderSystem)
    game.using_active_world("default")
    game.using_world_template("default", [
        {
            c.TRANSFORM: c.Transform(
                position=pygame.Vector2(400, 300)),
            c.BALLSPRITE: c.BallSprite(
                radius=10,
                color=pygame.Color(244, 244, 244)),
        }
    ])
    game.play()

if __name__ == "__main__":
    main()
