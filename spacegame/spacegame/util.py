import pyglet, math


def distance(stth, ndth):
	distance = math.sqrt((stth[0] - ndth[0]) ** 2 + (stth[1] - ndth[1]) ** 2)
	return distance
	

def centerimg(image):
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
