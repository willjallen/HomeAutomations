from automations.constants import ColorType


class Point():
	def __init__(self, x, y):
		self.x = x
		self.y = y

def triangleArea(p1, p2, p3):  # find area of triangle formed by p1, p2 and p3
	return abs((p1.x*(p2.y-p3.y) + p2.x*(p3.y-p1.y)+ p3.x*(p1.yp2.y))/2.0)

def isInside(p1, p2, p3, p):
	area = triangleArea(p1, p2, p3)         #area of triangle ABC
	area1 = triangleArea(p, p2, p3)         #area of PBC
	area2 = triangleArea(p1, p, p3)         #area of APC
	area3 = triangleArea(p1, p2, p)         #area of ABP

	return (area == area1 + area2 + area3)        #when three triangles are forming the whole triangle


#For all newer model Hue lights (Gamut C) the corners of the triangle are
# Red: 0.6915, 0.3038
# Green: 0.17, 0.7
# Blue: 0.1532, 0.0475

gamut_r_point = Point(0.6915, 0.3038)
gamut_g_point = Point(0.17, 0.7)
gamut_b_point = Point(0.1532, 0.0475)



class Color():
	def __init__(self, color_type, **kwargs):
		self.color_type = color_type
		
		if(color_type == ColorType.TEMPERATURE):
			self.mirek = kwargs['mirek']
		
		if(color_type == ColorType.XY):
			self.x = kwargs['x']
			self.y = kwargs['y']

		if(color_type == ColorType.GAMUT_RGB_XY):
			self.r_x = r_x
			self.r_y = r_y

			self.g_x = g_x
			self.g_y = g_y

			self.b_x = b_x
			self.b_y = b_y

		if(color_type == ColorType.RGB):
			red = kwargs['red']
			green = kwargs['green']
			blue = kwargs['blue']

			# Normalize colors
			red = red / 255
			green = green / 255
			blue = blue / 255


			# Convert RGB to xy
			self.color_type = ColorType.XY
			if(red > 0.04045):
				red = pow((red + 0.055) / (1.0 + 0.055), 2.4)
			else:
				red = (red / 12.92) 

			if(green > 0.04045):
				green = pow((green + 0.055) / (1.0 + 0.055), 2.4)
			else: 
				green = (green / 12.92);


			if(blue > 0.04045):
				blue = pow((blue + 0.055) / (1.0 + 0.055), 2.4)
			else:
				blue = (blue / 12.92);

			X = red * 0.4124 + green * 0.3576 + blue * 0.1805;
			Y = red * 0.2126 + green * 0.7152 + blue * 0.0722;
			Z = red * 0.0193 + green * 0.1192 + blue * 0.9505;

			x = X / (X + Y + Z);
			y = Y / (X + Y + Z);

			if(isInside(gamut_r_point, gamut_g_point, gamut_b_point, point(x, y))):
				self.x = x
				self.y = y
			else:
				print('Color is outside gamut triangle')
			

