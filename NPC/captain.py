import arcade

from consts import SCALE
from textures import Textures
from views.dialog import Dialog
from texts import text_d


class Captain(arcade.Sprite):
    def __init__(self, x, y, story=0):
        super().__init__()
        Textures.texture_captain()
        self.textures = Textures.captain['Captain']
        self.texture = self.textures[0]
        self.texture_change_time = 0
        self.texture_change_delay = 0.8
        self.current_texture = 0
        self.name = text_d['captain_name']

        self.position = (x, y + 15 * SCALE)
        self.scale = SCALE * 4
        self.story = story
        self.greeting = 'captain_replic_1'
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

    def story_change(self):
        if self.story == 0:
            self.dialog = Dialog(text_d['captain_replic_1'],
                                 {text_d['hero_captain_replic_1']:
                                      {text_d['captain_replic_2']:
                                           {text_d['hero_captain_replic_2']:
                                                text_d['captain_replic_3']}},
                                  text_d['hero_captain_replic_3']:
                                      text_d['captain_replic_5'],

                                  text_d['hero_replic_bye']: 0},
                                 'Captain/captain_dialog.png', Textures.hero['Dialog'], self, self.name)

        if self.story != 0:
            self.dialog = Dialog(text_d[self.greeting],
                                 self.dialog.hero_answers,
                                 'Captain/captain_dialog.png', Textures.hero['Dialog'], self, self.name)

    def dialog_end(self):
        if self.story == 0:
            self.story = 1
            self.greeting = 'captain_replic_4'
