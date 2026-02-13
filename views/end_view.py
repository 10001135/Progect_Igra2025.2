from math import sqrt

import arcade

from texts import text_d
from textures import Textures
from consts import *


class EndView(arcade.View):
    def __init__(self, music_popup):
        super().__init__()
        Textures.end_story_textures()
        self.music_popup = music_popup
        self.texture = Textures.hero_with_cat
        self.text_png = Textures.konec
        self.dust_texture = arcade.make_soft_square_texture(SCREEN_HEIGHT // 45, arcade.color.DUST_STORM,
                                                            outer_alpha=200)
        self.lay = [[True for x in range(81)] for y in range(46)]
        self.mouse_pr = False
        self.text_hint_b = True
        self.text_hint = arcade.Text(text_d['hint'],
                                     SCREEN_WIDTH - 80 * SCALE, 36 * SCALE, (182, 154, 122),
                                     30 * SCALE)
        self.text_hint.position = (SCREEN_WIDTH - self.text_hint.content_width - 50 * SCALE, 36 * SCALE)

        self.text_esc = arcade.Text(text_d['esc'],
                                    80 * SCALE, 36 * SCALE, (182, 154, 122),
                                    30 * SCALE)
        self.text_esc.position = (self.text_esc.content_width - 666 * SCALE, SCREEN_HEIGHT - 50 * SCALE)

        self.music_popup.music_pla(11)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.LRBT(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT))
        arcade.draw_texture_rect(self.text_png,
                                 arcade.LRBT(200 * SCALE, 600 * SCALE, SCREEN_HEIGHT - 400 * SCALE, SCREEN_HEIGHT),
                                 pixelated=True)
        for yc, y in enumerate(self.lay):
            for xc, x in enumerate(y):
                if x:
                    xcc = xc * SCREEN_HEIGHT // 45
                    ycc = yc * SCREEN_HEIGHT // 45
                    arcade.draw_texture_rect(self.dust_texture, arcade.Rect(x=xcc, y=ycc, width=SCREEN_HEIGHT // 22.5,
                                                                            height=SCREEN_HEIGHT // 22.5,
                                                                            top=ycc + SCREEN_HEIGHT // 180,
                                                                            left=xcc - SCREEN_HEIGHT // 180,
                                                                            bottom=ycc - SCREEN_HEIGHT // 180,
                                                                            right=xcc + SCREEN_HEIGHT // 180))
        if self.text_hint_b:
            self.text_hint.draw()
            self.text_esc.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pr = True
        self.text_hint_b = False

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pr = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.mouse_pr:
            for yc, yl in enumerate(self.lay):
                for xc, xl in enumerate(yl):
                    if xl:
                        xcc = xc * SCREEN_HEIGHT // 45
                        ycc = yc * SCREEN_HEIGHT // 45
                        if sqrt(abs(x - xcc) ** 2 + abs(y - ycc) ** 2) < 200 * SCALE:
                            self.lay[yc][xc] = False

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.music_popup.music_st()
            from views.main_menu_view import MainMenuView

            main_menu_view = MainMenuView()
            self.window.show_view(main_menu_view)
