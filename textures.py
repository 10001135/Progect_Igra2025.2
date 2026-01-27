import arcade
from consts import *


class Textures:
    @staticmethod
    def textures_main_menu():
        Textures.textures_in_menu = {
            'first_plan': arcade.load_texture('assets/textures/character_at_ground.png'),
            'fog': arcade.load_texture('assets/textures/main_menu_bg/parallax-fog.png'),
            'mountain_bg': arcade.load_texture('assets/textures/main_menu_bg/parallax-mountain-bg.png'),
            'mountain_far': arcade.load_texture('assets/textures/main_menu_bg/parallax-mountain-montain-far.png'),
            'mountains_far': arcade.load_texture('assets/textures/main_menu_bg/parallax-mountain-mountains.png'),
            'trees_near_mount': arcade.load_texture('assets/textures/main_menu_bg/parallax-mountain-trees.png'),
            'foreground_trees': arcade.load_texture(
                'assets/textures/main_menu_bg/parallax-mountain-foreground-trees.png'),
            'name': arcade.load_texture('assets/textures/name_pic.png'),
            'buttons': {
                'style1':{
                    'normal': arcade.load_texture("assets/textures/Buttons/normal_button.png"),
                    'hovered': arcade.load_texture("assets/textures/Buttons/hovered_button.png"),
                    'pressed': arcade.load_texture("assets/textures/Buttons/pressed_button.png")
            }}
        }

    @staticmethod
    def set_fonts():
        Textures.fonts = {
            'pixel_sans': arcade.load_font('assets/fonts/Comic Sans MS Pixel.ttf'),
            'alfa_slab_one': arcade.load_font('assets/fonts/AlfaSlabOne-Regular.ttf'),
        }

    @staticmethod
    def textures_pause():
        Textures.textures_in_pause = {

        }

    @staticmethod
    def textures_test_1():
        Textures.map_test_1 = "assets/levels/Test1.tmx"
        Textures.tile_map_test_1 = arcade.load_tilemap(Textures.map_test_1, scaling=3 * SCALE)

    @staticmethod
    def textures_test_2():
        Textures.map_test_2 = "assets/levels/Test2.tmx"
        Textures.tile_map_test_2 = arcade.load_tilemap(Textures.map_test_2, scaling=3 * SCALE)

    @staticmethod
    def texture_hero_1():
        hero = {'to_us': arcade.load_texture('assets/textures/Hero/Engineer.png'), 'walk': [],
                'in_air': arcade.load_texture('assets/textures/Hero/Engineer_Walk_4.png'),
                'climb': arcade.load_texture('assets/textures/Hero/Engineer_climb.png')}
        for i in range(1, 5):
            hero['walk'].append(arcade.load_texture(f"assets/textures/Hero/Engineer_Walk_{i}.png"))
        Textures.hero = {'Hero': hero}

    @staticmethod
    def inventory_textures():
        inventory_icons = {
            'dash': arcade.load_texture('assets/items/dash_shild.png'),
            'hook': arcade.load_texture('assets/items/kruck.png'),
            'jump': arcade.load_texture('assets/items/cloud_in_a_bottle.png'),
            'kogti': arcade.load_texture('assets/items/Master_Ninja_Gear.png'),
        }
