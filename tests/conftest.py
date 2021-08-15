#!/usr/bin/env python3


import pygame
import pytest

from isogame.map import Map


@pytest.fixture(scope='session')
def isometric_map():

    cartesian_size = 64

    pygame.init()
    yield Map(None, 10, 10, cartesian_size)
