import arcade
from PIL import ImageEnhance
from consts import *
from textures import Textures


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = 4 * SCALE
        self.speed = MOVE_SPEED
        self.jump_speed = JUMP_SPEED
        self.max_health = 3
        self.health = self.max_health

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

        self.jump_pressed = False

        self.engine = 0
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
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left_hero = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_hero = True
        elif key in (arcade.key.UP, arcade.key.W):
            self.up_hero = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_hero = True
        elif key == arcade.key.SPACE:
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER

        if key == arcade.key.LSHIFT:
            self.run = True

        if key == arcade.key.X and self.dash_time <= 0:
            self.dash = True
            self.dash_time = DASH_TIME
            self.dash_light = (False, False)

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
            self.jump_pressed = False
            if self.change_y > 0:
                self.change_y *= 0.45

        if key == arcade.key.LSHIFT:
            self.run = False

    def on_update(self, dt):
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

        self.change_x = move

        grounded = self.engine.can_jump(y_distance=6)
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.time_since_ground += dt

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= dt

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)

        if want_jump:
            can_coyote = (self.time_since_ground <= COYOTE_TIME)
            if grounded or can_coyote:
                self.engine.jump(self.jump_speed)
                self.jump_buffer_timer = 0

        if self.change_x and self.change_y == 0:
            self.is_walking = True
            self.is_in_air = False
        else:
            if self.change_y != 0:
                self.is_in_air = True
            else:
                self.is_in_air = False
            self.is_walking = False

        self.engine.update()

    def update_animation(self, delta_time: float = 1 / 60):
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
