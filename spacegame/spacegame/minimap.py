import pyglet
from . import resources, config


class MiniMap(pyglet.sprite.Sprite):

    def __init__(self, enemy=False, batch=None, *args, **kwargs):
        super(MiniMap, self).__init__(img=resources.background_image, batch=batch, group=pyglet.graphics.OrderedGroup(1), *args, **kwargs)
        self.scale = 0.2
        self.x = config.WINDOW_WIDTH - self.width
        self.minimap_scale_x = self.width / config.MAP_X
        self.minimap_scale_y = self.height / config.MAP_Y
        self.enemy = enemy
        self.my_ship = pyglet.sprite.Sprite(resources.my_ship_image, batch=batch, group=pyglet.graphics.OrderedGroup(2))
        self.my_ship.scale = 0.2
        if enemy:
            self.enemy_ship = pyglet.sprite.Sprite(resources.enemy_ship_image, batch=batch, group=pyglet.graphics.OrderedGroup(2))
            self.enemy_ship.scale = 0.2

    def update(self, my_ship, enemy_ship=False):

        self.my_ship.x = my_ship.xom * self.minimap_scale_x + config.WINDOW_WIDTH - self.width
        self.my_ship.y = my_ship.yom * self.minimap_scale_y
        self.my_ship.rotation = my_ship.rotation

        if enemy_ship:
             self.enemy_ship.x = enemy_ship.xom * self.minimap_scale_x + config.WINDOW_WIDTH - self.width
             self.enemy_ship.y = enemy_ship.yom * self.minimap_scale_x
             self.enemy_ship.rotation = enemy_ship.rotation
