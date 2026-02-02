import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class QuestPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False

        Textures.quest_textures(Textures)
        self.textures = getattr(Textures, 'quest_icons', {})

        self.manager = UIManager(self.parent_view.window)

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

        self.initialize_quest_items()

        self.text = "Нажмите на предмет, чтобы увидеть описание"

        self.setup_ui()

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
            texture=buttons_textures.get('normal'),
            texture_hovered=buttons_textures.get('hovered'),
            texture_pressed=buttons_textures.get('pressed'),
            width=200 * SCALE,
            height=75 * SCALE,
            text="Закрыть")

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
        if self.visible:
            self.manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if self.visible:
            self.manager.on_mouse_release(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.visible:
            self.manager.on_mouse_motion(x, y, dx, dy)

    def resize_position(self):
        self.close_button.center_x = SCREEN_WIDTH // 2
        self.close_button.center_y = SCREEN_HEIGHT // 2 - self.settings_height // 2 + 50 * SCALE

        start_x = SCREEN_WIDTH // 2 - 125 * SCALE
        start_y = SCREEN_HEIGHT // 2 + 50 * SCALE

        spacing_x = 150 * SCALE
        spacing_y = 125 * SCALE

        for i, button in enumerate(self.item_buttons):
            row = i // 2
            col = i % 2

            button.center_x = start_x + (col * spacing_x)
            button.center_y = start_y - (row * spacing_y)

    def show(self):
        self.visible = True
        self.manager.enable()
        self.resize_position()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()

    def key1_show(self, event=None):
        self.text = "Ключ как ключ. На вид очень старый"

    def key2_show(self, event=None):
        self.text = "Ключ как ключ. О рубин!!! Можно продать;)"

    def key3_show(self, event=None):
        self.text = "Ключ как ключ. Ничего особенного."

    def grosbuch_show(self, event=None):
        self.text = "Большая книга. Что тут у нас? Просто список припасов на складе:("

    def gugunek_axe_show(self, event=None):
        self.text = "Топор как топор. Явно не для рубки дров."

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
            color=arcade.color.GOLD,
            border_width=3)

        arcade.draw_text(
            "Квестовые предметы",
            SCREEN_WIDTH // 2,
            self.window_top - 40,
            arcade.color.WHITE,
            font_size=min(24, int(SCREEN_WIDTH * 0.03)),
            anchor_x="center",
            anchor_y="center",
            bold=True)

        arcade.draw_text(
            self.text,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 100 * SCALE,
            arcade.color.WHITE,
            font_size=min(18, int(SCREEN_WIDTH * 0.02)),
            anchor_x="center",
            anchor_y="center",
            width=self.settings_width - 120,
            multiline=True,
            align="center")

        self.manager.draw()

    def on_resize(self, width, height):
        self.settings_width = max(300, width * 0.6)
        self.settings_height = max(400, height * 0.7)

        self.window_left = width // 2 - self.settings_width // 2
        self.window_right = self.window_left + self.settings_width
        self.window_bottom = height // 2 - self.settings_height // 2
        self.window_top = self.window_bottom + self.settings_height

        self.resize_position()
