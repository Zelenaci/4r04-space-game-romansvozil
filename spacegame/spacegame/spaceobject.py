import pyglet, math
from . import util, config


class SpaceObject(pyglet.sprite.Sprite):

	def __init__(self, *args, **kwargs):
		super(SpaceObject, self).__init__(*args, **kwargs)

		self.args, self.kwargs = args, kwargs
		self.xom = 0
		self.yom = 0
		self.on_screen = True
		#self.photo = self.image

		self.direction = 0
		self.speed = 0
		self.rspeed = 0

		self.smaller_side = min(self.width, self.height) // 2

		self.dead = False

	def update(self, dt, my_ship):
		new_x = self.xom - (my_ship.xom - config.WINDOW_WIDTH // 2)
		new_y = self.yom - (my_ship.yom - config.WINDOW_HEIGHT // 2)
		a = new_x <= - config.WINDOW_WIDTH or new_x >= (config.WINDOW_WIDTH * 2)
		b = new_y <= - config.WINDOW_HEIGHT or new_y >= (config.WINDOW_HEIGHT * 2)
		was_on_screen = self.on_screen
		self.on_screen = False if a or b else True

		if self.on_screen and was_on_screen:
			if my_ship.xom < (config.WINDOW_WIDTH / 2):
				self.x = self.xom
			elif my_ship.xom > (config.MAP_X - (config.WINDOW_WIDTH / 2)):
				self.x = self.xom - config.MAP_X + config.WINDOW_WIDTH
			else:
				self.x = new_x

			if my_ship.yom < (config.WINDOW_HEIGHT / 2):
				self.y = self.yom
			elif my_ship.yom > (config.MAP_Y - (config.WINDOW_HEIGHT / 2)):
				self.y = self.yom - config.MAP_Y + config.WINDOW_HEIGHT
			else:
				self.y = new_y

		elif was_on_screen:
			self.visible = False
			#self.delete()
		elif not(was_on_screen) and self.on_screen:
			self.visible = True
			#super(SpaceObject, self).__init__(img=self.photo, x=-150, y=-150)
		else:
			pass

	def collides_with(self, other_object):
		collision_distance = min(self.width, self.height) * 0.5 \
                             + min(other_object.width, other_object.height) * 0.5
		actual_distance = util.distance(self.position, other_object.position)
		return (actual_distance <= collision_distance)

	def handle_collision_with(self, other_object):
		if other_object.__class__ is not self.__class__:
			self.dead = True
