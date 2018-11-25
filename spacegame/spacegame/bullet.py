from . import resources, spaceobject
import pyglet

class Bullet(spaceobject.SpaceObject):
	
	def __init__(self, *agrs, **kwargs):
		super(Bullet, self).__init__(img=resources.bullet_image, *args, **kwargs)
		self.source = ''
		self.is_bullet = True
		pyglet,clock.schedule_once(self.die, 1)
		
	def die(self, dt):
		self.dead = True
