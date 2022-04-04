from vector3d.vector import Vector


def dot(v1: Vector, v2: Vector):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


class Light:
    def __init__(self, position: Vector, strength: int):
        self.position = position
        self.strength = strength

    def get_lighting(self, position: Vector, normal: Vector):
        distance = (position - self.position).length()
        intensity = (1/(distance * distance)) * self.strength
        light_direction = (self.position - position).normalize()
        shading = (dot(normal, light_direction) / 3 + 1) / 2 + 0.5
        return intensity * shading
