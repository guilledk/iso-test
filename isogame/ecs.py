#!/usr/bin/env python3

import uuid
import traceback

from abc import ABC
from time import time
from uuid import UUID
from typing import Dict, List, Callable

import pygame

from pygame.math import Vector2


class CallAlreadyAssignedError(BaseException):
    ...


def on_call(flag: str):
    def decorator(func):
        if hasattr(func, 'call_flag'):
            raise CallAlreadyAssignedError

        func.call_flag = flag
        return func
    return decorator


class Component(ABC):
    
    def __init__(
        self,
        entity
    ):
        self.entity = entity
        self.game = game_state()
       
        methods = [
            getattr(self, attr)
            for attr in dir(self)
            if (callable(getattr(self, attr)) and 
                not attr.startswith('__'))
        ]

        for fn in methods:
            flag = getattr(fn, 'call_flag', None)
            if flag:
                if flag not in self.entity._on_call:
                    self.entity._on_call[flag] = []

                self.entity._on_call[flag].append(fn)


class Entity:

    def __init__(
        self,
        level,
        name: str
    ):
        self.level = level
        self.name = name
        self.id = uuid.uuid4()
       
        self.position = Vector2()
        self.components: List[Component] = []

        self._on_call = {}

    def get_component(self, comp_type) -> Component:
        for comp in self.components:
            if isinstance(comp, comp_type):
                return comp

    def add_component(self, component, *args, **kwargs) -> Component:
        new_comp = component(self, *args, **kwargs)
        self.components.append(new_comp)
        return new_comp


class Level:

    def __init__(self):
        self.entities: Dict[str, Entity] = {}

    def perform_calls(self, flag: str):
        for entity in self.entities.values():
            if flag not in entity._on_call:
                continue

            for fn in entity._on_call[flag]:
                fn()

    def spawn(self, name: str):
        self.entities[name] = Entity(self, name)
        return self.entities[name] 

    def destroy(self, name: str):
        self.entities[name].cleanup()
        del self.entities[name]


class Game:

    def __init__(self):

        from .input import Input
        from .display import Display
        
        pygame.init()
        self.display = Display()
        self.input = Input()
        self.level = Level()

        self.delta = 0

        self._stop = False
        self._prev_time = time()
        self._current_time = time()

    def init(self):

        from .map import Map, Minimap
        from .display import Camera
        from .humanoid import Humanoid

        # default entities
        _map = self.level.spawn('map')
        self.map = _map.add_component(Map, 50, 50, 64)

        self.minimap = self.level.spawn('minimap')
        self.minimap.add_component(Minimap)

        self.camera = self.level.spawn('camera')
        self.camera.position = Vector2(25)
        self.camera.add_component(
            Camera, self.display.size)

        for i in range(3):
            humanoid = self.level.spawn(f'humanoid-{i}')
            humanoid.add_component(
                Humanoid, Vector2(i, i))

        print(self.level.entities.keys())

    def run(self):
        try:
            while not self._stop:    
                self._current_time = time()
                self.delta = self._current_time - self._prev_time

                print(1 / self.delta)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self._stop = True

                self.input.update()

                self.level.perform_calls('update')
                self.level.perform_calls('draw')

                self.display.present()

                self._prev_time = self._current_time
                

        except Exception:
            traceback.print_exc()
            breakpoint()

        finally:
            pygame.quit()


_GAME = None

def run_game():
    global _GAME
    assert _GAME == None
    _GAME = Game()
    _GAME.init()
    _GAME.run()

def game_state():
    global _GAME
    return _GAME
