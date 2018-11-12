import sys, pygame
import numpy as np
from lib import Car
from lib import Net

SIZE = WIDTH, HEIGHT = 960, 640
CARS = 40
PERENTS_SIZE = 5

def init():
	global m, cars, screen, text, scores, bestS

	pygame.init()
	
	screen = pygame.display.set_mode(SIZE)
	pygame.display.set_caption("Car learning")
	
	m = pygame.image.load("static/map2.png")
	m = m.convert()

	cars = []
	for i in range(CARS):
		n = Net()
		n.randomize()
		c = Car(80,20,n)
		cars.append(c)

	scores = np.zeros(CARS)
	bestS = [0]
	
	text = ["","","","","",""]

def new_generation():
	global scores, cars, bestS
	tempc = []
	for i in scores.argsort()[::-1]:
		tempc.append(cars[i])
	cars = []
	for i in range(PERENTS_SIZE):
		for j in range(PERENTS_SIZE):
			if not j == i:
				cars.append(Car(80,20,Net.CHILD(tempc[i].getNet(), tempc[j].getNet())))	
				cars.append(Car(80,20,Net.CHILD(tempc[i].getNet(), tempc[j].getNet())))	
	bestS.append(max(scores))
	print "new generation! | max: " + str(int(max(scores))) + " - avg: " + str(int(np.average(scores)))
	scores = np.zeros(len(cars))

def main():	
	global m, cars, screen, text, scores
	
	init()	

	space = False
	tickCount = 0
	g = 1
	
	while 1:
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

		if tickCount >= 400:
			tickCount = 0
			new_generation()
	 		g += 1
	 		continue

		screen.blit(m, (0,0))

		for carIndex in range(CARS):
			x,y = cars[carIndex].getXY()
			if x < 0 or x > WIDTH or y < 0 or y > HEIGHT or m.get_at((x,y)) == (255,200,255,255) or m.get_at((x, y)) == (0,0,0,255):
				continue				
			cars[carIndex].update()
			cars[carIndex].updateView(m)
			v = cars[carIndex].getVelocity()
			scores[carIndex] += np.sqrt(pow(v[0],2) + pow(v[1], 2))	

			cars[carIndex].draw(screen)

		tickCount += 1

		text[0] = "Tick: " + str(tickCount)
		text[2] = "Generation: " + str(g)
		text[3] = "G-"+str(g-1)+" Best: " + str(bestS[g-1])
		
		pygame.font.init()
		f = pygame.font.SysFont("Comic Sans MS", 30)
		temp = 10
		for t in text:
			screen.blit(f.render(t, False, (128,128, 128)),(WIDTH - 150,temp))
			temp += 20

		pygame.display.flip()

main()
