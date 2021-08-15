#!/usr/bin/env python3

import random

from pygame.math import Vector2


def test_transformations_identity(isometric_map):
    
    iso_coords = Vector2(1, 1)

    world_coords = isometric_map.iso_to_cartesian(iso_coords)

    assert world_coords == Vector2(isometric_map.cartesian_size, 0)

    assert iso_coords == isometric_map.cartesian_to_iso(world_coords)


def test_transformations_random(isometric_map):

    _min, _max = (0, 1000)

    iso_coords = Vector2(
        random.randint(_min, _max),
        random.randint(_min, _max),
    )

    assert iso_coords == isometric_map.cartesian_to_iso(
        isometric_map.iso_to_cartesian(iso_coords))
