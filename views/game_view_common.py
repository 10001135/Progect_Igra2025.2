import arcade

class GameView_common(arcade.View):
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.walls_list.draw(pixelated=True)
        self.hero_l.draw(pixelated=True)

    def on_update(self, delta_time):
        for hero in self.hero_l:
            hero.on_update(delta_time)
            hero.update_animation(delta_time)
        self.world_camera.on_update()

    def on_key_press(self, key, modifiers):
        self.hero.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.hero.on_key_release(key, modifiers)
