import arcade
from consts import *
from textures import Textures


class Razor(arcade.Sprite):
    def __init__(self, x1, y1, direction=1):
        super().__init__(Textures.razor)
        self.center_x = x1
        self.center_y = y1
        self.scale = SCALE * 0.5
        self.do_round = 0
        self.direction = direction

    def update(self, delta_time):
        self.do_round += delta_time
        self.center_x += 250 * SCALE * delta_time * self.direction
        if self.do_round >= 0.01:
            self.angle += 5
            self.do_round = 0