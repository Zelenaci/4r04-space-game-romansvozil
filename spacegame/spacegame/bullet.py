from . import resources, spaceobject
import pyglet, math

class Bullet(spaceobject.SpaceObject):

	def __init__(self, batch=None, *args, **kwargs):
		super(Bullet, self).__init__(img=resources.bullet_image,batch=batch, *args, **kwargs)
		self.source = None
		self.is_bullet = True
		pyglet.clock.schedule_once(self.die, 2)

	def die(self, dt):
		self.dead = True
		self.delete()

	def update(self, dt, player):
		super(Bullet, self).update(dt, player)
		self.xom += self.speed * dt * math.cos(math.pi / 2 - math.radians(self.rotation))
		self.yom += self.speed * dt * math.sin(math.pi / 2 - math.radians(self.rotation))
