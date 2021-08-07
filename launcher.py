#!/usr/bin/env python3

import time
import copy

import pygame

from pygame.math import Vector2

from isogame.map import Map, Minimap
from isogame.input import Input
from isogame.utils import world_to_iso
from isogame.display import Display
from isogame.humanoid import Humanoid


pygame.init()
display = Display()

input = display.instantiate_drawable(Input)
tmap = display.instantiate_drawable(Map, 50, 50)
minimap = display.instantiate_drawable(Minimap, tmap)

# center cam
display.camera.position = Vector2(
    25 * tmap.tile_size.x,
    25 * tmap.tile_size.y
)

humanoid = display.instantiate_drawable(
    Humanoid, copy.copy(display.camera.position))

prev_time = time.time()

stop = False
while not stop:

    current_time = time.time()

    delta = current_time - prev_time
    prev_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True

    input.update()

    display.camera.update(delta, input)
    tmap.trap_camera(display.camera)

    display.draw(tmap)
    display.draw(minimap)
    display.draw(humanoid)
    display.draw(input)

    display.present()
    pygame.display.flip()

pygame.quit()