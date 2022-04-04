import math
from vector3d.vector import Vector

from light import Light
from mesh import Cylinder, Ground, Scene, Sphere


def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z


class Renderer:
    def __init__(self, width: int, height: int, ray_length: int, ray_step: float):
        self.width = width
        self.height = height
        self.ray_length = ray_length
        self.ray_step = ray_step
        self.aspect = height/width
        color = Vector(247, 178, 109) * (1/255)
        self.scene = Scene(
            Ground(Vector(0, -1, 0), 1, Vector(0.6,
                   0.9, 0.6), False, 'grass.png'),
            Sphere(Vector(0.5, -0.25, 3), 0.5, color, False),
            Sphere(Vector(-0.5, -0.25, 3), 0.5, color, False),
            Cylinder(Vector(0, 0, 0), 0.5, color, False, height=3)
        )

        self.light = Light(Vector(2, 2, -2), 10)

    def tone_map(self, color: Vector) -> Vector:
        return Vector(math.sqrt(color.x), math.sqrt(color.y), math.sqrt(color.z))

    def render_at(self, pixel_x: int, pixel_y: int) -> Vector:
        x = (pixel_x / self.width) * 2 - 1
        y = -((pixel_y / self.height) * 2 - 1) * self.aspect

        ray = Vector()
        ray_dir = Vector(x, y, 1).normalize()
        step = 0
        trace = True
        out_color = Vector(0.2, 0.2, 0.2)
        while trace and step < self.ray_length:
            ray += ray_dir * self.ray_step
            hit, normal, reflection, color, mirror, obj = self.scene.get_hit(
                ray, ray_dir)
            if hit:
                if mirror:
                    ray_dir = reflection * 1
                else:
                    out_color = color * self.light.get_lighting(ray, normal)
                    ray_dir = (self.light.position - ray).normalize()
                    shadow_trace = True
                    shadow_step = 0
                    while shadow_trace and shadow_step < self.ray_length:
                        ray += ray_dir * self.ray_step
                        hit, normal, reflection, color, mirror, new_obj = self.scene.get_hit(
                            ray, ray_dir)
                        if hit and (obj != new_obj):
                            out_color = out_color * 0.5
                            shadow_trace = False

                        shadow_step += 1

                    trace = False
            step += 1
        return self.tone_map(out_color)
