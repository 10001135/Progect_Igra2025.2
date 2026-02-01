import arcade
import math
from consts import SCALE
from textures import Textures


class Visor(arcade.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        Textures.textures_future_level_2()
        self.textures = Textures.visor
        self.texture = self.textures[0]
        self.texture_change_time = 0
        self.texture_change_delay = 2
        self.current_texture = 0
        self.scale = SCALE * 0.5
        self.position = (x1, y1)
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)
        self.time = 0
        self.float_speed = 1.5

    def update(self, delta_time):
        self.time += delta_time * self.float_speed
        sine_value = math.sin(self.time)
        distance = self.end_pos[1] - self.start_pos[1]
        offset = (sine_value + 1) / 2
        self.center_y = self.start_pos[1] + distance * offset

    def update_animation(self, delta_time):
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.current_texture += 1
            if self.current_texture >= len(self.textures):
                self.current_texture = 0
        self.texture = self.textures[self.current_texture]