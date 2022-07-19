import pygame as pg
from vector3d.vector import Vector


class Material:
    def __init__(self, color, glossy, texture=None):
        self.color = color
        self.glossy = glossy
        if texture is None:
            self.texture = pg.Surface((1, 1))
            self.texture.fill((255, 255, 255))
        else:
            self.texture = pg.image.load(texture)

    def get_pixel(self, uv):
        width, height = self.texture.get_size()

        x = int(min(1, max(0, uv.x)) * (width-1))
        y = int(min(1, max(0, uv.y)) * (height-1))

        color = self.texture.get_at((x, y))
        out = Vector(color[0] / 255, color[1] / 255, color[2] / 255)
        return out

    def get_color(self, uv):
        tex_color = self.get_pixel(uv)

        return Vector(tex_color.x * self.color.x, tex_color.y * self.color.y, tex_color.z * self.color.z)
