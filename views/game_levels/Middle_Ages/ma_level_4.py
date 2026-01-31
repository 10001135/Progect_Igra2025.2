import arcade
from math import sqrt

from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
from views.load_view import LoadView


class GameView_ma_level_4(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_ma_level_4()
        Textures.texture_chests_opened_1()
        Textures.texture_chestsg_opened_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_ma_level_4
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.reborn_bed_list = self.tile_map.sprite_lists['Reborn_bed']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']

        self.chests_list = self.tile_map.sprite_lists['Chests']
        self.chestsg_list = self.tile_map.sprite_lists['ChestsG']

        self.decor_list_b = self.tile_map.sprite_lists['Decor_back']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

        self.barrier_l = self.tile_map.sprite_lists['Barrier_l']
        self.walls_list_p = arcade.SpriteList()
        for wall in (*self.walls_list, *self.barrier_l):
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        self.ladders_list = self.tile_map.sprite_lists['Ladders']

        self.hero.level = self
        if level_p:
            if level_p == 3:
                self.reborn_point = self.reborn_point_list[1].position
            if level_p == 5:
                self.reborn_point = self.reborn_point_list[0].position
            if level_p == 6:
                self.reborn_point = self.reborn_point_list[2].position
        else:
            self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point
        self.hero_l = arcade.SpriteList()
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, self.tile_map)
        self.world_camera.set()
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.walls_list_p,
            ladders=self.ladders_list,
        )
        self.hero.engine = self.engine

        self.set_darkness()

    def on_draw(self):
        super().on_draw()
        self.decor_list_b.draw(pixelated=True)
        self.reborn_bed_list.draw(pixelated=True)
        self.chests_list.draw(pixelated=True)
        self.chestsg_list.draw(pixelated=True)
        self.walls_list_p.draw(pixelated=True)

        self.ladders_list.draw(pixelated=True)

        self.thorns_list.draw(pixelated=True)

        self.d_list.draw(pixelated=True)

        self.hero_l.draw(pixelated=True)

        self.update_darkness()

        self.gui_camera.use()
        self.gui()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        for hero in self.hero_l:
            b = [1 for enter1 in self.tile_map.sprite_lists['Enter_1'] if hero.left > enter1.right and sqrt(
                abs(hero.center_x - enter1.center_x) ** 2 + abs(hero.center_y - enter1.center_y) ** 2) < 16 * 5 * SCALE]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_3 import GameView_ma_level_3
            self.window.show_view(LoadView(self.hero, 4, GameView_ma_level_3))

        for hero in self.hero_l:
            b = [1 for enter2 in self.tile_map.sprite_lists['Enter_2'] if hero.top < enter2.bottom and sqrt(
                abs(hero.center_x - enter2.center_x) ** 2 + abs(hero.center_y - enter2.center_y) ** 2) < 16 * 5 * SCALE]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_6 import GameView_ma_level_6
            self.window.show_view(LoadView(self.hero, 4, GameView_ma_level_6))

        for hero in self.hero_l:
            b = [1 for enter3 in self.tile_map.sprite_lists['Enter_3'] if hero.right < enter3.left and sqrt(
                abs(hero.center_x - enter3.center_x) ** 2 + abs(hero.center_y - enter3.center_y) ** 2) < 16 * 5 * SCALE]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_5 import GameView_ma_level_5
            self.window.show_view(LoadView(self.hero, 4, GameView_ma_level_5))

