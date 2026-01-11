import arcade
from arcade.particles import Emitter, EmitBurst, FadeParticle
from consts import *


def make_trace(hero):
    return Emitter(
        center_xy=(hero.center_x, hero.center_y),
        emit_controller=EmitBurst(1),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=arcade.texture.make_soft_square_texture(int(hero.height), arcade.color.BLUEBERRY),
            change_xy=(0, 0),
            lifetime=0.2,
            start_alpha=220, end_alpha=0
        ),
    )

class GameView_common(arcade.View):
    def __init__(self):
        super().__init__()
        self.emitter_trace = {}

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.walls_list.draw(pixelated=True)
        for h in self.emitter_trace:
            for e in self.emitter_trace[h]:
                e.draw()

        self.hero_l.draw(pixelated=True)

    def on_update(self, delta_time):
        for hero in self.hero_l:
            if hero.dash:
                if hero not in self.emitter_trace:
                    self.emitter_trace[hero] = [make_trace(hero)]
                else:
                    self.emitter_trace[hero].append(make_trace(hero))

            hero.on_update(delta_time)
            hero.update_animation(delta_time)
        self.world_camera.on_update()

        emitter_trace_copy = self.emitter_trace.copy()
        for h in emitter_trace_copy:
            for e in emitter_trace_copy[h]:
                e.update(delta_time)
        for h in emitter_trace_copy:
            for e in emitter_trace_copy[h]:
                if e.can_reap():
                    self.emitter_trace[h].remove(e)

    def on_key_press(self, key, modifiers):
        self.hero.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.hero.on_key_release(key, modifiers)
