import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class PausPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.music = True
        self.music_play = arcade.Sound(":assets/music/standart.mp3", streaming=True)
        self.manager = UIManager()

    def setup_ui(self):
        self.manager.clear()

        Textures.textures_main_menu()

        buttons_textures = Textures.textures_in_menu['buttons']['style1']

        self.music1 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="1",
            style=BUTTON_STYLE1)

        self.music2 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="2",
            style=BUTTON_STYLE1)

        self.music3 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="3",
            style=BUTTON_STYLE1)

        self.music4 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="4",
            style=BUTTON_STYLE1)

        self.music5 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="5",
            style=BUTTON_STYLE1)

        self.music6 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="6",
            style=BUTTON_STYLE1)

        self.music7 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="7",
            style=BUTTON_STYLE1)

        self.music8 = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="8",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=280 * SCALE,
            height=65 * SCALE,
            text="Continue",
            style=BUTTON_STYLE1)

        self.close_button.on_click = self.close

        self.manager.add(self.close_button)

        self.resize_positihon()

    def set_music1(self):
        self.music_play = arcade.Sound(":assets/music/standart.mp3", streaming=True)
        self.play_music()

    def set_music2(self):
        self.music_play = arcade.Sound(":assets/music/music2.mp3", streaming=True)
        self.play_music()

    def set_music3(self):
        self.music_play = arcade.Sound(":assets/music/music3.mp3", streaming=True)
        self.play_music()

    def set_music4(self):
        self.music_play = arcade.Sound(":assets/music/music4.mp3", streaming=True)
        self.play_music()

    def set_music5(self):
        self.music_play = arcade.Sound(":assets/music/standart(cyber).ogg", streaming=True)
        self.play_music()

    def set_music6(self):
        self.music_play = arcade.Sound(":assets/music/music6.ogg", streaming=True)
        self.play_music()

    def set_music7(self):
        self.music_play = arcade.Sound(":assets/music/music7.ogg", streaming=True)
        self.play_music()

    def set_music8(self):
        self.music_play = arcade.Sound(":assets/music/music8.ogg", streaming=True)
        self.play_music()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def resize_positihon(self):
        self.music1.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music1.center_y = SCREEN_HEIGHT // 2 + 75 * SCALE

        self.music2.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music2.center_y = SCREEN_HEIGHT // 2 + 25 * SCALE

        self.music3.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music3.center_y = SCREEN_HEIGHT // 2 - 25 * SCALE

        self.music4.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music4.center_y = SCREEN_HEIGHT // 2 - 75 * SCALE

        self.music5.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music5.center_y = SCREEN_HEIGHT // 2 + 75 * SCALE

        self.music6.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music6.center_y = SCREEN_HEIGHT // 2 + 25 * SCALE

        self.music7.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music7.center_y = SCREEN_HEIGHT // 2 - 25 * SCALE

        self.music8.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music8.center_y = SCREEN_HEIGHT // 2 - 75 * SCALE

        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - 250 * SCALE

    def play_music(self, event=None):
        if self.music:
            self.music_play.play(volume=0.5, loop=True)
        else:
            arcade.stop_sound(self.music_play)

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
            color=arcade.color.GOLD,
            border_width=3)

        arcade.draw_text(
            "Music",
            SCREEN_WIDTH // 2,
            window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(SCREEN_WIDTH * 0.03)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

    def on_resize(self, width, height):
        self.resize_positihon()
