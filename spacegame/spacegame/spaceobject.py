import pyglet, math
from . import util, config


class SpaceObject(pyglet.sprite.Sprite):
	
	def __init__(self, *args, **kwargs):
		super(SpaceObject, self).__init__(*args, **kwargs)

		self.args, self.kwargs = args, kwargs
		self.xom = 0
		self.yom = 0
		self.on_screen = True
		self.photo = self.image
		
		self.direction = 0
		self.speed = 0
		self.rspeed = 0
		
		self.dead = False
		
	def update(self, dt, hrac):
		new_x = self.xom - (hrac[0] - config.WINDOW_WIDTH // 2)
		new_y = self.yom - (hrac[1] - config.WINDOW_HEIGHT // 2)
		self.xom += self.speed * dt * math.cos(math.pi / 2 - math.radians(self.rotation))
		self.yom += self.speed * dt * math.sin(math.pi / 2 - math.radians(self.rotation))
		a = new_x <= -200 or new_x >= (config.WINDOW_WIDTH + 200)
		b = new_y <= -200 or new_y >= (config.WINDOW_HEIGHT + 200)
		was_on_screen = self.on_screen
		self.on_screen = False if a or b else True
		if self.on_screen and was_on_screen:
			self.x, self.y = new_x, new_y
		elif was_on_screen:
			self.delete()
			print('Something has been deleted..')
		elif not(was_on_screen) and self.on_screen:
			super(SpaceObject, self).__init__(img=self.photo, x=-150, y=-150)
			print('Someting has been rebuilt..')
		else:
			pass
			
		
		
	def collides_with(self, other_object):
		collision_distance = self.image.width * 0.5 * self.scale \
                             + other_object.image.width * 0.5 * other_object.scale
		actual_distance = util.distance(self.position, other_object.position)
		return (actual_distance <= collision_distance)

	def handle_collision_with(self, other_object):
		if other_object.__class__ is not self.__class__:
			self.dead = True

