import pygame
from chip8 import Chip8

pygame.init()

WIDTH = 64
HEIGHT = 32

screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

chip8 = Chip8()
chip8.loadgame()

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# execute one cycle
	chip8.cycle()

	# if chip8.drawFlagSet(): draw()
	# chip8.setKeys()

	screen.fill((0,0,0))
	pygame.display.flip()

pygame.quit()