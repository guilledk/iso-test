#!/usr/bin/env python3

import pygame

from pygame.math import Vector2

from .display import Drawable, Display


class Humanoid(Drawable):

    def __init__(self, display: Display, pos: Vector2, _map):
        super().__init__(display)
        self.position = pos
        self._map = _map

        self._graphic = pygame.image.load("res/humanoid_medium.png")
        self._anchor = Vector2(.5, .875)
        self._anchor_deltas = Vector2(
            self._anchor.x * self._graphic.get_width(),
            self._anchor.y * self._graphic.get_height()
        )

    def get_order_value(self) -> int:
        cam_world = self._map.iso_to_cartesian(
            self.display.camera.position)
        cam_world.y += self.display.size.y / 2
        return -int(
            self._map.cartesian_to_iso(cam_world)
                .distance_to(self.position)
        )

    def raw_draw(self):
        world_coords = (
            self._map.iso_to_cartesian(self.position)
            - self._anchor_deltas
            + self.display.camera.get_draw_delta()
        )
        self.display.screen.blit(self._graphic,  world_coords)
