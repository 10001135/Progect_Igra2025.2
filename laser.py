import arcade
from consts import *
from textures import Textures


class Laser:
    def __init__(self, x1, y1, x2):
        self.x1 = x1
        self.x2 = x2
        self.y = y1
        self.left = x1
        self.right = x2
        self.center_y = y1
        self.center_x = (x1 + x2) / 2
        self.width = abs(x2 - x1)
        self.height = 10 * SCALE
        self.scale = SCALE * 0.5
        self.time_accumulator = 0.0
        self.blink_interval = 0.3
        self.blink_count = 0
        self.max_blinks = 3
        self.is_active = False
        self.active_timer = 0.0
        self.active_duration = 0.3
        self.cycle_count = 0
        self.max_cycles = 3
        self.alpha = 100

    def draw(self):
        color = (255, 0, 0, self.alpha)
        line_width = 5 * SCALE if self.is_active else 4 * SCALE

        arcade.draw_line(
            self.x1,
            self.y,
            self.x2,
            self.y,
            color,
            line_width
        )

    def update(self, delta_time):
        if self.cycle_count >= self.max_cycles:
            self.alpha = 0
            return

        if self.is_active:
            self.alpha = 255
            self.active_timer += delta_time

            if self.active_timer >= self.active_duration:
                self.is_active = False
                self.active_timer = 0.0
                self.blink_count = 0
                self.cycle_count += 1
                self.alpha = 100
            return
        self.time_accumulator += delta_time

        if self.time_accumulator >= self.blink_interval:
            self.time_accumulator = 0
            self.blink_count += 1
            if self.alpha == 100:
                self.alpha = 50
            else:
                self.alpha = 100
            if self.blink_count >= self.max_blinks * 2:
                self.is_active = True