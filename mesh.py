import math
from vector3d.vector import Vector
from vecmath import dot


class Scene:
    def __init__(self, background, light, *meshes):
        self.meshes = meshes
        self.background = background
        self.light = light

    def get_closest_distance(self, ray):
        closest_distance = 1e10
        closest_object = None
        for mesh in self.meshes:
            if mesh.get_distance(ray) < closest_distance:
                closest_distance = mesh.get_distance(ray)
                closest_object = mesh
        return closest_distance, closest_object


class Mesh:
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material

    def get_distance(self, ray):
        return 1

    def get_reflection(self, ray, direction):
        return direction - (self.get_normal(ray) * dot(direction, self.get_normal(ray)) * 2)

    def get_normal(self, ray):
        return Vector(0, 1, 0)

    def get_uv(self, ray):
        return Vector(0, 0)

    def get_color(self, ray):
        return self.material.get_color(self.get_uv(ray))


class Ground(Mesh):
    def get_distance(self, ray):
        return ray.y - self.position.y

    def get_normal(self, ray):
        return Vector(0, 1, 0)


    def get_uv(self, ray):
        return Vector((ray.x / 4) % 8, (-ray.z / 8) % 1)


class Sphere(Mesh):
    def get_distance(self, ray):
        return (self.position - ray).length() - self.size

    def get_normal(self, ray):
        return (ray - self.position).normalize()

    def get_uv(self, ray):
        # n = Normalize(sphere_surface_point - sphere_center)
        # u = atan2(n.x, n.z) / (2*pi) + 0.5
        # v = n.y * 0.5 + 0.5

        n = self.get_normal(ray)

        u = math.atan2(n.x, n.z) / (2 * math.pi) + 0.5
        v = n.y * 0.5 + 0.5

        return Vector(u, v)
