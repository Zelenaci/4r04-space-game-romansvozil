import spacegame
import pyglet, random

window = pyglet.window.Window(spacegame.config.WINDOW_WIDTH, spacegame.config.WINDOW_HEIGHT)
batch = pyglet.graphics.Batch()

'''
image = pyglet.image.load('/home/roman/git/spacegame/resources/playerShip1_blue.png')		
pokus = spacegame.asteroid.Asteroid(batch=batch)
pokus.xom = 100
pokus.yom = -1000
pokus.update(0.1, wind)
print(pokus.x, pokus.y, pokus.xom, pokus. yom)

pokus.xom = 200
pokus.yom = 200
pokus.update(0.1, wind)
print(pokus.x, pokus.y, pokus.xom, pokus. yom)

pokus.update(0.1, wind)
print(pokus.x, pokus.y, pokus.xom, pokus. yom)
print(pokus.batch)
'''

def update(dt):
	player.update(dt, (player.xom, player.yom))
	for x in range(len(meteors)):
		meteors[x].update(dt, (player.xom, player.yom))

player = spacegame.player.Player(batch=batch)
player.xom = 1000
player.yom = 1200

meteors = []
for x in range(0, spacegame.config.METEORS):
	meteor = spacegame.asteroid.Asteroid(batch=batch)
	meteor.xom = random.randint(0, spacegame.config.MAP_X)
	meteor.yom = random.randint(0, spacegame.config.MAP_Y)
	meteors.append(meteor)

@window.event
def on_draw():
	window.clear()
	batch.draw()
	
@window.event
def on_key_press(symbol, modifiers):
	player.pressed_keys.append(symbol)

@window.event
def on_key_release(symbol, modifiers):
	player.pressed_keys.remove(symbol)

pyglet.clock.schedule_interval(update, 0.02)
pyglet.app.run()
