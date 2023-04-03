import pygame
import moderngl
import random

from model import Quad, create_texture
from camera import GuiCamera


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
