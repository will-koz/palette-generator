#!/usr/bin/python3

from PIL import Image

import colorsys, random

input_location = "wallpaper.png"
retries = 2048
escape_character = "\033"

colors = [((0, 255), (0, 255), (0, 20)), # Black
	((0, 30), (160, 255), (128, 255)), # Red
	((70, 100), (160, 255), (128, 255)), # Green
	((30, 60), (120, 255), (128, 255)), # Yellow
	((160, 180), (180, 255), (50, 255)), # Blue
	((190, 220), (180, 255), (0, 128)), # Purple
	((100, 130), (160, 255), (128, 255)), # Cyan
	((0, 255), (0, 20), (235, 255))] # White

#----------------------------------------------------------------------------------------------------

def get_random_pixel_from_image (image):
	pointx = random.randint(0, image.size[0] - 1) # Get random point between 0 and width
	pointy = random.randint(0, image.size[1] - 1) # Get random point between 0 and height
	return image.getpixel((pointx, pointy))

#----------------------------------------------------------------------------------------------------

input_image = Image.open(input_location)
input_image = input_image.convert("HSV")
found_colors = []

for color in colors:
	tested_pixels = 0
	while tested_pixels < retries and tested_pixels != -1:
		current_pixel = get_random_pixel_from_image(input_image)
		tested_pixels += 1
		test_passes = True
		test_passes &= current_pixel[0] >= color[0][0] and current_pixel[0] <= color[0][1] # Test against red in rgb
		test_passes &= current_pixel[1] >= color[1][0] and current_pixel[1] <= color[1][1] # Test against green in rgb
		test_passes &= current_pixel[2] >= color[2][0] and current_pixel[2] <= color[2][1] # Test against blue in rgb
		if test_passes:
			tested_pixels = -1 # Found a match
			found_colors.append(current_pixel)
	if tested_pixels != -1:
		print("Cound not find color matching", color)
		found_colors.append(get_random_pixel_from_image(input_image))

final_rgb_colors = []

coloroutput = ""
print("HSV :", found_colors)
for color in found_colors:
	rgb_from_hsb = (color[0] / 255, color[1] / 255, color[2] / 255)
	rgb_from_hsb = colorsys.hsv_to_rgb(rgb_from_hsb[0], rgb_from_hsb[1], rgb_from_hsb[2])
	rgb_from_hsb = (int(rgb_from_hsb[0] * 255), int(rgb_from_hsb[1] * 255), int(rgb_from_hsb[2] * 255))
	final_rgb_colors.append(rgb_from_hsb)
	coloroutput += escape_character + "[48;2;" + str(rgb_from_hsb[0]) + ";" + str(rgb_from_hsb[1]) + ";" + str(rgb_from_hsb[2]) + "m   " + escape_character + "[0m"
print(coloroutput)
coloroutput = ""
for color in found_colors:
	rgb_from_hsb = (color[0] / 255, max(color[1] - 30, 0) / 255, min(color[2] + 30, 255) / 255)
	rgb_from_hsb = colorsys.hsv_to_rgb(rgb_from_hsb[0], rgb_from_hsb[1], rgb_from_hsb[2])
	rgb_from_hsb = (int(rgb_from_hsb[0] * 255), int(rgb_from_hsb[1] * 255), int(rgb_from_hsb[2] * 255))
	final_rgb_colors.append(rgb_from_hsb)
	coloroutput += escape_character + "[48;2;" + str(rgb_from_hsb[0]) + ";" + str(rgb_from_hsb[1]) + ";" + str(rgb_from_hsb[2]) + "m   " + escape_character + "[0m"
print(coloroutput)
