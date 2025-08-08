from ursina import *

app = Ursina()

class UnderwaterEffect(Entity):
    def __init__(self, blur_texture=None, fog_density=0.03, tint_color=color.rgba(50, 100, 255, 100), enabled=True):
        super().__init__()
        self.tint_color = tint_color
        self.fog_density = fog_density
        self.blur_texture = blur_texture
        self.blur_overlay = None
        self.active = False

        if enabled:
            self.enable()

    def enable(self):
        if self.active:
            return
        self.active = True

        # Apply fog
        window.fog_color = self.tint_color
        window.fog_density = self.fog_density

        # Apply camera tint
        camera.overlay_color = self.tint_color

        # Optional blur overlay
        if self.blur_texture:
            self.blur_overlay = Entity(
                model='quad',
                texture=self.blur_texture,
                scale=2,
                color=color.rgba(255, 255, 255, 80),
                parent=camera.ui,
                z=-1
            )

    def disable(self):
        if not self.active:
            return
        self.active = False

        # Remove fog and tint
        window.fog_density = 0
        camera.overlay_color = color.clear

        # Remove blur overlay
        if self.blur_overlay:
            destroy(self.blur_overlay)
            self.blur_overlay = None

app.run()