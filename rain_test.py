from ursina import *
from random import random

app = Ursina()
raindrops = []

def spawn_rain():
    drop = Entity(
        model='cube',
        color=color.azure.tint(-0.2),
        scale=(0.02, 0.4, 0.02),
        position=(random()*10 - 5, random()*5 + 5, random()*10 - 5)
    )
    raindrops.append(drop)

def update():
    if random() < time.dt * 10:
        spawn_rain()

    for drop in raindrops[:]:
        drop.y -= time.dt * 15
        if drop.y < 0:
            raindrops.remove(drop)
            destroy(drop)

ground = Entity(model='plane', scale=20, color=color.dark_gray, collider='box')
EditorCamera()
app.run()