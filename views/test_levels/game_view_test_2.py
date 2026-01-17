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
        self.hero.double_jump = True

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.walls_list.draw(pixelated=True)
        self.reborn_point_list.draw(pixelated=True)
        self.hook_points_list.draw()
        if self.hero.is_hooked:
            hook_x = self.hook_points_list[0].center_x
            hook_y = self.hook_points_list[0].center_y
            if self.hero.face_direction:
                hero_x = self.hero.center_x + 20 * SCALE
            else:
                hero_x = self.hero.center_x - 20 * SCALE
            hero_y = self.hero.center_y
            line_width = 15 * SCALE
            arcade.draw_line(
                hook_x, hook_y, hero_x, hero_y,
                color=arcade.color.DIM_GRAY,
                line_width=line_width)
            radius = line_width / 2 * SCALE
            arcade.draw_circle_filled(hook_x, hook_y, radius, arcade.color.DIM_GRAY)
            arcade.draw_circle_filled(hero_x, hero_y, radius, arcade.color.DIM_GRAY)
        for h in self.emitter_trace:
            for e in self.emitter_trace[h]:
                e.draw()
        self.hero_l.draw(pixelated=True)
