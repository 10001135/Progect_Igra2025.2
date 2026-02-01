import arcade
from consts import *
from textures import Textures
from texts import text_d
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

from views.load_view import LoadView
from views.test_levels.game_view_test_1 import GameView_test_1
from hero import Hero
from views.game_levels.Middle_Ages.ma_level_1 import GameView_ma_level_1
from views.game_levels.Middle_Ages.ma_level_2 import GameView_ma_level_2
from views.game_levels.Middle_Ages.ma_level_3 import GameView_ma_level_3
from views.game_levels.Middle_Ages.ma_level_4 import GameView_ma_level_4
from views.game_levels.Middle_Ages.ma_level_5 import GameView_ma_level_5
from views.game_levels.Middle_Ages.ma_level_6 import GameView_ma_level_6



class BgPart(arcade.Sprite):
    def __init__(self, texture, scale, speed):
        super().__init__(texture, scale)
        self.speed = speed

    def update(self, delta_time):
        self.center_x -= self.speed * delta_time


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        Textures.textures_main_menu()
        self.textures = Textures.textures_in_menu

        self.first_plan = arcade.Sprite(self.textures['first_plan'], SCALE)
        self.first_plan.position = (SCREEN_WIDTH // 2, 230 * SCALE)
        self.name = arcade.Sprite(self.textures['name'], SCALE)
        self.name.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6 * 5)

        self.bg = arcade.Sprite(self.textures['mountain_bg'], SCALE * 5)
        self.bg.width = SCREEN_WIDTH
        self.bg.height = SCREEN_HEIGHT
        self.bg.left = 0
        self.bg.top = SCREEN_HEIGHT
        self.back_ground = arcade.SpriteList()
        self.back_ground.append(self.bg)

        self.mount_far = BgPart(self.textures['mountain_far'], SCALE * 5, 50 * SCALE)
        self.mount_far.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 1.25)
        self.mount_far_2 = BgPart(self.textures['mountain_far'], SCALE * 5, 50 * SCALE)
        self.mount_far_2.left = SCREEN_WIDTH
        self.mount_far_2.center_y = SCREEN_HEIGHT // 2 * 1.25
        self.mountain_far = arcade.SpriteList()
        self.mountain_far.append(self.mount_far)
        self.mountain_far.append(self.mount_far_2)

        self.mounts_far = BgPart(self.textures['mountains_far'], SCALE * 5, 80 * SCALE)
        self.mounts_far.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 1.25)
        self.mounts_far_2 = BgPart(self.textures['mountains_far'], SCALE * 5, 80 * SCALE)
        self.mounts_far_2.left = SCREEN_WIDTH
        self.mounts_far_2.center_y = SCREEN_HEIGHT // 2 * 1.25
        self.mountains_far = arcade.SpriteList()
        self.mountains_far.append(self.mounts_far)
        self.mountains_far.append(self.mounts_far_2)

        self.mount_trees = BgPart(self.textures['trees_near_mount'], SCALE * 5, 100 * SCALE)
        self.mount_trees.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 1.25)
        self.mount_trees_2 = BgPart(self.textures['trees_near_mount'], SCALE * 5, 100 * SCALE)
        self.mount_trees_2.left = SCREEN_WIDTH
        self.mount_trees_2.center_y = SCREEN_HEIGHT // 2 * 1.25
        self.mountain_trees = arcade.SpriteList()
        self.mountain_trees.append(self.mount_trees)
        self.mountain_trees.append(self.mount_trees_2)

        self.foreground_trees = BgPart(self.textures['foreground_trees'], SCALE * 5, 120 * SCALE)
        self.foreground_trees.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 1.25)
        self.foreground_trees_2 = BgPart(self.textures['foreground_trees'], SCALE * 5, 120 * SCALE)
        self.foreground_trees_2.left = SCREEN_WIDTH
        self.foreground_trees_2.center_y = SCREEN_HEIGHT // 2 * 1.25
        self.foreground_trees_list = arcade.SpriteList()
        self.foreground_trees_list.append(self.foreground_trees)
        self.foreground_trees_list.append(self.foreground_trees_2)

        self.pics = arcade.SpriteList()
        self.pics.append(self.first_plan)
        self.pics.append(self.name)

        self.fog = BgPart(self.textures['fog'], SCALE * 7.2, 70 * SCALE)
        self.fog.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 * 1.5)
        self.fog_2 = BgPart(self.textures['fog'], SCALE * 7.2, 70 * SCALE)
        self.fog_2.left = self.fog.right
        self.fog_2.center_y = SCREEN_HEIGHT // 2 * 1.5
        self.fog_list = arcade.SpriteList()
        self.fog_list.append(self.fog)
        self.fog_list.append(self.fog_2)

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)

    def on_update(self, delta_time):
        for i in self.mountain_far:
            i.update(delta_time)
            if i.right <= 0:
                i.remove_from_sprite_lists()
        if len(self.mountain_far) == 1:
            self.new_1 = BgPart(self.textures['mountain_far'], SCALE * 5, 110 * SCALE)
            self.new_1.left = self.mountain_far[0].right
            self.new_1.center_y = SCREEN_HEIGHT // 2 * 1.25
            self.mountain_far.append(self.new_1)

        for i in self.mountains_far:
            i.update(delta_time)
            if i.right <= 0:
                i.remove_from_sprite_lists()
        if len(self.mountains_far) == 1:
            self.new_2 = BgPart(self.textures['mountains_far'], SCALE * 5, 120 * SCALE)
            self.new_2.left = self.mountains_far[0].right
            self.new_2.center_y = SCREEN_HEIGHT // 2 * 1.25
            self.mountains_far.append(self.new_2)

        for i in self.mountain_trees:
            i.update(delta_time)
            if i.right <= 0:
                i.remove_from_sprite_lists()
        if len(self.mountain_trees) == 1:
            self.new_3 = BgPart(self.textures['trees_near_mount'], SCALE * 5, 130 * SCALE)
            self.new_3.left = self.mountain_trees[0].right
            self.new_3.center_y = SCREEN_HEIGHT // 2 * 1.25
            self.mountain_trees.append(self.new_3)

        for i in self.foreground_trees_list:
            i.update(delta_time)
            if i.right <= 0:
                i.remove_from_sprite_lists()
        if len(self.foreground_trees_list) == 1:
            self.new_4 = BgPart(self.textures['foreground_trees'], SCALE * 5, 140 * SCALE)
            self.new_4.left = self.foreground_trees_list[0].right
            self.new_4.center_y = SCREEN_HEIGHT // 2 * 1.25
            self.foreground_trees_list.append(self.new_4)

        for i in self.fog_list:
            i.update(delta_time)
            if i.right <= 0:
                i.remove_from_sprite_lists()
        if len(self.fog_list) == 1:
            self.new_5 = BgPart(self.textures['fog'], SCALE * 7.2, 70 * SCALE)
            self.new_5.left = self.fog_list[0].right
            self.new_5.center_y = SCREEN_HEIGHT // 2 * 1.5
            self.fog_list.append(self.new_5)

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

        setting_button = UITextureButton(texture=texture_normal,
                                         position=(SCREEN_WIDTH // 6, SCREEN_HEIGHT - 100),
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         width=texture_normal.width * SCALE,
                                         height=texture_normal.height * SCALE * 0.7,
                                         text=text_d['setting_button'],
                                         style=BUTTON_STYLE2)

        play_button.on_click = lambda event: (Textures.texture_hero_1(),
                                              self.manager.disable(),
                                              self.window.show_view(LoadView(Hero(), None, GameView_ma_level_3)))

        self.box_layout.add(play_button)
        self.box_layout.add(setting_button)

    def on_draw(self):
        self.clear()
        self.back_ground.draw(pixelated=True)
        self.mountain_far.draw(pixelated=True)
        self.mountains_far.draw(pixelated=True)
        self.mountain_trees.draw(pixelated=True)
        self.foreground_trees_list.draw(pixelated=True)
        self.fog_list.draw()
        self.pics.draw(pixelated=True)
        self.manager.draw(pixelated=True)
