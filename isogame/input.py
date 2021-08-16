#!/usr/bin/env python3

import pygame

from pygame import (
    Rect,
    K_UP, K_DOWN, K_LEFT, K_RIGHT,
    K_w,  K_s,    K_a,    K_d
)
from pygame.math import Vector2


def get_index_or(i, default, array):
    try:
        return array[i]
    except IndexError:
        return default


class Input():

    def __init__(self):
        self.axis = Vector2(0)

        self.keys_down = []  # pressed right now
        self.keys_pressed = []  # pressed this frame
        self.keys_released = []  # released this frame

        self.mouse_down = (False, False, False)
        self.mouse_pressed = (False, False, False)
        self.mouse_released = (False, False, False)

        self.selecting = False
        self.selection_color = (255, 255, 255)
        self.selection_border_width = 1
        self.selection_begin = Vector2(0)
        self.selection_in_progress = Vector2(0)
        self.selection_end = Vector2(0)

    def is_down(self, key) -> bool:
        return self.keys_down[key]

    def was_pressed(self, key) -> bool:
        return self.keys_pressed[key]

    def was_released(self, key) -> bool:
        return self.keys_released[key]

    def is_mouse_down(self, btn) -> bool:
        return self.mouse_down[btn]

    def was_mouse_pressed(self, btn) -> bool:
        return self.mouse_pressed[btn]

    def was_mouse_released(self, btn) -> bool:
        return self.mouse_released[btn] 

    def update(self):
        keys = pygame.key.get_pressed()
        self.keys_pressed = [
            True
            if not get_index_or(key, False, self.keys_down) and value
            else False
            for key, value in enumerate(keys)
        ]
        self.keys_released = [
            True
            if get_index_or(key, False, self.keys_down) and not value
            else False
            for key, value in enumerate(keys)
        ]
        self.keys_down = keys

        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
        self.mouse_pressed = [
            True
            if not self.mouse_down[btn] and value
            else False
            for btn, value in enumerate(mouse_buttons)
        ]
        self.mouse_released = [
            True
            if self.mouse_down[btn] and not value
            else False
            for btn, value in enumerate(mouse_buttons)
        ]
        self.mouse_down = mouse_buttons

        if self.was_mouse_pressed(0):
            self.selecting = True
            self.selection_begin = Vector2(*pygame.mouse.get_pos())

        if self.is_mouse_down(0):
            self.selection_in_progress = Vector2(*pygame.mouse.get_pos())

        if self.was_mouse_released(0):
            self.selecting = False
            self.selection_end = Vector2(*pygame.mouse.get_pos())

        self.axis = Vector2(0)

        if self.is_down(K_UP) or self.is_down(K_w):
            self.axis.y -= 1

        if self.is_down(K_DOWN) or self.is_down(K_s):
            self.axis.y += 1

        if self.is_down(K_LEFT) or self.is_down(K_a):
            self.axis.x -= 1

        if self.is_down(K_RIGHT) or self.is_down(K_d):
            self.axis.x += 1

        if self.axis.x != 0 or self.axis.y != 0:
            self.axis = self.axis.normalize()

    # def get_order_value(self) -> int:
    #     return 10000

    # def raw_draw(self):
    #     if self.selecting:
    #         size = self.selection_in_progress - self.selection_begin
    #         pygame.draw.rect(
    #             self.display.screen,
    #             self.selection_color,
    #             Rect(self.selection_begin, size),
    #             self.selection_border_width
    #         )
