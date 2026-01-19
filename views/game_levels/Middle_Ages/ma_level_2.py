import arcade
from math import sqrt
from camera_for_hero import CameraForHero
from textures import Textures
from hero import Hero
from consts import *
from views.game_view_common import GameView_common


class GameView_ma_level_2(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_ma_level_2()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_ma_level_2
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']

        self.decor_list_b_f = self.tile_map.sprite_lists['Decor_back_f']
        self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b_b = self.tile_map.sprite_lists['Decor_back_b']
        # self.decor_list_f = self.tile_map.sprite_lists['Decor_forw']

        # self.thorns_list = self.tile_map.sprite_lists['Thorns']

        # self.barrier_l = self.tile_map.sprite_lists['Barrier_l']
        self.walls_list_p = self.walls_list
        # for wall in (*self.walls_list, *self.barrier_l):
        #     self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        # self.ladders_list = self.tile_map.sprite_lists['Ladders']

        self.hero = Hero(self.tile_map)
        if level_p:
            if level_p == 1:
                self.reborn_point = self.reborn_point_list[0].position
        else:
            self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point
        self.hero_l = arcade.SpriteList()
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, self.tile_map)
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.walls_list_p,
            # ladders=self.ladders_list,
        )
        self.hero.engine = self.engine

        self.set_darkness()

    def on_draw(self):
        super().on_draw()
        self.decor_list_b_b.draw(pixelated=True)
        self.decor_list_b.draw(pixelated=True)
        self.decor_list_b_f.draw(pixelated=True)
        # self.decor_list_f.draw(pixelated=True)

        # self.ladders_list.draw(pixelated=True)

        # self.thorns_list.draw(pixelated=True)

        self.d_list.draw(pixelated=True)

        self.hero_l.draw(pixelated=True)

        self.update_darkness()



    def on_update(self, delta_time):
        super().on_update(delta_time)
        if not self.load:
            for hero in self.hero_l:
                b = [1 for enter1 in self.tile_map.sprite_lists['Enter_1'] if hero.right< enter1.left]
            if sum(b) > 0:
                self.load = True
                from views.game_levels.Middle_Ages.ma_level_1 import GameView_ma_level_1
                self.window.show_view(GameView_ma_level_1(self.hero, 2))
