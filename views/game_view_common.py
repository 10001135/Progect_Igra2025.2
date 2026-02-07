import arcade
from math import sqrt
from random import uniform
from arcade.particles import Emitter, EmitBurst, FadeParticle
from texts import text_d

from consts import *
from textures import Textures
from views.dialog import Dialog

from arcade.camera import Camera2D
from views.pause_view import PausPopup
from views.quest_view import QuestPopup
from views.inventory_view import InventoryPopup


def make_trace(hero):
    return Emitter(
        center_xy=(hero.center_x, hero.center_y),
        emit_controller=EmitBurst(1),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.texture.make_soft_square_texture(int(hero.height), arcade.color.BLUEBERRY),
            change_xy=(0, 0),
            lifetime=0.2,
            start_alpha=220, end_alpha=0
        ),
    )


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


class GameView_common(arcade.View):
    def __init__(self, hero):
        super().__init__()
        self.hero = hero
        if self.__class__.__name__ not in self.hero.chests_open_coord:
            self.hero.chests_open_coord[self.__class__.__name__] = []
        Textures.texture_gui()
        Textures.texture_objects()
        self.emitter_trace = {}
        self.emitter_clouds = {}
        self.reborn_point = (200, 200)
        self.npc = arcade.SpriteList()
        self.gui_camera = arcade.camera.Camera2D()

        self.text_talk = arcade.Text(text_d['t_to_talk'],
                                     SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                     30 * SCALE)
        self.text_talk.position = (SCREEN_WIDTH - self.text_talk.content_width - 50 * SCALE, 36 * SCALE)

        self.text_save = arcade.Text(text_d['q_to_save'],
                                     SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                     30 * SCALE)
        self.text_save.position = (SCREEN_WIDTH - self.text_save.content_width - 50 * SCALE, 36 * SCALE)

        self.text_open = arcade.Text(text_d['o_to_open'],
                                     SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                     30 * SCALE)
        self.text_open.position = (SCREEN_WIDTH - self.text_open.content_width - 50 * SCALE, 36 * SCALE)

        self.pause_popup = PausPopup(self)
        self.quest_popup = QuestPopup(self)

        self.pause_popup.setup_ui()
        self.quest_popup.setup_ui()

        self.inventory_popup = InventoryPopup(self)
        self.inventory_popup.setup_ui()

    def draw_hook(self):
        if self.hero.is_hooked and self.hero.joint:
            hook_x, hook_y = self.hero.joint.anchor_a

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

    def set_darkness(self):
        self.d_list = arcade.SpriteList()
        for d in self.darkness_list:
            a = 255
            for light in self.light_list:
                r = sqrt(abs(d.center_x - light.center_x) ** 2 + abs(d.center_y - light.center_y) ** 2) / (
                        SCALE / (1 / 3))
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

    def update_walls_forw(self):
        for w in self.walls_front_list:
            if (abs(self.world_camera.position[0] - w.center_x) <= (SCREEN_WIDTH // 2)) and (
                    abs(self.world_camera.position[1] - w.center_y) <= (SCREEN_HEIGHT // 2)):
                for hero in self.hero_l:
                    r = sqrt(abs(w.center_x - hero.center_x) ** 2 + abs(w.center_y - hero.center_y) ** 2) / (
                            SCALE / 0.5)
                w.alpha = r

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        if self.background_list:
            self.background_list.draw(pixelated=True)
        p = self.world_camera.position
        self.reborn_point_list.draw(pixelated=True)
        arcade.draw.draw_lbwh_rectangle_filled(p[0] - SCREEN_WIDTH / 2, p[1] - SCREEN_HEIGHT / 2, SCREEN_WIDTH,
                                               SCREEN_HEIGHT, arcade.color.Color(0, 0, 0, 120))
        self.walls_list_p.draw(pixelated=True)
        self.reborn_bed_list.draw(pixelated=True)
        for emmiter in (self.emitter_trace, self.emitter_clouds):
            for h in emmiter:
                for e in emmiter[h]:
                    e.draw()

        self.hero_l.draw(pixelated=True)

        ui_camera = Camera2D()
        ui_camera.use()

        if self.quest_popup.visible:
            self.quest_popup.draw()

        if self.inventory_popup.visible:
            self.inventory_popup.draw()

    def on_update(self, delta_time):
        for hero in self.hero_l:
            if hero.dash:
                if hero not in self.emitter_trace:
                    self.emitter_trace[hero] = [make_trace(hero)]
                else:
                    self.emitter_trace[hero].append(make_trace(hero))

            if hero.jumps_left == 1 and hero.jump_pressed and hero.engine.allowed_jumps == 2 and not hero.jump_emit:
                hero.jump_emit = True
                if hero not in self.emitter_clouds:
                    self.emitter_clouds[hero] = [*make_cloud_for_hero(hero)]
                else:
                    em = make_cloud_for_hero(hero)
                    for i in em:
                        self.emitter_clouds[hero].append(i)

            tile_map_size = (self.tile_map.width * self.tile_map.tile_width * 3 * SCALE,
                             self.tile_map.height * self.tile_map.tile_height * 3 * SCALE)
            if ((hero.center_y < 0 - (hero.height // 2) - 16 * SCALE) or
                    (hero.center_x < 0 - (hero.width // 2) - 16 * SCALE) or
                    (hero.center_x > tile_map_size[0] + (hero.width // 2) + 16 * SCALE)):
                hero.health = 0

            if hero.health <= 0:
                self.deth(hero)

            hero.on_update(delta_time)
            hero.update_animation(delta_time)
        self.world_camera.on_update(delta_time)

        if 'Barrier_l' in self.tile_map.sprite_lists:
            for hero in self.hero_l:
                if hero.dash:
                    barrier_l_c = arcade.SpriteList()
                    for b in self.barrier_l:
                        barrier_l_c.append(b)
                    for b in barrier_l_c:
                        if abs(b.right - (hero.left + hero.change_x)) < 10 and (
                                sqrt(abs(hero.center_x - b.center_x) ** 2 + abs(
                                        hero.center_y - b.center_y) ** 2) < 16 * 3 * 4 * SCALE):
                            self.walls_list_p.remove(b)
                            self.barrier_l.remove(b)
                            if b not in self.emitter_clouds:
                                self.emitter_clouds[b] = [*make_cloud_for_hero(b)]
                            else:
                                em = make_cloud_for_hero(b)
                                for i in em:
                                    self.emitter_clouds[b].append(i)

        if 'Barrier_r' in self.tile_map.sprite_lists:
            for hero in self.hero_l:
                if hero.dash:
                    barrier_r_c = arcade.SpriteList()
                    for b in self.barrier_r:
                        barrier_r_c.append(b)
                    for b in barrier_r_c:
                        if abs(b.left - (hero.right + hero.change_x)) < 10 and (
                                sqrt(abs(hero.center_x - b.center_x) ** 2 + abs(
                                        hero.center_y - b.center_y) ** 2) < 16 * 3 * 4 * SCALE):
                            self.walls_list_p.remove(b)
                            self.barrier_r.remove(b)
                            if b not in self.emitter_clouds:
                                self.emitter_clouds[b] = [*make_cloud_for_hero(b)]
                            else:
                                em = make_cloud_for_hero(b)
                                for i in em:
                                    self.emitter_clouds[b].append(i)

        for emitter in (self.emitter_trace, self.emitter_clouds):
            emitter_copy = emitter.copy()
            for h in emitter_copy:
                for e in emitter_copy[h]:
                    e.update(delta_time)
            for h in emitter_copy:
                for e in emitter_copy[h]:
                    if e.can_reap():
                        emitter[h].remove(e)

        if 'Chests' in self.tile_map.sprite_lists:
            for chest in self.chests_list:
                if chest.position in self.hero.chests_open_coord[self.__class__.__name__]:
                    chest.texture = Textures.chest_opened['Chest_opened']

        if 'ChestsG' in self.tile_map.sprite_lists:
            for chestg in self.chestsg_list:
                if chestg.position in self.hero.chests_open_coord[self.__class__.__name__]:
                    chestg.texture = Textures.chestg_opened['ChestG_opened']

        while self.pause_popup.visible:
            pass

    def on_key_press(self, key, modifiers):
        self.hero.on_key_press(key, modifiers)
        if key == arcade.key.Q:
            for bed in self.hero.collides_with_list(self.reborn_bed_list):
                self.reborn_point = bed.position
                self.hero.light_time = LIGHT_TIME
                self.hero.health = self.hero.max_health

        if key == arcade.key.O:
            if 'Chests' in self.tile_map.sprite_lists:
                for chest in self.hero.collides_with_list(self.chests_list):
                    if chest.position not in self.hero.chests_open_coord[self.__class__.__name__]:
                        self.hero.chests_open_coord[self.__class__.__name__].append(chest.position)
                        self.hero.gold += 1

            if 'ChestsG' in self.tile_map.sprite_lists:
                for chestg in self.hero.collides_with_list(self.chestsg_list):
                    if chestg.position not in self.hero.chests_open_coord[self.__class__.__name__]:
                        self.hero.chests_open_coord[self.__class__.__name__].append(chestg.position)
                        self.hero.max_health += 1
                        self.hero.health = self.hero.max_health

        if key == arcade.key.ESCAPE:
            self.window.show_view(self.pause_popup)

        if key == arcade.key.O:
            if self.quest_popup.visible:
                self.quest_popup.close()
            else:
                self.quest_popup.show()

        if key == arcade.key.P:
            if self.inventory_popup.visible:
                self.inventory_popup.close()
            else:
                self.inventory_popup.show()

    def on_key_release(self, key, modifiers):
        self.hero.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.hero.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.hero.on_mouse_release(x, y, button, modifiers)

    def deth(self, hero):
        hero.position = self.reborn_point
        hero.health = hero.max_health
        hero.dash_time = 0
        hero.light_time = LIGHT_TIME

    def text_field(self, text):
        arcade.draw_lbwh_rectangle_filled(text.position[0] - 10 * SCALE,
                                          text.position[1] - text.content_height + 30 * SCALE,
                                          text.content_width + 20 * SCALE,
                                          text.content_height + 20 * SCALE, (21, 32, 59))

        arcade.draw_circle_filled(text.position[0] - 10 * SCALE,
                                  text.position[1] - text.content_height + 30 * SCALE + (
                                          text.content_height + 20 * SCALE) / 2, (
                                          text.content_height + 20 * SCALE) / 2, (21, 32, 59))
        arcade.draw_circle_filled(text.position[0] + text.content_width,
                                  text.position[1] - text.content_height + 30 * SCALE + (
                                          text.content_height + 20 * SCALE) / 2, (
                                          text.content_height + 20 * SCALE) / 2, (21, 32, 59))

    def gui(self):
        if self.hero.collides_with_list(self.npc):
            self.text_field(self.text_talk)
            self.text_talk.draw()

        self.hearts = arcade.SpriteList()
        for h in range(self.hero.max_health):
            if h <= self.hero.health - 1:
                self.hearts.append(
                    arcade.Sprite(Textures.gui['Heart'], 4 * SCALE, SCALE * (40 + h * 65), SCREEN_HEIGHT - 40 * SCALE))
            else:
                self.hearts.append(arcade.Sprite(Textures.gui['Unheart'], 4 * SCALE, SCALE * (40 + h * 65),
                                                 SCREEN_HEIGHT - 40 * SCALE))
        self.hearts.draw(pixelated=True)

        self.money = arcade.SpriteList()
        if 0 < self.hero.gold < 3:
            self.money.append(arcade.Sprite(Textures.gui['Money1'], 4 * SCALE, SCREEN_WIDTH - SCALE * 50, SCREEN_HEIGHT - 40 * SCALE))
        elif 3 <= self.hero.gold < 5:
            self.money.append(arcade.Sprite(Textures.gui['Money3'], 4 * SCALE, SCREEN_WIDTH - SCALE * 50, SCREEN_HEIGHT - 40 * SCALE))
        elif 5 <= self.hero.gold:
            self.money.append(arcade.Sprite(Textures.gui['Money5'], 4 * SCALE, SCREEN_WIDTH - SCALE * 50, SCREEN_HEIGHT - 40 * SCALE))
        self.money.draw(pixelated=True)
        if self.hero.gold > 0:
            self.text_money = arcade.Text(str(self.hero.gold), SCREEN_WIDTH - SCALE * 100, SCREEN_HEIGHT - 55 * SCALE, (230, 230, 245), 30 * SCALE, font_name='Comic Sans MS pixel rus eng')
            self.text_money.draw()

        if 'Reborn_bed' in self.tile_map.sprite_lists:
            if self.hero.collides_with_list(self.reborn_bed_list):
                self.text_field(self.text_save)
                self.text_save.draw()

        if 'Chests' in self.tile_map.sprite_lists:
            if self.hero.collides_with_list(self.chests_list):
                if self.hero.collides_with_list(self.chests_list)[0].position not in self.hero.chests_open_coord[
                    self.__class__.__name__]:
                    self.text_field(self.text_open)
                    self.text_open.draw()

        if 'ChestsG' in self.tile_map.sprite_lists:
            if self.hero.collides_with_list(self.chestsg_list):
                if self.hero.collides_with_list(self.chestsg_list)[0].position not in self.hero.chests_open_coord[
                    self.__class__.__name__]:
                    self.text_field(self.text_open)
                    self.text_open.draw()

    def on_show_view(self):
        self.window.set_mouse_visible(True)
        if hasattr(self, 'pause_popup'):
            self.pause_popup.setup_ui()

        if hasattr(self, 'quest_popup'):
            self.quest_popup.setup_ui()

        if hasattr(self, 'pause_popup'):
            self.inventory_popup.setup_ui()
