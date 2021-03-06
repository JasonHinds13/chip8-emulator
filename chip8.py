import random

# CHIP-8 Specifications
class Chip8:
	def __init__(self):
		self.pc = 0x200 # program counter starts at 512
		self.I = 0 # 16 bit address register
		self.v = [0 for i in range(16)] # V0 - VF (16 8 bit registers)

		self.dtimer = 0 # delay timer
		self.stimer = 0 # sound timer

		self.stack = [0 for i in range(16)] # stack of 16 levels
		self.stackptr = -1 # 8 bit stack pointer

		self.memory = [0 for i in range(4096)] # 4096 bytes

		self.drawFlag = True # Indicate if draw instruction is called

		self.pixels = [0 for i in range(64 * 32)] # pixel states

		self.key = [0 for i in range(16)] # 16 possible keys for the CHIP8

		self.font = [
			0xF0, 0x90, 0x90, 0x90, 0xF0,
			0x20, 0x60, 0x20, 0x20, 0x70,
			0xF0, 0x10, 0xF0, 0x80, 0xF0,
			0xF0, 0x10, 0xF0, 0x10, 0xF0,
			0x90, 0x90, 0xF0, 0x10, 0x10,
			0xF0, 0x80, 0xF0, 0x10, 0xF0,
			0xF0, 0x80, 0xF0, 0x90, 0xF0,
			0xF0, 0x10, 0x20, 0x40, 0x40,
			0xF0, 0x90, 0xF0, 0x90, 0xF0,
			0xF0, 0x90, 0xF0, 0x10, 0xF0,
			0xF0, 0x90, 0xF0, 0x90, 0x90,
			0xE0, 0x90, 0xE0, 0x90, 0xE0,
			0xF0, 0x80, 0x80, 0x80, 0xF0,
			0xE0, 0x90, 0x90, 0x90, 0xE0,
			0xF0, 0x80, 0xF0, 0x80, 0xF0,
			0xF0, 0x80, 0xF0, 0x80, 0x80
		]

		# load fontset into memory
		for i in range(80):
			self.memory[i] = self.font[i]

	def loadgame(self, filename):
		""" Load contents of game file into memory"""
		with open(filename, "rb") as f:
			byte = f.read(1)
			count = 0
			while byte != b"":
				# convert bytes to integers (big-endian)
				byte_int = int.from_bytes(byte, 'big')
				self.memory[count + 0x200] = byte_int
				byte = f.read(1)
				count += 1

	def drawFlagSet(self):
		""" Check if the draw flag, VF, is set"""
		return self.drawFlag

	def setDrawFlag(self, state):
		self.drawFlag = state

	def setKey(self, index, val):
		self.key[index] = val

	def cycle(self):
		""" Fetch, Decode, and Execute"""

		# Fetch opcode
		opcode = self.memory[self.pc] << 8 | self.memory[self.pc +1]

		# Decode by checking opcode and execute
		if (opcode & 0xF000) == 0x0000:

			if (opcode & 0xF0FF) == 0x00E0:
				self.pixels = [0 for i in range(64 * 32)]
				self.pc += 2

			elif (opcode & 0xF0FF) == 0x00EE:
				self.pc = self.stack[self.stackptr]
				self.stackptr -= 1
				self.pc += 2
			else:
				print("Unknown opcode {:x}".format(opcode))

		elif (opcode & 0xF000) == 0x1000:
			self.pc = opcode & 0x0FFF;

		elif (opcode & 0xF000) == 0x2000:
			self.stackptr += 1
			self.stack[self.stackptr] = self.pc
			self.pc = opcode & 0x0FFF

		elif (opcode & 0xF000) == 0x3000:
			if self.v[(opcode & 0x0F00) >> 8] == (opcode & 0x00FF):
				self.pc += 4
			else:
				self.pc += 2

		elif (opcode & 0xF000) == 0x4000:
			if self.v[(opcode & 0x0F00) >> 8] != (opcode & 0x00FF):
				self.pc += 4
			else:
				self.pc += 2

		elif (opcode & 0xF000) == 0x5000:
			if self.v[(opcode & 0x0F00) >> 8] == self.v[(opcode & 0x00F0) >> 4]:
				self.pc += 4
			else:
				self.pc += 2

		elif (opcode & 0xF000) == 0x6000:
			self.v[(opcode & 0x0F00) >> 8] = opcode & 0x00FF
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
			self.pc += 2

		elif (opcode & 0xF000) == 0x7000:
			self.v[(opcode & 0x0F00) >> 8] += opcode & 0x00FF
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
			self.pc += 2

		# 0x8
		elif (opcode & 0xF000) == 0x8000:

			if (opcode & 0x000F) == 0x0000:
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x00F0) >> 4]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0001:
				self.v[(opcode & 0x0F00) >> 8] |= self.v[(opcode & 0x00F0) >> 4]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0002:
				self.v[(opcode & 0x0F00) >> 8] &= self.v[(opcode & 0x00F0) >> 4]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0003:
				self.v[(opcode & 0x0F00) >> 8] ^= self.v[(opcode & 0x00F0) >> 4]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0004:
				if self.v[(opcode & 0x00F0) >> 4] > (0xFF - self.v[(opcode & 0x0F00) >> 8]):
					self.v[15] = 1
				else:
					self.v[15] = 0

				self.v[(opcode & 0x0F00) >> 8] += self.v[(opcode & 0x00F0) >> 4]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0005:
				if self.v[(opcode & 0x00F0) >> 4] > self.v[(opcode & 0x0F00) >> 8]:
					self.v[15] = 0
				else:
					self.v[15] = 1
				self.v[(opcode & 0x0F00) >> 8] -= self.v[(opcode & 0x00F0) >> 4]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0006:
				self.v[15] = self.v[(opcode & 0x0F00) >> 8] & 0x1
				self.v[(opcode & 0x0F00) >> 8] >>= 1
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x0007:
				if self.v[(opcode & 0x0F00) >> 8] > self.v[(opcode & 0x00F0) >> 4]:
					self.v[15] = 0
				else:
					self.v[15] = 1
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x00F0) >> 4] - self.v[(opcode & 0x0F00) >> 8]
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x000F) == 0x000E:
				self.v[15] = self.v[(opcode & 0x0F00) >> 8] >> 0x7
				self.v[(opcode & 0x0F00) >> 8] <<= 1
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			else:
				print("Unknown opcode {:x}".format(opcode))

		elif (opcode & 0xF000) == 0x9000:
			if self.v[(opcode & 0x0F00) >> 8] != self.v[(opcode & 0x00F0) >> 4]:
				self.pc += 4
			else:
				self.pc += 2

		elif (opcode & 0xF000) == 0xA000:
			self.I = opcode & 0x0FFF
			self.pc += 2

		elif (opcode & 0xF000) == 0xB000:
			self.pc = (opcode & 0x0FFF) + self.v[0]

		elif (opcode & 0xF000) == 0xC000:
			self.v[(opcode & 0x0F00) >> 8] = random.randint(0, 255) & (opcode & 0x00FF)
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
			self.pc += 2

		elif (opcode & 0xF000) == 0xD000:
			vx = self.v[(opcode & 0x0F00) >> 8]
			vy = self.v[(opcode & 0x00F0) >> 4]
			height = opcode & 0x000F

			self.v[15] = 0

			for y in range(height):
				pix = self.memory[self.I + y]
				for x in range(8):
					if (pix & (0x80 >> x)) != 0:
						if self.pixels[(vx + x + ((vy + y) * 64))] == 1:
							self.v[15] = 1
						self.pixels[vx + x + ((vy + y) * 64)] ^= 1

			self.drawFlag = True
			self.pc += 2

		# 0xE
		elif (opcode & 0xF000) == 0xE000:

			if (opcode & 0x00FF) == 0x009E:
				vx = self.v[(opcode & 0x0F00) >> 8]
				if self.key[vx] != 0:
					self.pc += 4
				else:
					self.pc += 2

			elif (opcode & 0x00FF) == 0x00A1:
				vx = self.v[(opcode & 0x0F00) >> 8]
				if self.key[vx] == 0:
					self.pc += 4
				else:
					self.pc += 2

		# 0xF
		elif (opcode & 0xF000) == 0xF000:

			if (opcode & 0x00FF) == 0x0007:
				self.v[(opcode & 0x0F00) >> 8] = self.dtimer
				self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2

			elif (opcode & 0x00FF) == 0x000A:
				x = (opcode & 0x0F00) >> 8
				key_press = False
				for i in range(16):
					if self.key[i] != 0:
						self.v[x] = i
						self.pc += 2
						key_press = True
				if key_press == False:
					self.pc -= 2

			elif (opcode & 0x00FF) == 0x0015:
				self.dtimer = self.v[(opcode & 0x0F00) >> 8]
				self.pc += 2

			elif (opcode & 0x00FF) == 0x0018:
				self.stimer = self.v[(opcode & 0x0F00) >> 8]
				self.pc += 2

			elif (opcode & 0x00FF) == 0x001E:
				self.I += self.v[(opcode & 0x0F00) >> 8]
				self.pc += 2

			elif (opcode & 0x00FF) == 0x0029:
				vx = self.v[(opcode & 0x0F00) >> 8]
				# I = FONT_BASE + (Vx * 5) FONT_BASE is 0 in this case and each char is 5 bytes
				self.I = vx * 0x5
				self.pc += 2

			elif (opcode & 0x00FF) == 0x0033:
				vx = self.v[(opcode & 0x0F00) >> 8]
				index = 2
				while vx > 0:
					self.memory[self.I + index] = vx % 10
					vx = vx // 10
				self.pc += 2

			elif (opcode & 0x00FF) == 0x0055:
				x = (opcode & 0x0F00) >> 8
				for i in range(x+1):
					self.memory[self.I + i] = self.v[i]
				self.pc += 2

			elif (opcode & 0x00FF) == 0x0065:
				x = (opcode & 0x0F00) >> 8
				for i in range(x+1):
					self.v[i] = self.memory[self.I + i]
					self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] % 256
				self.pc += 2
			else:
				print("Unknown opcode {:x}".format(opcode))

		else:
			print("INVALID OPCODE {}".format(opcode))
			self.pc += 2

		# update timers
		if self.dtimer > 0:
			self.dtimer -= 1

		if self.stimer > 0:
			if self.stimer == 1:
				print("BEEP")
			self.stimer -= 1

