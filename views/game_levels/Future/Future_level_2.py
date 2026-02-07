import arcade
from laser import Laser

from bosses.visor.visor import Visor
from bullet_generator import BulletGenerator
from moving_razor import Razor
from camera_for_hero import CameraForHero
from textures import Textures
from consts import *
from views.game_view_common import GameView_common
from views.load_view import LoadView
from random import uniform, choice
from arcade.particles import Emitter, EmitBurst, FadeParticle


def make_cloud_for_boss(boss):
    start_scale = 15 * SCALE
    end_scale = uniform(55 * SCALE, 85 * SCALE)
    return Emitter(
        center_xy=(boss.center_x + uniform(-boss.width // 2, boss.width // 2),
                   boss.center_y + uniform(-boss.height // 2, boss.height // 2)),
        emit_controller=EmitBurst(1),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.texture.make_soft_circle_texture(12, choice([arcade.color.WHITE,
                                                                                    arcade.color.DIM_GRAY,
                                                                                    arcade.color.PURPLE_MOUNTAIN_MAJESTY])),
            change_xy=(0, 0),
            lifetime=0.8,
            start_alpha=255,
            end_alpha=0,
            scale=start_scale,
            mutation_callback=lambda p: setattr(p, 'scale',
                                                start_scale + (end_scale - start_scale) * (
                                                        p.lifetime_elapsed / p.lifetime_original))
        ),
    )


class GameView_fut_level_2(GameView_common):
    def __init__(self, hero, level_p=None):
        super().__init__(hero)
        self.setup_init()
        Textures.textures_future_level_2()
        Textures.textures_future_level_1()
        self.hero.level = self
        self.a = hero

        self.emitter_clouds_boss = {}

        self.tile_map = Textures.tile_map_future_level_2
        self.lad = self.tile_map.sprite_lists['Ladders']
        self.hero.tile_map = self.tile_map
        self.walls_list = self.tile_map.sprite_lists['Walls']
        self.reborn_point_list = self.tile_map.sprite_lists['Reborn_point']
        self.darkness_list = self.tile_map.sprite_lists['Darkness']
        self.light_list = self.tile_map.sprite_lists['Light']
        self.hook_points_list = self.tile_map.sprite_lists['Hook_points']
        self.decor_list = self.tile_map.sprite_lists['Decor']
        self.first_boss_pos = self.tile_map.sprite_lists['first_boss_pos']
        self.second_boss_pos = self.tile_map.sprite_lists['second_boss_pos']
        self.hook_decor = self.tile_map.sprite_lists['Hook_decor']
        self.generator_decor = self.tile_map.sprite_lists['Generator_decor']
        self.razor_spawn = self.tile_map.sprite_lists['Razor']
        self.laser_decor = self.tile_map.sprite_lists['Lasers_decor']

        self.laser_list = []
        if 'Lasers' in self.tile_map.sprite_lists:
            lasers = self.tile_map.sprite_lists['Lasers']
            for i in range(0, len(lasers), 2):
                if i + 1 < len(lasers):
                    laser = Laser(
                        lasers[i].center_x,
                        lasers[i].center_y,
                        lasers[i + 1].center_x
                    )
                    self.laser_list.append(laser)

        self.generators = []
        for i in range(len(self.tile_map.sprite_lists['Generator'])):
            if not i % 2:
                direction = 1
            else:
                direction = -1
            generator = BulletGenerator(
                self.tile_map.sprite_lists['Generator'][i].center_x,
                self.tile_map.sprite_lists['Generator'][i].center_y,
                direction
            )
            self.generators.append(generator)

        self.razor_list = arcade.SpriteList()
        self.razors = []
        for i in range(2):
            if not i % 2:
                direction = -1
                razor = Razor(self.razor_spawn[1].right, self.razor_spawn[1].bottom, direction)
            else:
                direction = 1
                razor = Razor(self.razor_spawn[0].left, self.razor_spawn[0].bottom, direction)
            self.razors.append(razor)
            self.razor_list.append(razor)
        self.walls_list_p = arcade.SpriteList()
        for wall in self.walls_list:
            self.walls_list_p.append(wall)

        self.background_list = self.tile_map.sprite_lists['Background']
        self.ladders_list = self.lad

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


        self.hero_l = arcade.SpriteList(use_spatial_hash=True)
        self.hero_l.append(self.hero)
        self.world_camera = CameraForHero(self.hero, self.tile_map)
        self.hero.world_camera = self.world_camera

        self.set_darkness()

    def setup_init(self):
        print(1)
        self.damage_timer = 0
        self.move_timer = 0
        self.boss_death_timer = 0
        self.boss_is_dead = False

        self.start_attack_series = False
        self.second_attach_end = False

        self.boss_attach_time = 0
        self.first_attach_time = 10
        self.second_attach_delay = 0
        self.third_attach_delay = 0
        self.boss_spawn_timer = 0
        self.do_first_attach = False
        self.do_second_attach = False
        self.do_third_attach = False
        self.return_map_from_first = False
        self.third_attach_end = False
        self.boss_l = arcade.SpriteList(use_spatial_hash=True)
        self.boss = False

        self.hook_points_draw = False
        self.hook_points_decor_draw = False


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

        if self.boss:
            if not self.start_attack_series:
                self.decor_list.draw(pixelated=True)
                self.draw_hook()
                self.ladders_list.draw(pixelated=True)
                self.hero_l.draw(pixelated=True)
                self.d_list.draw()
                self.boss_l.draw(pixelated=True)
                self.update_darkness()
                if self.boss.health > 0:
                    self.boss.draw_hearts()

            if self.do_first_attach and not self.return_map_from_first and not self.do_second_attach:
                self.decor_list.draw(pixelated=True)
                self.draw_hook()
                self.hero_l.draw(pixelated=True)
                self.d_list.draw()
                self.boss_l.draw(pixelated=True)
                for i in self.generators:
                    i.on_draw()
                self.generator_decor.draw(pixelated=True)
                self.update_darkness()
                if self.boss.health > 0:
                    self.boss.draw_hearts()

            if self.return_map_from_first:
                self.decor_list.draw(pixelated=True)
                self.ladders_list.draw(pixelated=True)
                self.draw_hook()
                self.hero_l.draw(pixelated=True)
                self.d_list.draw()
                self.boss_l.draw(pixelated=True)
                self.hook_decor.draw(pixelated=True)
                self.hook_points_list.draw(pixelated=True)
                self.update_darkness()
                if self.boss.health > 0:
                    self.boss.draw_hearts()

            if self.do_second_attach:
                self.decor_list.draw(pixelated=True)
                self.hero_l.draw(pixelated=True)
                self.d_list.draw()
                self.boss_l.draw(pixelated=True)
                self.razor_list.draw(pixelated=True)
                self.update_darkness()
                if self.boss.health > 0:
                    self.boss.draw_hearts()

            if self.do_third_attach:
                self.decor_list.draw(pixelated=True)
                self.hero_l.draw(pixelated=True)
                self.d_list.draw()
                self.boss_l.draw(pixelated=True)
                self.laser_decor.draw(pixelated=True)
                for laser in self.laser_list:
                    laser.draw()

                self.update_darkness()
                if self.boss.health > 0:
                    self.boss.draw_hearts()

            if self.third_attach_end:
                self.decor_list.draw(pixelated=True)
                self.hero_l.draw(pixelated=True)
                self.d_list.draw()
                self.boss_l.draw(pixelated=True)
                if self.boss.health > 0:
                    self.boss.draw_hearts()

            if self.boss.health == 0:
                for emitters in self.emitter_clouds_boss.values():
                    for emitter in emitters:
                        emitter.draw()
        else:
            self.decor_list.draw(pixelated=True)
            self.draw_hook()
            self.ladders_list.draw(pixelated=True)
            self.hero_l.draw(pixelated=True)
            self.d_list.draw()
            self.update_darkness()

        self.gui_camera.use()
        self.gui()

    def on_update(self, delta_time):
        super().on_update(delta_time)
        if not self.boss and self.boss_spawn_timer > 5:
            self.boss = self.boss = Visor(self.first_boss_pos[0].center_x, self.first_boss_pos[0].center_y,
                                          self.second_boss_pos[0].center_x, self.second_boss_pos[0].center_y)
            self.boss_l.append(self.boss)
        else:
            self.boss_spawn_timer += delta_time

        if self.boss:
            self.boss_l.update(delta_time)
            self.boss_l.update_animation(delta_time)
            self.boss_attach_time += delta_time

            if self.boss.health == 0:
                if not self.boss_is_dead:
                    self.boss_is_dead = True
                    self.boss_death_timer = 0
                    for boss in self.boss_l:
                        if boss not in self.emitter_clouds_boss:
                            self.emitter_clouds_boss[boss] = []
                        for _ in range(25):
                            self.emitter_clouds_boss[boss].append(make_cloud_for_boss(boss))

                self.boss_death_timer += delta_time
                for emitters in self.emitter_clouds_boss.values():
                    for emitter in emitters:
                        emitter.update()

                if self.boss_death_timer > 0.4:
                    self.boss_l.clear()

        if self.boss_attach_time > 5 and not self.start_attack_series:
            self.boss.attack_state()
            self.start_attack_series = True
            self.do_first_attach = True
            self.new_walls = list(self.tile_map.sprite_lists['new_walls'])
            self.tile_map.sprite_lists['new_walls'].clear()
            self.walls_list_p.extend(self.new_walls)

        if self.do_first_attach:
            for g in self.generators:
                g.update(delta_time)
            for generator in self.generators:
                for bullet in generator.bullet_list:
                    if bullet.collides_with_list(self.walls_list_p):
                        bullet.remove_from_sprite_lists()
                        continue

                    if bullet.collides_with_list(self.hero_l):
                        self.hero.health -= 1
                        bullet.remove_from_sprite_lists()

        if self.boss and self.boss.is_attacking:
            self.first_attach_time -= delta_time

        if self.first_attach_time <= 0 and not self.return_map_from_first:
            self.boss.damage_state()
            self.return_map_from_first = True
            self.generators = []
            for wall in self.new_walls:
                self.walls_list_p.remove(wall)

        if self.return_map_from_first and self.do_first_attach:
            if not self.boss.is_damaging:
                self.boss.damage_state()
            if self.hero.is_hooked and self.hero.collides_with_list(self.boss_l):
                self.boss.health -= 1
                self.hook_engine.space.remove(self.hero.joint)
                self.hero.is_hooked = False
                self.do_second_attach = True
                self.do_first_attach = False

        if self.do_second_attach:
            self.second_attach_delay += delta_time
            self.ladders_list = arcade.SpriteList()
            self.engine.ladders = self.ladders_list
            if self.second_attach_delay >= 3:
                self.razor_list.update(delta_time)
                self.boss.attack_state()
                for razor in list(self.razor_list):
                    if (razor.direction == -1 and razor.center_x <= 0) or \
                            (razor.direction == 1 and razor.center_x >= self.razor_spawn[1].right):
                        razor.remove_from_sprite_lists()
                if self.hero.collides_with_list(self.razor_list):
                    self.hero.health -= 1
                if len(self.razor_list) == 0:
                    self.ladders_list = self.lad
                    self.engine.ladders = self.ladders_list
                    self.boss.damage_state()
                    self.do_second_attach = False
                    self.second_attach_end = True

        if not self.do_second_attach and self.second_attach_end:
            if not self.boss.is_damaging:
                self.boss.damage_state()
                self.ladders_list = self.lad
                self.engine.ladders = self.ladders_list
            if self.hero.is_hooked and self.hero.collides_with_list(self.boss_l):
                self.boss.health -= 1
                self.hook_engine.space.remove(self.hero.joint)
                self.hero.is_hooked = False
                self.do_third_attach = True

        if self.do_third_attach and self.third_attach_delay < 2:
            self.third_attach_delay += delta_time

        if self.do_third_attach and self.third_attach_delay >= 2:
            self.boss.attack_state()
            self.ladders_list = arcade.SpriteList()
            self.engine.ladders = self.ladders_list
            all_lasers_finished = all(laser.cycle_count >= laser.max_cycles for laser in self.laser_list)

            if not all_lasers_finished:
                for laser in self.laser_list:
                    laser.update(delta_time)

                    if laser.is_active:
                        if (self.hero.left < laser.x2 and self.hero.right > laser.x1 and
                                abs(self.hero.center_y - laser.y) < self.hero.height / 2):
                            self.hero.health = 0
            else:
                self.ladders_list = self.lad
                self.engine.ladders = self.ladders_list
                self.third_attach_end = True
                self.do_third_attach = False
                self.boss.damage_state()

        if self.damage_timer > 0:
            self.damage_timer -= delta_time

        if self.damage_timer <= 0 and self.hero.collides_with_list(self.boss_l) and not self.boss.is_damaging:
            self.damage_timer = TIME_DAMAGE
            self.hero.health -= 1
            self.move_timer = 0.1

        if self.move_timer > 0:
            self.hero.change_x += self.hero.change_x * (-10 * SCALE)
            self.hero.change_y *= -1 * SCALE
            self.move_timer -= delta_time
            if not self.hero.is_hooked:
                self.engine.update()
            else:
                self.hook_engine.step(delta_time)

    def deth(self, hero):
        hero.is_hooked = False
        self.boss = False
        self.window.show_view(LoadView(self.hero, None, self.__class__))
        hero.position = self.reborn_point
        hero.health = hero.max_health
        hero.dash_time = 0
        hero.light_time = LIGHT_TIME

