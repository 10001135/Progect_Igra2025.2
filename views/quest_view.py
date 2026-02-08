import arcade
import sys
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton
from views.Settings_view import SettingsPopup


class QuestPopup(arcade.View):
    def __init__(self, parent_view):
        super().__init__()
        self.parent_view = parent_view
        self.visible = False
        self.manager = UIManager()

        self.settings_popup = SettingsPopup(parent_view)
        self.settings_popup_visible = False

        Textures.quest_textures(Textures)
        self.textures = getattr(Textures, 'quest_icons', {})

        self.settings_width = SCREEN_WIDTH * 0.6
        self.settings_height = SCREEN_HEIGHT * 0.7

        self.settings_width = max(300, self.settings_width)
        self.settings_height = max(400, self.settings_height)

        self.window_left = SCREEN_WIDTH // 2 - self.settings_width // 2
        self.window_right = self.window_left + self.settings_width
        self.window_bottom = SCREEN_HEIGHT // 2 - self.settings_height // 2
        self.window_top = self.window_bottom + self.settings_height

        self.all_items = []
        self.all_items_icons = []
        self.all_items_actions = []
        self.item_buttons = []

        self.texye = arcade.Text(
            "Quests",
            SCREEN_WIDTH // 2,
            850 * SCALE,
            arcade.color.WHITE,
            font_size=min(30, int(SCREEN_WIDTH * 0.04)),
            anchor_x="center",
            anchor_y="center")

        self.texte = arcade.Text(
            "Нажмите на предмет, чтобы увидеть описание",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 150 * SCALE,
            arcade.color.WHITE,
            font_size=min(18, int(SCREEN_WIDTH * 0.02)),
            anchor_x="center",
            anchor_y="center",
            width=self.settings_width - 120 * SCALE,
            multiline=True,
            align="center")

        self.initialize_quest_items()

    def update_description(self):
        self.texte.text = self.text

    def initialize_quest_items(self):
        if KEY1:
            self.all_items.append("key1")
            key1_icon = self.textures.get('key1_icon')
            self.all_items_icons.append(key1_icon)
            self.all_items_actions.append(self.key1_show)

        if KEY2:
            self.all_items.append("key2")
            key2_icon = self.textures.get('key2_icon')
            self.all_items_icons.append(key2_icon)
            self.all_items_actions.append(self.key2_show)

        if KEY3:
            self.all_items.append("key3")
            key3_icon = self.textures.get('key3_icon')
            self.all_items_icons.append(key3_icon)
            self.all_items_actions.append(self.key3_show)

        if GROSBUCH:
            self.all_items.append("grosbuch")
            grosbuch_icon = self.textures.get('grosbuch_icon')
            self.all_items_icons.append(grosbuch_icon)
            self.all_items_actions.append(self.grosbuch_show)

        if GUGUNEK_AXE:
            self.all_items.append("gugunek_axe")
            gugunek_axe_icon = self.textures.get('gugunek_axe_icon')
            self.all_items_icons.append(gugunek_axe_icon)
            self.all_items_actions.append(self.gugunek_axe_show)

    def setup_ui(self):
        self.manager.clear()
        self.item_buttons.clear()

        Textures.textures_main_menu()
        menu_textures = getattr(Textures, 'textures_in_menu', {})

        buttons_textures = menu_textures.get('buttons', {}).get('style1', {
            'normal': None,
            'hovered': None,
            'pressed': None})

        self.close_button = UITextureButton(
            texture=buttons_textures['normal'],
            texture_hovered=buttons_textures['hovered'],
            texture_pressed=buttons_textures['pressed'],
            width=300 * SCALE,
            height=65 * SCALE,
            text="Continue",
            style=BUTTON_STYLE1)

        self.close_button.on_click = self.close

        for i in range(len(self.all_items)):
            item_icon = self.all_items_icons[i]
            item_action = self.all_items_actions[i]

            if item_icon:
                button = UITextureButton(
                    texture=item_icon,
                    width=100 * SCALE,
                    height=100 * SCALE,
                    text="")

                button.on_click = item_action

                self.manager.add(button)
                self.item_buttons.append(button)

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

    def on_mouse_motion(self, x, y, dx, dy):
        if self.visible:
            self.manager.on_mouse_motion(x, y, dx, dy)

    def main_menu(self, event=None):
        del sys.modules['views.main_menu_view']

        from views.main_menu_view import MainMenuView

        main_menu_view = MainMenuView()
        self.window.show_view(main_menu_view)

    def resize_position(self):
        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - self.settings_height // 2 + 50 * SCALE

        start_x = SCREEN_WIDTH // 2 - 150 * SCALE
        start_y = SCREEN_HEIGHT // 2 + 200 * SCALE

        spacing_x = 150 * SCALE
        spacing_y = 125 * SCALE

        columns = 3

        for i, button in enumerate(self.item_buttons):
            row = i // columns
            col = i % columns

            button.center_x = start_x + (col * spacing_x)
            button.center_y = start_y - (row * spacing_y)

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
        self.initialize_quest_items()
        self.setup_ui()
        self.settings_popup.manager.disable()
        self.manager.enable()
        self.text = "Нажмите на предмет, чтобы увидеть описание"
        self.update_description()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()
        self.settings_popup_visible = False
        self.settings_popup.close()
        self.window.show_view(self.parent_view)

    def set_text(self, text):
        self.text = text
        self.update_description()

    def key1_show(self, event=None):
        self.set_text("Ключ как ключ. На вид очень старый")

    def key2_show(self, event=None):
        self.set_text("Ключ как ключ. О рубин!!! Можно продать;)")

    def key3_show(self, event=None):
        self.set_text("Ключ как ключ. Ничего особенного.")

    def grosbuch_show(self, event=None):
        self.set_text("Большая книга. Что тут у нас? Просто список припасов на складе:(")

    def gugunek_axe_show(self, event=None):
        self.set_text("Топор как топор. Явно не для рубки дров.")

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

        self.texye.draw()
        self.texte.draw()

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

        self.texte.font_size = min(18, int(width * 0.02))
        self.texte.width = self.settings_width - 120 * SCALE
        self.texte.x = width // 2
        self.texte.y = height // 2 - 150 * SCALE

        self.text.x = width // 2
        self.text.y = 850 * SCALE

        if self.visible:
            self.resize_position()
        if self.settings_popup_visible:
            self.settings_popup.on_resize(width, height)
