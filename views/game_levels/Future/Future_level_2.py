import arcade
from math import sqrt

from bosses.visor.visor import Visor
from bullet_generator import BulletGenerator
from views import load_view
from NPC.captain import Captain
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
from bosses.visor import visor
import random

from views.load_view import LoadView


class GameView_fut_level_2(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_future_level_2()
        self.hero.double_jump = True
        self.hero.level = self

        self.tile_map = Textures.tile_map_future_level_2
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']
        # self.hook_points_list = self.tile_map.sprite_lists['Hook_points']
        self.decor_list = self.tile_map.sprite_lists['Decor']
        self.first_boss_pos = self.tile_map.sprite_lists['first_boss_pos']
        self.second_boss_pos = self.tile_map.sprite_lists['second_boss_pos']

        # self.thorns_list = self.tile_map.sprite_lists['Thorns']
        self.walls_list_p = arcade.SpriteList()
        for wall in self.walls_list:
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']
        self.ladders_list = self.tile_map.sprite_lists['Ladders']

        self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.walls_list_p,
            ladders=self.ladders_list,
        )
        self.hook_engine = arcade.PymunkPhysicsEngine(gravity=(0, -900))

        self.hero.engine = self.engine
        self.hero.double_jump = True
        self.hero.hook_engine = self.hook_engine

        self.hook_engine.add_sprite(self.hero,
                                    mass=1.0,
                                    collision_type="player",
                                    body_type=arcade.PymunkPhysicsEngine.DYNAMIC)
        physics_object = self.hook_engine.get_physics_object(self.hero)
        physics_object.body.moment = float('inf')

        self.hook_engine.add_sprite_list(
            self.walls_list_p,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC
        )
        if self.hero.is_hooked and self.hero.collides_with_list(self.tile_map.sprite_lists['Thorns']):
            self.hero.damage(1)

        self.boss = Visor(self.first_boss_pos[0].center_x, self.first_boss_pos[0].center_y,
                          self.second_boss_pos[0].center_x, self.second_boss_pos[0].center_y)
        self.boss_l = arcade.SpriteList(use_spatial_hash=True)
        self.boss_l.append(self.boss)

        self.hero_l = arcade.SpriteList(use_spatial_hash=True)
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, self.tile_map)
        self.hero.world_camera = self.world_camera

        self.set_darkness()

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        cam_x, cam_y = self.world_camera.position
        arcade.draw_texture_rect(
            Textures.cosmo_bg,
            arcade.rect.LRBT(
                cam_x - SCREEN_WIDTH // 2,
                cam_x + SCREEN_WIDTH // 2,
                cam_y - SCREEN_HEIGHT // 2,
                cam_y + SCREEN_HEIGHT // 2
            )
        )

        if self.background_list:
            self.background_list.draw(pixelated=True)

        self.walls_list_p.draw(pixelated=True)
        self.reborn_point_list.draw(pixelated=True)

        for emmiter in (self.emitter_trace, self.emitter_clouds):
            for h in emmiter:
                for e in emmiter[h]:
                    e.draw()

        self.decor_list.draw(pixelated=True)
        self.draw_hook()
        self.ladders_list.draw(pixelated=True)
        self.hero_l.draw(pixelated=True)
        # self.thorns_list.draw(pixelated=True)
        self.d_list.draw()
        self.boss_l.draw(pixelated=True)
        # self.generator.on_draw()
        # self.electro_list.draw(pixelated=True)
        self.update_darkness()

        self.gui_camera.use()
        self.gui()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.boss_l.update(delta_time)
