import arcade
from textures import Textures
from consts import *


class EndView(arcade.View):
    def __init__(self):
        super().__init__()
        Textures.end_story_textures()
        self.texture = Textures.hero_with_cat
        self.text_png = Textures.konec

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.LRBT(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.text_png,
                                 arcade.LRBT(200 * SCALE, 600 * SCALE, SCREEN_HEIGHT - 400 * SCALE, SCREEN_HEIGHT),
                                 pixelated=True)
