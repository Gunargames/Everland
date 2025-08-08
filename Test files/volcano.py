from ursina import *
from random import uniform

app = Ursina()

volcano = Entity(model='cone', color=color.gray, scale=3, position=(0,0,0))
lava_particles = []

def erupt():
    for _ in range(10):
        lava = Entity(model='sphere', color=color.orange, scale=0.2, position=volcano.position)
        lava.animate_position(
            lava.position + Vec3(uniform(-2,2), uniform(3,6), uniform(-2,2)),
            duration=1,
            curve=curve.linear
        )
        lava_particles.append(lava)

eruption_trigger = Button(text='Erupt', scale=0.2, position=(-0.7,-0.4), on_click=erupt)

app.run()