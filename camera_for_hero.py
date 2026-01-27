from arcade.camera import Camera2D
from consts import *


class CameraForHero(Camera2D):
    def __init__(self, hero, tile_map):
        super().__init__()
        self.hero = hero
        self.tile_map = tile_map

        self.world_width = int(self.tile_map.width * self.tile_map.tile_width * 3 * SCALE)
        self.world_height = int(self.tile_map.height * self.tile_map.tile_height * 3 * SCALE)

    def on_update(self):
        cam_x, cam_y = self.position
        dz_left = cam_x - DEAD_ZONE_W // 2
        dz_right = cam_x + DEAD_ZONE_W // 2
        dz_bottom = cam_y - DEAD_ZONE_H // 2
        dz_top = cam_y + DEAD_ZONE_H // 2

        px, py = self.hero.center_x, self.hero.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - DEAD_ZONE_H // 2

        half_w = self.viewport_width / 2
        half_h = self.viewport_height / 2
        target_x = max(half_w, min(self.world_width - half_w, target_x))
        target_y = max(half_h, min(self.world_height - half_h, target_y))

        smooth_x = (1 - CAMERA_LERP) * cam_x + CAMERA_LERP * target_x
        smooth_y = (1 - CAMERA_LERP) * cam_y + CAMERA_LERP * target_y
        self.cam_target = (smooth_x, smooth_y)

        self.position = (self.cam_target[0], self.cam_target[1])