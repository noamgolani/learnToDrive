import sys, pygame

pygame.init()

size = width, height = 320, 240
speed = [2,2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("static/car.png")
ballrect = ball.get_rect()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	ballrect = ballrect.move(speed)
	
	screen.fill(black)
	screen.blit(ball, ballrect)
	pygame.display.flip()

