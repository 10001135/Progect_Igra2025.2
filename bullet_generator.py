import arcade
from consts import *
from textures import Textures


class Bullet(arcade.Sprite):
    def __init__(self, x, y, direction=1):
        super().__init__(Textures.bullet)
        self.center_x = x
        self.center_y = y
        self.scale = SCALE * 2.3
        self.do_round = 0
        self.direction = direction

    def update(self, delta_time):
        self.do_round += delta_time
        self.center_x += 250 * SCALE * delta_time * self.direction
        if self.do_round >= 0.05:
            self.angle += 3
            self.do_round = 0


class BulletGenerator:
    def __init__(self, x, y, direction=1):
        self.start_x = x
        self.start_y = y
        self.direction = direction
        self.bullet_list = arcade.SpriteList(use_spatial_hash=True)
        self.since_last_bullet = 0

    def update(self, delta_time):
        self.bullet_list.update(delta_time)
        self.since_last_bullet += delta_time
        if self.since_last_bullet >= 5:
            self.since_last_bullet = 0
            self.bullet_list.append(Bullet(self.start_x, self.start_y, self.direction))

    def on_draw(self):
        self.bullet_list.draw(pixelated=True)
