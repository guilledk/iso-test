#!/usr/bin/env python3

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


def world_to_iso(coords: Vector2) -> Vector2:
    return Vector2(
        coords.x - coords.y * 2,
        (coords.x + coords.y * 2) / 2
    )


def iso_to_world(coords: Vector2) -> Vector2:
    return Vector2(
        (2 * coords.y + coords.x) / 2,
        (coords.y - .5 * coords.x) / 2
    )