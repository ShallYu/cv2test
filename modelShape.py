#!/usr/bin/python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *

class Shape(object):
	"""docstring for Shape"""
	def __init__(self):
		super(Shape,self).__init__()
		self.num =0
	def draw(self):
		print("%s,%d" %(self.type,self.num))


class Sphere(Shape):
	type = 'Sphere'
	num = 0
	"""docstring for Sphere"""
	def __init__(self):
		super(Sphere,self).__init__()
		self.num +=1


class Cube(Shape):
	type = 'Cube'
	num = 0
	"""docstring for Cube"""
	def __init__(self):
		super(Cube, self).__init__()
		self.num +=1
		
		
