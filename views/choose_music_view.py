import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton
from views.Settings_view import SettingsPopup


class MusicPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.music = True
        self.music_play = arcade.Sound("assets/music/standart.mp3", streaming=True)
        self.mus_p = 0
        self.music_player = None
        self.manager = UIManager()

        self.music1 = None
        self.music2 = None
        self.music3 = None
        self.music4 = None
        self.music5 = None
        self.music6 = None
        self.music7 = None
        self.music8 = None
        self.close_button = None

        self.music_list = ["assets/music/music2.mp3", "assets/music/music3.mp3", "assets/music/music4.mp3",
                           "assets/music/music4.mp3", "assets/music/standart(cyber).ogg",
                           "assets/music/music6.ogg", "assets/music/music7.ogg", "assets/music/music8.ogg"]

        self.setup_ui()

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

        self.music_s = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="Stop",
            style=BUTTON_STYLE1)

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=280 * SCALE,
            height=65 * SCALE,
            text="Back",
            style=BUTTON_STYLE1)

        self.music1.on_click = lambda event: self.music_pla(0)
        self.music2.on_click = lambda event: self.music_pla(1)
        self.music3.on_click = lambda event: self.music_pla(2)
        self.music4.on_click = lambda event: self.music_pla(3)
        self.music5.on_click = lambda event: self.music_pla(4)
        self.music6.on_click = lambda event: self.music_pla(5)
        self.music7.on_click = lambda event: self.music_pla(6)
        self.music8.on_click = lambda event: self.music_pla(7)
        self.music_s.on_click = self.music_st
        self.close_button.on_click = lambda event: self.close()

        self.manager.add(self.music1)
        self.manager.add(self.music2)
        self.manager.add(self.music3)
        self.manager.add(self.music4)
        self.manager.add(self.music5)
        self.manager.add(self.music6)
        self.manager.add(self.music7)
        self.manager.add(self.music8)
        self.manager.add(self.music_s)
        self.manager.add(self.close_button)

        self.resize_positihon()

    def music_pla(self, i):
        self.mus_p = i
        if self.music_player:
            self.music_play.stop(self.music_player)
        self.music_play = arcade.Sound(self.music_list[i], streaming=True)
        self.music_player = self.music_play.play(volume=0.2)

    def music_st(self, event=None):
        self.music_play.stop(self.music_player)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def resize_positihon(self):
        if not self.music1:
            return

        self.music1.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music1.center_y = SCREEN_HEIGHT // 2 + 150 * SCALE

        self.music2.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music2.center_y = SCREEN_HEIGHT // 2 + 75 * SCALE

        self.music3.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music3.center_y = SCREEN_HEIGHT // 2

        self.music4.center_x = SCREEN_WIDTH // 2 - 200 * SCALE
        self.music4.center_y = SCREEN_HEIGHT // 2 - 75 * SCALE

        self.music5.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music5.center_y = SCREEN_HEIGHT // 2 + 150 * SCALE

        self.music6.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music6.center_y = SCREEN_HEIGHT // 2 + 75 * SCALE

        self.music7.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music7.center_y = SCREEN_HEIGHT // 2

        self.music8.center_x = SCREEN_WIDTH // 2 + 200 * SCALE
        self.music8.center_y = SCREEN_HEIGHT // 2 - 75 * SCALE

        self.music_s.center_x = SCREEN_WIDTH // 2
        self.music_s.center_y = SCREEN_HEIGHT // 2 - 175 * SCALE

        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - 250 * SCALE

    def show(self):
        self.visible = True
        self.manager.enable()
        self.resize_positihon()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()
        self.settings_popup_visible = True
        self.settings_popup.show()
        self.settings_popup.manager.enable()

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

        if self.music_player is not None:
            if not self.music_play.is_playing(self.music_player):
                if self.mus_p == 7:
                    self.mus_p = 0
                else:
                    self.mus_p += 1
                self.music_pla(self.mus_p)

    def on_resize(self, width, height):
        self.resize_positihon()
