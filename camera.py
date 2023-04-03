import pygame
import glm


FOV = 50
NEAR = 0.01
FAR = 10000
CAM_SPEED = 0.001


class Camera:
    def __init__(self, window: pygame.Surface):
        self.window_size = window.get_size()
        self.aspect_ratio = self.window_size[0] / self.window_size[1]

        self.position = glm.vec3(0, 0, 1)
        self.rotation = 0.0

        self.right = glm.vec3(1, 0, 0)
        self.up = glm.vec3(0, 1, 0)
        self.into = glm.vec3(0, 0, 1)

        self.m_view = self.get_view_matrix()
        self.m_proj = self.get_projection_matrix()

    def update(self, elapsed_ms: int) -> None:
        # consider camera speed, elapsed time and zoom (z-position)
        """
        velocity = CAM_SPEED * elapsed_ms * self.position.z
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.position += self.up * velocity
        if keys[pygame.K_s]:
            self.position -= self.up * velocity
        if keys[pygame.K_d]:
            self.position += self.right * velocity
        if keys[pygame.K_a]:
            self.position -= self.right * velocity
        """
        """
        if keys[pygame.K_q]:
            self.position += self.into * velocity
        if keys[pygame.K_e]:
            self.position -= self.into * velocity
        """

        # limit z-position
        if self.position.z <= 0:
            self.position.z = 0.1
        # FIXME: implement camera rotation but also rotate up/right vectors accordingly

        self.m_view = self.get_view_matrix()

    def get_view_matrix(self) -> glm.mat4x4:
        """Recalculate view matrix after camera got moved"""
        up_vector = glm.rotate(self.up, glm.radians(self.rotation), glm.vec3(0.0, 0.0, 1.0))
        return glm.lookAt(self.position, self.position - self.into, up_vector)

    def get_projection_matrix(self) -> glm.mat4x4:
        """Calculate projection matrix once"""
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)


class GuiCamera(Camera):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)

    def get_view_matrix(self) -> glm.mat4x4:
        return glm.lookAt(glm.vec3(0, 0, 1), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    def get_projection_matrix(self) -> glm.mat4x4:
        return glm.ortho(0, self.window_size[0], 0, self.window_size[1], NEAR, FAR)
