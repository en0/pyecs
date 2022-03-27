import pygame
from ..components import flags, models
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
from . import SPLASH


ENTITIES = [

    { # Ball
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(400, 300)),
        flags.CIRCLE_SPRITE: models.CircleSprite(
            radius=10, thinkness=3),
        flags.BALLISTIC: models.Ballistic(
            force=pygame.Vector2(1, -1)),
        flags.RECT_COLLIDER: models.RectCollider(
            rect=pygame.Rect(0, 0, 15, 15)),
    },

    { # Top Wall
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, -10)),
        flags.RECT_COLLIDER: models.RectCollider(
            rect=pygame.Rect(0, 0, SCREEN_WIDTH, 10)),
        flags.COLLIDER: None,
    },

    { # Bottom Wall
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT)),
        flags.RECT_COLLIDER: models.RectCollider(
            rect=pygame.Rect(0, 0, SCREEN_WIDTH, 10)),
        flags.COLLIDER: None,
    },

    { # Left Paddle
        flags.PADDLE_CONTROL: models.PaddleControl(),
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(25, SCREEN_HEIGHT/2)),
        flags.RECT_COLLIDER: models.RectCollider(
            rect=pygame.Rect(0, 0, 25, 100)),
        flags.RECT_SPRITE: models.RectSprite(
            width=25,
            height=100),
        flags.COLLIDER: None,
        flags.PLAYER_CONTROLLER: models.PlayerController(
            up=pygame.K_UP,
            down=pygame.K_DOWN)
    },

    { # Right Paddle
        flags.AI_CONTROLLER: models.AiController(
            reaction_time=500
        ),
        flags.PADDLE_CONTROL: models.PaddleControl(),
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH-25, SCREEN_HEIGHT/2)),
        flags.RECT_COLLIDER: models.RectCollider(
            rect=pygame.Rect(0, 0, 25, 100)),
        flags.RECT_SPRITE: models.RectSprite(
            width=25,
            height=100),
        flags.COLLIDER: None,
    },

    { # center line
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)),
        flags.RECT_SPRITE: models.RectSprite(
            width=5,
            height=SCREEN_HEIGHT),
    },

    { # HUD
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, 50)),
        flags.TEXT_SPRITE: models.TextSprite(
            value="0   0"
        ),
        flags.SCORE_HUD: models.ScoreHud(
            left_score=0,
            right_score=0),
    },

    { # Escape To Return To Splash
        flags.SCENE_CHANGE_TRIGGER: models.SceneChangeTrigger(
            key=pygame.K_ESCAPE,
            to_scene=SPLASH,
        ),
    },
]
