import pyglet
from . import util

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

player_image = pyglet.resource.image('playerShip1_orange.png')
meteor_image = pyglet.resource.image('Meteors/meteorGrey_big1.png')
bullet_image = pyglet.resource.image('Lasers/laserBlue02.png')
background_image = pyglet.resource.image('Map/map_1.png')

util.centerimg(player_image)
util.centerimg(meteor_image)
util.centerimg(bullet_image)
