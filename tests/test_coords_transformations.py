#!/usr/bin/env python3

import random

from pygame.math import Vector2

from isogame.utils import iso_to_world, world_to_iso


def test_transformations_identity():
	
	iso_coords = Vector2(1, 1)

	world_coords = iso_to_world(iso_coords)

	assert world_coords == Vector2(1.5, 0.25)

	assert iso_coords == world_to_iso(world_coords)


def test_transformations_random():

	_min, _max = (0, 1000)

	iso_coords = Vector2(
		random.randint(_min, _max),
		random.randint(_min, _max),
	)

	assert iso_coords == world_to_iso(iso_to_world(iso_coords))
