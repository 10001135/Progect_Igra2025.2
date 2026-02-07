import arcade
import sys
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton
from views.Settings_view import SettingsPopup


class PausPopup(arcade.View):
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.visible = False
        self.manager = UIManager()

        self.settings_popup = SettingsPopup(parent_view)
        self.settings_popup_visible = False

    def setup_ui(self):
        self.manager.clear()
        Textures.textures_main_menu()

        buttons_textures = Textures.textures_in_menu['buttons']['style1']

        self.saves_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=300 * SCALE,
            height=65 * SCALE,
            text="Settings",
            style=BUTTON_STYLE1)

        self.main_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=300 * SCALE,
            height=65 * SCALE,
            text="To_Menu",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=300 * SCALE,
            height=65 * SCALE,
            text="Continue",
            style=BUTTON_STYLE1)

        self.saves_button.on_click = self.saves
        self.main_button.on_click = self.main_menu
        self.close_button.on_click = self.close

        self.manager.add(self.saves_button)
        self.manager.add(self.main_button)
        self.manager.add(self.close_button)

        self.resize_position()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.settings_popup_visible:
            self.settings_popup.on_mouse_press(x, y, button, modifiers)
        elif self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.settings_popup_visible:
            self.settings_popup.on_mouse_release(x, y, button, modifiers)
        elif self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def main_menu(self, event=None):
        del sys.modules['views.main_menu_view']

        from views.main_menu_view import MainMenuView

        main_menu_view = MainMenuView()
        self.window.show_view(main_menu_view)

    def resize_position(self):
        self.saves_button.center_x = SCREEN_WIDTH // 2
        self.saves_button.center_y = SCREEN_HEIGHT // 2 + 100 * SCALE

        self.main_button.center_x = SCREEN_WIDTH // 2
        self.main_button.center_y = SCREEN_HEIGHT // 2

        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - 100 * SCALE

    def saves(self, event=None):
        self.close_pause_only()
        self.settings_popup_visible = True
        self.settings_popup.show()
        self.settings_popup.manager.enable()
        self.manager.disable()

    def close_pause_only(self):
        self.visible = False
        self.manager.disable()

    def show(self):
        self.visible = True
        self.settings_popup_visible = False
        self.resize_position()
        self.settings_popup.manager.disable()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()
        self.settings_popup_visible = False
        self.settings_popup.close()
        self.window.show_view(self.parent_view)

    def on_draw(self):
        self.parent_view.on_draw()
        if not self.settings_popup.visible:
            self.manager.enable()

        settings_width = SCREEN_WIDTH * 0.6
        settings_height = SCREEN_HEIGHT * 0.7

        settings_width = max(300, settings_width)
        settings_height = max(400, settings_height)

        window_left = SCREEN_WIDTH // 2 - settings_width // 2
        window_right = window_left + settings_width
        window_bottom = SCREEN_HEIGHT // 2 - settings_height // 2
        window_top = window_bottom + settings_height

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
            color=arcade.color.PINK,
            border_width=3)

        arcade.draw_text(
            "Pause",
            SCREEN_WIDTH // 2,
            window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(SCREEN_WIDTH * 0.03)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

        if self.settings_popup_visible:
            self.settings_popup.draw()

    def on_resize(self, width, height):
        if self.visible:
            self.resize_position()
        if self.settings_popup_visible:
            self.settings_popup.on_resize(width, height)
