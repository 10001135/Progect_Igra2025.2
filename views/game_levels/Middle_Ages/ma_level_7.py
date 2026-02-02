import arcade
from math import sqrt

from camera_for_hero import CameraForHero
from texts import text_d
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
from views.load_view import LoadView
from random import uniform
from arcade.particles import Emitter, EmitBurst, FadeParticle


def make_cloud_for_hero(hero):
    return [Emitter(
        center_xy=(hero.center_x + uniform(-hero.width // 2, hero.width // 2), hero.bottom + uniform(0, 5 * SCALE)),
        emit_controller=EmitBurst(1),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.texture.make_soft_circle_texture(4, arcade.color.WHITE),
            change_xy=(0, 0),
            lifetime=0.2,
            start_alpha=220, end_alpha=0,
            scale=uniform(2.5 * SCALE, 18.5 * SCALE)
        ),
    ) for _ in range(15)]

class GameView_ma_level_7(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        Textures.textures_ma_level_7()
        Textures.texture_key_opened()
        arcade.set_background_color(arcade.color.FRENCH_SKY_BLUE)

        self.tile_map = Textures.tile_map_ma_level_7
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.reborn_bed_list = self.tile_map.sprite_lists['Reborn_bed']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']

        self.enter_b = False

        self.keys_place = self.tile_map.sprite_lists['Keys_place']
        self.enter_place = self.tile_map.sprite_lists['ENTER']

        self.decor_list_b = self.tile_map.sprite_lists['Decor_back']
        self.decor_list_b_b = self.tile_map.sprite_lists['Decor_back_b']
        self.decor_list_b_b_f = self.tile_map.sprite_lists['Decor_back_b_f']

        self.thorns_list = self.tile_map.sprite_lists['Thorns']
        self.barrier_keys = self.tile_map.sprite_lists['Barrier_keys']

        self.walls_list_p = arcade.SpriteList()
        for wall in (*self.walls_list, *self.barrier_keys):
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']

        self.text_insert = arcade.Text(text_d['o_to_open'],
                                     SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                     30 * SCALE)
        self.text_insert.position = (SCREEN_WIDTH - self.text_insert.content_width - 50 * SCALE, 36 * SCALE)

        self.text_enter = arcade.Text(text_d['e_to_activate'],
                                       SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                       30 * SCALE)
        self.text_enter.position = (SCREEN_WIDTH - self.text_enter.content_width - 50 * SCALE, 36 * SCALE)

        self.hero.level = self
        if level_p:
            if level_p == 3:
                self.reborn_point = self.reborn_point_list[0].position
            if level_p == 61:
                self.reborn_point = self.reborn_point_list[1].position
            if level_p == 62:
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
        )
        self.hero.engine = self.engine


        for npc in self.npc:
            if npc.__class__.__name__ in self.hero.story_npc:
                npc.story, npc.dialog, npc.greeting = self.hero.story_npc[npc.__class__.__name__]
                npc.story_change()

        self.set_darkness()

    def on_draw(self):
        super().on_draw()
        self.decor_list_b_b.draw(pixelated=True)
        self.walls_list_p.draw(pixelated=True)
        self.decor_list_b.draw(pixelated=True)
        self.reborn_bed_list.draw(pixelated=True)
        self.npc.draw(pixelated=True)

        self.thorns_list.draw(pixelated=True)
        self.enter_place.draw(pixelated=True)
        self.keys_place.draw(pixelated=True)
        self.barrier_keys.draw(pixelated=True)

        self.d_list.draw(pixelated=True)

        for emmiter in (self.emitter_trace, self.emitter_clouds):
            for h in emmiter:
                for e in emmiter[h]:
                    e.draw()

        self.hero_l.draw(pixelated=True)

        self.update_darkness()

        self.gui_camera.use()
        self.gui()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        for hero in self.hero_l:
            b = [1 for enter1 in self.tile_map.sprite_lists['Enter_1'] if hero.bottom > enter1.top and sqrt(
                abs(hero.center_x - enter1.center_x) ** 2 + abs(hero.center_y - enter1.center_y) ** 2) < 16 * 5 * SCALE]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_3 import GameView_ma_level_3
            self.window.show_view(LoadView(self.hero, 7, GameView_ma_level_3))

        for hero in self.hero_l:
            b = [1 for enter2 in self.tile_map.sprite_lists['Enter_2'] if hero.right < enter2.left and sqrt(
                abs(hero.center_x - enter2.center_x) ** 2 + abs(hero.center_y - enter2.center_y) ** 2) < 16 * 5 * SCALE]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_6 import GameView_ma_level_6
            self.window.show_view(LoadView(self.hero, 71, GameView_ma_level_6))

        for hero in self.hero_l:
            b = [1 for enter3 in self.tile_map.sprite_lists['Enter_3'] if hero.right < enter3.left and sqrt(
                abs(hero.center_x - enter3.center_x) ** 2 + abs(hero.center_y - enter3.center_y) ** 2) < 16 * 5 * SCALE]
        if sum(b) > 0:
            from views.game_levels.Middle_Ages.ma_level_6 import GameView_ma_level_6
            self.window.show_view(LoadView(self.hero, 72, GameView_ma_level_6))

        if self.enter_b:
            from views.game_levels.Middle_Ages.ma_level_1 import GameView_ma_level_1  # Заглушка. Будет переносить в будущее.
            self.window.show_view(LoadView(self.hero, None, GameView_ma_level_1))

        for key_p in self.keys_place:
            if key_p.position in self.hero.chests_open_coord[self.__class__.__name__]:
                key_p.texture = Textures.key_open['Key_open']

        for npc in self.npc:
            npc.update_animation(delta_time)

        if self.hero.insert_keys >= 3:
            for b in self.barrier_keys:
                if b not in self.emitter_clouds:
                    self.emitter_clouds[b] = [*make_cloud_for_hero(b)]
                else:
                    em = make_cloud_for_hero(b)
                    for i in em:
                        self.emitter_clouds[b].append(i)
                self.walls_list_p.remove(b)
            self.barrier_keys = arcade.SpriteList()

        self.enter_b = False

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)
        if key == arcade.key.O:
            for key_p in self.hero.collides_with_list(self.keys_place):
                if key_p.position not in self.hero.chests_open_coord[self.__class__.__name__]:
                    if self.hero.keys > 0:
                        self.hero.chests_open_coord[self.__class__.__name__].append(key_p.position)
                        self.hero.keys -= 1
                        self.hero.insert_keys += 1

        if key == arcade.key.E:
            if self.hero.collides_with_list(self.enter_place):
                self.enter_b = True


    def gui(self):
        super().gui()
        if self.hero.collides_with_list(self.keys_place):
            if self.hero.collides_with_list(self.keys_place)[0].position not in self.hero.chests_open_coord[
                self.__class__.__name__]:
                if self.hero.keys > 0:
                    self.text_field(self.text_insert)
                    self.text_insert.draw()

        if self.hero.collides_with_list(self.enter_place):
            self.text_field(self.text_enter)
            self.text_enter.draw()
