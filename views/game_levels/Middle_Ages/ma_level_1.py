import arcade
from math import sqrt
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
from views.load_view import LoadView


class GameView_ma_level_1(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_ma_level_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_ma_level_1
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']

        self.decor_list_b_f = self.tile_map.sprite_lists['Decor_back_f']
        self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b_b = self.tile_map.sprite_lists['Decor_back_b']
        self.decor_list_f = self.tile_map.sprite_lists['Decor_forw']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

        self.barrier_l = self.tile_map.sprite_lists['Barrier_l']
        self.walls_list_p = arcade.SpriteList()
        for wall in (*self.walls_list, *self.barrier_l):
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        self.ladders_list = self.tile_map.sprite_lists['Ladders']

        if level_p:
            if level_p == 2:
                self.reborn_point = self.reborn_point_list[1].position
        else:
            self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point
        self.hero.level = self
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
        self.decor_list_b_b.draw(pixelated=True)
        self.decor_list_b.draw(pixelated=True)
        self.decor_list_b_f.draw(pixelated=True)
        self.decor_list_f.draw(pixelated=True)

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
            b = [1 for enter2 in self.tile_map.sprite_lists['Enter_2'] if
                 hero.left > enter2.right and abs(hero.center_y - enter2.center_y) < enter2.height]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_2 import GameView_ma_level_2
            self.window.show_view(LoadView(self.hero, 1, GameView_ma_level_2))
