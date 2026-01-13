import arcade
from consts import *
from arcade.gui import UIManager, UITextureButton


class SettingsPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.manager = UIManager()
        self.setup_ui()

    def setup_ui(self):
        self.manager.enable()

        close_button = UITextureButton(
            texture=self.parent_view.textures['buttons']['style1']['normal'],
            texture_hovered=self.parent_view.textures['buttons']['style1']['hovered'],
            texture_pressed=self.parent_view.textures['buttons']['style1']['pressed'],
            width=200,
            height=50,
            text="Закрыть",
            style=BUTTON_STYLE1)

        close_button.center_x = SCREEN_WIDTH // 2
        close_button.center_y = 50
        close_button.on_click = self.close

        self.manager.add(close_button)

    def show(self):
        self.visible = True
        self.manager.enable()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()

    def draw(self):
        if not self.visible:
            return

        window_width = 600
        window_height = 600
        window_left = SCREEN_WIDTH // 2 - window_width // 2
        window_right = window_left + window_width
        window_bottom = SCREEN_HEIGHT // 2 - window_height // 2
        window_top = window_bottom + window_height

        arcade.draw_lrbt_rectangle_filled(
            left=window_left,
            right=window_right,
            top=window_top,
            bottom=window_bottom,
            color=TRANSPARENT_BLACK)

        arcade.draw_lrbt_rectangle_outline(
            left=window_left,
            right=window_right,
            top=window_top,
            bottom=window_bottom,
            color=arcade.color.BLACK,
            border_width=3)

        arcade.draw_text(
            "НАСТРОЙКИ",
            SCREEN_WIDTH // 2,
            window_top - 50,
            arcade.color.WHITE,
            24,
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)