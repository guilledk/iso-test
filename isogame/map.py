#!/usr/bin/env python3

import random

from math import sqrt

import pygame

from pygame import Rect
from pygame.math import Vector2

from opensimplex import OpenSimplex

from .utils import tint, iso_to_world, world_to_iso
from .display import Drawable, Display


def noise_to_tile_id(simplex, x, y, delta):
	"""OpenSimplex returns values from in the range
	(-1, 1), so we add 1 to put it in the range (0, 2) and
	divide to clamp it to (0, 1), then multiply by delta and cast to int
	to get the final integer range: (0, delta)

	simplex: noise generator
	x: sample 0 <= x <= delta
	y: sample 0 <= y <= delta
	delta: maximun sample diference
	"""
	return int(
		((simplex.noise2d(
			x=x / delta, y=y / delta
		) + 1) / 2) * delta
	)



class Map(Drawable):

	def __init__(self, display: Display, size_x, size_y):
		super().__init__(display)
		self.size_x = size_x
		self.size_y = size_y

		self.map_delta = 20

		self._tile = pygame.image.load("res/tile_medium.png")
		self.tiles = []
		for i in range(self.map_delta):
			self.tiles.append(
				tint(
					self._tile,
					[0,
					(i * 255) / self.map_delta,
					(max(0, i - 50) * 255) / self.map_delta]
				)
			)

		simplex = OpenSimplex(seed=random.randint(0, 99999999))
		self.map_data = [
			[
				noise_to_tile_id(simplex, x, y, self.map_delta)
				for x in range(size_x)
			]
			for y in range(size_y)
		]

		self.tile_size = Vector2(64, 32)
		self.map_size = Vector2(
			self.tile_size.x * size_x,
			self.tile_size.y * size_y
		)

	def trap_camera(self, camera):
		if camera.position.x < 0:
			camera.position.x = 0

		if camera.position.x > self.map_size.x:
			camera.position.x = self.map_size.x

		if camera.position.y < 0:
			camera.position.y = 0

		if camera.position.y > self.map_size.y:
			camera.position.y = self.map_size.y

	def get_order_value(self) -> int:
		return -10000000

	def raw_draw(self):
		for y in range(self.size_y):
			for x in range(self.size_x):
				world_coords = iso_to_world(
					Vector2(
						x * self.tile_size.x,
						y * self.tile_size.y
					)
				) + self.display.camera.get_draw_delta() + Vector2(0, self.map_data[x][y])
				self.display.screen.blit(
					self.tiles[self.map_data[x][y]],
					world_coords
				)


class Minimap(Drawable):

	def __init__(self, display: Display, _map: Map):
		super().__init__(display)
		self.map = _map

		self.cam_color = (218, 224, 44)
		self.tile_colors = []
		for i in range(_map.map_delta):
			self.tile_colors.append(
				(0,
				(i * 255) / _map.map_delta,
				(max(0, i - 50) * 255) / _map.map_delta)
			)

		self.set_scale(3)
		
	def set_scale(self, scale: float):
		self._tile_size = Vector2(2, 1) * scale
		self.scale_ratio = Vector2(
			self._tile_size.x / self.map.tile_size.x,
			self._tile_size.y / self.map.tile_size.y
		)
		self.size = Vector2(
			self._tile_size.x * self.map.size_x,
			((self._tile_size.y * self.map.size_y) / 2) + self._tile_size.y / 2
		)

	def world_to_mini(self, point: Vector2) -> Vector2:
		return (self.display.size - self.size) + Vector2(
			point.x * self.scale_ratio.x,
			point.y * self.scale_ratio.y
		)

	def get_order_value(self) -> int:
		return 1000000

	def raw_draw(self):
		pos = self.display.size - self.size

		for y in range(self.map.size_y):
			for x in range(self.map.size_x):
				world_coords = pos + iso_to_world(
					Vector2(
						x * self._tile_size.x,
						y * self._tile_size.y
					)
				)
				pygame.draw.rect(
					self.display.screen,
					self.tile_colors[self.map.map_data[x][y]],
					Rect(world_coords, self._tile_size)
				)

		scaled_size = Vector2(
			self.display.size.x * self.scale_ratio.x,
			self.display.size.y * self.scale_ratio.y
		)
		pygame.draw.rect(
			self.display.screen,
			self.cam_color,
			Rect(
				self.world_to_mini(iso_to_world(self.display.camera.position)) - scaled_size / 2,
				scaled_size
			),
			2
		)






