import pygame
import moderngl
import numpy
import glm

from typing import List


vertex_shader = """
#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_position;

out vec2 uv_0;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    uv_0 = in_texcoord_0;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}"""


fragment_shader = """
#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0;

void main() {
    vec4 texColor = texture(u_texture_0, uv_0);
    vec3 color = texColor.rgb * texColor.a;
    fragColor = vec4(color, texColor.a);
}"""


def create_texture(ctx: moderngl.Context, img: pygame.Surface) -> moderngl.Texture:
    tex = ctx.texture(size=img.get_size(), components=4, data=pygame.image.tostring(img, 'RGBA', True))
    tex.filter = moderngl.NEAREST, moderngl.NEAREST
    return tex


class Quad:
    def __init__(self, ctx: moderngl.Context, pos: pygame.math.Vector2, size: pygame.math.Vector2):
        self.position = pos
        self.rotation = 0
        self.z_pos = 0
        w, h = size.xy

        # build vertex data
        vertices = [(-w/2, -h/2, 0.0), (w/2, -h/2, 0.0), (w/2, h/2, 0.0), (-w/2, h/2, 0.0)]
        indices = [(0, 1, 2), (0, 2, 3)]
        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 1, 2), (0, 2, 3)]

        # create vertices
        def build_vertices(vertices_array, indices_array) -> numpy.array:
            data = [vertices_array[ind] for triangle in indices_array for ind in triangle]
            return numpy.array(data, dtype='f4')

        vertex_data = build_vertices(vertices, indices)
        tex_coord_data = build_vertices(tex_coord, tex_coord_indices)
        vertex_data = numpy.hstack([tex_coord_data, vertex_data])

        # create vertex buffer object, shader program and vertex array object
        self.vbo = ctx.buffer(vertex_data)
        self.shader = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.vao = ctx.vertex_array(self.shader, [(self.vbo, '2f 3f', 'in_texcoord_0', 'in_position')])

        # apply textures
        self.texture = None
        self.texture_index = 0
        self.shader['u_texture_0'] = 0

    def __del__(self):
        self.vbo.release()
        self.shader.release()
        self.vao.release()

    def render(self, m_view: glm.mat4x4, m_proj: glm.mat4x4) -> None:
        if self.texture is None:
            return

        m_model = glm.translate(glm.mat4(), glm.vec3(*self.position, self.z_pos))
        m_model *= glm.rotate(glm.mat4(), glm.radians(self.rotation), glm.vec3(0, 0, 1))

        self.texture.use()
        self.shader['m_model'].write(m_model)
        self.shader['m_view'].write(m_view)
        self.shader['m_proj'].write(m_proj)

        self.vao.render()


# ---------------------------------------------------------------------------------------------------------------------

class Animator(object):
    def __init__(self, tex_list: List[moderngl.Texture], animation_delay: int):
        self.texture_list = tex_list
        self.texture_index = 0

        self.animation_delay = animation_delay
        self.elapsed_time = 0

    def update(self, elapsed_ms: int, quad: Quad) -> None:
        needs_update = quad.texture is None

        self.elapsed_time += elapsed_ms
        if self.elapsed_time > self.animation_delay:
            self.elapsed_time -= self.animation_delay
            self.texture_index = (self.texture_index + 1) % len(self.texture_list)
            needs_update = True

        if needs_update:
            quad.texture = self.texture_list[self.texture_index]
