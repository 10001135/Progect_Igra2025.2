import arcade

from consts import SCALE
from textures import Textures
from views.dialog import Dialog
from texts import text_d


class KingWithoutKindom(arcade.Sprite):
    def __init__(self, hero, x, y, story=0):
        super().__init__()
        Textures.texture_king()
        self.textures = Textures.king['King']
        self.texture = self.textures[0]
        self.texture_change_time = 0
        self.texture_change_delay = 0.8
        self.current_texture = 0
        self.name = text_d['king_name']
        self.hero = hero

        self.position = (x, y)
        self.scale = SCALE * 4
        self.story = story
        self.greeting = 'king_replic_1'
        if self.story == 0:
            self.story_change()

    def update_animation(self, delta_time):
        self.texture_change_time += delta_time
        if self.texture_change_time >= self.texture_change_delay:
            self.texture_change_time = 0
            self.current_texture += 1
            if self.current_texture >= len(self.textures):
                self.current_texture = 0
        self.texture = self.textures[self.current_texture]

    def story_change(self, gold=0):
        if self.story == 0:
            self.dialog = Dialog(text_d['king_replic_1'],
                                 {text_d['hero_king_replic_1']:
                                      text_d['king_replic_2'],
                                  text_d['hero_king_replic_2']:
                                      text_d['king_replic_3'],
                                  text_d['hero_king_replic_3']:
                                      text_d['king_replic_4'],
                                  text_d['hero_replic_bye']: 0},
                                 'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)

        if self.story != 0:
            self.dialog = Dialog(text_d[self.greeting],
                                 self.dialog.hero_answers,
                                 'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
            if self.story == 2 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = text_d['king_replic_6']
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 31

            if self.story == 3 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = text_d['king_replic_7']
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 41

            if self.story == 4 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = {
                    text_d['king_replic_8']: {text_d['hero_king_replic_5']: text_d['king_replic_9']}}
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 51

            if self.story == 5 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = text_d['king_replic_10']
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 61

            if self.story == 6 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = {text_d['king_replic_11']: {
                    text_d['hero_king_replic_6']: {text_d['king_replic_111']: {text_d['hero_king_replic_7']: {
                        text_d['king_replic_12']: {text_d['hero_king_replic_8']: text_d['king_replic_13']}}}}}}
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 71

            if self.story == 7 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = text_d['king_replic_14']
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 81

            if self.story == 8 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = {
                    text_d['king_replic_15']: {text_d['hero_king_replic_9']: text_d['king_replic_16']}}
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 91

            if self.story == 9 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = {
                    text_d['king_replic_17']: {text_d['hero_king_replic_10']: text_d['king_replic_18']}}
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 101

            if self.story == 100 and gold > 0:
                self.dialog.hero_answers[text_d['hero_king_replic_4']] = {text_d['king_replic_19']: {text_d['hero_king_replic_11']: 1}}
                self.dialog = Dialog(text_d[self.greeting],
                                     self.dialog.hero_answers,
                                     'King_without_kindom/king_dialog.png', Textures.hero['Dialog'], self, self.name)
                self.story = 111

    def dialog_end(self):
        if self.story == 0:
            self.story = 1
            self.greeting = 'king_replic_5'

        if self.story == 1 and text_d['hero_king_replic_3'] not in self.dialog.hero_answers:
            self.story = 2

        if self.story == 31 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 3
            self.hero.gold -= 1

        if self.story == 41 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 4
            self.hero.gold -= 1

        if self.story == 51 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 5
            self.hero.gold -= 1
            self.hero.gugunek_axe = True

        if self.story == 61 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 6
            self.hero.gold -= 1

        if self.story == 71 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 7
            self.hero.gold -= 1

        if self.story == 81 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 8
            self.hero.gold -= 1

        if self.story == 91 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 9
            self.hero.gold -= 1
            self.hero.max_health += 1

        if self.story == 101 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 100
            self.hero.gold -= 1

        if self.story == 111 and text_d['hero_king_replic_4'] not in self.dialog.hero_answers:
            self.story = 110
            self.hero.gold -= 1
            self.hero.pearl_of_moira = True
            del self.dialog.hero_answers[text_d['hero_replic_bye']]

        if self.story == 110:
            self.dialog.hero_answers[text_d['hero_king_replic_11']] = 0
            self.greeting = 'king_replic_20'
