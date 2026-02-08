import arcade
from math import sqrt
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
from views.load_view import LoadView
from texts import text_d


class GameView_ma_level_1(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_ma_level_1()
        Textures.texture_chests_opened_1()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_ma_level_1
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.reborn_bed_list = self.tile_map.sprite_lists['Reborn_bed']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']

        self.chests_list = self.tile_map.sprite_lists['Chests']

        self.decor_list_b_f = self.tile_map.sprite_lists['Decor_back_f']
        self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b_b = self.tile_map.sprite_lists['Decor_back_b']
        self.decor_list_f = self.tile_map.sprite_lists['Decor_forw']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']

        self.climb_pos = self.tile_map.sprite_lists['Climb_ob']
        self.climb_obj_list = arcade.SpriteList()
        if not self.hero.climb_b:
            self.climb_obj = arcade.Sprite(Textures.objects['Climb'], SCALE * 3, *self.climb_pos[0].position)
            self.climb_obj_list.append(self.climb_obj)

        self.barrier_l = self.tile_map.sprite_lists['Barrier_l']
        self.walls_list_p = arcade.SpriteList()
        for wall in (*self.walls_list, *self.barrier_l):
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        self.ladders_list = self.tile_map.sprite_lists['Ladders']

        self.text_obj = arcade.Text(text_d['o_to_take'],
                                    SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                    30 * SCALE)
        self.text_obj.position = (SCREEN_WIDTH - self.text_obj.content_width - 50 * SCALE, 36 * SCALE)

        if level_p:
            if level_p == 2:
                self.reborn_point = self.reborn_point_list[1].position
            if level_p == 993:
                self.reborn_point = self.hero.reborn_point
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
        self.reborn_bed_list.draw(pixelated=True)
        self.chests_list.draw(pixelated=True)
        self.decor_list_f.draw(pixelated=True)

        self.ladders_list.draw(pixelated=True)

        self.thorns_list.draw(pixelated=True)
        self.climb_obj_list.draw(pixelated=True)

        self.d_list.draw(pixelated=True)

        self.hero_l.draw(pixelated=True)

        self.update_darkness()

        self.gui_camera.use()
        self.gui()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        for hero in self.hero_l:
            b = [1 for enter2 in self.tile_map.sprite_lists['Enter_2'] if
                 hero.left > enter2.right and (sqrt(abs(hero.center_x - enter2.center_x) ** 2 + abs(hero.center_y - enter2.center_y) ** 2) < 16 * 5 * SCALE)]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_2 import GameView_ma_level_2
            self.window.show_view(LoadView(self.hero, 1, GameView_ma_level_2))

    def gui(self):
        super().gui()
        if not self.hero.climb_b and self.hero.collides_with_list(self.climb_pos):
            self.text_field(self.text_obj)
            self.text_obj.draw()


    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        if key == arcade.key.O:
            if self.hero.collides_with_list(self.climb_pos) and not self.hero.climb_b:
                self.hero.climb_b = True
                self.climb_obj_list = arcade.SpriteList()
