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
	
	m = pygame.image.load("static/map4.png")
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
	global scores, cars, bestS, anim
	tempc = []
	tempa = []
	for i in scores.argsort()[::-1]:
		tempc.append(cars[i])
		if len(tempa)<= PERENTS_SIZE:
			tempa.append(anim[i])
	anim = tempa
	cars = []
	for i in range(PERENTS_SIZE):
		for j in range(PERENTS_SIZE):
			if not j == i:
				cars.append(Car(80,20,Net.CHILD(tempc[i].getNet(), tempc[j].getNet(), 1)))	
				cars.append(Car(80,20,Net.CHILD(tempc[i].getNet(), tempc[j].getNet(), 1)))	
	bestS.append(max(scores))
	print "new generation! | max: " + str(int(max(scores))) + " - avg: " + str(int(np.average(scores)))
	scores = np.zeros(len(cars))

def check_events():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()		 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if not space:
					m = pygame.image.load("static/map2.png")
					m = m.convert()
					space = True
					continue
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				space = False	

def main():	
	global m, cars, screen, text, scores, anim
	
	init()	

	anim = [[] for x in range(len(cars))]
	space = False
	tickCount = 0
	g = 1
	
	while 1:

		while tickCount < 1000:
			check_events()
			for carIndex in range(CARS):
				x,y = cars[carIndex].getXY()
				if x < 0 or x > WIDTH or y < 0 or y > HEIGHT or m.get_at((x,y)) == (255,200,255,255) or m.get_at((x, y)) == (0,0,0,255):
					anim[carIndex].append([cars[carIndex].getXY(),cars[carIndex].getDiraction()])
					continue				
				if m.get_at((x,y)) == (255, 255, 200, 255):
					if scores[carIndex] == 0:
						scores[carIndex] = 1000 - tickCount
					anim[carIndex].append([cars[carIndex].getXY(),cars[carIndex].getDiraction()])
					continue
				cars[carIndex].updateView(m)
				cars[carIndex].update()
				anim[carIndex].append([cars[carIndex].getXY(),cars[carIndex].getDiraction()])
			tickCount += 1

		tickCount = 0
		new_generation()
	 	g += 1
		c = Car()	
		for i in range(1000):
			check_events()
			screen.blit(m, (0,0))
			for ci in range(PERENTS_SIZE):
				c.DRAW(anim[ci][i][0],anim[ci][i][1], screen)
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
		anim = [[] for x in range(len(cars))]

main()
