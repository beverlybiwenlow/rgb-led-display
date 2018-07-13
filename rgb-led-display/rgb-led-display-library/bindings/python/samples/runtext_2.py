# -*- coding: utf-8 -*-
#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import fileinput


class RunText(SampleBase):

	def __init__(self, *args, **kwargs):
		super(RunText, self).__init__(*args, **kwargs)


	def run(self):
		font_size_key = "7x13"
		font_size_val = "9x15B"
		font_size_small = "6x10"

		offscreen_canvas = self.matrix.CreateFrameCanvas()

		font_key = graphics.Font()
		font_key.LoadFont("../../../fonts/{}.bdf".format(font_size_key))
		font_val = graphics.Font()
		font_small = graphics.Font()
		font_small.LoadFont("../../../fonts/{}.bdf".format(font_size_small))

		color_key = graphics.Color(255, 255, 255)
		color_val = graphics.Color(110, 255, 255)
		x_pos_key = 2
		x_pos_val = offscreen_canvas.width # Temporary value. Will changed based on length of values

		# y_pos of each item in the list (only 2nd & 3rd row since 1st is for header)
		y_pos_list = [13, 28]

		while True:
			with open("data-files/data_keys.txt", 'r') as f:
				list_keys = f.readlines()

			with open("data-files/data_values.txt", 'r') as f:
				list_values = f.readlines()

			font_val.LoadFont("../../../fonts/{}.bdf".format(font_size_val))

			for i in range(len(list_keys)):
				list_keys[i] = list_keys[i].replace("\n", "")
			for i in range(len(list_values)):
				list_values[i] = list_values[i].replace("\n", "")

			offscreen_canvas.Clear()

			# Light up keys
			length_key_1 = self.light_keys(offscreen_canvas, list_keys[2], font_key, font_small, x_pos_key, y_pos_list[0], color_key, 1)
			length_key_2 = self.light_keys(offscreen_canvas, list_keys[3], font_key, font_small, x_pos_key, y_pos_list[1], color_key, 2)

			# Light up borders
			self.light_borders(offscreen_canvas)

			# Light up values
			self.light_values(offscreen_canvas, font_val, font_small, color_val, list_values[2], x_pos_key, length_key_1, y_pos_list[0], 1)
			self.light_values(offscreen_canvas, font_val, font_small, color_val, list_values[3], x_pos_key, length_key_2, y_pos_list[1], 2)

			offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
			time.sleep(0.05)



	def light_values(self, offscreen_canvas, font_val, font_small, color_val, values_text, x_pos_key, length_key, y_pos_val, row):

		# Get length of values
		length_val = graphics.DrawText(offscreen_canvas, font_val, offscreen_canvas.width, 0, color_val, values_text)

		# Check if number becomes too big (crosses boundary)
		val_boundary = x_pos_key + length_key
		if length_val + val_boundary >= offscreen_canvas.width:

			# Decrease the font size until it does not cross boundary
			fonts = ['8x13B','7x13B', '6x13', '6x12', '6x10', '6x9']
			for font in fonts:
				font_val.LoadFont("../../../fonts/{}.bdf".format(font))
				length_val = graphics.DrawText(offscreen_canvas, font_val, offscreen_canvas.width, 0, color_val, values_text)

				if length_val + val_boundary < offscreen_canvas.width:
					x_pos_val = offscreen_canvas.width - 1 - length_val
					length_val = graphics.DrawText(offscreen_canvas, font_val, x_pos_val, y_pos_val, color_val, values_text)
					break

				else:
					# if smallest font is still too big, split number into 2 rows
					if font == fonts[-1]:
						num = int(len(values_text) / 2)
						values_array = []
						values_array.append(values_text[:num])
						values_array.append(values_text.replace(values_array[0], ''))
						height1 = (row * 16) - 8
						height2 = (row * 16) - 1
						length_val1 = graphics.DrawText(offscreen_canvas, font_small, offscreen_canvas.width, 0, color_val, values_array[0])
						length_val2 = graphics.DrawText(offscreen_canvas, font_small, offscreen_canvas.width, 0, color_val, values_array[1])

						if length_val1 > length_val2:
							max_length_val = length_val1
						else:
							max_length_val = length_val2

						x_pos_val = offscreen_canvas.width - 6 - max_length_val # New position for values
						length_val1 = graphics.DrawText(offscreen_canvas, font_small, x_pos_val, height1, color_val, values_array[0])
						length_val2 = graphics.DrawText(offscreen_canvas, font_small, x_pos_val, height2, color_val, values_array[1])
						break

		else:
			x_pos_val = offscreen_canvas.width - 1 - length_val
			length_val = graphics.DrawText(offscreen_canvas, font_val, x_pos_val, y_pos_val, color_val, values_text)


	def light_keys(self, offscreen_canvas, keys_text, font_key, font_small, x_pos_key, y_pos_key, color_key, row):
		if " " in keys_text:
			keys_text = keys_text.split()
			height1 = (row * 16) - 8
			height2 = (row * 16) - 1
			length_key1 = graphics.DrawText(offscreen_canvas, font_small, x_pos_key, height1, color_key, keys_text[0])
			length_key2 = graphics.DrawText(offscreen_canvas, font_small, x_pos_key, height2, color_key, keys_text[1])

			if length_key1 > length_key2:
				length_key = length_key1
			else:
				length_key = length_key2

		else:
			length_key = graphics.DrawText(offscreen_canvas, font_key, x_pos_key, y_pos_key, color_key, keys_text)
		return length_key


	def light_borders(self, offscreen_canvas):
		for x in range(0, offscreen_canvas.width):
			offscreen_canvas.SetPixel(x, 0, 47, 86, 233)
			offscreen_canvas.SetPixel(x, 15, 47, 86, 233)
		for y in range(0, offscreen_canvas.height):
			offscreen_canvas.SetPixel(0, y, 47, 86, 233)
			offscreen_canvas.SetPixel(offscreen_canvas.width - 1, y, 47, 86, 233)



# Main function
if __name__ == "__main__":
	run_text = RunText()
	if (not run_text.process()):
		run_text.print_help()
