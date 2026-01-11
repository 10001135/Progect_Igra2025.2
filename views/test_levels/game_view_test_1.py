import arcade
from camera_for_hero import CameraForHero
from textures import Textures
from hero import Hero
from consts import *
from views.game_view_common import GameView_common
from views.test_levels.game_view_test_2 import GameView_test_2


class GameView_test_1(GameView_common):
    def __init__(self):
        super().__init__()
        Textures.textures_test_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_test_1
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.enter_list = self.tile_map.sprite_lists['Enter']

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

    def on_draw(self):
        super().on_draw()
        self.enter_list.draw()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if self.hero.collides_with_list(self.enter_list):
            self.window.show_view(GameView_test_2())
