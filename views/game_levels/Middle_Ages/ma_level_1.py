import arcade
from math import sqrt
from camera_for_hero import CameraForHero
from textures import Textures
from hero import Hero
from consts import *
from views.game_view_common import GameView_common
from views.test_levels.game_view_test_2 import GameView_test_2


class GameView_ma_level_1(GameView_common):
    def __init__(self):
        super().__init__()
        Textures.textures_ma_level_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_ma_level_1
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']

        self.decor_list1 = self.tile_map.sprite_lists['Decor_back2']
        self.decor_list2 = self.tile_map.sprite_lists['Decor_back']
        self.decor_list3 = self.tile_map.sprite_lists['Decor_back3']
        self.decor_list4 = self.tile_map.sprite_lists['Decor_forw']

        self.background_list = self.tile_map.sprite_lists['Background']

        self.hero = Hero()
        self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point
        self.hero_l = arcade.SpriteList()
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, self.tile_map)
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.walls_list,
        )
        self.hero.engine = self.engine

        self.d_list = arcade.SpriteList()
        for d in self.darkness_list:
            a = 255
            for light in self.light_list:
                r = max(abs(d.center_x - light.center_x), abs(d.center_y - light.center_y), sqrt(abs(d.center_x - light.center_x) ** 2 + abs(d.center_y - light.center_y) ** 2)) / 1.5
                if r < a:
                    a = r
            d.alpha = a
            d.alpha_p = a
            self.d_list.append(d)

    def on_draw(self):
        super().on_draw()
        self.decor_list1.draw(pixelated=True)
        self.decor_list2.draw(pixelated=True)
        self.decor_list3.draw(pixelated=True)
        self.decor_list4.draw(pixelated=True)
        self.d_list.draw(pixelated=True)

        self.hero_l.draw(pixelated=True)

        for d in self.d_list:
            a = 255
            # if (self.world_camera.position[0] - d.center_x <= SCREEN_WIDTH // 2) and (self.world_camera.position[1] - d.center_y <= SCREEN_HEIGHT // 2):
            for hero in self.hero_l:
                r = max(abs(d.center_x - hero.center_x), abs(d.center_y - hero.center_y),
                        sqrt(abs(d.center_x - hero.center_x) ** 2 + abs(d.center_y - hero.center_y) ** 2))
                if r < a:
                    a = r
            d.alpha = min(d.alpha_p, a)



    def on_update(self, delta_time):
        super().on_update(delta_time)
