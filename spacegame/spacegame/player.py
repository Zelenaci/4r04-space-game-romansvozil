import pyglet, math
from pyglet.window import key
from . import spaceobject, resources, config


class Player(spaceobject.SpaceObject):
	
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
		self.thrust = 20
		self.max_speed = 1700
		self.rotate_speed = 200
		self.bullet_speed = 1000
		
		self.pressed_keys = []
		#self.key_handler = key.KeyStateHandler()
		#self.event_handlers = [self, self.key_handler]
		
	def update(self, dt, wind):
		super(Player, self).update(dt, wind)
		
		self.xom = config.MAP_X if self.xom > config.MAP_X else self.xom
		self.xom = 0 if self.xom < 0 else self.xom

		self.yom = config.MAP_Y if self.yom > config.MAP_Y else self.yom
		self.yom = 0 if self.yom < 0 else self.yom

		
		if key.LEFT in self.pressed_keys:
			self.rotation -= self.rotate_speed * dt
		if key.RIGHT in self.pressed_keys:
			self.rotation += self.rotate_speed * dt
			
		if key.DOWN in self.pressed_keys:
			self.speed = (self.speed - 50) if self.speed >= 50 else 0
		if key.UP in self.pressed_keys:
			self.speed = (self.speed + self.thrust) if self.speed <= \
						self.max_speed else self.max_speed
