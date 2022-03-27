import pygame
from ..components import flags, models
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from . import PLAY


ENTITIES = [
    { # Press Enter Prompt
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2),
        ),
        flags.TEXT_SPRITE: models.TextSprite(
            value="[ Press Enter ]",
        ),
        flags.SCENE_CHANGE_TRIGGER: models.SceneChangeTrigger(
            key=pygame.K_RETURN,
            to_scene=PLAY,
        ),
    },
]
