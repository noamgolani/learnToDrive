import sys, pygame
import numpy as np
from lib import Car

def main():
	pygame.init()

	pygame.key.set_repeat(100,10)		
	
	size = width, height = 960, 640
	white = 255, 255, 255

	screen = pygame.display.set_mode(size)
	m = pygame.image.load("static/map2.png")
	m = m.convert()

	cars = []
	for c in range(100):
		cars.append(Car(80,20))

	text = ["","","","","",""]

	carIndex = 0
	space = False

	clock = pygame.time.Clock()
	while 1:
		clock.tick(60)	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()		 
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if not space:
						space = True
						carIndex += 1
						continue
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					space = False
		cars[carIndex].update()
		cars[carIndex].updateView(m)
	
		x,y = cars[carIndex].getXY()

		if x < 0 or x > width or y < 0 or y > height or m.get_at((x,y)) == (255,200,255,255):
			carIndex += 1
			continue

		text[1] = "X: " + str(x)
		text[2] = "Y: " + str(y)
		text[0] = "Car number: " + str(carIndex)

		screen.blit(m, (0,0))
		cars[carIndex].draw(screen)
		
		pygame.font.init()
		f = pygame.font.SysFont("Comic Sans MS", 30)
		temp = 10
		for t in text:
			screen.blit(f.render(t, False, (128,128, 128)),(width - 150,temp))
			temp += 20

		pygame.display.flip()

main()
