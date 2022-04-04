import pygame
from pyecs import EntityManager, EntityManagerOpts, SystemManager, Game
from pyecs.typing import ISystem


TRANSFORM = 0b00001
PLAYER_CONTROLLED = 0b00010
CONTROLLER = 0b00100
BALISTIC = 0b01000
CIRCLE_SPRITE = 0b10000

PLAYER_CONTROLLABLE = PLAYER_CONTROLLED | CONTROLLER
MOVEABLE_BALL = TRANSFORM | CONTROLLER | BALISTIC
RENDERABLE = TRANSFORM | CIRCLE_SPRITE


class PlayerControl(ISystem):

    def update(self):
        keys = pygame.key.get_pressed()
        for entity in self.em.get_entities(PLAYER_CONTROLLABLE):
            bindings = entity[PLAYER_CONTROLLED]
            controller = entity[CONTROLLER]
            for direction, key in bindings.items():
                controller[direction] = keys[key]

    def __init__(self, em: EntityManager, screen: pygame.Surface):
        self.em = em
        self.screen = screen


class MoveObjects(ISystem):

    def update(self):
        frame_delta = self.clock.tick(60) / 1000
        for entity in self.em.get_entities(MOVEABLE_BALL):
            transform = entity[TRANSFORM]
            controller = entity[CONTROLLER]
            balistic = entity[BALISTIC]
            i, j = 0, 0
            if controller["up"]:
                j -= 1
            if controller["down"]:
                j += 1
            if controller["left"]:
                i -= 1
            if controller["right"]:
                i += 1
            x, y = transform["position"]
            transform["position"] = (
                x + (i * frame_delta * balistic["speed"]),
                y + (j * frame_delta * balistic["speed"]),
            )

    def __init__(self, em: EntityManager, screen: pygame.Surface):
        self.em = em
        self.screen = em
        self.clock = pygame.time.Clock()


class RenderCircle(ISystem):

    def update(self):
        screen.fill((0, 0, 255))
        for entity in self.em.get_entities(RENDERABLE):
            sprite = entity[CIRCLE_SPRITE]
            transform = entity[TRANSFORM]
            pygame.draw.circle(
                self.screen,
                sprite["color"],
                transform["position"],
                sprite["radius"]
            )
        pygame.display.flip()

    def __init__(self, em: EntityManager, screen: pygame.Surface):
        self.em = em
        self.screen = screen


class BallGame(Game):

    def setup(self):
        self.entity_manager.spawn({
            TRANSFORM: {"position": (400, 300)},
            CIRCLE_SPRITE: {"radius": 10, "color": (255,255,255)},
            BALISTIC: {"speed": 200},
            CONTROLLER: {
                "up": False,
                "down": False,
                "left": False,
                "right": False
            },
            PLAYER_CONTROLLED: {
                "up": pygame.K_UP,
                "down":  pygame.K_DOWN,
                "left":  pygame.K_LEFT,
                "right": pygame.K_RIGHT,
            },
        })


if __name__ == "__main__":

    screen = pygame.display.set_mode((800, 600))

    entity_manager = EntityManager(EntityManagerOpts({
        PLAYER_CONTROLLABLE,
        MOVEABLE_BALL,
        RENDERABLE
    }))

    system_manager = SystemManager()
    system_manager.install(PlayerControl(entity_manager, screen))
    system_manager.install(MoveObjects(entity_manager, screen))
    system_manager.install(RenderCircle(entity_manager, screen))

    ball_game = BallGame(entity_manager, system_manager, factory=None)

    ball_game.play()

