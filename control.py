import pygame


class KeyboardControls(object):
    """Defines keyboard bindings and fires callbacks"""
    def __init__(self):
        self.mapping = dict()

    def __setitem__(self, key: int, value: callable) -> None:
        self.mapping[key] = value

    def __delitem__(self, key: int) -> None:
        del self.mapping[key]

    def update(self, elapsed_ms: int) -> None:
        pressed = pygame.key.get_pressed()

        for key in self.mapping:
            if pressed[key]:
                self.mapping[key](elapsed_ms)
