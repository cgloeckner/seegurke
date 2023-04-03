import pygame
import moderngl
import glm

import random
import math

from typing import List

from camera import Camera, GuiCamera
from sprite import create_texture, Quad, Animator
from control import KeyboardControls


class WaterTiles(object):
    """A single (animated) tile is spread across the entire game.
    """
    def __init__(self, ctx: moderngl.Context, img_list: List[pygame.Surface]):
        self.tex = [create_texture(ctx, img) for img in img_list]
        self.ani = Animator(self.tex, 500)
        self.model = Quad(ctx, pygame.math.Vector2(0, 0), pygame.math.Vector2(1, 1))

    def update(self, elapsed_ms: int) -> None:
        self.ani.update(elapsed_ms, self.model)

    def render(self, cam: Camera) -> None:
        x_min = int(cam.position.x - cam.position.z)
        x_max = int(cam.position.x + cam.position.z) + 1
        delta_x = x_max - x_min

        y_min = int(cam.position.y - cam.position.z)
        y_max = int(cam.position.y + cam.position.z) + 1
        delta_y = y_max - y_min

        for y in range(delta_y):
            self.model.position.y = y + y_min
            for x in range(delta_x):
                self.model.position.x = x + x_min
                self.model.render(cam.m_view, cam.m_proj)


class Ship(object):
    def __init__(self, ctx: moderngl.Context, img_list: List[pygame.Surface]):
        self.tex = [create_texture(ctx, img) for img in img_list]
        self.model = Quad(ctx, pygame.math.Vector2(0, 0), pygame.math.Vector2(1, 1))
        self.model.rotation = 90
        self.ani = Animator(self.tex, 1500)

        self.swim_ms = random.randrange(5000)

    def steer(self, value):
        self.model.rotation += value

    def update(self, elapsed_ms: int, wind: pygame.math.Vector2) -> None:
        # frame animation
        self.ani.update(elapsed_ms, self.model)

        # z-position for swimming animation
        self.swim_ms += elapsed_ms
        angle = (2 * math.pi * self.swim_ms / 3000) % 360
        self.model.z_pos = 0.05 * math.sin(angle * 0.9)

        # apply wind
        ship_vector = pygame.math.Vector2(1, 0).rotate(self.model.rotation)
        move = 3 * ship_vector + wind
        self.model.position += move * elapsed_ms * 0.0001

    def render(self, cam: Camera) -> None:
        self.model.render(cam.m_view, cam.m_proj)


class Wind(object):
    def __init__(self, ctx: moderngl.Context, img: pygame.Surface):
        # wind rose (GUI mode)
        self.model = Quad(ctx, pygame.math.Vector2(50, 50), pygame.math.Vector2(100, 100))
        self.model.texture = create_texture(ctx, img)

        # actual wind vector
        self.vector = pygame.math.Vector2(1, 0).rotate(random.randrange(360))
        self.elapsed = 0
        self.angle = 0

    def update(self, elapsed_ms: int) -> None:
        self.elapsed += elapsed_ms

        if self.angle != 0:
            angle = (self.angle / elapsed_ms) * 0.1
            self.vector.rotate_ip(angle)
            self.model.rotation += angle

        if self.elapsed < 1000:
            return

        # set new direction
        self.angle = (random.randrange(3) - 1) * 45
        self.elapsed -= 1000

    def render(self, cam: GuiCamera) -> None:
        self.model.render(cam.m_view, cam.m_proj)


def init(width, height):
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    window = pygame.display.set_mode((width, height), flags=pygame.OPENGL | pygame.DOUBLEBUF)
    context = moderngl.create_context()
    context.enable(flags=moderngl.BLEND)
    clock = pygame.time.Clock()

    return window, context, clock


def main():
    window, context, clock = init(800, 600)

    scene_cam = Camera(window)
    scene_cam.position.z = 2
    gui_cam = GuiCamera(window)

    water_tiles = WaterTiles(context, [pygame.image.load(f'data/water{n:02d}.png') for n in range(4)])

    ship1 = Ship(context, [pygame.image.load(f'data/ship{n:02d}.png') for n in range(2)])
    ship2 = Ship(context, [pygame.image.load(f'data/ship{n:02d}.png') for n in range(2)])
    ship2.model.position.x = 2

    key1 = KeyboardControls()
    key1[pygame.K_a] = lambda ms: ship1.steer(0.02 * ms)
    key1[pygame.K_d] = lambda ms: ship1.steer(-0.02 * ms)

    key2 = KeyboardControls()
    key2[pygame.K_LEFT] = lambda ms: ship2.steer(0.02 * ms)
    key2[pygame.K_RIGHT] = lambda ms: ship2.steer(-0.02 * ms)

    wind = Wind(context, pygame.image.load('data/wind.png'))

    elapsed_ms = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # animate water tile
        water_tiles.update(elapsed_ms)
        wind.update(elapsed_ms)

        key1.update(elapsed_ms)
        key2.update(elapsed_ms)
        ship1.update(elapsed_ms, wind.vector)
        ship2.update(elapsed_ms, wind.vector)

        # Kamera zwischen beiden Schiffen
        scene_cam.position.x = (ship1.model.position.x + ship2.model.position.x) / 2
        scene_cam.position.y = (ship1.model.position.y + ship2.model.position.y) / 2
        distance = max(2, ship1.model.position.distance_to(ship2.model.position))
        scene_cam.position.z = 1.5 * distance
        scene_cam.update(elapsed_ms)

        context.clear(color=(0.0, 0.0, 0.0, 0.0))
        water_tiles.render(scene_cam)#, 0, 40, 0, 40)
        ship1.render(scene_cam)
        ship2.render(scene_cam)
        wind.render(gui_cam)
        pygame.display.flip()

        elapsed_ms = clock.tick(60)
        pygame.display.set_caption(f'FPS: {clock.get_fps():.1f} ({elapsed_ms}ms)'
                                   f'cam_at ({scene_cam.position.x:.1f}; {scene_cam.position.y:.1f}; '
                                   f'{scene_cam.position.z:.1f})')

    pygame.quit()


if __name__ == '__main__':
    main()
