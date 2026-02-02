import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class MusicPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.music = True
        self.stop = False
        self.music_play = arcade.Sound("assets/music/standart.mp3", streaming=True)
        self.mus_p = 0
        self.music_player = None
        self.manager = UIManager()

        self.music_buttons = []
        self.music_s = None
        self.close_button = None

        self.not1_icon = None
        self.not2_icon = None
        self.not1 = None
        self.not2 = None

        self.music_list = ["assets/music/music2.mp3", "assets/music/music3.mp3", "assets/music/music4.mp3",
                           "assets/music/music4.mp3", "assets/music/standart(cyber).ogg",
                           "assets/music/music6.ogg", "assets/music/music7.ogg", "assets/music/music8.ogg"]

        self.on_back_to_settings = None

        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()

        Textures.textures_main_menu()

        Textures.decor_textures(Textures)
        self.decor_textures = getattr(Textures, 'decor', {})

        buttons_textures = Textures.textures_in_menu['buttons']['style1']

        if self.decor_textures:
            self.not1_icon = self.decor_textures.get('not1')
            self.not2_icon = self.decor_textures.get('not2')

        for i in range(8):
            btn = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=250 * SCALE,
                height=65 * SCALE,
                text=str(i + 1),
                style=BUTTON_STYLE1)

            btn.on_click = lambda event: self.music_pla(i)

            self.music_buttons.append(btn)
            self.manager.add(btn)

        self.music_s = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text="Stop",
            style=BUTTON_STYLE1)
        self.music_s.on_click = self.music_st

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=280 * SCALE,
            height=65 * SCALE,
            text="Back",
            style=BUTTON_STYLE1)

        self.close_button.on_click = self.close

        self.not1 = UITextureButton(
            texture=self.not1_icon,
            width=200 * SCALE,
            height=200 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.not2 = UITextureButton(
            texture=self.not1_icon,
            width=200 * SCALE,
            height=200 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.manager.add(self.music_s)
        self.manager.add(self.close_button)

        if self.not1:
            self.manager.add(self.not1)
        if self.not2:
            self.manager.add(self.not2)

        self.resize_positihon()

    def music_pla(self, i):
        self.stop = True
        self.mus_p = i
        if self.music_player:
            self.music_play.stop(self.music_player)
        self.music_play = arcade.Sound(self.music_list[i], streaming=True)
        self.music_player = self.music_play.play(volume=0.2)

    def music_st(self, event=None):
        self.stop = False
        if self.music_player:
            self.music_play.stop(self.music_player)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            return self.manager.on_mouse_press(x, y, button, modifiers)
        return False

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            return self.manager.on_mouse_release(x, y, button, modifiers)
        return False

    def on_key_press(self, key, modifiers):
        if self.visible:
            if key == arcade.key.ESCAPE:
                self.close()
                return True
        return False

    def resize_positihon(self):
        if not self.music_buttons:
            return

        y = 100 * SCALE
        x = 400 * SCALE

        self.music_buttons[0].center_x = SCREEN_WIDTH // 2 - x // 2
        self.music_buttons[0].center_y = SCREEN_HEIGHT // 2 + 150 * SCALE

        self.music_buttons[1].center_x = SCREEN_WIDTH // 2 - x // 2
        self.music_buttons[1].center_y = SCREEN_HEIGHT // 2 + 50 * SCALE

        self.music_buttons[2].center_x = SCREEN_WIDTH // 2 - x // 2
        self.music_buttons[2].center_y = SCREEN_HEIGHT // 2 - 50 * SCALE

        self.music_buttons[3].center_x = SCREEN_WIDTH // 2 - x // 2
        self.music_buttons[3].center_y = SCREEN_HEIGHT // 2 - 150 * SCALE

        self.music_buttons[4].center_x = SCREEN_WIDTH // 2 + x // 2
        self.music_buttons[4].center_y = SCREEN_HEIGHT // 2 + 150 * SCALE

        self.music_buttons[5].center_x = SCREEN_WIDTH // 2 + x // 2
        self.music_buttons[5].center_y = SCREEN_HEIGHT // 2 + 50 * SCALE

        self.music_buttons[6].center_x = SCREEN_WIDTH // 2 + x // 2
        self.music_buttons[6].center_y = SCREEN_HEIGHT // 2 - 50 * SCALE

        self.music_buttons[7].center_x = SCREEN_WIDTH // 2 + x // 2
        self.music_buttons[7].center_y = SCREEN_HEIGHT // 2 - 150 * SCALE

        self.music_s.center_x = SCREEN_WIDTH // 2
        self.music_s.center_y = SCREEN_HEIGHT // 2 - 275 * SCALE

        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - 350 * SCALE

        self.not1.center_x = SCREEN_WIDTH // 2 - 400 * SCALE
        self.not1.center_y = SCREEN_HEIGHT // 2 + 200 * SCALE

        self.not2.center_x = SCREEN_WIDTH // 2 + 400 * SCALE
        self.not2.center_y = SCREEN_HEIGHT // 2 + 125 * SCALE

    def show(self):
        self.visible = True
        self.manager.enable()
        self.resize_positihon()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()
        if self.on_back_to_settings:
            self.on_back_to_settings()

    def draw(self):
        if not self.visible:
            return

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
            color=arcade.color.GOLD,
            border_width=3)

        arcade.draw_text(
            "Music",
            SCREEN_WIDTH // 2,
            window_top - 70 * SCALE,
            arcade.color.WHITE,
            font_size=min(30, int(SCREEN_WIDTH * 0.04)),
            anchor_x="center",
            anchor_y="center")

        self.manager.draw()

        if self.stop:
            if self.music_player is not None:
                if not self.music_play.is_playing(self.music_player):
                    if self.mus_p == 7:
                        self.mus_p = 0
                    else:
                        self.mus_p += 1
                    self.music_pla(self.mus_p)

    def on_resize(self, width, height):
        self.resize_positihon()
