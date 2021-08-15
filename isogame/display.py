#!/usr/bin/env python3

from abc import ABC, abstractmethod

import pygame

from pygame import Surface
from pygame.math import Vector2

from sortedcontainers import SortedList


class Camera:

    def __init__(
        self,
        position: Vector2,
        size: Vector2,
        _map
    ):
        self.position = position
        self.size = size
        self._map = _map

        self.scroll_speed = 600 

    def get_draw_delta(self) -> Vector2:
        return -(
            self._map.iso_to_cartesian(self.position) -
            (self.size / 2)
        )

    def update(self, delta, input):
        self.position += self._map.cartesian_to_iso(
            input.axis * self.scroll_speed * delta,
        )
        self._map.trap_camera(self)


class Drawable(ABC):

    def __init__(self, display: 'Display'):
        self.display = display

    @abstractmethod
    def get_order_value(self) -> int:
        ...

    @abstractmethod
    def raw_draw(self):
        ...


class Display:

    def __init__(self):
        self.size = Vector2(1280, 720)
        self.screen = pygame.display.set_mode(
            (int(self.size.x), int(self.size.y)))
        self.camera = None 
        self.renderlist = SortedList(
            key=lambda x: x.get_order_value())

    def instantiate_drawable(self, _type, *args, **kwargs):
        return _type(self, *args, **kwargs)

    def draw(self, obj: Drawable):
        self.renderlist.add(obj)

    def present(self):
        self.screen.fill((0, 0, 0))
        
        for obj in self.renderlist:
            obj.raw_draw()

        self.renderlist.clear()

