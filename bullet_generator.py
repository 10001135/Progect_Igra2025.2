import arcade
from consts import *
from textures import Textures


class Bullet(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(Textures.bullet)
        self.center_x = x
        self.center_y = y

    def update(self, delta_time):
        self.center_x += 250 * SCALE * delta_time


class BulletGenerator(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.start_x = x
        self.start_y = y
        self.bullet_list = arcade.SpriteList(use_spatial_hash=True)
        self.since_last_bullet = 0

    def update(self, delta_time):
        self.bullet_list.update(delta_time)
        self.since_last_bullet += delta_time
        if self.since_last_bullet >= 6:
            self.since_last_bullet = 0
            self.bullet_list.append(Bullet(self.start_x, self.start_y))

    def on_draw(self):
        self.bullet_list.draw(pixelated=True)