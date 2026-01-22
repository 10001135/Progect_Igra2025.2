import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class PausPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.manager = UIManager()

    def setup_ui(self):
        self.manager.clear()

        Textures.textures_main_menu()

        buttons_textures = Textures.textures_in_menu['buttons']['style1']

        self.saves_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=200*SCALE,
            height=50*SCALE,
            text="Сохранения",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=200*SCALE,
            height=50*SCALE,
            text="Закрыть",
            style=BUTTON_STYLE1)

        self.saves_button.on_click = self.saves
        self.close_button.on_click = self.close

        self.manager.add(self.saves_button)
        self.manager.add(self.close_button)

        self.resize_positihon()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def resize_positihon(self):
        width = SCREEN_WIDTH

        hiegh = SCREEN_HEIGHT

        self.saves_button.center_x = SCREEN_WIDTH // 2
        self.saves_button.center_y = SCREEN_HEIGHT // 2

        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - 150

    def saves(self, event=None):
        print("Будет отдельное окно с сохранениями")

    def show(self):
        self.visible = True
        self.manager.enable()
        self.resize_positihon()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()

    def draw(self):
        if not self.visible:
            return

        settings_width = SCREEN_WIDTH * 0.6
        settings_hieg = SCREEN_HEIGHT * 0.7

        settings_width = max(300, settings_width)
        settings_hieg = max(400, settings_hieg)

        window_left = SCREEN_WIDTH // 2 - settings_width // 2
        window_right = window_left + settings_width
        window_bottom = SCREEN_HEIGHT // 2 - settings_hieg // 2
        window_top = window_bottom + settings_hieg

        arcade.draw_lrbt_rectangle_filled(
            left=window_left,
            right=window_right,
            top=window_top,
            bottom=window_bottom,
            color=(0, 0, 0, 200))

        arcade.draw_lrbt_rectangle_outline(
            left=window_left,
            right=window_right,
            top=window_top,
            bottom=window_bottom,
            color=arcade.color.BLACK,
            border_width=3)

        arcade.draw_text(
            "Пауза",
            SCREEN_WIDTH // 2,
            window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(SCREEN_WIDTH * 0.03)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

    def on_resize(self, width, height):
        self.resize_positihon()
