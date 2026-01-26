import arcade
from consts import *
from audioplayer import AudioPlayer
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class SettingsPopup:
    def __init__(self):
        self.visible = False
        self.vki_music = True
        self.musik = AudioPlayer("assets/music/standart.mp3")
        self.manager = UIManager()
        Textures.textures_main_menu()
        self.textures = Textures.textures_in_menu['buttons']['style1']
        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()
        self.music_button = UITextureButton(
            texture=self.textures['buttons']['style1']['normal'],
            texture_hovered=self.textures['buttons']['style1']['hovered'],
            texture_pressed=self.textures['buttons']['style1']['pressed'],
            width=200,
            height=50,
            text="Музыка",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=self.textures['buttons']['style1']['normal'],
            texture_hovered=self.textures['buttons']['style1']['hovered'],
            texture_pressed=self.textures['buttons']['style1']['pressed'],
            width=200,
            height=50,
            text="Назад",
            style=BUTTON_STYLE1)

        self.music_button.on_click = self.music
        self.close_button.on_click = self.close

        self.manager.add(self.music_button)
        self.manager.add(self.close_button)

        self.resize_positihon()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def resize_positihon(self):
        width = self.parent_view.window.width

        hiegh = self.parent_view.window.height

        self.music_button.center_x = width // 2
        self.music_button.center_y = hiegh // 2 + 75

        self.close_button.center_x = width // 2
        self.close_button.center_y = hiegh // 2 - 150

    def music(self, event=None):
        if self.vki_music:
            self.musik.play(loop=-1)
            self.vki_music = False
        else:
            self.musik.stop()
            self.vki_music = True

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

        window_width = self.parent_view.window.width
        window_hieg = self.parent_view.window.height

        settings_width = window_width * 0.6
        settings_hieg = window_hieg * 0.7

        settings_width = max(300, settings_width)
        settings_hieg = max(400, settings_hieg)

        window_left = window_width // 2 - settings_width // 2
        window_right = window_left + settings_width
        window_bottom = window_hieg // 2 - settings_hieg // 2
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
            "НАСТРОЙКИ",
            window_width // 2,
            window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(window_width * 0.03)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

    def on_resize(self, width, height):
        self.resize_positihon()
