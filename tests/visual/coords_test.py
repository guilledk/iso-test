#!/usr/bin/env python3


import time
import pygame

from pygame.math import Vector2


# ordinary pygame init
pygame.init()
size_x, size_y = (800, 600)

screen = pygame.display.set_mode(
    (size_x, size_y))

title = "Isometric coordinate systems visual test"

pygame.display.set_caption(title)


# configuration constants

# size in pixels of an isometric 1x1 tile in cartesian coords, remember actual
# pixel size of an individual tile image resource should be width equal to 
# ``tile_size`` and height equal to ``tile_size / 2``
tile_size = 64
 
iso_scaling = 8  # scale factor for the isometric coords display

iso_size_x = 13  # total width of map in isometric system
iso_size_y = 13  # total height of map in isometric system

red_color = (255, 0, 0)
green_color = (0, 255, 0)
blue_color = (0, 0, 255)
yellow_color = (255, 255, 0)

# when drawing the cartesian space add this delta to center "camera"
cartesian_delta = Vector2(20, size_y / 2)

# when drawing the isometric space add this delta to offset from window corner
iso_delta = Vector2(40)

def draw_point(pos: Vector2, color, width: int = 3):
    """Helper function to draw a point
    """
    pygame.draw.circle(
        screen,
        color,
        pos,
        width
    )

"""Transformations
"""

def iso_to_cartesian(pos: Vector2) -> Vector2:
    return Vector2(
        (pos.y + pos.x) / 2,
        (pos.y - pos.x) / 4 
    ) * tile_size


def cartesian_to_iso(pos: Vector2) -> Vector2:
    return Vector2(
        pos.x - (2 * pos.y),
        pos.x + (2 * pos.y)
    ) / tile_size


if __name__ == '__main__':

    # create isometric position list
    positions = []
    for y in range(iso_size_y):
        for x in range(iso_size_x):
            positions.append(Vector2(x, y))

    # transform those positions to cartesian space
    cartesian_positions = []
    for pos in positions:
        cartesian_positions.append(iso_to_cartesian(pos))

    # transform back to isometric and compare to original coords
    checks = True
    for pos, cpos in zip(positions, cartesian_positions):
        checks = checks and (pos == cartesian_to_iso(cpos))

    if checks:
        pygame.display.set_caption(title + " - [PASSED]")
    else:
        pygame.display.set_caption(title + " - [NOT PASSED]")
 
    # begin main loop
    stop = False
    while not stop:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True

        screen.fill((0, 0, 0))

        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        mouse_pos = Vector2(mouse_pos_x, mouse_pos_y) - cartesian_delta

        # isometric drawing
        for pos in positions:
            draw_point((pos * iso_scaling) + iso_delta, red_color, width=1)

        iso_pos = cartesian_to_iso(mouse_pos)

        # mouse inside map?
        if (iso_pos.x >= 0 and iso_pos.y >= 0 and
            iso_pos.x < iso_size_x and iso_pos.y < iso_size_y):

            # pointer
            draw_point((iso_pos * iso_scaling) + iso_delta, yellow_color)

            # horizontal line
            pygame.draw.line(
                screen,
                yellow_color,
                (Vector2(0, iso_pos.y) * iso_scaling) + iso_delta,
                (Vector2(iso_size_x, iso_pos.y) * iso_scaling) + iso_delta
            )

            # vertical line
            pygame.draw.line(
                screen,
                yellow_color,
                (Vector2(iso_pos.x, 0) * iso_scaling) + iso_delta,
                (Vector2(iso_pos.x, iso_size_y) * iso_scaling) + iso_delta
            )



        # cartesian drawing
        for pos in cartesian_positions:
            draw_point(pos + cartesian_delta, blue_color)
        
        # mouse inside map?
        if (iso_pos.x >= 0 and iso_pos.y >= 0 and
            iso_pos.x < iso_size_x and iso_pos.y < iso_size_y):

            # pointer
            draw_point(mouse_pos + cartesian_delta, green_color)

            # horizontal line
            pygame.draw.line(
                screen,
                green_color,
                iso_to_cartesian(Vector2(0, iso_pos.y)) + cartesian_delta,
                iso_to_cartesian(Vector2(iso_size_x, iso_pos.y)) + cartesian_delta
            )

            # vertical line
            pygame.draw.line(
                screen,
                green_color,
                iso_to_cartesian(Vector2(iso_pos.x, 0)) + cartesian_delta,
                iso_to_cartesian(Vector2(iso_pos.x, iso_size_y)) + cartesian_delta
            )

        pygame.display.flip()

    pygame.quit()
