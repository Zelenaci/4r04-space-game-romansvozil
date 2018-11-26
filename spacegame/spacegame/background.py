import pyglet
from . import resources, config


class BackGround(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(BackGround, self).__init__(img=resources.background_image,group=pyglet.graphics.OrderedGroup(0), *args, **kwargs)
        self.scx = (self.width - config.WINDOW_WIDTH) / config.MAP_X
        self.scy = (self.height - config.WINDOW_HEIGHT) / config.MAP_Y
        self.x, self.y = 0, 0

    def update(self, hrac):
        self.x = - hrac[0] * self.scx
        self.y = - hrac[1] * self.scy