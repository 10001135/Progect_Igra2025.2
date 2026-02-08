import arcade
import sys
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton
from views.Settings_view import SettingsPopup


class InventoryPopup(arcade.View):
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.visible = False
        self.manager = UIManager()

        self.settings_popup = SettingsPopup(parent_view)
        self.settings_popup_visible = False

        Textures.inventory_textures(Textures)
        self.textures = getattr(Textures, 'inventory_icons', {})

        Textures.decor_textures(Textures)
        self.decor_textures = getattr(Textures, 'decor', {})

        self.settings_width = SCREEN_WIDTH * 0.6
        self.settings_height = SCREEN_HEIGHT * 0.7

        self.settings_width = max(300, self.settings_width)
        self.settings_height = max(400, self.settings_height)

        self.window_left = SCREEN_WIDTH // 2 - self.settings_width // 2
        self.window_right = self.window_left + self.settings_width
        self.window_bottom = SCREEN_HEIGHT // 2 - self.settings_height // 2
        self.window_top = self.window_bottom + self.settings_height

        self.dash_icon = None
        self.climb_icon = None
        self.hook_icon = None
        self.jump_icon = None
        self.player_icon = None
        self.robot2_icon = None
        self.rastenie_icon = None

        # Позиция заголовка относительно верха окна
        self.texts = arcade.Text(
            "Inventory",
            SCREEN_WIDTH // 2,
            self.window_top - 60 * SCALE,
            arcade.color.WHITE,
            font_size=min(30, int(SCREEN_WIDTH * 0.04)),
            anchor_x="center",
            anchor_y="center")

        self.text = ''

        self.texye = arcade.Text(
            self.text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50 * SCALE,
            arcade.color.WHITE,
            font_size=min(18, int(SCREEN_WIDTH * 0.02)),
            anchor_x="center",
            anchor_y="center",
            width=self.settings_width - 120 * SCALE,
            multiline=True,
            align="center")

        self.icons()

    def update_description(self):
        self.texye.text = self.text
        # Обновляем позицию текста описания
        self.texye.x = SCREEN_WIDTH // 2
        self.texye.y = SCREEN_HEIGHT // 2 - 100 * SCALE
        self.texye.width = self.settings_width - 120 * SCALE

    def icons(self):
        if not self.textures:
            return

        if DASH:
            self.dash_icon = self.textures.get('dash')
        else:
            self.dash_icon = self.textures.get('chto_eto')

        if CLIMB:
            self.climb_icon = self.textures.get('cogti')
        else:
            self.climb_icon = self.textures.get('chto_eto')

        if HOOK:
            self.hook_icon = self.textures.get('hook')
        else:
            self.hook_icon = self.textures.get('chto_eto')

        if DOBL_JUMP:
            self.jump_icon = self.textures.get('jump')
        else:
            self.jump_icon = self.textures.get('chto_eto')

        if self.decor_textures:
            self.player_icon = self.decor_textures.get('igrok')
            self.robot2_icon = self.decor_textures.get('robot2')
            self.rastenie_icon = self.decor_textures.get('astenie')

    def setup_ui(self):
        self.manager.clear()

        Textures.textures_main_menu()
        menu_textures = getattr(Textures, 'textures_in_menu', {})
        buttons_textures = menu_textures.get('buttons', {}).get('style1', {'normal': None, 'hovered': None,
                                                                           'pressed': None})

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=200 * SCALE,
            height=90 * SCALE,
            text="Close",
            style=BUTTON_STYLE1)

        self.dash_button = UITextureButton(
            texture=self.dash_icon,
            width=100 * SCALE,
            height=100 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.hook_button = UITextureButton(
            texture=self.hook_icon,
            width=100 * SCALE,
            height=100 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.dobl_jump_button = UITextureButton(
            texture=self.jump_icon,
            width=100 * SCALE,
            height=100 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.climb_button = UITextureButton(
            texture=self.climb_icon,
            width=100 * SCALE,
            height=100 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.igrok = UITextureButton(
            texture=self.player_icon,
            width=200 * SCALE,
            height=200 * SCALE,
            text="",
            style=BUTTON_STYLE1)

        self.close_button.on_click = self.close
        self.climb_button.on_click = self.climb
        self.dobl_jump_button.on_click = self.dobl_jump
        self.hook_button.on_click = self.hook
        self.dash_button.on_click = self.dash
        self.igrok.on_click = self.player_info

        self.manager.add(self.close_button)
        self.manager.add(self.climb_button)
        self.manager.add(self.dobl_jump_button)
        self.manager.add(self.hook_button)
        self.manager.add(self.dash_button)
        self.manager.add(self.igrok)

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

    def on_mouse_motion(self, x, y, dx, dy):
        if self.visible:
            self.manager.on_mouse_motion(x, y, dx, dy)

    def main_menu(self, event=None):
        del sys.modules['views.main_menu_view']

        from views.main_menu_view import MainMenuView

        main_menu_view = MainMenuView()
        self.window.show_view(main_menu_view)

    def resize_position(self):
        spacing_horizontal = 150 * SCALE
        spacing_vertical_upper = 120 * SCALE
        spacing_vertical_lower = 20 * SCALE

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        self.close_button.center_x = center_x
        self.close_button.center_y = center_y - 150 * SCALE

        self.igrok.center_x = center_x
        self.igrok.center_y = center_y + 70 * SCALE

        self.dash_button.center_x = center_x - spacing_horizontal
        self.dash_button.center_y = center_y + spacing_vertical_upper

        self.dobl_jump_button.center_x = center_x - spacing_horizontal
        self.dobl_jump_button.center_y = center_y + spacing_vertical_lower

        self.climb_button.center_x = center_x + spacing_horizontal
        self.climb_button.center_y = center_y + spacing_vertical_upper

        self.hook_button.center_x = center_x + spacing_horizontal
        self.hook_button.center_y = center_y + spacing_vertical_lower

        self.texts.x = center_x
        self.texts.y = self.window_top - 40 * SCALE

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
        self.icons()
        self.setup_ui()
        self.settings_popup.manager.disable()
        self.manager.enable()
        self.text = ''
        self.update_description()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()
        self.settings_popup_visible = False
        self.settings_popup.close()
        self.window.show_view(self.parent_view)

    def dash(self, event=None):
        if DASH:
            self.text = ("Странный щит с глазом по середине. Стоп что, глаз стал ртом? ААААААААА!! Почему"
                         " меня перенесло вперёд? (даёт dash)")
        else:
            self.text = 'Что это:('
        self.update_description()

    def dobl_jump(self, event=None):
        if DOBL_JUMP:
            self.text = "Облако в бутылке. Странно но оно твёрдое00? На нём можно прыгать!? ГДЕ ЗАКОНЫ ФИЗИКИ!!!!!"
        else:
            self.text = 'Что это:('
        self.update_description()

    def climb(self, event=None):
        if CLIMB:
            self.text = "Это когти и шипы на ботинки. Ими вы можете цепляться за стены(они отличаются от обычных;)"
        else:
            self.text = 'Что это:('
        self.update_description()

    def hook(self, event=None):
        if HOOK:
            self.text = "Странная металлическая лоза. Ей вы можете цепляться за уступы(они выглядят как чёрные круги)"
        else:
            self.text = 'Что это:('
        self.update_description()

    def player_info(self, event=None):
        self.text = "Это пасхалка поздравляю."
        self.update_description()

    def on_draw(self):
        self.parent_view.on_draw()
        if not self.settings_popup.visible:
            self.manager.enable()

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
            color=arcade.color.GOLD,
            border_width=3)

        self.texts.draw()

        self.texye.draw()

        self.manager.draw()

        if self.settings_popup_visible:
            self.settings_popup.draw()

    def on_resize(self, width, height):
        self.settings_width = max(300, width * 0.6)
        self.settings_height = max(400, height * 0.7)

        self.window_left = width // 2 - self.settings_width // 2
        self.window_right = self.window_left + self.settings_width
        self.window_bottom = height // 2 - self.settings_height // 2
        self.window_top = self.window_bottom + self.settings_height

        if self.visible:
            self.resize_position()
        if self.settings_popup_visible:
            self.settings_popup.on_resize(width, height)