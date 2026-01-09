import arcade
from consts import *
from textures import Textures
from texts import text_d
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout
from views.test_levels.game_view_test_1 import GameView_test_1


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        Textures.textures_main_menu()
        self.textures = Textures.textures_in_menu

        self.bg = arcade.Sprite(self.textures['bg'], SCALE)
        self.bg.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.name = arcade.Sprite(self.textures['name'], SCALE)
        self.name.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 * 5)

        self.pics = arcade.SpriteList()
        self.pics.append(self.bg)
        self.pics.append(self.name)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def setup_widgets(self):
        texture_normal = self.textures['buttons']['style1']['normal']
        texture_hovered = self.textures['buttons']['style1']['hovered']
        texture_pressed = self.textures['buttons']['style1']['pressed']
        play_button = UITextureButton(texture=texture_normal,
                                      texture_hovered=texture_hovered,
                                      texture_pressed=texture_pressed,
                                      width=texture_normal.width * SCALE,
                                      height=texture_normal.height * SCALE * 0.7,
                                      text=text_d['play_button'],
                                      style=BUTTON_STYLE1)
        play_button.on_click = lambda event: (Textures.texture_hero_1(),
                                              self.window.show_view(GameView_test_1()),
                                              self.manager.disable())

        self.box_layout.add(play_button)

    def on_draw(self):
        self.clear()
        self.pics.draw(pixelated=True)
        self.manager.draw(pixelated=True)
