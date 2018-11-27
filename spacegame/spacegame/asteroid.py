import random, pyglet, math
from . import spaceobject, resources, config


class Asteroid(spaceobject.SpaceObject):

	def __init__(self, *args, **kwargs):
		super(Asteroid, self).__init__(resources.meteor_image, *args, **kwargs)
		self.rotate_speed = random.randint(0, 100)
		self.speed = 100
		self.direction = random.randint(0, 359)

		self.x, self.y = -200, -200

		#self.visible = False

	def update(self, dt, wind):
		super(Asteroid, self).update(dt, wind)

		self.xom += self.speed * dt * math.cos(math.pi / 2 - math.radians(self.direction))
		self.yom += self.speed * dt * math.sin(math.pi / 2 - math.radians(self.direction))

		if self.xom > (config.MAP_X - self.smaller_side):
			self.xom = config.MAP_X - self.smaller_side
			self.direction = - self.direction
		elif self.xom < self.smaller_side:
			self.xom = self.smaller_side
			self.direction = - self.direction
		if self.yom > (config.MAP_Y - self.smaller_side):
			self.yom = config.MAP_Y - self.smaller_side
			self.direction = 180 - self.direction
		elif self.yom < self.smaller_side:
			self.yom = self.smaller_side
			self.direction = 180 - self.direction


		if self.on_screen:
			self.rotation += self.rotate_speed * dt
