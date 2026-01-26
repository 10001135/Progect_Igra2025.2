import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class InventoryPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False
        self.manager = UIManager()

        self.settings_width = SCREEN_WIDTH * 0.6
        self.settings_hieg = SCREEN_HEIGHT * 0.7

        self.settings_width = max(300, self.settings_width)
        self.settings_hieg = max(400, self.settings_hieg)

        self.window_left = SCREEN_WIDTH // 2 - self.settings_width // 2
        self.window_right = self.window_left + self.settings_width
        self.window_bottom = SCREEN_HEIGHT // 2 - self.settings_hieg // 2
        self.window_top = self.window_bottom + self.settings_hieg

        self.text = ''

        self.setup_ui()

    def setup_ui(self):
        self.manager.clear()

        Textures.textures_main_menu()

        buttons_textures = Textures.textures_in_menu['buttons']['style1']

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=200 * SCALE,
            height=50 * SCALE,
            text="Закрыть",
            style=BUTTON_STYLE1)

        if DASH:
            self.dash_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="Dash",
                style=BUTTON_STYLE1)
        else:
            self.dash_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="",
                style=BUTTON_STYLE1)

        if HOOK:
            self.hook_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="Hook",
                style=BUTTON_STYLE1)
        else:
            self.hook_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="",
                style=BUTTON_STYLE1)

        if DOBL_JUMP:
            self.dobl_jump_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="Jump",
                style=BUTTON_STYLE1)
        else:
            self.dobl_jump_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="",
                style=BUTTON_STYLE1)

        if CLIMB:
            self.climb_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="Climb",
                style=BUTTON_STYLE1)
        else:
            self.climb_button = UITextureButton(
                texture=buttons_textures['normal'],
                texture_hovered=buttons_textures['hovered'],
                texture_pressed=buttons_textures['pressed'],
                width=200 * SCALE,
                height=50 * SCALE,
                text="",
                style=BUTTON_STYLE1)

        self.close_button.on_click = self.close
        self.climb_button.on_click = self.climb
        self.dobl_jump_button.on_click = self.dobl_jump
        self.hook_button.on_click = self.hook
        self.dash_button.on_click = self.dash

        self.manager.add(self.close_button)
        self.manager.add(self.climb_button)
        self.manager.add(self.dobl_jump_button)
        self.manager.add(self.hook_button)
        self.manager.add(self.dash_button)

        self.resize_positihon()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def resize_positihon(self):
        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - 150

        self.hook_button.center_x = SCREEN_WIDTH // 2 + 150
        self.hook_button.center_y = SCREEN_HEIGHT // 2 + 50

        self.dash_button.center_x = SCREEN_WIDTH // 2 - 150
        self.dash_button.center_y = SCREEN_HEIGHT // 2 + 100

        self.dobl_jump_button.center_x = SCREEN_WIDTH // 2 - 150
        self.dobl_jump_button.center_y = SCREEN_HEIGHT // 2 + 50

        self.climb_button.center_x = SCREEN_WIDTH // 2 + 150
        self.climb_button.center_y = SCREEN_HEIGHT // 2 + 100

    def show(self):
        self.visible = True
        self.manager.enable()
        self.resize_positihon()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()

    def dash(self, event=None):
        if DASH:
            self.text = "Странный щит с глазом по середине. Стоп что, глаз стал ртом? ААААААААА!! Почему меня перенесло\
        вперёд? (даёт dash)"
        else:
            self.text = 'Что это:('

    def dobl_jump(self, event=None):
        if DOBL_JUMP:
            self.text = "Облако в бутылке. Странно но оно твёрдое00? На нём можно прыгать!? ГДЕ ЗАКОНЫ ФИЗИКИ!!!!!"
        else:
            self.text = 'Что это:('

    def climb(self, event=None):
        if CLIMB:
            self.text = "Это когти и шипы на ботинки. Ими вы можете цепляться за стены(они отличаются от обычных;)"

        else:
            self.text = 'Что это:('

    def hook(self, event=None):
        if HOOK:
            arcade.draw_text(
                "Странная металлическая лоза. Ей вы можете цепляться за уступы(они выглядят как чёрные круги)",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 150,
                arcade.color.WHITE,
                font_size=min(24, int(SCREEN_WIDTH * 0.03)),
                anchor_x="center",
                anchor_y="center")
        else:
            self.text = 'Что это:('

    def draw(self):
        if not self.visible:
            return

        arcade.draw_lrbt_rectangle_filled(
            left=self.window_left,
            right=self.window_right,
            top=self.window_top,
            bottom=self.window_bottom,
            color=(0, 0, 0, 200))

        arcade.draw_lrbt_rectangle_outline(
            left=self.window_left,
            right=self.window_right,
            top=self.window_top,
            bottom=self.window_bottom,
            color=arcade.color.BLACK,
            border_width=3)

        arcade.draw_text(
            "Инвентарь",
            SCREEN_WIDTH // 2,
            self.window_top - 50,
            arcade.color.WHITE,
            font_size=min(24, int(SCREEN_WIDTH * 0.03)),
            anchor_x="center",
            anchor_y="center")

        arcade.draw_text(
            self.text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            arcade.color.WHITE,
            font_size=min(18, int(SCREEN_WIDTH * 0.02)),
            anchor_x="center",
            anchor_y="center",
            width=self.settings_width - 120,
            multiline=True,
            align="center")

        self.manager.draw()

    def on_resize(self, width, height):
        self.resize_positihon()
