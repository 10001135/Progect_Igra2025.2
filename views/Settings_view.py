import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton
from views.choose_music_view import MusicPopup


class SettingsPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.vki_music = True
        self.manager = UIManager()

        self.music_popup = MusicPopup(parent_view)
        self.music_popup_visible = False
        self.music_popup.on_back_to_settings = self.on_back_from_music

        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()

        Textures.textures_main_menu()

        buttons_textures = Textures.textures_in_menu['buttons']['style1']

        self.music_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=280 * SCALE,
            height=65 * SCALE,
            text="Music",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=400 * SCALE,
            height=65 * SCALE,
            text="Back to game",
            style=BUTTON_STYLE1)

        self.music_button.on_click = self.music
        self.close_button.on_click = self.close

        self.manager.add(self.music_button)
        self.manager.add(self.close_button)

        self.resize_positihon()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.music_popup_visible:
            self.music_popup.on_mouse_press(x, y, button, modifiers)
        elif self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.music_popup_visible:
            self.music_popup.on_mouse_release(x, y, button, modifiers)
        elif self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, key, modifiers):
        if self.music_popup_visible:
            if key == arcade.key.ESCAPE:
                self.music_popup.close()
        elif self.visible:
            if key == arcade.key.ESCAPE:
                self.close()

    def resize_positihon(self):
        if hasattr(self, 'music_button') and self.music_button:
            self.music_button.center_x = SCREEN_WIDTH // 2
            self.music_button.center_y = SCREEN_HEIGHT // 2 + 75 * SCALE

        if hasattr(self, 'close_button') and self.close_button:
            self.close_button.center_x = SCREEN_WIDTH // 2
            self.close_button.center_y = SCREEN_HEIGHT // 2 - 150 * SCALE

    def saves(self, event=None):
        print("Будет отдельное окно с сохранениями")

    def music(self, event=None):
        self.manager.disable()
        self.music_popup.show()
        self.music_popup_visible = True

    def show(self):
        self.setup_ui()
        self.visible = True
        self.music_popup_visible = False
        self.manager.enable()
        self.resize_positihon()

    def on_back_from_music(self):
        self.music_popup_visible = False

        self.manager.enable()

    def close(self, event=None):
        self.visible = False
        self.music_popup_visible = False

        self.manager.disable()

        if hasattr(self.music_popup, 'visible') and self.music_popup.visible:
            self.music_popup.close()

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
            color=arcade.color.PURPLE,
            border_width=3)

        arcade.draw_text(
            "НАСТРОЙКИ",
            SCREEN_WIDTH // 2,
            window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(SCREEN_WIDTH * 0.03)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

        if self.music_popup_visible:
            self.music_popup.draw()

    def on_resize(self, width, height):
        self.resize_positihon()
        self.music_popup.on_resize(width, height)
