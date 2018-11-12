import sys, pygame
import numpy as np
import matplotlib.pyplot as plt
from lib import Car
from lib import Net
import time

SIZE = WIDTH, HEIGHT = 960, 640

global m, cars, screen

def init():
	global m, cars, screen

	pygame.init()
	
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Car learning")
	
	m = pygame.image.load("static/map2.png")
	m = m.convert()

def main():	
	global m, cars, screen
	
	init()	

	cars = []
	for i in range(24):
		n = Net()
		n.randomize()
		c = Car(80,20,n)
		cars.append(c)
	scores = np.zeros(24)

	text = ["","","","","",""]

	carIndex = 0
	space = False
	tickCount = 0
	g = 1
	bestS = [0]
	
	clock = pygame.time.Clock()
	while 1:
		#clock.tick(60)
	
		if tickCount >= 180:
			tickCount = 0
			carIndex += 1		

		if carIndex >= len(cars):
			print "Done"
			bestS.append(max(scores))
			#plt.plot(bestS)
			#plt.show()
			tempc = []
			for i in scores.argsort()[::-1]:
				tempc.append(cars[i])
			cars = []
			for i in range(4):
				for j in range(4):
					if not j == i:
						cars.append(Car(80,20,Net.CHILD(tempc[i].getNet(), tempc[j].getNet())))	
						cars.append(Car(80,20,Net.CHILD(tempc[i].getNet(), tempc[j].getNet())))	
			print len(cars)
			carIndex = 0	
			tickCount = 0
			scores = np.zeros(len(cars))
			g+= 1
			continue

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()		 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if not space:
						space = True
						carIndex += 1
						tickCount = 0
						continue
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					space = False

		cars[carIndex].update()
		cars[carIndex].updateView(m)
		v = cars[carIndex].getVelocity()
		scores[carIndex] += np.sqrt(pow(v[0],2) + pow(v[1], 2))

		x,y = cars[carIndex].getXY()

		if x < 0 or x > WIDTH or y < 0 or y > HEIGHT or m.get_at((x,y)) == (255,200,255,255) or m.get_at((x, y)) == (0,0,0,255):
			carIndex += 1
			tickCount = 0
			continue

		tickCount += 1

		text[0] = "Car number: " + str(carIndex)
		text[1] = "Score: " + str(scores[carIndex])
		text[2] = "Generation: " + str(g)
		text[3] = "G-"+str(g-1)+" Best: " + str(bestS[g-1])
		
		if 0 == 0:
			screen.blit(m, (0,0))
			cars[carIndex].draw(screen)
		
			pygame.font.init()
			f = pygame.font.SysFont("Comic Sans MS", 30)
			temp = 10
			for t in text:
				screen.blit(f.render(t, False, (128,128, 128)),(WIDTH - 150,temp))
				temp += 20

			pygame.display.flip()

main()
