import arcade
from consts import *
from audioplayer import AudioPlayer
from arcade.gui import UIManager, UITextureButton


class SettingsPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.play_music = True
        self.player = AudioPlayer("assets/music/standart.mp3")
        self.manager = UIManager()
        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()
        self.music_button = UITextureButton(
            texture=self.parent_view.textures['buttons']['style1']['normal'],
            texture_hovered=self.parent_view.textures['buttons']['style1']['hovered'],
            texture_pressed=self.parent_view.textures['buttons']['style1']['pressed'],
            width=200,
            height=50,
            text="Музыка",
            style=BUTTON_STYLE1)

        self.saves_button = UITextureButton(
            texture=self.parent_view.textures['buttons']['style1']['normal'],
            texture_hovered=self.parent_view.textures['buttons']['style1']['hovered'],
            texture_pressed=self.parent_view.textures['buttons']['style1']['pressed'],
            width=200,
            height=50,
            text="Сохранения",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=self.parent_view.textures['buttons']['style1']['normal'],
            texture_hovered=self.parent_view.textures['buttons']['style1']['hovered'],
            texture_pressed=self.parent_view.textures['buttons']['style1']['pressed'],
            width=200,
            height=50,
            text="Закрыть",
            style=BUTTON_STYLE1)

        self.saves_button.on_click = self.saves
        self.music_button.on_click = self.music
        self.close_button.on_click = self.close

        self.manager.add(self.music_button)
        self.manager.add(self.saves_button)
        self.manager.add(self.close_button)

        self.resize_positihon()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible and self.manager:
            pass

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible and self.manager:
            pass

    def resize_positihon(self):
        width = self.parent_view.window.width

        hiegh = self.parent_view.window.height

        self.music_button.center_x = width // 2
        self.music_button.center_y = hiegh // 2 + 75

        self.saves_button.center_x = width // 2
        self.saves_button.center_y = hiegh // 2

        self.close_button.center_x = width // 2
        self.close_button.center_y = hiegh // 2 - 150

    def saves(self, event=None):
        print("Будет отдельное окно с сохранениями")

    def music(self, event=None):
        if self.play_music:
            self.player.play(loop=-1)
            self.play_music = False
        else:
            self.player.stop()
            self.play_music = True

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

        win_w = self.parent_view.window.width
        win_h = self.parent_view.window.height

        popup_width = win_w * 0.6
        popup_height = win_h * 0.7

        popup_width = max(300, popup_width)
        popup_height = max(400, popup_height)

        window_left = win_w // 2 - popup_width // 2
        window_right = window_left + popup_width
        window_bottom = win_h // 2 - popup_height // 2
        window_top = window_bottom + popup_height

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
            win_w // 2,
            window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(win_w * 0.03)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

    def on_resize(self, width, height):
        self.resize_positihon()
