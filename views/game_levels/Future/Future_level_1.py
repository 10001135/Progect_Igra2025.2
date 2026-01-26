import arcade
from math import sqrt
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common


class GameView_fut_level_1(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_future_level_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_future_level_1
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.platform_list = self.tile_map.sprite_lists['Platforms']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        #self.darkness_list = self.tile_map.sprite_lists['Darkness']
        #self.light_list = self.tile_map.sprite_lists['Light']

        #self.decor_list_b_f = self.tile_map.sprite_lists['Decor_back_f']
        #self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b = self.tile_map.sprite_lists['Decor_b']
        for sprite in self.decor_list_b:
            sprite.alpha = 150
        self.decor_list = self.tile_map.sprite_lists['Decor']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

        #self.barrier_l = self.tile_map.sprite_lists['Barrier_l']
        self.walls_list_p = arcade.SpriteList()
        for wall in self.walls_list:
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        #self.ladders_list = self.tile_map.sprite_lists['Ladders']

        if level_p:
            if level_p == 2:
                self.reborn_point = self.reborn_point_list[1].position
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
            platforms=self.platform_list,
        )
        self.hero.engine = self.engine

        #self.set_darkness()


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

        self.decor_list_b.draw(pixelated=True)
        self.decor_list.draw(pixelated=True)
        self.hero_l.draw(pixelated=True)
        self.platform_list.draw(pixelated=True)
        self.thorns_list.draw(pixelated=True)