import pygame
from pyecs import GameBuilder

from .systems import RenderSystem, MovementSystem, InputSystem, PlaySystem, AiSystem, TemporialSystem
from .components import flags, models, queries
from .worlds import play


def main():
    game = GameBuilder()
    game.using_screen_mode((800, 600))
    game.using_component_groups({
        queries.BALL,
        queries.PADDLE,
        queries.PLAYER_PADDLE,
        queries.RECT,
        queries.CIRCLE,
        queries.RECT_COLLIDERS,
        queries.TEXT,
        queries.HUD,
        queries.NPC_PADDLE,
        queries.TEMPORIAL,
    })
    game.using_system(InputSystem)
    game.using_system(AiSystem)
    game.using_system(MovementSystem)
    game.using_system(PlaySystem)
    game.using_system(RenderSystem)
    game.using_system(TemporialSystem)
    game.using_active_world(play.NAME)
    game.using_world_template(play.NAME, play.ENTITIES)

    pygame.init()
    game.play()

if __name__ == "__main__":
    main()
