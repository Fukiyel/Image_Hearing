from PIL import Image
from pyaudio import PyAudio
import numpy as np


def hilbert_path(level):
	global current_level
	current_level = 1
	hilbert_curve = {0: [0, 0], 1: [0, 1], 2: [1, 1], 3: [1, 0]}

	def level_up(curve):
		global current_level

		def rotate_left(block):
			extremity = 2 ** (current_level) - 1
			for i in block:
				a = block[i][0]
				b = block[i][1]
				block[i] = [b, extremity - a]
			return block
		def rotate_right(block):
			extremity = 2 ** (current_level) - 1
			for i in block:
				a = block[i][0]
				b = block[i][1]
				block[i] = [extremity - b, a]
			return block
		def reverse(block):
			new_block = {}
			for i in block:
				new_block[i] = block[len(block) - 1 - i]
			return new_block
		def move(block, pos): # Move AFTER rotating !
			global current_level
			new_block = {}
			if pos == 1:
				for i in block.keys():
					new_block[i + len(block)] = [block[i][0], block[i][1] + current_level + 1]
			if pos == 2:
				for i in block.keys():
					new_block[i + len(block) * 2] = [block[i][0] + current_level + 1, block[i][1] + current_level + 1]
			if pos == 3:
				for i in block.keys():
					new_block[i + len(block) * 3] = [block[i][0] + current_level + 1, block[i][1]]

			return new_block

		curve_0 = reverse(rotate_left(curve.copy()))
		curve_1 = move(curve.copy(), pos=1)
		curve_2 = move(curve.copy(), pos=2)
		curve_3 = move(reverse(rotate_right(curve.copy())), pos=3)

		current_level += 1

		new_curve = {**curve_0, **curve_1, **curve_2, **curve_3}
		return new_curve

	for i in range(1, hilbert_level):
		hilbert_curve = level_up(hilbert_curve)

	return hilbert_curve

hilbert_level = 10
path = hilbert_path(hilbert_level)


im = Image.open("level-10.jpg")
im = im.convert("HSV")

hue, sat, val = [], [], []

original_y = []
for i in range(len(path)): original_y.append(path[i][1])
opposite_y = list(map(lambda x: max(original_y) - x, original_y))

for i in path:
	coords = (path[i][0], opposite_y[i])
	hue.append(im.getpixel(coords)[0])
	sat.append(im.getpixel(coords)[1])
	val.append(im.getpixel(coords)[2])


pa = PyAudio()
print("a")
