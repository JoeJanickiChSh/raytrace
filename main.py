from math import sqrt
import math
from random import randint, randrange
from socket import close
import pygame as pg
from vector3d.vector import Vector
from material import Material
import threading
from mesh import Ground, Scene, Sphere


from vecmath import dot, lerp, vec_to_color


def trace_color(start, direction, scene, reflections):
    ray = start * 1
    color = scene.background
    ray_direction = direction * 1
    reflected_color = scene.background
    glossy = 0
    for _ in range(60):
        closest_distance, closest_object = scene.get_closest_distance(
            ray)
        ray += ray_direction * closest_distance
        if closest_object is None:
            glossy = 0
        else:
            glossy = closest_object.material.glossy

        if closest_distance < 0.1:
            if reflections > 0:
                reflection = closest_object.get_reflection(
                    ray, ray_direction)
                reflected_color = trace_color(
                    ray + reflection * 0.9, reflection, scene, reflections - 1)
            else:
                reflected_color = scene.background

            light_direction = scene.light
            color = (closest_object.get_color(ray) *
                     (dot(closest_object.get_normal(ray),
                          light_direction) / 2 + 0.4))

            for _ in range(20):
                ray_direction = scene.light
                n_distance, n_object = scene.get_closest_distance(
                    ray)
                ray += ray_direction * n_distance
                if n_distance < 0.1 and n_object != closest_object:
                    color *= 0.5
                    break

            break
    return lerp(color, reflected_color, glossy)


def trace_thread(x_start, y_start, x_size, y_size, scene, surface):
    width, height = surface.get_size()
    for pixel_x in range(x_start, x_start + x_size):
        for pixel_y in range(y_start, y_start + y_size):
            x = (pixel_x / width) * 2 - 1
            y = -((pixel_y / height) * 2 - 1)
            ray_direction = Vector(
                x, y * (height / width), 1).normalize()

            ray = Vector()
            color = trace_color(ray, ray_direction, scene, 5)
            color.x = sqrt(max(0, color.x))
            color.y = sqrt(max(0, color.y))
            color.z = sqrt(max(0, color.z))
            surface.set_at((pixel_x, pixel_y), vec_to_color(color))


def main():
    THREAD_DIVISIONS = 4
    pg.init()
    d = pg.display.set_mode((800, 600))

    scene = Scene(
        Vector(0.2, 0.6, 0.8),
        Vector(-1, 1, -1).normalize(),
        Ground(Vector(0, -1, 0), 1, Material(Vector(1, 1, 1), 0.2, 'wood.png')),
        Sphere(Vector(-3, 0, 5), 1, Material(Vector(1, 1, 1), 0.5, 'metal.png')),
        Sphere(Vector(0, 0, 7), 1, Material(
            Vector(1, 1, 1), 0.5, 'metal.png')),
        Sphere(Vector(2, 0, 3), 1, Material(
            Vector(1, 1, 1), 0.5, 'metal.png')),
    )

    width, height = d.get_size()

    thread_width = width // THREAD_DIVISIONS
    thread_height = height // THREAD_DIVISIONS

    for x in range(THREAD_DIVISIONS):
        for y in range(THREAD_DIVISIONS):
            t = threading.Thread(target=trace_thread, args=[
                x * thread_width, y * thread_height, thread_width, thread_height, scene, d])
            t.start()

            print(f"Thread Started: ({x}, {y})")

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                quit()
            elif e.type == pg.KEYDOWN:
                pg.image.save(d, 'out.png')
        pg.display.update()


if __name__ == '__main__':
    main()
