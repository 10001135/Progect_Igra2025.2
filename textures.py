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
    def texture_chests_opened_1():
        chest_opened = arcade.load_texture(f'assets/textures/Chest_opened.png')
        Textures.chest_opened = {'Chest_opened': chest_opened}

    @staticmethod
    def texture_chestsg_opened_1():
        chest_openedg = arcade.load_texture(f'assets/textures/ChestG_opened.png')
        Textures.chestg_opened = {'ChestG_opened': chest_openedg}

    @staticmethod
    def texture_key_opened():
        key_open = arcade.load_texture(f'assets/textures/key_on.png')
        Textures.key_open = {'Key_open': key_open}

    @staticmethod
    def textures_ma_level_1():
        Textures.map_ma_level_1 = "assets/levels/MA_Level_1.tmx"
        Textures.tile_map_ma_level_1 = arcade.load_tilemap(Textures.map_ma_level_1, scaling=3 * SCALE)

    @staticmethod
    def textures_ma_level_2():
        Textures.map_ma_level_2 = "assets/levels/MA_Level_2.tmx"
        Textures.tile_map_ma_level_2 = arcade.load_tilemap(Textures.map_ma_level_2, scaling=3 * SCALE)

    @staticmethod
    def textures_future_level_1():
        Textures.map_future_level_1 = "assets/levels/Fut_Level_1.tmx"
        Textures.tile_map_future_level_1 = arcade.load_tilemap(Textures.map_future_level_1, scaling=3 * SCALE)
        Textures.cosmo_bg = arcade.load_texture("assets/textures/cosmobg.png")
        Textures.bullet = arcade.load_texture(":resources:/images/space_shooter/laserBlue01.png")

    @staticmethod
    def textures_future_level_2():
        Textures.map_future_level_2 = "assets/levels/Fut_Level_2.tmx"
        Textures.tile_map_future_level_2 = arcade.load_tilemap(Textures.map_future_level_2, scaling=3 * SCALE)
        visor = [arcade.load_texture(f'bosses/visor/visor{i}.png') for i in range(3)]
        Textures.visor = {'Visor': visor}

    @staticmethod
    def textures_ma_level_3():
        Textures.map_ma_level_3 = "assets/levels/MA_Level_3.tmx"
        Textures.tile_map_ma_level_3 = arcade.load_tilemap(Textures.map_ma_level_3, scaling=3 * SCALE)

    @staticmethod
    def textures_ma_level_4():
        Textures.map_ma_level_4 = "assets/levels/MA_Level_4.tmx"
        Textures.tile_map_ma_level_4 = arcade.load_tilemap(Textures.map_ma_level_4, scaling=3 * SCALE)

    @staticmethod
    def textures_ma_level_5():
        Textures.map_ma_level_5 = "assets/levels/MA_Level_5.tmx"
        Textures.tile_map_ma_level_5 = arcade.load_tilemap(Textures.map_ma_level_5, scaling=3 * SCALE)

    @staticmethod
    def textures_ma_level_6():
        Textures.map_ma_level_6 = "assets/levels/MA_Level_6.tmx"
        Textures.tile_map_ma_level_6 = arcade.load_tilemap(Textures.map_ma_level_6, scaling=3 * SCALE)

    @staticmethod
    def textures_ma_level_7():
        Textures.map_ma_level_7 = "assets/levels/MA_Level_7.tmx"
        Textures.tile_map_ma_level_7 = arcade.load_tilemap(Textures.map_ma_level_7, scaling=3 * SCALE)

    @staticmethod
    def texture_hero_1():
        hero = {'to_us': arcade.load_texture('assets/textures/Hero/Engineer.png'), 'walk': [],
                'in_air': arcade.load_texture('assets/textures/Hero/Engineer_Walk_4.png'),
                'climb': arcade.load_texture('assets/textures/Hero/Engineer_climb.png'),
                'to_forest': arcade.load_texture('assets/textures/Hero/Engineer_to_forest.png'),}
        for i in range(1, 5):
            hero['walk'].append(arcade.load_texture(f"assets/textures/Hero/Engineer_Walk_{i}.png"))
        Textures.hero = {'Hero': hero, 'Dialog': 'assets/textures/Hero/Engineer_dialog.png'}

    @staticmethod
    def texture_king():
        king = [arcade.load_texture(f'assets/textures/NPC/King_without_kindom/king{i}.png') for i in range(1, 3)]
        Textures.king = {'King': king}

    @staticmethod
    def texture_gugunek():
        gugunek = [arcade.load_texture(f'assets/textures/NPC/Gugunek/Gugunek{i}.png') for i in range(2)]
        Textures.gugunek = {'Gugunek': gugunek}

    @staticmethod
    def texture_nikshulp():
        nikshulp = [arcade.load_texture(f'assets/textures/NPC/Nikshulp/Nikshulp{i}.png') for i in range(2)]
        Textures.nikshulp = {'Nikshulp': nikshulp}

    @staticmethod
    def texture_captain():
        captain = [arcade.load_texture(f'assets/textures/NPC/Captain/Captain{i}.png').flip_horizontally() for i in range(2)]
        Textures.captain = {'Captain': captain}

    @staticmethod
    def texture_fara():
        fara = [arcade.load_texture(f'assets/textures/NPC/Fara/Fara{i}.png') for i in range(2)]
        Textures.fara = {'Fara': fara}

    @staticmethod
    def texture_gui():
        heart = arcade.load_texture(f'assets/textures/GUI/Heart.png')
        unheart = arcade.load_texture(f'assets/textures/GUI/Unheart.png')
        money1 = arcade.load_texture(f'assets/textures/GUI/Money1.png')
        money3 = arcade.load_texture(f'assets/textures/GUI/Money3.png')
        money5 = arcade.load_texture(f'assets/textures/GUI/Money5.png')
        Textures.gui = {'Heart': heart, 'Unheart': unheart, 'Money1': money1, 'Money3': money3, 'Money5': money5}

    @staticmethod
    def texture_objects():
        book = arcade.load_texture('assets/textures/Book.png')
        bell = arcade.load_texture('assets/textures/bell.png')
        climb = arcade.load_texture('assets/textures/climb.png')
        cloud = arcade.load_texture('assets/textures/Cloud.png')
        Textures.objects = {'Book': book, 'Bell': bell, 'Climb': climb, 'Cloud': cloud}