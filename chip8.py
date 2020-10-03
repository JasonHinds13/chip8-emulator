import random

# CHIP-8 Specifications
class Chip8:
	def __init__(self):
		self.pc = 0x200 # program counter starts at 512
		self.I = 0 # 16 bit address register
		self.v = [0 for i in range(16)] # V0 - VF (16 8 bit registers)

		self.dtimer = 60 # delay timer
		self.stimer = 60 # sound timer

		self.stack = [0 in range(16)] # stack of 16 levels
		self.stackptr = -1 # 8 bit stack pointer

		self.memory = [0 for i in range(4096)] # 4096 bytes

		self.opcode = '' # 16 bit Opcode read

		self.pixels = [0 for i in range(64 * 32)] # pixel states

		self.key = None # key pressed

		self.keys = [0 for i in range(16)] # 16 possible keys for the CHIP8

	def loadgame(self, filename="c8games/PONG"):
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
		return self.v[15] == 1

	def cycle(self):
		""" Fetch, Decode, and Execute"""

		# Fetch opcode
		opcode = self.memory[self.pc] << 8 | self.memory[self.pc +1]

		# Decode by checking opcode
		if (opcode & 0xF000) == 0xA000:
			# execute
			self.I = opcode & 0x0FFF
			self.pc += 2

		elif (opcode & 0xF000) == 0x00E0:
			self.pc += 2
			# learn to clear screen
			print("clear screen")

		elif (opcode & 0xF000) == 0x00EE:
			pc = self.stack[self.stackptr]
			self.stackptr -= 1

		elif (opcode & 0xF000) == 0x1000:
			self.pc = opcode & 0x0FFF;

		elif (opcode & 0xF000) == 0x2000:
			self.stackptr += 1
			self.stack[self.stackptr] = self.pc
			self.pc = opcode & 0x0FFF

		elif (opcode & 0xF000) == 0x3000:
			if self.v[(opcode & 0x0F00) >> 8] == opcode & 0x00FF:
				self.pc += 4
			else:
				self.pc += 2

		elif (opcode & 0xF000) == 0x4000:
			if self.v[(opcode & 0x0F00) >> 8] != opcode & 0x00FF:
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
			self.pc += 2

		elif (opcode & 0xF000) == 0x7000:
			self.v[(opcode & 0x0F00) >> 8] += opcode & 0x00FF
			self.pc += 2

		elif (opcode & 0xF00F) == 0x8000:
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x00F0) >> 4]
			self.pc += 2

		elif (opcode & 0xF00F) == 0x8001:
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] | self.v[(opcode & 0x00F0) >> 4]
			self.pc += 2

		elif (opcode & 0xF00F) == 0x8002:
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] & self.v[(opcode & 0x00F0) >> 4]
			self.pc += 2

		elif (opcode & 0xF00F) == 0x8003:
			self.v[(opcode & 0x0F00) >> 8] = self.v[(opcode & 0x0F00) >> 8] ^ self.v[(opcode & 0x00F0) >> 4]
			self.pc += 2

		elif (opcode & 0xF00F) == 0x8004:
			if(self.v[(opcode & 0x0F00) >> 8] > (0xFF - self.v[(opcode & 0x00F0) >> 4])):
				self.v[15] = 1
			else:
				self.v[15] = 0

			self.v[(opcode & 0x0F00) >> 8] += self.v[(opcode & 0x00F0) >> 4]
			self.pc += 2

		# FIX THESE

		elif (opcode & 0xF00F) == 0x8005:
			self.pc += 2
		elif (opcode & 0xF00F) == 0x8006:
			self.pc += 2
		elif (opcode & 0xF00F) == 0x8007:
			self.pc += 2
		elif (opcode & 0xF00F) == 0x800E:
			self.pc += 2

		elif (opcode & 0xF000) == 0x9000:
			if self.v[(opcode & 0x0F00) >> 8] != self.v[(opcode & 0x00F0) >> 4]:
				self.pc += 4
			else:
				self.pc += 2

		elif (opcode & 0xF000) == 0xB000:
			self.pc = opcode & 0x0FFF

		elif (opcode & 0xF000) == 0xC000:
			self.v[(opcode & 0x0F00) >> 8] = random.randint(0, 256) & (opcode & 0x00FF)
			self.pc += 2

		elif (opcode & 0xF000) == 0xD000:
			# learn to draw later
			self.pc += 2
			print("draw")

		elif (opcode & 0xF0FF) == 0xE09E:
			# if(key()==Vx)
			self.pc += 2
			print("Skips the next instruction if the key stored in VX is pressed")

		elif (opcode & 0xF0FF) == 0xE0A1:
			# if(key()!=Vx)
			self.pc += 2
			print("Skips the next instruction if the key stored in VX isn't pressed")

		elif (opcode & 0xF0FF) == 0xF007:
			self.v[(opcode & 0x0F00) >> 8] = self.dtimer
			self.pc += 2

		elif (opcode & 0xF0FF) == 0xF00A:
			# Vx = get_key()
			self.pc += 2
			print("A key press is awaited, and then stored in VX.")

		elif (opcode & 0xF0FF) == 0xF015:
			self.dtimer = self.v[(opcode & 0x0F00) >> 8]
			self.pc += 2

		elif (opcode & 0xF0FF) == 0xF018:
			self.stimer = self.v[(opcode & 0x0F00) >> 8]
			self.pc += 2

		elif (opcode & 0xF0FF) == 0xF01E:
			self.I += self.v[(opcode & 0x0F00) >> 8]
			self.pc += 2

		elif (opcode & 0xF0FF) == 0xF029:
			# I=sprite_addr[Vx]
			# self.I = sprite_addr[self.v[(opcode & 0x0F00) >> 8]]
			self.pc += 2
			print("Sets I to the location of the sprite for the character in VX")

		elif (opcode & 0xF0FF) == 0xF033:
			# self.v[(opcode & 0x0F00) >> 8]
			self.pc += 2

		elif (opcode & 0xF0FF) == 0xF055:
			# self.v[(opcode & 0x0F00) >> 8]
			self.pc += 2

		elif (opcode & 0xF0FF) == 0xF065:
			# self.v[(opcode & 0x0F00) >> 8]
			self.pc += 2

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

