import pygame
import moderngl
import glm

import random
import math

from typing import List

from camera import Camera, GuiCamera
from sprite import create_texture, Quad, Animator


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


def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    window = pygame.display.set_mode((800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF)
    context = moderngl.create_context()
    context.enable(flags=moderngl.BLEND)
    clock = pygame.time.Clock()

    scene_cam = Camera(window)
    scene_cam.position.z = 2
    gui_cam = GuiCamera(window)

    water_tiles = WaterTiles(context, [pygame.image.load(f'data/water{n:02d}.png') for n in range(4)])

    ship = Ship(context, [pygame.image.load(f'data/ship{n:02d}.png') for n in range(2)])
    ship2 = Ship(context, [pygame.image.load(f'data/ship{n:02d}.png') for n in range(2)])
    ship2.model.position.x = 2

    wind_img = pygame.image.load('data/wind.png')
    wind_tex = create_texture(context, wind_img)
    wind_sprite = Quad(context, pygame.math.Vector2(50, 50), pygame.math.Vector2(100, 100))
    wind_sprite.texture = wind_tex

    wind_vector = pygame.math.Vector2(0, 1)

    elapsed_ms = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # animate water tile
        water_tiles.update(elapsed_ms)

        keys = pygame.key.get_pressed()

        # Schiff 1
        if keys[pygame.K_a]:
            ship.model.rotation += 0.02 * elapsed_ms
        if keys[pygame.K_d]:
            ship.model.rotation -= 0.02 * elapsed_ms
        ship.update(elapsed_ms, wind_vector)

        # Schiff 2
        if keys[pygame.K_LEFT]:
            ship2.model.rotation += 0.02 * elapsed_ms
        if keys[pygame.K_RIGHT]:
            ship2.model.rotation -= 0.02 * elapsed_ms
        ship2.update(elapsed_ms, wind_vector)

        # Kamera zwischen beiden Schiffen
        scene_cam.position.x = (ship.model.position.x + ship2.model.position.x) / 2
        scene_cam.position.y = (ship.model.position.y + ship2.model.position.y) / 2
        scene_cam.position.z = 1.5 * ship.model.position.distance_to(ship2.model.position)
        scene_cam.update(elapsed_ms)

        context.clear(color=(0.0, 0.0, 0.0, 0.0))
        water_tiles.render(scene_cam)#, 0, 40, 0, 40)
        ship.render(scene_cam)
        ship2.render(scene_cam)
        wind_sprite.render(gui_cam.m_view, gui_cam.m_proj)
        pygame.display.flip()

        elapsed_ms = clock.tick(60)
        pygame.display.set_caption(f'FPS: {clock.get_fps():.1f} ({elapsed_ms}ms)'
                                   f'cam_at ({scene_cam.position.x:.1f}; {scene_cam.position.y:.1f}; '
                                   f'{scene_cam.position.z:.1f})')

    pygame.quit()


if __name__ == '__main__':
    main()
