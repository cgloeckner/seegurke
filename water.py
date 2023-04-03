import pygame
import moderngl

from typing import List

from model import create_texture, Animator, Quad
from camera import Camera

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
        x_min = int(cam.position.x - cam.position.z * 2) - 1
        x_max = int(cam.position.x + cam.position.z * 2) + 1
        delta_x = x_max - x_min

        y_min = int(cam.position.y - cam.position.z * 2) - 1
        y_max = int(cam.position.y + cam.position.z * 2) + 1
        delta_y = y_max - y_min

        for y in range(delta_y):
            self.model.position.y = y + y_min
            for x in range(delta_x):
                self.model.position.x = x + x_min
                self.model.render(cam.m_view, cam.m_proj)
