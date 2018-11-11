import sys, pygame
import numpy as np
from lib import Car

def main():
	pygame.init()

	size = width, height = 960, 640
	white = 255, 255, 255

	screen = pygame.display.set_mode(size)
	m = pygame.image.load("static/map1.png")
	m = m.convert()

	car1 = Car(200,200)
	car1.setDiraction(0.2)

	text = ["","","","","",""]

	clock = pygame.time.Clock()
	while 1:
		clock.tick(60)	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		 
		car1.update()
		car1.updateView(m)
	
		x,y = car1.getXY()
		text[0] = "X: " + str(x)
		text[1] = "Y: " + str(y)
		text[2] = "right view: " + str(car1.getView()[0])
		text[3] = "center view: " + str(car1.getView()[1])
		text[4] = "left view: " + str(car1.getView()[2])
			

		screen.blit(m, (0,0))
		car1.draw(screen)
		
		pygame.font.init()
		f = pygame.font.SysFont("Comic Sans MS", 20)
		temp = 10
		for t in text:
			screen.blit(f.render(t, False, (128,128, 128)),(width - 150,temp))
			temp += 20

		pygame.display.flip()

main()
