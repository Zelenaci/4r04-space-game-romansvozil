import pyglet
from math import sin, cos, radians, pi, sqrt
from random import randint
WINDOW_WIDTH, WINDOW_HEIGHT = 1300, 700 #1366, 768
MAP_X, MAP_Y = 20000, 20000
METEORS = 3000
fps = 144
batch = pyglet.graphics.Batch()
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
keys = []
space_things = []

current_window_x = 0
current_window_y = 0

life = 1

"""______________________________OBJECT_____________________________________"""

def load_image(path):
    load = pyglet.image.load(path)
    return load


class Main(object):

    def __init__(self):
        self.new_game()
        pyglet.clock.schedule_interval(self.tick, 1 / fps)
        pyglet.app.run()

    def new_game(self):
        space_things.append(PlayerShip("test.png", MAP_X // 2, MAP_Y // 2))
        space_things.append(BackGround('background.jpeg'))
        space_things.append(MiniMap('minimap.jpg', 'target.png'))
        space_things.append(Coordinates(50, 50))
        for _ in range(0, METEORS):
            while True:
                x = randint(0, MAP_X)
                y = randint(0, MAP_Y)
                if (x < ((MAP_X / 2) - 500) or (x > ((MAP_X / 2) + 500))) and (y < ((MAP_Y / 2) - 500) or (y > ((MAP_Y / 2) + 500))):
                    break
            space_things.append(Meteor('PNG/Meteors/meteorBrown_big1.png', x, y))

    def end_game(self):
        pass

    def load_config(self):
        pass

    def tick(self, dt):
        if life:
            for thing in space_things:
                if thing.name == 'meteor':
                    thing.adddelbatch()
                    thing.controlinwindow()
                    thing.refresh()
                    thing.collision()
                elif thing.name == 'playership':
                    thing.control()
                    thing.move(dt)
                    thing.border()
                    thing.drag()
                    thing.refresh()
                    thing.other()
                elif thing.name == 'background':
                    thing.move()
                    thing.refresh()
                elif thing.name == 'minimap':
                    thing.move()
                elif thing.name == 'coordinates':
                    thing.update_coor()


class Label(object):

    def __init__(self,x , y, text):
        self.winx = x
        self.winy = y
        self.text = text
        self.label = pyglet.text.Label(text=text, x=x, y=y, batch=batch, group=pyglet.graphics.OrderedGroup(3))

    def change_pos(self, new_x, new_y):
        self.winx = new_x
        self.winy = new_y

    def new_text(self, text):
        self.label.text = text

    def refresh(self):
        self.label.x = self.winx
        self.label.y = self.winy

class Coordinates(Label):

    def __init__(self,x ,y, text=''):
        super().__init__(x, y, text)
        self.name = 'coordinates'

    def update_coor(self):
        self.new_text('x: {0}, y: {1}'.format(int(space_things[0].x), int(space_things[0].y)))


class MiniMap(object):

    def __init__(self, mmimg_file, tgimg_file):
        self.name = 'minimap'
        self.mmimage = load_image(mmimg_file)
        self.tgimage = load_image(tgimg_file)
        self.tgimage.anchor_x = self.tgimage.width // 2
        self.tgimage.anchor_y = self.tgimage.height // 2
        self.mmsprite = pyglet.sprite.Sprite(self.mmimage, batch=batch, group=pyglet.graphics.OrderedGroup(2))
        self.tgsprite = pyglet.sprite.Sprite(self.tgimage,batch=batch, group=pyglet.graphics.OrderedGroup(3))
        self.mmsprite.x = WINDOW_WIDTH - self.mmimage.width
        self.mmsprite.y = 0
        self.tgsprite.x = 0
        self.tgsprite.y = 0
        self.scale_x = self.mmsprite.width / MAP_X
        self.scale_y = self.mmsprite.height / MAP_Y

    def move(self):
        self.tgsprite.x = space_things[0].x * self.scale_x + WINDOW_WIDTH - self.mmsprite.width
        self.tgsprite.y = space_things[0].y * self.scale_y

class BackGround(object):

    def __init__(self, img_file):
        self.name = 'background'
        self.image = load_image(img_file)
        self.sprite= pyglet.sprite.Sprite(self.image, batch=batch, group=pyglet.graphics.OrderedGroup(0))
        self.scale_x = (self.sprite.width - WINDOW_WIDTH) / MAP_X
        self.scale_y = (self.sprite.height - WINDOW_HEIGHT) / MAP_Y
        self.winy = 0
        self.winx = 0

    def move(self):
        self.winx =  - space_things[0].x * self.scale_x
        self.winy = - space_things[0].y * self.scale_y

    def refresh(self):
        self.sprite.x = self.winx
        self.sprite.y = self.winy

class SpaceObject(object):

    def __init__(self, img_file, x, y):
        self.x = x # globalni souradnice
        self.y = y  # -//-
        self.winx = 0 # v okne
        self.winy = 0 # -//-
        self.image = load_image(img_file)
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        self.rotation = 0
        self.in_window = 1
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch, group=pyglet.graphics.OrderedGroup(1))
        self.hitbox = (self.image.width / 2) if self.image.width < self.image.height else (self.image.height / 2)
    
    def refresh(self):
        self.winx = self.x - (space_things[0].x - window.width // 2)
        self.winy = self.y - (space_things[0].y - window.height // 2)
        if self.in_window:
            self.sprite.x = self.winx
            self.sprite.y = self.winy
            self.sprite.rotation = self.rotation

    def move(self, dt):
        self.speed = self.maxspeed if self.speed > self.maxspeed else self.speed
        self.speed = 0 if self.speed < 0 else self.speed
        self.x += dt * self.speed * cos(pi/2 - radians(self.direction))
        self.y += dt * self.speed * sin(pi/2 - radians(self.direction))

    def inwindow(self):
        x = self.winx <= -200 or self.winx >= (window.width + 200)
        y = self.winy <= -200 or self.winy >= (window.height + 200)
        return False if x or y else True

    def controlinwindow(self):
        self.in_window = self.inwindow()

    def adddelbatch(self):
        a = self.in_window
        b = self.inwindow()
        if a and b:
            pass
        elif a:
            self.sprite.delete()
        elif b and not(a):
            self.sprite = pyglet.sprite.Sprite(self.image, batch=batch, group=pyglet.graphics.OrderedGroup(1))
        else:
            pass

    def collision(self):
        global life
        if sqrt((self.x - space_things[0].x) ** 2 + (self.y - space_things[0].y) ** 2) <= self.hitbox + space_things[0].hitbox:
            life = 0
            print('You died!')



"""_______________________________PLAYER____________________________________"""
class PlayerShip(SpaceObject):
    
    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.name = 'playership'
        self.direction = 0
        self.speed = 0
        self.maxspeed = 700
        self.thrust = 50         # zrychlení
        self.deceleration = 100   # zpomalení
        self.rspeed = 10         # rychlost otáčení
        #pyglet.clock.schedule_interval(self.tick, 1 / fps)

    def __str__(self):
        return str(self.x) + ' ' + str(self.y)
    
    def control(self):
        """W = 119
           S = 115
           A = 97
           D = 100
           spc = 32"""
           
        for key in keys:
            if key == 119:
                self.speed += self.thrust
            elif key == 115:
                self.speed -= self.thrust
            elif key == 97:
                self.direction -= 0.001 * self.speed * self.rspeed
                self.rotation -= 0.001 * self.speed * self.rspeed
            elif key == 100:
                self.direction += 0.001 * self.speed * self.rspeed
                self.rotation += 0.001 * self.speed * self.rspeed

    def border(self):
        if self.x >= MAP_X:
            self.x = MAP_X
        elif self.x <= 0:
            self.x = 0

        if self.y >= MAP_Y:
            self.y = MAP_Y
        elif self.y <= 0:
            self.y = 0

    def drag(self):
        self.speed -= self.deceleration/fps

    def other(self):
        global current_window_y, current_window_x
        current_window_x = self.x + window.width / 2
        current_window_y = self.y + window.height / 2


"""______________________________________ENEMY______________________________"""
class EnemyShip(SpaceObject):
    pass

"""__________________________________________METEOR_________________________"""
class Meteor(SpaceObject):

    def __init__(self, img_file, x, y):
        super().__init__(img_file, x, y)
        self.name = 'meteor'
        #pyglet.clock.schedule_interval(self.tick, 1 / fps)


"""_______________________________EVENTS____________________________________"""
@window.event
def on_key_press(symbol, modifiers):
    keys.append(symbol)


@window.event
def on_key_release(symbol, modifier):
    keys.remove(symbol)

@window.event
def on_draw():
    window.clear()
    batch.draw()
  
"""_________________________________MAIN____________________________________"""

game = Main()
