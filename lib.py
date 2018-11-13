import sys, pygame
import numpy as np

class Net(object):
	def __init__(self, w1 = np.zeros((3,5)), w2 = np.zeros((5,5)), w3 = np.zeros((5,2))):
		self.w1 = w1
		self.w2 = w2
		self.w3 = w3
	def randomize(self):
		self.w1 = np.random.rand(3,5) * 2 -1 
		self.w2 = np.random.rand(5,5) * 2 -1
		self.w3 = np.random.rand(5,2) * 2 -1
	def calc(self, a):
		a1 = np.array([a[0],a[1],a[2]])
		b1 = a1.dot(self.w1)
		a2 = np.tanh(b1)
		b2 = a2.dot(self.w2)
		a3 = np.tanh(b2)
		b3 = a3.dot(self.w3)
		R = np.tanh(b3)
		return R
	def setWeights(self, w1,w2,w3):
		self.w1 = w1
		self.w2 = w2
		self.w3 = w3
	def getWeights(self):
		return self.w1,self.w2,self.w3
	def CHILD(n1,n2,o):
		def a(a ,b):
			if np.random.rand() < 0.02:
				return (a + b) / 2 + np.random.rand() - 0.5
			else:
				if o == 1:
					if np.random.rand() < 0.5: 
						return a
					else:
						return b
				elif o == 2:
					return (a + b) / 2
		a1,a2,a3 = n1.getWeights()
		b1,b2,b3 = n2.getWeights()
		F = np.vectorize(a)
		n = Net(F(a1,b1),F(a2,b2),F(a3,b3))
		return n

class Car(object):
	def __init__(self, x=0, y=0, net = Net()):
		self.l = np.array([0.0 + x,0.0 + y])
		self.diraction = 0 
		self.v = np.array([0.0,0.0]) 
		self.view = [1,1,1]
		self.net = net
	def reset(self,x,y):
		self.l = np.array([0.0 + x,0.0 + y])
		self.diraction = 0
		self.v = np.array([0.0,0.0]) 
		self.view = [1,1,1]
	def setDiraction(self, d):
		if d > 1: d = 1
		if d < -1: d = -1
		self.diraction = d * np.pi / 2
	def getDiraction(self):
		return self.diraction
	def update(self):
		A, D = self.net.calc(self.view)
 		self.diraction += D * np.pi / 2
		self.v = np.array([np.sin(self.diraction) * A, np.cos(self.diraction) * A]) * 5
		V = np.sqrt(np.power(self.v[0],2) + np.power(self.v[1],2))
		if V >= 8:
			self.v = (self.v / V) * 8
		self.l += self.v
	def updateView(self, mapp):
		temp1,temp2,temp3 = (self.l[0],self.l[1]), (self.l[0],self.l[1]), (self.l[0],self.l[1])

		angle1, angle2, angle3 = self.diraction-np.pi/4 , self.diraction, self.diraction+np.pi/4
		view = [-1,-1,-1]
		for i in range(0,100):
			if view[0] == -1:
				temp1 = temp1[0] + np.sin(angle1), temp1[1] + np.cos(angle1)
				if temp1[0] < 0 or temp1[0] > mapp.get_width() or temp1[1] < 0 or temp1[1] > mapp.get_height():
					view[0] = i/100.0
				elif mapp.get_at((int(temp1[0]), int(temp1[1]))) == (0,0,0,255):
					view[0] = i/100.0
			if view[1] == -1:
				temp2 = temp2[0] + np.sin(angle2), temp2[1] + np.cos(angle2)
				if temp2[0] < 0 or temp2[0] > mapp.get_width() or temp2[1] < 0 or temp2[1] > mapp.get_height():
					view[0] = i/100.0
				elif mapp.get_at((int(temp2[0]), int(temp2[1]))) == (0,0,0,255):
					view[1] = i/100.0
			if view[2] == -1:
				temp3 = temp3[0] + np.sin(angle3), temp3[1] + np.cos(angle3)
				if temp3[0] < 0 or temp3[0] > mapp.get_width() or temp3[1] < 0 or temp3[1] > mapp.get_height():
					view[0] = i/100.0
				elif mapp.get_at((int(temp3[0]), int(temp3[1]))) == (0,0,0,255):
					view[2] = i/100.0
		for i in range(len(view)):
			if view[i] == -1: view[i] = 1
		self.view = view
	def getView(self):
		return self.view
	def draw(self, screen):
		c = 255, 0, 0, 100
		pygame.draw.circle(screen, c, self.l.astype(int), 5)

		angle = self.diraction
		temp = np.array([np.sin(angle) * 30, np.cos(angle) * 30]) + self.l
		pygame.draw.line(screen, c, self.l.astype(int), temp.astype(int))

		#temp = np.array([np.sin(angle-np.pi/4) * self.view[0] * 100, np.cos(angle-np.pi/4) * self.view[0] * 100]) + self.l
		#pygame.draw.circle(screen, (128,128,255), temp.astype(int),5)
	#	temp = np.array([np.sin(angle) * self.view[1] * 100, np.cos(angle) * self.view[1] * 100]) + self.l
	#	pygame.draw.circle(screen, (128,128,255), temp.astype(int),5)
	#	temp = np.array([np.sin(angle+np.pi/4) * self.view[2] * 100, np.cos(angle+np.pi/4) * self.view[2] * 100]) + self.l
	#	pygame.draw.circle(screen, (128,128,255), temp.astype(int),5)
	def DRAW(self, L, d, screen):
		l = np.array([L[0], L[1]])
		c = 255, 0, 0, 100
		pygame.draw.circle(screen, c, l.astype(int), 5)

		angle = d
		temp = np.array([np.sin(angle) * 30, np.cos(angle) * 30]) + l
		pygame.draw.line(screen, c, l.astype(int), temp.astype(int))
	def getXY(self):
		return int(self.l[0]),int(self.l[1])
	def setXY(self, x, y):
		  self.l = np.array([0.0 + x,0.0 + y])
	def getVelocity(self):
		return self.v
	def getNet(self):
		return self.net
