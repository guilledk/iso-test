#!/usr/bin/env python3

import time
import copy

import pygame

from pygame.math import Vector2

from isogame.map import Map, Minimap
from isogame.input import Input
from isogame.display import Camera, Display
from isogame.humanoid import Humanoid


pygame.init()
display = Display()

input = display.instantiate_drawable(Input)
tmap = display.instantiate_drawable(Map, 50, 50, 64)
minimap = display.instantiate_drawable(Minimap, tmap)

# init cam
display.camera = Camera(
    Vector2(0, 0), display.size, tmap
)

# center cam
display.camera.position = Vector2(25)

humanoid = display.instantiate_drawable(
    Humanoid, copy.copy(display.camera.position), tmap)

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

    display.draw(tmap)
    display.draw(minimap)
    display.draw(humanoid)
    display.draw(input)

    display.present()
    pygame.display.flip()

pygame.quit()
