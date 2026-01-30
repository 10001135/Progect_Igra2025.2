import arcade
from consts import *
from textures import Textures
from arcade.gui import UIManager, UITextureButton


class InventoryPopup:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.visible = False

        Textures.inventory_textures(Textures)
        self.textures = getattr(Textures, 'quest_icons', {})

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

        self.all_items = []
        self.all_items_icons = []
        self.all_items_actions = []

        if KEY1:
            self.all_items.append(self.key1)
            self.all_items_icons.append(self.key1_icon)
            self.all_items_actions.append(self.key1_show)

        if KEY2:
            self.all_items.append(self.key2)
            self.all_items_icons.append(self.key2_icon)
            self.all_items_actions.append(self.key2_show)

        if KEY3:
            self.all_items.append(self.key3)
            self.all_items_icons.append(self.key3_icon)
            self.all_items_actions.append(self.key3_show)

        if GROSBUCH:
            self.all_items.append(self.grosbuch)
            self.all_items_icons.append(self.grosbuch_icon)
            self.all_items_actions.append(self.grosbuch_show)

        if GUGUNEK_AXE:
            self.all_items.append(self.gugunek_axe)
            self.all_items_icons.append(self.gugunek_axe_icon)
            self.all_items_actions.append(self.gugunek_axe_show)

        self.setup_ui()

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
            height=50 * SCALE,
            text="Close",
            style=BUTTON_STYLE1)

        if self.all_items:
            for i in self.all_items:
                i = UITextureButton(
                    texture=self.all_items_icons[self.all_items.index(i)],
                    width=100 * SCALE,
                    height=100 * SCALE,
                    text="",
                    style=BUTTON_STYLE1)

                self.manager.add(i)
                self.i.on_click = self.all_items_actions[self.all_items.index(i)]

        self.close_button.on_click = self.close

        self.manager.add(self.close_button)

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

        x, y = -150, 100
        for i in self.all_items:
            self.i.center_x = SCREEN_WIDTH // 2 + x
            self.i.center_y = SCREEN_HEIGHT // 2 + y
            if self.all_items.index(i) % 2 == 1:
                x += 100
                y = 100
            else:
                y -= 75
                
    def show(self):
        self.setup_ui()
        self.visible = True
        self.manager.enable()
        self.resize_positihon()

    def close(self, event=None):
        self.visible = False
        self.manager.disable()

    def key1_show(self):
        self.text = "Ключ как ключ. На вид очень старый"

    def key2_show(self):
        self.text = "Ключ как ключ. О рубин!!! Можно продать;)"

    def key3_show(self):
        self.text = "Ключ как ключ. Ничего особенного."

    def grosbuch_show(self):
        self.text = "Большая книга. Что тут у нас? Просто список припасов на складе:("

    def gugunek_axe_show(self):
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
