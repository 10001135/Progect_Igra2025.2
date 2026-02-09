import arcade

from views import load_view
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
import random
from math import sqrt

from views.load_view import LoadView


class GameView_fut_level_3(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_future_level_3()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)
        self.hero.double_jump = True
        self.hero.level = self

        self.charge = 0
        self.reverse_alpha = True

        self.tile_map = Textures.tile_map_future_level_3
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.reborn_bed = self.tile_map.sprite_lists['Reborn_bed']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']
        self.electro_list = self.tile_map.sprite_lists['Electro']

        self.decor_list_b = self.tile_map.sprite_lists['Decor_b']
        for sprite in self.decor_list_b:
            sprite.alpha = 150
        self.decor_list = self.tile_map.sprite_lists['Decor']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

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
            ladders=self.ladders_list,
        )

        self.hero.engine = self.engine
        self.hero.double_jump = True
        self.hero_l = arcade.SpriteList(use_spatial_hash=True)
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, self.tile_map)
        self.hero.world_camera = self.world_camera

        selfm = self.pause_popup.settings_popup.music_popup
        selfm.music_st()
        selfm.music_play = arcade.Sound(selfm.music_list[9], streaming=True)
        selfm.music_player = selfm.music_play.play(volume=0.2, loop=True)

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
        self.ladders_list.draw(pixelated=True)
        self.draw_hook()
        self.hero_l.draw(pixelated=True)
        self.thorns_list.draw(pixelated=True)
        self.electro_list.draw(pixelated=True)
        self.reborn_bed.draw(pixelated=True)
        self.d_list.draw()
        self.update_darkness()

        self.gui_camera.use()
        self.gui()

    def on_update(self, delta_time):
        super().on_update(delta_time)

        self.charge += delta_time
        if self.charge >= random.uniform(0.02, 0.08):
            self.charge = 0
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

    def set_darkness(self):
        self.d_list = arcade.SpriteList()
        for d in self.darkness_list:
            a = 255
            for light in self.light_list:
                r = sqrt(abs(d.center_x - light.center_x) ** 2 + abs(d.center_y - light.center_y) ** 2) / (
                    SCALE)
                if r < a:
                    a = r
            d.alpha = a
            d.alpha_p = a
            self.d_list.append(d)

    def update_darkness(self):
        for d in self.d_list:
            a = 255
            if (abs(self.world_camera.position[0] - d.center_x) <= (SCREEN_WIDTH // 2)) and (
                    abs(self.world_camera.position[1] - d.center_y) <= (SCREEN_HEIGHT // 2)):
                for hero in self.hero_l:
                    r = sqrt(abs(d.center_x - hero.center_x) ** 2 + abs(d.center_y - hero.center_y) ** 2) / (
                            SCALE / 0.5)
                    if r < a:
                        a = r
                d.alpha = min(d.alpha_p, a)
