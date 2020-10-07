import pygame
from pygame.locals import *

from chip8 import Chip8

pygame.init()

SCALE = 10
WIDTH = 64 * SCALE
HEIGHT = 32 * SCALE

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

chip8 = Chip8()
chip8.loadgame()

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == K_x:
				chip8.setKey(0,1)
			if event.key == K_1:
				chip8.setKey(1,1)
			if event.key == K_2:
				chip8.setKey(2,1)
			if event.key == K_3:
				chip8.setKey(3,1)
			if event.key == K_4:
				chip8.setKey(12,1)
			if event.key == K_q:
				chip8.setKey(4,1)
			if event.key == K_w:
				chip8.setKey(5,1)
			if event.key == K_e:
				chip8.setKey(6,1)
			if event.key == K_r:
				chip8.setKey(13,1)
			if event.key == K_a:
				chip8.setKey(7,1)
			if event.key == K_s:
				chip8.setKey(8,1)
			if event.key == K_d:
				chip8.setKey(9,1)
			if event.key == K_f:
				chip8.setKey(14,1)
			if event.key == K_z:
				chip8.setKey(10,1)
			if event.key == K_c:
				chip8.setKey(11,1)
			if event.key == K_v:
				chip8.setKey(15,1)

		if event.type == pygame.KEYUP:
			if event.key == K_x:
				chip8.setKey(0,0)
			if event.key == K_1:
				chip8.setKey(1,0)
			if event.key == K_2:
				chip8.setKey(2,0)
			if event.key == K_3:
				chip8.setKey(3,0)
			if event.key == K_4:
				chip8.setKey(12,0)
			if event.key == K_q:
				chip8.setKey(4,0)
			if event.key == K_w:
				chip8.setKey(5,0)
			if event.key == K_e:
				chip8.setKey(6,0)
			if event.key == K_r:
				chip8.setKey(13,0)
			if event.key == K_a:
				chip8.setKey(7,0)
			if event.key == K_s:
				chip8.setKey(8,0)
			if event.key == K_d:
				chip8.setKey(9,0)
			if event.key == K_f:
				chip8.setKey(14,0)
			if event.key == K_z:
				chip8.setKey(10,0)
			if event.key == K_c:
				chip8.setKey(11,0)
			if event.key == K_v:
				chip8.setKey(15,0)

	# execute one cycle
	chip8.cycle()

	# if chip8.drawFlagSet(): draw()
	# chip8.setKeys()

	screen.fill((0,0,0))
	pygame.display.flip()

	clock.tick(60)

pygame.quit()