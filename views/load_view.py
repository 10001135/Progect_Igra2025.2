import arcade

from texts import text_d
from camera_for_hero import CameraForHero
from consts import *
from random import choice


class LoadView(arcade.View):
    def __init__(self, hero, level_from, level_to):
        super().__init__()
        self.hero = hero
        self.level_from = level_from
        self.level_to = level_to
        self.clear(color=(21, 32, 59))
        self.world_camera = CameraForHero()
        self.world_camera.use()
        texts = text_d['load_text'].split('|')
        text = choice(texts)
        font_size = int(40 * SCALE)
        text_size = font_size * len(text) / 2
        text_a = arcade.Text(text, SCREEN_WIDTH / 2 - text_size * SCALE, SCREEN_HEIGHT / 2, color=(182, 154, 122),
                             font_name='Comic Sans MS pixel rus eng', font_size=font_size)
        text_a.position = ((SCREEN_WIDTH / 2) - (text_a.content_width / 2), SCREEN_HEIGHT / 2)
        text_a.draw()

    def on_update(self, delta_time):
        self.window.show_view(self.level_to(self.hero, self.level_from))
