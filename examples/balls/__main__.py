import pygame
from random import randint, choice
from pyecs import EntityManager


TRANSFORM = 0b00001
PLAYER_CONTROLLED = 0b00010
CONTROLLER = 0b00100
BALISTIC = 0b01000
CIRCLE_SPRITE = 0b10000

PLAYER_CONTROLLABLE = PLAYER_CONTROLLED | CONTROLLER
MOVEABLE_BALL = TRANSFORM | CONTROLLER | BALISTIC
RENDERABLE = TRANSFORM | CIRCLE_SPRITE


def player_control(manager: EntityManager, screen: pygame.Surface, delta: float):
    keys = pygame.key.get_pressed()
    for entity in manager.get_entities(PLAYER_CONTROLLABLE):
        bindings = entity[PLAYER_CONTROLLED]
        controller = entity[CONTROLLER]
        for direction, key in bindings.items():
            controller[direction] = keys[key]


def move_objects(manager: EntityManager, screen: pygame.Surface, delta: float):
    for entity in manager.get_entities(MOVEABLE_BALL):
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
            x + (i * delta * balistic["speed"]),
            y + (j * delta * balistic["speed"]),
        )


def render_circle(manager: EntityManager, screen: pygame.Surface, delta: float):
    for entity in manager.get_entities(RENDERABLE):
        sprite = entity[CIRCLE_SPRITE]
        transform = entity[TRANSFORM]
        pygame.draw.circle(
            screen,
            sprite["color"],
            transform["position"],
            sprite["radius"]
        )


def main():

    playing = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))
    manager = EntityManager({PLAYER_CONTROLLABLE, MOVEABLE_BALL, RENDERABLE}, {"default"})

    manager.activate_world("default")

    systems = [
        player_control,
        render_circle,
        move_objects
    ]

    for i in range(1000):
        manager.spawn({
            TRANSFORM: {"position": (randint(100, 700), randint(100, 500))},
            CIRCLE_SPRITE: {"radius": 10, "color": (randint(155, 255), randint(155, 255), randint(155,255))},
            BALISTIC: {"speed": randint(100, 200)},
            CONTROLLER: {
                "up": False,
                "down": False,
                "left": False,
                "right": False
            },
            PLAYER_CONTROLLED: {
                "up": choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]),
                "down": choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]),
                "left": choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]),
                "right": choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]),
            },
        })

    while playing:

        delta = clock.tick(60) / 1000

        if pygame.event.get(pygame.QUIT):
            playing = False

        screen.fill((0, 0, 255))

        for sys in systems:
            sys(manager, screen, delta)

        pygame.display.flip()
        pygame.event.pump()


if __name__ == "__main__":
    main()
