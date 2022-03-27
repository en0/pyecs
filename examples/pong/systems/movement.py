import pygame
from typing import List
from pyecs.typing import ISystem, IEntityManager

from ..components import flags, queries, Transform, Ballistic, PaddleControl, RectCollider, ScoreHud
from ..constants import SCREEN_HEIGHT, SPEED, SCREEN_WIDTH


class MovementSystem(ISystem):

    def update(self, frame_delta: float):

        self.move_paddles(frame_delta)
        self.update_collision_boxes()
        self.move_ball(frame_delta)

    def update_collision_boxes(self):

        for entity in self.em.get_entities(queries.RECT_COLLIDERS):
            xfr: Transform = entity[flags.TRANSFORM]
            box: RectCollider = entity[flags.RECT_COLLIDER]
            box.rect.center = xfr.position
            self.colliders.append(entity)
            self.collider_rects.append(box.rect)

    def move_paddles(self, frame_delta: float):

        for entity in self.em.get_entities(queries.PADDLE):
            xfr: Transform = entity[flags.TRANSFORM]
            box: pygame.Rect = entity[flags.RECT_COLLIDER].rect
            ctrl: PaddleControl = entity[flags.PADDLE_CONTROL]

            # Compute target Location
            force = 0
            if ctrl.moving_up:
                force += -1
            if ctrl.moving_down:
                force += 1
            if not force:
                continue
            y = xfr.position.y
            y += force * frame_delta * SPEED

            # Check target location and apply if valid
            if y + (box.height/2) > SCREEN_HEIGHT:
                y = SCREEN_HEIGHT - (box.height/2)
            elif y - (box.height/2) < 0:
                y = box.height/2
            xfr.position.y = y

    def move_ball(self, frame_delta: float):

        hud: ScoreHud = next(self.em.get_entities(queries.HUD))[flags.SCORE_HUD]
        for entity in self.em.get_entities(queries.BALL):
            xfr: Transform = entity[flags.TRANSFORM]
            mov: Ballistic = entity[flags.BALLISTIC]
            box: RectCollider = entity[flags.RECT_COLLIDER]
            xfr.position += (mov.force * frame_delta * SPEED)
            future_position = xfr.position + (mov.force * frame_delta * SPEED)
            box.rect.center = future_position
            i = box.rect.collidelist(self.collider_rects)
            if i != -1:
                collider = self.colliders[i]
                collider_rect = self.collider_rects[i]
                if collider_rect.collidepoint(box.rect.midtop):
                    mov.force.x *=-1
                if collider_rect.collidepoint(box.rect.midbottom):
                    mov.force.x *=-1
                if collider_rect.collidepoint(box.rect.midleft):
                    mov.force.y *=-1
                if collider_rect.collidepoint(box.rect.midright):
                    mov.force.y *=-1
                # this isn't right but it's a start
                mov.force *= -1

    def __init__(self, em: IEntityManager):

        self.em = em
        self.colliders: List[dict] = []
        self.collider_rects: List[pygame.Rect] = []

