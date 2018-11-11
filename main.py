import sys, pygame
import numpy as np

class Car(object):
	def __init__(self, x, y):
		self.l = np.array([0.0 + x,0.0 + y])
		self.diraction = 0 
		self.a = 0.15
		self.v = np.array([0.0,0.0]) 
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
	def draw(self, screen):
		c = 255, 0, 0
		pygame.draw.circle(screen, c, self.l.astype(int), 15)
	def getAV(self):
		angle = self.diraction * np.pi / 2
		return np.array([np.sin(angle) * self.a, np.cos(angle) * self.a])

pygame.init()

size = width, height = 640, 480
white = 255, 255, 255

screen = pygame.display.set_mode(size)

car1 = Car(200,200)

clock = pygame.time.Clock()

while 1:
	clock.tick(60)	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	car1.setDiraction(car1.getDiraction() + 0.1)	
	car1.update()

	screen.fill(white)
	
	car1.draw(screen)
	
	pygame.display.flip()

