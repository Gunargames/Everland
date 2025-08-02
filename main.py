from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.conversation import Conversation

# Initialize the game
app = Ursina()

# island one

temple = Entity(model='temple', texture='Textures/House wall.jpeg', position=(-3500, -90, 1000), scale=5)
shrine_gem = Entity(model='gems', scale=2, color=color.green, collider='mesh', position=(3500, -73, 3000), rotation_y=-130)
shrine = Entity(model='shrine', scale=5, texture='Textures/House wall.jpeg', collider='mesh', position=(3500, -80, 3000), rotation_y=-130)
player = FirstPersonController(collider='box')
island = Entity(model='iisland', scale=60, texture='Textures/Grasss.jpg', collider='mesh', position=(1000, -60, 300), rotation_y=-130)
statue = Entity(model='statue', scale=60, texture='Textures/House wall.jpeg', collider='mesh', position=(1000, -60, 300), rotation_y=-130)
sword = Entity(model='sword oof doom', parent=camera, position=Vec3(0.5, -0.5, 1), scale=(0.2), origin_z=-5)
world = Entity(model='everythiing', scale=5, texture='grass', collider='mesh', position=(0, -60, 0))
house_layout = Entity(model='House layooout', scale=5, texture='Textures/House wall.jpeg', collider='mesh', texture_scale=(10, 10), position=(0, -60, 0))
water = Entity(model='plane', scale=10000, texture='Water', texture_scale=(40, 40), position=(0, -70, 0))
under_sea = Entity(model='plane', scale=10000, texture='Textures/Sand.jpg', texture_scale=(80, 80), collider='box', position=(0, -90, 0))
boat = Entity(model='booat', scale=5, texture='Textures/Tree texture.jpg', collider='mesh', position=(0, -60, 0))
Tree_layout = Entity(model='Treeeee pattern', scale=5, texture='Textures/Tree texture.jpg', collider='mesh', position=(0, -60, 0))
everland = Entity(model='Everland', scale=5, texture='Textures/House wall.jpeg', collider='mesh', position=(0, -60, 0))

sky = Entity(model='sphere', scale=10000, texture='sky_sunset', double_sided=True, rotation=(0, 180, 0))

#text

inscription_text = Text('here lies hope', origin=(0,0), background=True)
inscription_text.visible = False

# Audio

WalkingSound = Audio('audio/walking-sound-effect-272246.mp3', loop=False, volume=1)
GameMusic = Audio('audio/koden-348767.mp3', loop=True, volume=0.5, autoplay=True)

# boat movement

def move_boat_to(target_pos, speed=5):
    boat.animate_position(target_pos, duration=distance(boat.position, target_pos)/speed, curve=curve.linear)
    player.animate_position(target_pos + Vec3(0, 2, 0), duration=distance(player.position, target_pos)/speed, curve=curve.linear)

# Create quest progress text
quest_text = Text(text='Fragments: 0/3', position=(-0.85, 0.4), scale=2)
# Create text for when you enter the game
welcome_text = Text(text='Welcome to Everland', position=(0, 0.4), scale=2, background=False)
invoke(setattr, welcome_text, 'visible', False, delay=5)





# Update function now also refreshes progress display
def update():
    global time_of_day, enemy_spawned
    time_of_day += time.dt / 300
    if time_of_day > 1:
        time_of_day = 0

    # adjust sky brightness and color
    sky.rotation_y += time.dt * 5
    if time_of_day < 0.5:
        sky.color = color.white
    else:
        sky.color = color.gray

    # Walking sound logic
    if held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']:
        if not WalkingSound.playing:
            WalkingSound.play()
    else:
        WalkingSound.stop()

    # Quest progress update
    if quest_manager.quest_active and not quest_manager.quest_completed:
        quest_text.text = f'Fragments: {quest_manager.fragments_collected}/{quest_manager.total_fragments}'
    elif quest_manager.quest_completed:
        quest_text.text = "Quest Complete"

    if distance(player.position, fara.position) < 5:
        fara_name.visible = True
    else:
        fara_name.visible = False

    if distance(player.position, elder_miro.position) < 5:
        npc_name.visible = True
    else:
        npc_name.visible = False
    if distance(player.position, zintra.position) < 5:
        zintra_name.visible = True
    else:
        zintra_name.visible = False





# Simple inventory implementation
class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name):
        self.items[item_name] = self.items.get(item_name, 0) + 1
        self.update_ui()

    def remove_item(self, item_name):
        if item_name in self.items:
            self.items[item_name] -= 1
            if self.items[item_name] <= 0:
                del self.items[item_name]
            self.update_ui()

    def has_item(self, item_name):
        return item_name in self.items

    def update_ui(self):
        content = '\n'.join([f'{name}: {amount}' for name, amount in self.items.items()])
        inventory_panel.content.text = content



# goblin = Entity(model='goblin', position=Vec3(0, -20, 0), collider='mesh')
# goblin.add_script(SmoothFollow(target=player, speed=1))

