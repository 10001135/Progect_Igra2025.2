import arcade
from consts import *
from textures import Textures
from texts import text_d
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class Inventory(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(100, 100, 200, arcade.color.GREEN)