import arcade
from math import sqrt
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
import random


class GameView_fut_level_1(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_future_level_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)
        self.hero.double_jump = True
        self.draw_fake_floor = True

        self.asdf = 0
        self.reverse_alpha = True

        self.tile_map = Textures.tile_map_future_level_1
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.platform_list = self.tile_map.sprite_lists['Platforms']
        for i in range(len(self.platform_list)):
            if i == 0:
                self.platform_list[i].boundary_left *= SCALE
                self.platform_list[i].boundary_right *= SCALE
                self.platform_list[i].change_x *= SCALE
            else:
                self.platform_list[i].boundary_top *= SCALE
                self.platform_list[i].boundary_bottom *= SCALE
                self.platform_list[i].change_y *= SCALE
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']
        self.no_light_list = self.tile_map.sprite_lists['No_light']
        self.fake_floor_list = self.tile_map.sprite_lists['Fake_floor']
        self.hook_points_list = self.tile_map.sprite_lists['Hook_points']
        self.decor_list_f = self.tile_map.sprite_lists['Decor_f']
        self.electro_list = self.tile_map.sprite_lists['Electro']

        # self.decor_list_b_f = self.tile_map.sprite_lists['Decor_back_f']
        # self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b = self.tile_map.sprite_lists['Decor_b']
        for sprite in self.decor_list_b:
            sprite.alpha = 150
        self.decor_list = self.tile_map.sprite_lists['Decor']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

        # self.barrier_l = self.tile_map.sprite_lists['Barrier_l']
        self.walls_list_p = arcade.SpriteList()
        for wall in self.walls_list:
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        self.ladders_list = self.tile_map.sprite_lists['Ladders']

        if level_p:
            if level_p == 2:
                self.reborn_point = self.reborn_point_list[1].position
        else:
            self.reborn_point = self.reborn_point_list[0].position
        self.hero.position = self.reborn_point
        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.hero,
            gravity_constant=GRAVITY,
            walls=self.walls_list_p,
            platforms=self.platform_list,
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

        self.hero_l = arcade.SpriteList()
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
        if self.draw_fake_floor:
            self.fake_floor_list.draw(pixelated=True)
        self.reborn_point_list.draw(pixelated=True)

        for emmiter in (self.emitter_trace, self.emitter_clouds):
            for h in emmiter:
                for e in emmiter[h]:
                    e.draw()
        self.decor_list_b.draw(pixelated=True)
        self.decor_list.draw(pixelated=True)
        self.decor_list_f.draw(pixelated=True)
        self.ladders_list.draw(pixelated=True)
        self.d_list.draw()
        self.draw_hook()
        self.no_light_list.draw(pixelated=True)
        self.hook_points_list.draw(pixelated=True)
        self.hero_l.draw(pixelated=True)
        self.platform_list.draw(pixelated=True)
        self.thorns_list.draw(pixelated=True)
        self.electro_list.draw(pixelated=True)
        self.update_darkness()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.asdf += delta_time
        if self.asdf >= random.uniform(0.02, 0.08):
            self.asdf = 0
            for sprite in self.electro_list:
                chance = random.random()
                if chance < 0.3:
                    sprite.alpha = 255
                elif chance < 0.6:
                    sprite.alpha = random.randint(150, 200)
                elif chance < 0.85:
                    sprite.alpha = random.randint(80, 130)
                else:
                    sprite.alpha = random.randint(40, 80)

        if self.fake_floor_list[0].left <= self.hero_l[0].center_x <= self.fake_floor_list[-1].right:
            self.draw_fake_floor = False
