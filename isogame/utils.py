#!/usr/bin/env python3

import copy

import pygame

from pygame import Vector2


def tint(surf, tint_color):
    """Adds tint_color onto surf.
    https://www.pygame.org/wiki/Tint
    """
    surf = surf.copy()
    surf.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    tint_color = (*tint_color[0:3], 0)
    surf.fill(tint_color, None, pygame.BLEND_RGBA_ADD)
    return surf


def diagonal_iter(start_x: int, start_y: int, width: int):
    for i in range(width):
        yield i, start_x + i, start_y + i

def diagonal_box_iter(start_x: int, start_y: int, width: int, height: int):
    """
    This generator will yield four integers, the first two are the local
    coordinates within the selected region, the other the global coords 
    within the array, for example:

    start_x = 3
    start_y = 1
    width = 4
    height = 4

    The generator will zig zag from point * to @.

     __0_1_2_3_4_5_6_7
    0| - - - - - - - -
    1| - - - * - - - -
    2| - - 1 1 1 - - -
    3| - - 1 1 1 1 - -
    4| - - - 1 1 1 1 -
    5| - - - - 1 1 1 -
    6| - - - - - @ - -
    7| - - - - - - - -
    """
    for j in range(height):
        if j > 0:
            if j % 2 == 0:
                start_x -= 1
            else:
                start_y += 1

        for i, x, y in diagonal_iter(start_x, start_y, width):
            yield i, j, x, y
