#!/usr/bin/env python3

import pygame

from pygame.math import Vector2

from .ecs import on_call
from .display import Drawable, Camera


class Humanoid(Drawable):

    def __init__(self, entity, pos: Vector2):
        super().__init__(entity)
        self.position = pos
        self.map = self.game.map

        self._graphic = pygame.image.load("res/humanoid_medium.png")
        self._anchor = Vector2(.5, .875)
        self._anchor_deltas = Vector2(
            self._anchor.x * self._graphic.get_width(),
            self._anchor.y * self._graphic.get_height()
        )
        self._cam = self.game.camera.get_component(Camera)

    @on_call('draw')
    def draw(self):
        self.display.draw(self)
 
    def get_order_value(self) -> int:
        cam_world = self.map.iso_to_cartesian(
            self.game.camera.position)
        cam_world.y += self.display.size.y / 2
        return -int(
            self.map.cartesian_to_iso(cam_world)
                .distance_to(self.entity.position)
        )

    def raw_draw(self):
        world_coords = (
            self.map.iso_to_cartesian(self.entity.position)
            - self._anchor_deltas
            + self._cam.get_draw_delta()
        )
        self.display.screen.blit(self._graphic,  world_coords)
