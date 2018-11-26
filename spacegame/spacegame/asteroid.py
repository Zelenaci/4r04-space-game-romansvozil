import random, pyglet
from . import spaceobject, resources


class Asteroid(spaceobject.SpaceObject):

	def __init__(self, *args, **kwargs):
		super(Asteroid, self).__init__(resources.meteor_image, *args, **kwargs)
		self.rotate_speed = random.randint(0, 100)

	def update(self, dt, wind):
		super(Asteroid, self).update(dt, wind)
		if self.on_screen:
			self.rotation += self.rotate_speed * dt
