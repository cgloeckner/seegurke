import pygame
import moderngl
import random
import math

from typing import List

from model import create_texture, Quad, Animator
from camera import Camera


class Ship(object):
    def __init__(self, ctx: moderngl.Context, img_list: List[pygame.Surface]):
        self.tex = [create_texture(ctx, img) for img in img_list]
        self.model = Quad(ctx, pygame.math.Vector2(0, 0), pygame.math.Vector2(1, 1))
        self.model.rotation = 90
        self.ani = Animator(self.tex, 1500)

        self.swim_ms = random.randrange(5000)

    def steer(self, value):
        self.model.rotation += value

    def get_ship_vector(self):
        return pygame.math.Vector2(1, 0).rotate(self.model.rotation)

    def update(self, elapsed_ms: int, wind: pygame.math.Vector2) -> None:
        # frame animation
        self.ani.update(elapsed_ms, self.model)

        # z-position for swimming animation
        self.swim_ms += elapsed_ms
        angle = (2 * math.pi * self.swim_ms / 3000) % 360
        self.model.scale += math.sin(angle * 0.9) * 0.0005

        # apply wind
        ship_vector = self.get_ship_vector()
        move = 3 * ship_vector + wind
        self.model.position += move * elapsed_ms * 0.0001

    def render(self, cam: Camera) -> None:
        self.model.render(cam.m_view, cam.m_proj)


class Cannonball(object):
    def __init__(self, ctx: moderngl.Context, tex: moderngl.Texture, move: pygame.math.Vector2):
        self.model = Quad(ctx, pygame.math.Vector2(0, 0), pygame.math.Vector2(0.05, 0.05))
        self.model.texture = tex
        self.move = move

        self.z_func = lambda s: -0.65 * s**2 + 1.87 * s + 0.23
        self.delta_time = 0
        self.model.scale = self.z_func(0)

    def update(self, elapsed_ms: int) -> None:
        self.model.position += self.move * elapsed_ms * 0.0001
        print(self.move, self.model.position)

        self.delta_time += elapsed_ms / 1000
        self.model.scale = self.z_func(self.delta_time)

    def render(self, cam: Camera) -> None:
        self.model.render(cam.m_view, cam.m_proj)


class CannonballManager(object):
    def __init__(self, ctx: moderngl.Context, img: pygame.Surface):
        self.ctx = ctx
        self.texture = create_texture(ctx, img)
        self.balls = list()
        self.cooldown = dict()

    def add(self, ship: Ship, direction: int):
        if ship in self.cooldown and self.cooldown[ship] > 0:
            return

        ship_vector = ship.get_ship_vector()
        move = ship_vector.rotate(75 * direction)
        print(ship_vector, move)
        cb = Cannonball(self.ctx, self.texture, move * 5)
        cb.model.position = ship.model.position.copy()
        self.balls.append(cb)
        self.cooldown[ship] = 500

    def update(self, elapsed_ms: int) -> None:
        for s in self.cooldown:
            self.cooldown[s] -= elapsed_ms
            if self.cooldown[s] < 0:
                self.cooldown[s] = 0

        for b in self.balls:
            b.update(elapsed_ms)
            if b.model.scale < 0.1:
                self.balls.remove(b)

    def render(self, cam: Camera) -> None:
        for b in self.balls:
            b.render(cam)
