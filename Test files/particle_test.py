from ursina import *
import numpy as np
import random

class ParticleSystem(Entity):
    def __init__(self, number_of_particles=100, duration=1, **kwargs):
        self.points = np.array([Vec3(0, 0, 0) for _ in range(number_of_particles)])
        self.directions = np.array([Vec3(random.random()-.5, random.random()-.5, random.random()-.5)*.05 for _ in range(number_of_particles)])
        self.frames = []

        for i in range(60 * duration):
            self.points += self.directions
            self.frames.append(copy(self.points))

        super().__init__(
            model=Mesh(vertices=self.points.tolist(), mode='point', static=False, render_points_in_3d=True, thickness=.1),
            t=0,
            duration=duration,
            **kwargs
        )

    def update(self):
        self.t += time.dt
        if self.t >= self.duration:
            destroy(self)
            return
        self.model.vertices = self.frames[floor(self.t * 60)].tolist()
        self.model.generate()

app = Ursina()
window.color = color.black

def input(key):
    if key == 'space':
        ParticleSystem(position=(random(-5, +5), random(), random()) * 2, color=color.random_color())

Text('Press SPACE to spawn particles', origin=(0,0), y=-.45)
EditorCamera()
app.run()