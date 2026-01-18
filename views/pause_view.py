import arcade
import textures
from pyglet.graphics import Batch


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(100, 100, 200, arcade.color.GREEN)

    def on_update(self, delta_time):
        print(textures.Textures.pvt)
        textures.Textures.f2()
        self.window.show_view(self.game_view)