inventory_panel = WindowPanel(
    title='Inventory',
    content=[Text(text='', scale=1)],  # Bigger text
    enabled=False,
    scale=0.5,
    scale_x=0.9,  # Make the panel larger overall
    position=(-0.6, 0.5),  # Position it to the right side of the screen
)
# Create an inventory instance
player_inventory = Inventory()


fara = Entity(model='statue', color=color.green, scale=(1,1,1), position=(1000, -6, 305), collider='box', rotation_y=160)
fara_name = Text(text='Fara the Herbalist', position=(0, 0.42), scale=1.2, background=True)
fara_name.visible = False

zintra = Entity(model='statue', color=color.cyan, scale=(1, 1, 1), position=(1000, -4, 290), collider='box')
zintra_name = Text(text='Zintra the Memory Keeper', position=(0, 0.42), scale=1.2, background=True)
zintra_name.visible = False
zintra_dialog = [
    "Memories whisper through the sands...",
    "Would you like to remember who you were before the light scattered?",
    "The relic remembers. Now... do you?"
]
zintra_dialog3 = [
    "You have fragments, let me help you remember."
    "Your dad was a hero, a guardian of light."
    "But darkness fell, scattering the light and your memories."
    "Now, you must gather the fragments to restore his past."
]
zintra_dialog_index = 0
zintra_dialog_text = Text(text='', color=color.violet, position=(0, -0.35), scale=1.5, background=False)
zintra_dialog_text.visible = False

allGemsCollected = False
relicCollected = False
sunrootCollected = False



elder_miro = Entity(model='statue', color=color.gold, scale=(1, 1, 1), position=(-55, -18, -12), collider='box')
npc_name = Text(text='Elder Miro', position=(0, 0.45), scale=1.5, background=True)
npc_name.visible = False

# Define QuestManager
class QuestManager:
    def __init__(self):
        self.fragments_collected = 0
        self.total_fragments = 3
        self.quest_active = True
        self.quest_completed = False

    def collect_fragment(self):
        if self.quest_active and not self.quest_completed:
            self.fragments_collected += 1
            print(f'Fragment collected: {self.fragments_collected}/{self.total_fragments}')
            if self.fragments_collected >= self.total_fragments:
                self.complete_quest()

    def complete_quest(self):
        self.quest_completed = True
        print("Quest Complete: Echoes of the Forgotten Light")
        sword.color = color.yellow
        sword.scale *= 1
        sword.tooltip = Tooltip("Empowered Sword")
        Audio('audio/success.mp3', loop=False, volume=1).play()

quest_manager = QuestManager()

fragments = []

for pos in [(-55, -15, -3), (3220, -45, 1900), (-3990, -10, -1100)]:
    frag = Entity(model='gems', scale=0.5, color=color.azure, position=pos, collider='box')
    
    
    fragments.append(frag)

def frags(key):
    if key == 'e' and quest_manager.quest_active:  # <-- Add this check
        for frag in fragments[:]:
            if distance(player.position, frag.position) < 2:
                quest_manager.collect_fragment()
                fragments.remove(frag)
                destroy(frag)
                allGemsCollected == True
                break
    elif key == 'e' and quest_manager.quest_active == False:
        pass


fara_dialog = [
    "Shh! The statue listens...",
    "Bring me a sunroot and I'll brew a potion of clarity."
]

npc_dialog = [
    "Welcome to Everland, son of raven.",
    "Darkness fell, light scattered…",
    "Bring me the relic and I shall restore hope."
]

zintra_dialog = [
    "Memories whisper through the sands.",
    "Would you like to remember who you were before the light scattered?"
    "I can help you with that, but it will cost you a fragment of your past."
    "collect fragments to remember your past."
]

zintra_dialog2 = [
    "You have fragments, let me help you remember."
    "You were a hero, a guardian of light."
    "But darkness fell, scattering the light and your memories."
    "Now, you must gather the fragments to restore your past."
]


dialog_index = 0
dialog_text = Text(text='', color=color.blue, position=(0, -0.4), scale=1.5, background=False)
dialog_text.visible = False

sunroot_found = False

