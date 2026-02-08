import copyreg
import pickle

import arcade

from texts import text_d
from camera_for_hero import CameraForHero
from consts import *
from random import choice
import sqlite3

from textures import Textures
from views.dialog import Dialog


class LoadView(arcade.View):
    def __init__(self, hero, level_from, level_to):
        super().__init__()
        self.hero = hero
        if not hero.save_f:
            con = sqlite3.connect("saves/saves_sql.db")
            cur = con.cursor()
            result = cur.execute("""SELECT save FROM saves""").fetchall()
            if result:
                saves_numbs = []
                for save in result:
                    saves_numbs.append(int(save[0][4:]))
                new_numb = max(saves_numbs) + 1
                save_f = f'save{new_numb}'
                cur.execute("""INSERT INTO saves(save, time, name, level) VALUES(?, 0, ?, 'MA1')""", (f'save{new_numb}', f'Сохранение {new_numb}'))
            else:
                save_f = 'save1'
                cur.execute("""INSERT INTO saves(save, time, name, level) VALUES('save1', 0, 'Сохранение 1', 'MA1')""")
            con.commit()
            con.close()
            self.hero.save_f = save_f
            Textures.textures_ma_level_1()
            self.hero.reborn_bed_pos = Textures.tile_map_ma_level_1.sprite_lists['Reborn_point'][0].position
            self.hero.save(level_to.__name__)

        self.level_from = level_from
        self.level_to = level_to
        self.clear(color=(21, 32, 59))
        self.world_camera = CameraForHero()
        self.world_camera.use()
        texts = text_d['load_text'].split('|')
        text = choice(texts)
        font_size = int(40 * SCALE)
        text_size = font_size * len(text) / 2
        text_a = arcade.Text(text, SCREEN_WIDTH / 2 - text_size * SCALE, SCREEN_HEIGHT / 2, color=(182, 154, 122),
                             font_name='Comic Sans MS pixel rus eng', font_size=font_size)
        text_a.position = ((SCREEN_WIDTH / 2) - (text_a.content_width / 2), SCREEN_HEIGHT / 2)
        text_a.draw()

    def on_update(self, delta_time):
        self.window.show_view(self.level_to(self.hero, self.level_from))

def pickle_custom_dialog(obj):
    return Dialog, (obj.text_npc, obj.hero_answers, obj.npc, obj.hero, obj.npc_name)
