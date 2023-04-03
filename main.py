import pygame
import moderngl
import glm

from camera import OrthoCamera, GuiCamera
from control import KeyboardControls
from wind import Wind
from water import WaterTiles
from ship import CannonballManager, Ship


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

    scene_cam = OrthoCamera(window)
    scene_cam.position.z = 2
    gui_cam = GuiCamera(window)

    water_tiles = WaterTiles(context, [pygame.image.load(f'data/water{n:02d}.png') for n in range(4)])

    ship1 = Ship(context, [pygame.image.load(f'data/ship{n:02d}.png') for n in range(2)])
    ship2 = Ship(context, [pygame.image.load(f'data/ship{n:02d}.png') for n in range(2)])
    ship2.model.position.x = 2

    wind = Wind(context, pygame.image.load('data/wind.png'))

    cannonballs = CannonballManager(context, pygame.image.load('data/cannonball.png'))

    elapsed_ms = 0

    key1 = KeyboardControls()
    key1[pygame.K_a] = lambda ms: ship1.steer(0.02 * ms)
    key1[pygame.K_d] = lambda ms: ship1.steer(-0.02 * ms)
    key1[pygame.K_q] = lambda ms: cannonballs.add(ship1, 1)
    key1[pygame.K_e] = lambda ms: cannonballs.add(ship1, -1)

    key2 = KeyboardControls()
    key2[pygame.K_LEFT] = lambda ms: ship2.steer(0.02 * ms)
    key2[pygame.K_RIGHT] = lambda ms: ship2.steer(-0.02 * ms)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # animate water tile
        water_tiles.update(elapsed_ms)
        wind.update(elapsed_ms)
        cannonballs.update(elapsed_ms)

        key1.update(elapsed_ms)
        key2.update(elapsed_ms)
        ship1.update(elapsed_ms, wind.vector)
        ship2.update(elapsed_ms, wind.vector)

        # Kamera zwischen beiden Schiffen
        scene_cam.position.x = (ship1.model.position.x + ship2.model.position.x) / 2
        scene_cam.position.y = (ship1.model.position.y + ship2.model.position.y) / 2
        distance = max(1, ship1.model.position.distance_to(ship2.model.position))
        scene_cam.position.z = 1.5 * distance
        scene_cam.update(elapsed_ms)

        context.clear(color=(0.0, 0.0, 0.0, 0.0))
        water_tiles.render(scene_cam)
        ship1.render(scene_cam)
        ship2.render(scene_cam)
        cannonballs.render(scene_cam)
        wind.render(gui_cam)
        pygame.display.flip()

        elapsed_ms = clock.tick(60)
        pygame.display.set_caption(f'FPS: {clock.get_fps():.1f} ({elapsed_ms}ms)'
                                   f'cam_at ({scene_cam.position.x:.1f}; {scene_cam.position.y:.1f}; '
                                   f'{scene_cam.position.z:.1f})')

    pygame.quit()


if __name__ == '__main__':
    main()
