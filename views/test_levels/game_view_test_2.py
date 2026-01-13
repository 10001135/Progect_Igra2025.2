import arcade
from camera_for_hero import CameraForHero
from textures import Textures
from hero import Hero
from consts import *
from views.game_view_common import GameView_common


class GameView_test_2(GameView_common):
    def __init__(self):
        super().__init__()
        Textures.textures_test_2()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_test_2
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.hook_points_list = self.tile_map.sprite_lists['Hook_points']

        self.hero = Hero(tile_map=self.tile_map)
        self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.walls_list,
        )
        self.hook_engine = arcade.PymunkPhysicsEngine(gravity=(0, -900))

        self.hero.engine = self.engine
        self.hero.hook_engine = self.hook_engine

        self.hook_engine.add_sprite(self.hero,
                                    mass=1.0,
                                    collision_type="player",
                                    body_type=arcade.PymunkPhysicsEngine.DYNAMIC)
        physics_object = self.hook_engine.get_physics_object(self.hero)
        physics_object.body.moment = float('inf')

        self.hook_engine.add_sprite_list(
            self.walls_list,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC
        )

        self.hero_l = arcade.SpriteList()
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, Textures.tile_map_test_2)
        self.hero.world_camera = self.world_camera

    def on_draw(self):
        super().on_draw()
        self.hook_points_list.draw()
