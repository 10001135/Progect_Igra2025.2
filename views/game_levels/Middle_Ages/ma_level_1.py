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

        self.decor_list_b_f = self.tile_map.sprite_lists['Decor_back_f']
        self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b_b = self.tile_map.sprite_lists['Decor_back_b']
        self.decor_list_f = self.tile_map.sprite_lists['Decor_forw']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

        self.background_list = self.tile_map.sprite_lists['Background']

        self.hero = Hero(self.tile_map)
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

        self.set_darkness()

    def on_draw(self):
        super().on_draw()
        self.decor_list_b_b.draw(pixelated=True)
        self.decor_list_b.draw(pixelated=True)
        self.decor_list_b_f.draw(pixelated=True)
        self.decor_list_f.draw(pixelated=True)

        self.thorns_list.draw(pixelated=True)

        self.d_list.draw(pixelated=True)

        self.hero_l.draw(pixelated=True)

        self.update_darkness()



    def on_update(self, delta_time):
        super().on_update(delta_time)
