import arcade
from PIL import ImageEnhance
from consts import *
from textures import Textures
import pymunk
import math


class Hero(arcade.Sprite):
    def __init__(self, tile_map=None, engine=None, hook_engine=None):
        super().__init__()

        self.tile_map = tile_map
        self.engine = engine
        self.hook_engine = hook_engine

        self.is_hooked = False
        self.joint = None
        self.preserve_moment = False
        self.moment_timer = 0

        self.scale = 3.5 * SCALE
        self.speed = MOVE_SPEED
        self.jump_speed = JUMP_SPEED
        self.max_health = 3
        self.health = self.max_health

        self.gold = 0

        self.left_hero = False
        self.right_hero = False
        self.up_hero = False
        self.down_hero = False

        self.run = False
        self.dash = False
        self.dash_size = DASH_SIZE
        self.dash_time = 0
        self.dash_light = (True, False)
        self.light_time = 0

        self.climb = False
        self.double_jump = True

        self.jump_pressed = False
        self.world_camera = arcade.camera.Camera2D()

        self.textures_hero = Textures.hero['Hero']
        self.texture = self.textures_hero['to_us']

        self.walk_textures = []
        for texture in self.textures_hero['walk']:
            self.walk_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1
        self.is_walking = False
        self.is_in_air = False
        self.face_direction = True

        self.jump_buffer_timer = 0
        self.jumps_left = 0
        self.jump_emit = False

        self.on_ladder = False

        self.story_npc = {}
        self.chests_open_coord = {}
        self.det_t = [9, 0]

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_hero = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_hero = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_hero = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_hero = True

        if key in (arcade.key.UP, arcade.key.W):
            if self.is_hooked and self.joint:
                if not self.collides_with_list(self.tile_map.sprite_lists['Walls']):
                    self.joint.distance = max(20 * SCALE, self.joint.distance - 20 * SCALE)
        if key in (arcade.key.DOWN, arcade.key.S):
            if self.is_hooked and self.joint:
                if not self.collides_with_list(self.tile_map.sprite_lists['Walls']):
                    self.joint.distance = min(400 * SCALE, self.joint.distance + 20 * SCALE)

        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER

        if key == arcade.key.LSHIFT:
            self.run = True

        if key == arcade.key.X and self.dash_time <= 0:
            self.dash = True
            self.dash_time = DASH_TIME
            self.dash_light = (False, False)

        if key == arcade.key.T:
            for npc in self.collides_with_list(self.level.npc):
                npc.story_change()
                npc.dialog.start()
                self.story_npc[npc.__class__.__name__] = (npc.story, npc.dialog, npc.greeting)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_hero = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_hero = False
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_hero = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_hero = False
        elif key == arcade.key.SPACE:
            self.jumps_left += 1
            self.jump_pressed = False
            if self.change_y > 0:
                self.change_y *= 0.45

        if key == arcade.key.LSHIFT:
            self.run = False

    def do_hook(self, pos):
        if not self.is_hooked:
            self.is_hooked = True
            hero_body = self.hook_engine.sprites[self].body
            hero_body.position = self.center_x, self.center_y
            hero_body.velocity = self.change_x * 60 * SCALE, self.change_y * 60 * SCALE

            self.joint = pymunk.PinJoint(
                self.hook_engine.space.static_body,
                hero_body,
                pos,
                (0, 0)
            )
            self.hook_engine.space.add(self.joint)

    def on_mouse_press(self, x, y, button, modifiers):
        world_pos = self.world_camera.unproject((x, y))
        world_x, world_y = world_pos.x, world_pos.y

        if 'Hook_points' in self.tile_map.sprite_lists:
            for hook_point in self.tile_map.sprite_lists['Hook_points']:
                if (world_x < hook_point.right) and (world_x > hook_point.left) and \
                        (world_y > hook_point.bottom) and (world_y < hook_point.top):
                    if math.sqrt(abs(world_x - self.center_x) ** 2 + abs(world_y - self.center_y) ** 2) <= 400 * SCALE:
                        self.do_hook((world_x, world_y))

    def on_mouse_release(self, x, y, button, modifiers):
        if self.is_hooked and self.joint:
            hero_body = self.hook_engine.sprites[self].body
            self.change_x = hero_body.velocity.x / 60
            self.change_y = hero_body.velocity.y / 60
            self.hook_engine.space.remove(self.joint)
            self.joint = None
            self.is_hooked = False
            self.preserve_moment = True
            self.moment_timer = 0.2

    def on_update(self, dt):
        self.speed = MOVE_SPEED * (dt ** 0.3)
        if dt > self.det_t[1]:
            self.det_t[1] = dt
        if dt < self.det_t[0]:
            self.det_t[0] = dt
        if self.moment_timer > 0:
            self.moment_timer -= dt
            if self.moment_timer <= 0:
                self.preserve_moment = False

        move = 0
        if not self.dash:
            if self.left_hero and not self.right_hero:
                move = -self.speed
                self.face_direction = False
            elif self.right_hero and not self.left_hero:
                move = self.speed
                self.face_direction = True

        if self.run:
            move *= 2

        if self.dash:
            self.change_y = 0
            self.engine.gravity_constant = 0
            self.jump_speed = 0
            if self.face_direction:
                move = self.dash_size
            else:
                move = -self.dash_size
            self.dash_size *= 0.7
            if int(self.dash_size) == 0:
                self.dash = False
                self.dash_size = DASH_SIZE
        else:
            self.engine.gravity_constant = GRAVITY
            self.jump_speed = JUMP_SPEED

        if self.dash_time > 0:
            self.dash_time -= dt
        elif not self.dash_light[0]:
            self.dash_light = (False, True)
            self.light_time = LIGHT_TIME

        self.on_ladder = self.engine.is_on_ladder()
        if self.on_ladder:
            if self.up_hero and not self.down_hero:
                self.change_y = self.speed
            elif self.down_hero and not self.up_hero:
                self.change_y = -self.speed
            else:
                self.change_y = 0

        if not self.preserve_moment:
            self.change_x = move
        else:
            if move != 0:
                blend = 1 - (self.moment_timer / 0.2)
                self.change_x = self.change_x * (1 - blend) + move * blend

        self.engine.jumps_since_ground = self.jumps_left
        grounded = self.engine.can_jump(y_distance=6) or self.climb

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= dt

        want_jump = self.jump_pressed

        if want_jump:
            if grounded and self.jump_buffer_timer > 0:
                if self.climb:
                    if self.face_direction:
                        self.change_x = -self.speed * 2
                    else:
                        self.change_x = self.speed
                self.engine.jump(self.jump_speed * (dt ** 0.3))

        if self.change_x and self.change_y == 0:
            self.is_walking = True
            self.is_in_air = False
        else:
            if self.change_y != 0:
                self.is_in_air = True
            else:
                self.is_in_air = False
            self.is_walking = False

        if self.tile_map and 'Thorns' in self.tile_map.sprite_lists and self.collides_with_list(self.tile_map.sprite_lists['Thorns']):
            self.damage(1)

        self.climb = False

        if self.tile_map and 'Walls_climb_r' in self.tile_map.sprite_lists:
            walls_climb_touch = self.collides_with_list(self.tile_map.sprite_lists['Walls_climb_r'])
            if walls_climb_touch:
                for wall in walls_climb_touch:
                    if self.right + self.change_x > wall.right:
                        self.engine.gravity_constant = 0
                        if not self.climb:
                            self.climb = True
                            self.change_y = 0

        if self.tile_map and 'Walls_climb_l' in self.tile_map.sprite_lists:
            walls_climb_touch = self.collides_with_list(self.tile_map.sprite_lists['Walls_climb_l'])
            if walls_climb_touch:
                for wall in walls_climb_touch:
                    if self.left + self.change_x < wall.left:
                        self.engine.gravity_constant = 0
                        if not self.climb:
                            self.climb = True
                            self.change_y = 0

        if self.is_hooked:
            self.hook_engine.step(dt)
            hero_body = self.hook_engine.sprites[self].body
            self.center_x = hero_body.position.x
            self.center_y = hero_body.position.y
            if self.left_hero:
                hero_body.velocity = (hero_body.velocity.x - 5, hero_body.velocity.y)
            if self.right_hero:
                hero_body.velocity = (hero_body.velocity.x + 5, hero_body.velocity.y)
        else:
            if self.double_jump:
                self.engine.enable_multi_jump(2)
            else:
                self.engine.enable_multi_jump(1)

            self.engine.update()

        if not self.is_in_air and self.change_y == 0:
            self.jumps_left = 0
            self.jump_emit = False

    def update_animation(self, delta_time):
        if self.is_walking:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.walk_textures):
                    self.current_texture = 0
                if self.face_direction:
                    self.texture = self.walk_textures[self.current_texture]
                else:
                    self.texture = self.walk_textures[self.current_texture].flip_horizontally()
        elif self.is_in_air:
            if self.face_direction:
                self.texture = self.textures_hero['in_air']
            else:
                self.texture = self.textures_hero['in_air'].flip_horizontally()

        else:
            self.texture = self.textures_hero['to_us']

        if self.is_hooked:
            hook_x, hook_y = self.joint.anchor_a
            x_diff = hook_x - self.center_x
            y_diff = hook_y - self.center_y
            angle = math.atan2(y_diff, x_diff)

            self.angle = -math.degrees(angle) + 90

            if self.face_direction:
                self.texture = self.textures_hero['climb']
                self.angle -= 10
            else:
                self.texture = self.textures_hero['climb'].flip_horizontally()
                self.angle += 10
        else:
            self.angle = 0

        if self.climb:
            if self.face_direction:
                self.texture = self.textures_hero['climb']
            else:
                self.texture = self.textures_hero['climb'].flip_horizontally()

        if self.on_ladder:
            self.texture = self.textures_hero['to_forest']

        if self.dash_light == (False, True):
            self.dash_light = (True, False)

        if self.light_time > 0:
            self.light_time -= delta_time
            self.shine()

    def shine(self):
        if self.face_direction:
            self.texture = arcade.Texture(ImageEnhance.Brightness(self.texture.image).enhance(1.5))
        else:
            self.texture = arcade.Texture(
                ImageEnhance.Brightness(self.texture.image).enhance(1.5)).flip_horizontally()

    def damage(self, power):
        p = min([(abs(self.center_x - sp.center_x) + abs(self.center_y - sp.center_y), sp) for sp in
                 self.tile_map.sprite_lists['Safe_point']], key=lambda x: x[0])
        self.position = p[1].position
        self.health -= power
