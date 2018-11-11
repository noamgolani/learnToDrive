import sys, pygame
import numpy as np

class Car(object):
	def __init__(self, x, y):
		self.l = np.array([0.0 + x,0.0 + y])
		self.diraction = 0 
		self.a = 0.01
		self.v = np.array([0.0,0.0]) 
		self.view = [1,1,1]
	def setDiraction(self, d):
		if d > 1: d = 1
		if d < -1: d = -1
		self.diraction = d
	def getDiraction(self):
		return self.diraction
	def setAcceleration(self, a):
		self.a = a
	def update(self):
		self.v += self.getAV()
		self.l += self.v 
	def updateView(self, mapp):
		temp1,temp2,temp3 = (self.l[0],self.l[1]), (self.l[0],self.l[1]), (self.l[0],self.l[1])

		angle1, angle2, angle3 = self.diraction-np.pi/4 , self.diraction, self.diraction+np.pi/4
		view = [-1,-1,-1]
		for i in range(0,100):
			if view[0] == -1:
				temp1 = temp1[0] + np.sin(angle1), temp1[1] + np.cos(angle1)
				if mapp.get_at((int(temp1[0]), int(temp1[1]))) == (0,0,0,255):
					view[0] = i/100.0
			if view[1] == -1:
				temp2 = temp2[0] + np.sin(angle2), temp2[1] + np.cos(angle2)
				if mapp.get_at((int(temp2[0]), int(temp2[1]))) == (0,0,0,255):
					view[1] = i/100.0
			if view[2] == -1:
				temp3 = temp3[0] + np.sin(angle3), temp3[1] + np.cos(angle3)
				if mapp.get_at((int(temp3[0]), int(temp3[1]))) == (0,0,0,255):
					view[2] = i/100.0
		for i in range(len(view)):
			if view[i] == -1: view[i] = 1
		self.view = view
	def getView(self):
		return self.view
	def draw(self, screen):
		c = 255, 0, 0
		pygame.draw.circle(screen, c, self.l.astype(int), 15)

		angle = self.diraction * np.pi / 2
		temp = np.array([np.sin(angle) * 30, np.cos(angle) * 30]) + self.l
		pygame.draw.line(screen, c, self.l.astype(int), temp.astype(int))

		temp = np.array([np.sin(angle-np.pi/4) * self.view[0] * 100, np.cos(angle-np.pi/4) * self.view[0] * 100]) + self.l
		pygame.draw.circle(screen, (128,128,255), temp.astype(int),5)
		temp = np.array([np.sin(angle) * self.view[1] * 100, np.cos(angle) * self.view[1] * 100]) + self.l
		pygame.draw.circle(screen, (128,128,255), temp.astype(int),5)
		temp = np.array([np.sin(angle+np.pi/4) * self.view[2] * 100, np.cos(angle+np.pi/4) * self.view[2] * 100]) + self.l
		pygame.draw.circle(screen, (128,128,255), temp.astype(int),5)
	def getAV(self):
		angle = self.diraction * np.pi / 2
		return np.array([np.sin(angle) * self.a, np.cos(angle) * self.a])
	def getXY(self):
		return int(self.l[0]),int(self.l[1])