# player inreactions
# input for quitting the game
def input(key):
    global zintra_dialog_index
    global zintra_dialog3
    global bow_equipped
    if key == 'escape':
        quit()
    if key == 'shift':
        player.speed = 10
    if key == 'e' and distance(player.position, shrine_gem) < 10:
        if not quest_manager.quest_completed:
            shrine_gem.color = color.yellow
            shrine_gem.tooltip = Tooltip("Shrine Gem")
            destroy(shrine_gem)
    if key == 'shift up':
        player.speed = 5
    if key == 'left mouse':
        Audio.play('audio/sword-sound-260274.mp3', loop=False, volume=0.5)
    if key == 'i':
        inventory_panel.enabled = not inventory_panel.enabled
        if inventory_panel.enabled:
            application.paused = True
            mouse.visible = True
            mouse.locked = False
        else:
            application.paused = False
            mouse.visible = False
            mouse.locked = True
    if key == 'i':
        inventory_panel.enabled = not inventory_panel.enabled

        if inventory_panel.enabled:
            application.paused = True
            mouse.visible = True
            mouse.locked = False
        else:
            application.paused = False
            mouse.visible = False
            mouse.locked = True

    # Keep your other key events here...
    if key == '1':
        player.position = Vec3(0, 0, 0)
    if key == '4':
        player.position = Vec3(1000, 0, 300)
    if key == '2':
        player.position = Vec3(3200, 0, 2000)
    if key == '3':
        player.position = Vec3(-4000, 0, -1200)
    if key == 'f':
        player.gravity = -1
    if key == 'f up':
        player.gravity = 1
    if key == 'e' and distance(player.position, boat.position) < 50:
        if not quest_manager.quest_active:
            quest_manager.quest_active = True
            inscription_text.text = "The old boat whispers: 'Light is scattered... bring it home.'"
            inscription_text.visible = True
            inscription_text.position = (0, 0.4)
            quest_text.visible = True


            invoke(setattr, inscription_text, 'visible', False, delay=5)
    if key == 'b' and distance(player.position, boat.position) < 50:
        target_island = Vec3(1000, -100, 300)
        move_boat_to(target_island)
    if key == 'n':  # Move to another island
        target_island = Vec3(3200, -100, 2000)
        move_boat_to(target_island)
    if key == 'm':
        player.speed = 100
    if key == 'm up':
        player.speed = 5
    global relic_found
    if key == 'e' and not relic_found and distance(player.position, relic.position) < 20:
        relic_found = True
        destroy(relic)
        inscription_text.text = "Good job, hero! You found the relic!, now return to the Elder." \
        " he has much to say."
        inscription_text.visible = True
        inscription_text.background = False
        invoke(setattr, inscription_text, 'visible', False, delay=6)
        Audio('audio/success.mp3', loop=False, volume=1).play()
        relicCollected == True
        global dialog_index
    if key == 'e' and distance(player.position, sunroot.position) < 20:
        destroy(sunroot)
        sunrootCollected == True
        global dialog_index
    if key == 'left mouse' and bow_equipped:
        shoot_arrow()

    if key == 'e' and distance(player.position, elder_miro.position) < 5:
        dialog_text.visible = True
        dialog_text.text = npc_dialog[dialog_index]
        dialog_index = (dialog_index + 1) % len(npc_dialog)
        invoke(setattr, dialog_text, 'visible', False, delay=4)
    if key == 'e' and distance(player.position, fara.position) < 5:
        dialog_text.visible = True
    if key == 'e' and distance(player.position, zintra.position) < 5:
        zintra_dialog_text.visible = True
        zintra_dialog_text.text = zintra_dialog[zintra_dialog_index]
        zintra_dialog_index = (zintra_dialog_index + 1) % len(zintra_dialog)
        invoke(setattr, zintra_dialog_text, 'visible', False, delay=4)
    if key == '8':
        bow.enabled = True  # Show the bow when key 8 is pressed
    else:
        bow.enabled = False  # Hide the bow when any other key is pressed
    if key == '8':
        bow_equipped = not bow_equipped
        sword.enabled = not bow_equipped
        bow.enabled = bow_equipped

    if key == '9':
        bow_equipped = False
        sword.enabled = True
        bow.enabled = False 


        sword.scale *= 1
    frags(key)

relic = Entity(model='relic', scale=5, texture='Textures/Tree texture.jpg', position=(200, -80, -50), collider='box')
relic_found = False

sunroot = Entity(model='flower', scale=6, color=color.pink, position=(1000, 30, 300), collider='box')



from ursina import time

time_of_day = 0  # ranges from 0 to 1 (0 = dawn, 0.5 = noon, 1 = midnight)


bow = Entity(
    model='bow',  # Use a custom model if you have one!
    texture='Textures/BowTexture.jpg',
    parent=camera,
    position=Vec3(0.6, -0.5, 1),
    scale=(0.3),
    origin_z=-5,
    enabled=True,
    rotation_y=90,
    rotation_x=90
)

class allTheItems(Entity):
    if allGemsCollected == True and relicCollected == True and sunrootCollected == True:
        player.position = Vec3(0, 0, 0)





bow.enabled = False
sword.enabled = True  # Start with sword equipped

def shoot_arrow():
    arrow = Entity(
        model='cube',
        color=color.red,
        scale=(0.1, 0.1, 0.5),
        position=camera.world_position,
        rotation=camera.rotation,
        collider='box'
    )
    arrow.animate_position(camera.forward * 100 + arrow.position, duration=1, curve=curve.linear)
    destroy(arrow, delay=1.5)

def update_ui(self):
    text_element = inventory_panel.content[0]
    content = '\n'.join([f'{name}: {amount}' for name, amount in self.items.items()])
    text_element.text = content

        
# Add a simple UI

# Crosshair
crosshair = Entity(model='quad', scale=0.02, color=color.white, position=(0, 0, 0.1), origin=(0.5, 0.5))

bow_equipped = False








# Run the game
window.title = 'Everland'
window.fullscreen = True



app.run()