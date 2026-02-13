import arcade
from consts import *
from texts import text_d
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

        self.music_list = ["assets/music/level1.mp3", "assets/music/level2.mp3", "assets/music/level3.mp3",
                           "assets/music/level4.mp3", "assets/music/level5.mp3",
                           "assets/music/level6.mp3", "assets/music/level7.mp3", "assets/music/for_1_level.mp3",
                           "assets/music/for_2_level(boss).mp3", "assets/music/for_3_level.mp3",
                           'assets/music/menu.mp3', 'assets/music/end.mp3']

        self.on_back_to_settings = None

        self.text = arcade.Text(
            text_d['music'],
            SCREEN_WIDTH // 2,
            850 * SCALE,
            arcade.color.WHITE,
            font_size=min(30, int(SCREEN_WIDTH * 0.04)),
            anchor_x="center",
            anchor_y="center",
            font_name='Comic Sans MS pixel rus eng'
        )

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

        for i in range(10):
            btn = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=250 * SCALE,
                height=65 * SCALE,
                text=str(i + 1),
                style=BUTTON_STYLE1)

            x = 400 * SCALE
            q = 5
            if i < q:
                btn.center_x = SCREEN_WIDTH // 2 - x // 2
                btn.center_y = SCREEN_HEIGHT // 2 + 200 * SCALE - (90 * i) * SCALE
            else:
                btn.center_x = SCREEN_WIDTH // 2 + x // 2
                btn.center_y = SCREEN_HEIGHT // 2 + 200 * SCALE - (90 * (i - q)) * SCALE

            btn.on_click = lambda i, index=i: self.music_pla(index)

            self.music_buttons.append(btn)
            self.manager.add(btn)

        self.music_s = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=250 * SCALE,
            height=65 * SCALE,
            text=text_d['stop'],
            style=BUTTON_STYLE1)

        self.music_s.on_click = self.music_st

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=280 * SCALE,
            height=65 * SCALE,
            text=text_d['back'],
            style=BUTTON_STYLE1)

        self.close_button.on_click = self.close

        self.not1 = UITextureButton(
            texture=self.not1_icon,
            width=200 * SCALE,
            height=200 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.not2 = UITextureButton(
            texture=self.not2_icon,
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
        self.music_st()
        self.mus_p = i
        if self.music_player:
            self.music_play.stop(self.music_player)
        self.music_play = arcade.Sound(self.music_list[i], streaming=True)
        self.music_player = self.music_play.play(volume=0.2, loop=True)

    def music_st(self, event=None):
        self.stop = False
        if self.music_player:
            self.music_play.stop(self.music_player)

    def resize_positihon(self):
        if self.music_buttons:
            self.music_s.center_x = SCREEN_WIDTH // 2
            self.music_s.center_y = SCREEN_HEIGHT // 2 - 265 * SCALE

            self.close_button.center_x = SCREEN_WIDTH // 2
            self.close_button.center_y = SCREEN_HEIGHT // 2 - 340 * SCALE

            self.not1.center_x = SCREEN_WIDTH // 2 - 450 * SCALE
            self.not1.center_y = SCREEN_HEIGHT // 2 + 200 * SCALE

            self.not2.center_x = SCREEN_WIDTH // 2 + 450 * SCALE
            self.not2.center_y = SCREEN_HEIGHT // 2 - 200 * SCALE

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

        self.text.draw()

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
