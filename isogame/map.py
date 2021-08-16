#!/usr/bin/env python3

import random

from math import sqrt

import pygame

from pygame import Rect
from pygame.math import Vector2

from opensimplex import OpenSimplex

from .ecs import on_call
from .utils import tint, diagonal_box_iter
from .display import Drawable, Display, Camera


def noise_to_tile_id(simplex, x, y, delta):
    """OpenSimplex returns values from in the range
    (-1, 1), so we add 1 to put it in the range (0, 2) and
    divide to clamp it to (0, 1), then multiply by delta and cast to int
    to get the final integer range: (0, delta)

    simplex: noise generator
    x: sample 0 <= x <= delta
    y: sample 0 <= y <= delta
    delta: maximun sample diference
    """
    return int(
        ((simplex.noise2d(
            x=x / delta, y=y / delta
        ) + 1) / 2) * delta
    )



class Map(Drawable):

    def __init__(
        self,
        entity,
        iso_size_x: int,
        iso_size_y: int,
        cartesian_size: int
    ):
        super().__init__(entity)
        self.iso_size_x = iso_size_x
        self.iso_size_y = iso_size_y

        self.cartesian_size = cartesian_size

        self.map_delta = 20

        self._tile = pygame.image.load("res/tile_medium.png")
        self.tile_size = Vector2(*self._tile.get_size())

        assert self.tile_size.x == cartesian_size
        assert self.tile_size.y == cartesian_size // 2

        self.tiles = []
        for i in range(self.map_delta):
            self.tiles.append(
                tint(
                    self._tile,
                    [0,
                    (i * 255) / self.map_delta,
                    (max(0, i - 50) * 255) / self.map_delta]
                )
            )

        self.simplex = OpenSimplex(seed=random.randint(0, 99999999))
        self.map_data = [
            [
                noise_to_tile_id(self.simplex, x, y, self.map_delta)
                for x in range(iso_size_x)
            ]
            for y in range(iso_size_y)
        ]

        self._cam = None

    def iso_to_cartesian(self, pos: Vector2) -> Vector2:
        return Vector2(
             (pos.x + pos.y) / 2,
            (-pos.x + pos.y) / 4
        ) * self.cartesian_size

    def cartesian_to_iso(self, pos: Vector2) -> Vector2:
        return Vector2(
            pos.x - (2 * pos.y),
            pos.x + (2 * pos.y)
        ) / self.cartesian_size

    @on_call('draw')
    def draw(self):
        self.display.draw(self)

    def get_order_value(self) -> int:
        return -10000000

    def raw_draw(self):
        if not self._cam:
            self._cam = self.game.camera.get_component(Camera)
        cam_iso = self.game.camera.position
        cam_x, cam_y = (int(cam_iso.x), int(cam_iso.y))
        cam_size_x, cam_size_y = (
            int(self._cam.size.x / self.tile_size.x),
            int(self._cam.size.y / self.tile_size.y)
        )
        
        cam_x -= cam_size_x // 2
        cam_y -= int(cam_size_y * 1.5)
    
        for lx, ly, x, y in diagonal_box_iter(
            cam_x, cam_y - 2, cam_size_x * 2, (cam_size_y * 2) + 5):

            if (x < 0 or x >= self.iso_size_x or 
                y < 0 or y >= self.iso_size_y):
                continue

            world_pos = self.iso_to_cartesian(
                Vector2(x, y)
            ) + self._cam.get_draw_delta()
            
            self.display.screen.blit(
                self.tiles[self.map_data[x][y]],
                world_pos
            )



class Minimap(Drawable):

    def __init__(self, entity):
        super().__init__(entity)
        self.map = self.game.map

        self.cam_color = (218, 224, 44)
        self.tile_colors = []
        for i in range(self.map.map_delta):
            self.tile_colors.append(
                (0,
                (i * 255) / self.map.map_delta,
                (max(0, i - 50) * 255) / self.map.map_delta)
            )

        self.set_scale(3)
        
    def set_scale(self, scale: float):
        self._tile_size = Vector2(2, 1) * scale
        self.scale_ratio = Vector2(
            self._tile_size.x / self.map.tile_size.x,
            self._tile_size.y / self.map.tile_size.y
        )
        self.size = Vector2(
            self._tile_size.x * self.map.iso_size_x,
            ((self._tile_size.y * self.map.iso_size_y) / 2) + self._tile_size.y / 2
        )

    def world_to_mini(self, point: Vector2) -> Vector2:
        return (self.display.size - self.size) + Vector2(
            point.x * self.scale_ratio.x,
            point.y * self.scale_ratio.y
        )

    @on_call('draw')
    def draw(self):
        self.display.draw(self)

    def get_order_value(self) -> int:
        return 1000000

    def raw_draw(self):
        pos = self.display.size - self.size

        for y in range(self.map.iso_size_y):
            for x in range(self.map.iso_size_x):
                world_coords = pos + (self.map.iso_to_cartesian(
                    Vector2(
                        x * self._tile_size.x,
                        y * self._tile_size.y * 2
                    )
                ) / self.map.cartesian_size)
                pygame.draw.rect(
                    self.display.screen,
                    self.tile_colors[self.map.map_data[x][y]],
                    Rect(world_coords, self._tile_size)
                )

        scaled_size = Vector2(
            self.display.size.x * self.scale_ratio.x,
            self.display.size.y * self.scale_ratio.y
        )
        pygame.draw.rect(
            self.display.screen,
            self.cam_color,
            Rect(
                self.world_to_mini(
                    self.map.iso_to_cartesian(self.game.camera.position)
                ) - scaled_size / 2,
                scaled_size
            ),
            2
        )

