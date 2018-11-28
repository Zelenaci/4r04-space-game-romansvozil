import pyglet, math
from pyglet.window import key
from . import spaceobject, resources, config, bullet


class Player(spaceobject.SpaceObject):

	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=resources.my_ship_image, group=pyglet.graphics.OrderedGroup(2), *args, **kwargs)
		self.scale = 1
		self.thrust = 20
		self.max_speed = 1200
		self.rotate_speed = 200
		self.bullet_speed = 1000

		self.pressed_keys = []
		#self.key_handler = key.KeyStateHandler()
		#self.event_handlers = [self, self.key_handler]

	def update(self, dt, my_ship):
		super(Player, self).update(dt, my_ship)

		self.xom += self.speed * dt * math.cos(math.pi / 2 - math.radians(self.rotation))
		self.yom += self.speed * dt * math.sin(math.pi / 2 - math.radians(self.rotation))

		self.xom = (config.MAP_X - self.smaller_side) if (self.xom + self.smaller_side) > config.MAP_X else self.xom
		self.xom = self.smaller_side if self.xom < self.smaller_side else self.xom

		self.yom = (config.MAP_Y - self.smaller_side) if (self.yom + self.smaller_side) > config.MAP_Y else self.yom
		self.yom = self.smaller_side if self.yom < self.smaller_side else self.yom


		if key.LEFT in self.pressed_keys:
			self.rotation -= self.rotate_speed * dt
		if key.RIGHT in self.pressed_keys:
			self.rotation += self.rotate_speed * dt

		if key.DOWN in self.pressed_keys:
			self.speed = (self.speed - 50) if self.speed >= 50 else 0
		if key.UP in self.pressed_keys:
			self.speed = (self.speed + self.thrust) if self.speed <= \
						self.max_speed else self.max_speed

	def make_bullet(self, batch=None):
		fired_bull = bullet.Bullet(batch=batch)
		fired_bull.xom = self.xom + math.sin(math.radians(self.rotation)) * self.smaller_side
		fired_bull.yom = self.yom + math.cos(math.radians(self.rotation)) * self.smaller_side
		fired_bull.speed = self.speed * 2 + 1000
		fired_bull.rotation = self.rotation
		return fired_bull
