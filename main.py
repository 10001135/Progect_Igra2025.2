import arcade
import pyglet

from textures import Textures
from consts import *
from texts import text_d
from views.main_menu_view import MainMenuView


class Platformer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, text_d['title'], samples=16, antialiasing=True,
                         style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
        screen_width, screen_height = get_display_size()

        window_width, window_height = self.get_framebuffer_size()
        self.set_location((screen_width - window_width) // 2, (screen_height - window_height) // 2)
        self.set_update_rate(1 / 60)


def main():
    window = Platformer()
    Textures.set_fonts()
    main_menu_view = MainMenuView()
    window.show_view(main_menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
