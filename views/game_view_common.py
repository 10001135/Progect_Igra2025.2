import arcade
from math import sqrt
from random import uniform
from arcade.particles import Emitter, EmitBurst, FadeParticle
from consts import *


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
        arcade.draw_circle_outline(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 70 * SCALE, arcade.color.WHITE, 20 * SCALE)
        super().__init__()
        print(self.__class__.__name__)
        self.hero = hero
        self.emitter_trace = {}
        self.emitter_clouds = {}
        self.reborn_point = (200, 200)
        self.load = False

    def draw_hook(self):
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

    def set_darkness(self):
        self.d_list = arcade.SpriteList()
        for d in self.darkness_list:
            a = 255
            for light in self.light_list:
                r = sqrt(abs(d.center_x - light.center_x) ** 2 + abs(d.center_y - light.center_y) ** 2) / (SCALE / (1 / 3))
                if r < a:
                    a = r
            d.alpha = a
            d.alpha_p = a
            self.d_list.append(d)

    def update_darkness(self):
        for d in self.d_list:
            a = 255
            if (abs(self.world_camera.position[0] - d.center_x) <= (SCREEN_WIDTH // 2)) and (abs(self.world_camera.position[1] - d.center_y) <= (SCREEN_HEIGHT // 2)):
                for hero in self.hero_l:
                    r = sqrt(abs(d.center_x - hero.center_x) ** 2 + abs(d.center_y - hero.center_y) ** 2) / (SCALE / 0.5)
                    if r < a:
                        a = r
                d.alpha = min(d.alpha_p, a)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        if self.background_list:
            self.background_list.draw(pixelated=True)
        p = self.world_camera.position
        arcade.draw.draw_lbwh_rectangle_filled(p[0] - SCREEN_WIDTH / 2, p[1] - SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.Color(0, 0, 0, 120))
        self.walls_list_p.draw(pixelated=True)
        self.reborn_point_list.draw(pixelated=True)
        for emmiter in (self.emitter_trace, self.emitter_clouds):
            for h in emmiter:
                for e in emmiter[h]:
                    e.draw()

        self.hero_l.draw(pixelated=True)

    def on_update(self, delta_time):
        if not self.load:
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
                if ((hero.center_y < 0 - (hero.height // 2)) or
                        (hero.center_x < 0 - (hero.width // 2)) or
                        (hero.center_x > tile_map_size[0] + (hero.width // 2))):
                    hero.health = 0

                if hero.health <= 0:
                    self.deth(hero)

                hero.on_update(delta_time)
                hero.update_animation(delta_time)
            self.world_camera.on_update()

            if 'Barrier_l' in self.tile_map.sprite_lists:
                for hero in self.hero_l:
                    if hero.dash:
                        barrier_l_c = arcade.SpriteList()
                        for b in self.barrier_l:
                            barrier_l_c.append(b)
                        for b in barrier_l_c:
                            if abs(b.right - (hero.left + hero.change_x)) < 10:
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
                            if abs(b.left - (hero.right + hero.change_x)) < 10:
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

    def on_key_press(self, key, modifiers):
        self.hero.on_key_press(key, modifiers)

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
