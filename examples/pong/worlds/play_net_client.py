import pygame
from ..components import flags, models
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT


NAME = "play_net_client"
ENTITIES = [

    { # Ball
        flags.NETSYNC_IN: models.NetSyncIn(
            components=[flags.TRANSFORM]),
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(400, 300)),
        flags.CIRCLE_SPRITE: models.CircleSprite(
            radius=10, thinkness=3),
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
        flags.NETSYNC_IN: models.NetSyncIn(
            components=[flags.TRANSFORM]),
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(25, SCREEN_HEIGHT/2)),
        flags.RECT_SPRITE: models.RectSprite(
            width=25,
            height=100),
    },

    { # Right Paddle
        flags.NETSYNC_OUT: models.NetSyncOut(
            components=[flags.TRANSFORM]),
        flags.PADDLE_CONTROL: models.PaddleControl(),
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH-25, SCREEN_HEIGHT/2)),
        flags.RECT_COLLIDER: models.RectCollider(
            rect=pygame.Rect(0, 0, 25, 100)),
        flags.RECT_SPRITE: models.RectSprite(
            width=25,
            height=100),
        flags.PLAYER_CONTROLLER: models.PlayerController(
            up=pygame.K_UP,
            down=pygame.K_DOWN)
    },

    { # center line
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)),
        flags.RECT_SPRITE: models.RectSprite(
            width=5,
            height=SCREEN_HEIGHT),
    },

    { # HUD
        flags.NETSYNC_IN: models.NetSyncIn(
            components=[flags.TEXT_SPRITE]),
        flags.TRANSFORM: models.Transform(
            position=pygame.Vector2(SCREEN_WIDTH/2, 50)),
        flags.TEXT_SPRITE: models.TextSprite(
            value="0   0"),
    }
]
