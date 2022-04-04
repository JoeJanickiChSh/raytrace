import math

import pygame as pg
from vector3d.vector import Vector


class Mesh:

    def __init__(self, position: Vector, size: float, color: Vector, mirror: bool, texture: str = None, height: float = 0):
        self.position = position
        self.size = size
        self.color = color
        self.mirror = mirror
        self.texture = None if texture is None else pg.image.load(texture)
        self.height = height

    def hit(self, position: Vector) -> bool:
        return False

    def get_normal(self, position: Vector) -> Vector:
        return position.normalize()

    def get_reflection(self, position: Vector, direction: Vector) -> Vector:
        return self.get_normal(position)

    def get_uv(self, position: Vector) -> Vector:
        return Vector()

    def map_uv(self, uv):
        return (int(uv.x * self.texture.get_width()), int(uv.y * self.texture.get_height()))

    def get_color(self, position: Vector) -> Vector:
        if self.texture is None:
            return self.color
        else:
            color = self.texture.get_at(self.map_uv(self.get_uv(position)))
            color = tuple(map(lambda x: x / 255.0, color))
            return Vector(color[0], color[1], color[2])


class Scene():
    def __init__(self, *objects):
        self.objects = []
        for o in objects:
            self.objects.append(o)

    def add(self, *objects):
        for o in objects:
            self.objects.append(o)

    def get_hit(self, position: Vector, direction: Vector):
        for o in self.objects:
            if o.hit(position):
                return True, o.get_normal(position), o.get_reflection(position, direction), o.get_color(position), o.mirror, o
        return False, None, None, None, False, None


class Sphere(Mesh):
    def hit(self, position: Vector) -> bool:
        return (position - self.position).length() < self.size

    def get_normal(self, position: Vector) -> Vector:
        return (position - self.position).normalize()

    def get_reflection(self, position: Vector, direction: Vector) -> Vector:
        return self.get_normal(position)

    def get_uv(self, position: Vector) -> Vector:
        u = math.atan2(self.get_normal(position).x,
                       self.get_normal(position).z) / (math.tau) + 0.5
        v = self.get_normal(position).y * 0.5 + 0.5
        return Vector(u, v)


def xz(vec):
    return Vector(vec.x, vec.z, 0)


class Cylinder(Mesh):
    def hit(self, position: Vector) -> bool:
        if self.position.y - self.height < position.y < self.position.y + self.height:
            return (xz(position) - xz(self.position)).length() < self.size
        return False

    def get_normal(self, position: Vector) -> Vector:
        if self.position.y - self.height < position.y < self.position.y + self.height:
            sphere_normal = (position - self.position).normalize()
            sphere_normal.y = 0
            return sphere_normal
        elif position.y < self.position.y:
            return Vector(0, -1, 0)
        elif position.y > self.position.y:
            return Vector(0, 1, 0)

        return Vector()

    def get_reflection(self, position: Vector, direction: Vector) -> Vector:
        reflection = self.get_normal(position)
        reflection.y = direction.y
        return reflection

    def get_uv(self, position: Vector) -> Vector:
        return Vector()


class Ground(Mesh):
    def hit(self, position: Vector) -> bool:
        return position.y < self.position.y

    def get_normal(self, position: Vector) -> Vector:
        return Vector(0, 1, 0)

    def get_reflection(self, position: Vector, direction: Vector) -> Vector:
        return Vector(direction.x, abs(direction.y), direction.z)

    def get_uv(self, position: Vector) -> Vector:
        return Vector((position.x / 3.0) % 1, (position.z / 3.0) % 1)
