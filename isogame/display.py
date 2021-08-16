#!/usr/bin/env python3

from abc import abstractmethod

import pygame

from pygame import Surface
from pygame.math import Vector2

from sortedcontainers import SortedList

from .ecs import Entity, Component, on_call


class Camera(Component):

    def __init__(
        self,
        entity,
        size: Vector2
    ):
        super().__init__(entity)

        self.size = size
        self.scroll_speed = 600 

        self.map = self.game.map

    def get_draw_delta(self) -> Vector2:
        return -(
            self.map.iso_to_cartesian(self.entity.position) -
            (self.size / 2)
        )

    @on_call('update')
    def scroll_cam(self):
        self.entity.position += self.map.cartesian_to_iso(
            self.game.input.axis * self.scroll_speed * self.game.delta)

        if self.entity.position.x < 0:
            self.entity.position.x = 0

        if self.entity.position.x > self.map.iso_size_x:
            self.entity.position.x = self.map.iso_size_x

        if self.entity.position.y < 0:
            self.entity.position.y = 0

        if self.entity.position.y > self.map.iso_size_y:
            self.entity.position.y = self.map.iso_size_y


class Drawable(Component):

    def __init__(
        self,
        entity: Entity
    ):
        super().__init__(entity)
        self.display = self.game.display

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
        self.renderlist = SortedList(
            key=lambda x: x.get_order_value())

    def draw(self, obj: Drawable):
        self.renderlist.add(obj)

    def present(self):
        self.screen.fill((0, 0, 0))
        
        for obj in self.renderlist:
            obj.raw_draw()

        pygame.display.flip()
        self.renderlist.clear()
