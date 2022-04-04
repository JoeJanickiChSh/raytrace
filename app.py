import pygame as pg

from render import Renderer


def vec_to_color(v):
    return tuple(map(lambda x: min(255, max(0, int(x*255))), [v.x, v.y, v.z]))


class App:
    def __init__(self, width: int, height: int, title: str, ray_length: int, ray_step: float):

        pg.display.set_caption(title)
        self.window = pg.display.set_mode((width, height))
        self.renderer = Renderer(width, height, ray_length, ray_step)
        self.running = True

        self.width = width
        self.height = height
        self.ray_length = ray_length
        self.ray_step = ray_step

    def run(self):
        x = 0
        y = 0
        steps = 100
        while self.running:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit
                    self.running = False

            for i in range(steps):
                if y < self.height:
                    pixel = vec_to_color(self.renderer.render_at(x, y))
                    self.window.set_at((x, y), pixel)
                    x += 1
                    if x >= self.width:
                        x = 0
                        y += 1
            pg.display.update()
