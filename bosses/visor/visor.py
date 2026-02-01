import arcade
import math
from consts import SCALE
from textures import Textures
from consts import *


class Visor(arcade.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        Textures.textures_future_level_2()
        Textures.texture_gui()
        self.textures = Textures.visor['Visor']
        self.texture = self.textures[0]
        self.position = (x1, y1)
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)
        self.time = 0
        self.float_speed = 1.5
        self.is_attacking = False
        self.is_damaging = False
        self.health = 3
        self.max_health = 3
        self.gui_camera = arcade.camera.Camera2D()

    def update(self, delta_time):
        self.time += delta_time * self.float_speed
        sine_value = math.sin(self.time)
        distance = self.end_pos[1] - self.start_pos[1]
        offset = (sine_value + 1) / 2
        self.center_y = self.start_pos[1] + distance * offset
        if self.is_attacking:
            self.texture = Textures.visor_attach
        elif self.is_damaging:
            self.texture = Textures.visor_damage
        else:
            if offset < 0.33:
                self.texture = self.textures[2]
                self.scale = SCALE * 0.5
            elif offset < 0.66:
                self.texture = self.textures[1]
                self.scale = SCALE * 0.5
            else:
                self.texture = self.textures[0]
                self.scale = SCALE * 0.5

    def attack_state(self):
        self.is_attacking = True
        self.is_damaging = False

    def damage_state(self):
        self.is_damaging = True
        self.is_attacking = False

    def draw_hearts(self):
        self.hearts = arcade.SpriteList()
        for h in range(self.max_health):
            if h <= self.health - 1:
                self.hearts.append(
                    arcade.Sprite(Textures.gui['HeartBoss'], 4 * SCALE, self.center_x - 65 * SCALE + (h * 65),
                                  self.top + 30 * SCALE))
            else:
                self.hearts.append(
                    arcade.Sprite(Textures.gui['Unheart'], 4 * SCALE, self.center_x - 65 * SCALE + (h * 65),
                                  self.top + 30 * SCALE))
        self.hearts.draw(pixelated=True)
