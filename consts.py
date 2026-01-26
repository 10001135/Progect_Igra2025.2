from arcade.gui import UITextureButtonStyle

SCALE = 0.79
SCREEN_WIDTH = int(1920 * SCALE)
SCREEN_HEIGHT = int(1080 * SCALE)

GRAVITY = 3 * SCALE
JUMP_BUFFER = 0.12
MOVE_SPEED = 30 * SCALE
COYOTE_TIME = 0.08
JUMP_SPEED = 85 * SCALE
DASH_SIZE = 60 * SCALE
DASH_TIME = 2
LIGHT_TIME = 0.5

CAMERA_LERP = 0.7

DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)

BUTTON_STYLE1 = {'normal': UITextureButtonStyle(font_size=int(40 * SCALE),
                                                font_name='Alfa Slab One',
                                                font_color=(25, 82, 44, 255)),
                 'hover': UITextureButtonStyle(font_size=int(40 * SCALE),
                                               font_name='Alfa Slab One',
                                               font_color=(195, 123, 3, 255)),
                 'press': UITextureButtonStyle(font_size=int(40 * SCALE),
                                               font_name='Alfa Slab One')}

BUTTON_STYLE2 = {'normal': UITextureButtonStyle(font_size=int(40 * SCALE),
                                                font_name='Alfa Slab One',
                                                font_color=(45, 40, 50, 255)),
                 'hover': UITextureButtonStyle(font_size=int(40 * SCALE),
                                               font_name='Alfa Slab One',
                                               font_color=(195, 123, 3, 255)),
                 'press': UITextureButtonStyle(font_size=int(40 * SCALE),
                                               font_name='Alfa Slab One')}
