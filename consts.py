from arcade.gui import UITextureButtonStyle

SCALE = 0.5
SCREEN_WIDTH = int(1920 * SCALE)
SCREEN_HEIGHT = int(1080 * SCALE)

GRAVITY = 5 * SCALE
MAX_JUMPS = 1
JUMP_BUFFER = 0.12
MOVE_SPEED = 10 * SCALE
COYOTE_TIME = 0.08
JUMP_SPEED = 40 * SCALE

CAMERA_LERP = 0.08

DEAD_ZONE_W = int(SCREEN_WIDTH * 0.35)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.45)

BUTTON_STYLE1 = {'normal': UITextureButtonStyle(font_size=int(40 * SCALE),
                                                font_name='Comic Sans MS pixel rus eng',
                                                font_color=(225, 153, 33, 255)),
                 'hover': UITextureButtonStyle(font_size=int(40 * SCALE),
                                               font_name='Comic Sans MS pixel rus eng',
                                               font_color=(195, 123, 3, 255)),
                 'press': UITextureButtonStyle(font_size=int(40 * SCALE),
                                               font_name='Comic Sans MS pixel rus eng')}
