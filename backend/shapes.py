from PyQt5.QtCore import QPointF
import math


def get_circle_points(radius, num_points=360):
	"""
	Generate points on a circle of given radius, starting from the bottom (0, -r) and going clockwise.

	:param radius: Radius of the circle
	:param num_points: Number of points to generate on the circle
	:return: List of (x, y) tuples
	"""
	points = []
	# Start at 270° (bottom) and go clockwise by decreasing the angle
	for i in range(num_points):
		angle_deg = 270 - (360 * i / num_points)
		angle_rad = math.radians(angle_deg)
		x = radius * math.cos(angle_rad)
		y = radius * math.sin(angle_rad)
		points.append((x, y))
	return points


def generate_points(shape_id, width, height, between_layers_height):
	"""
	Generates points for a block.

	Args:
		shape_id (int): Type of the block. For more info, look at comments near if/elif
		width (int): Width of block (same for all layers)
		height (list): Height of each layer
		between_layers_height (list): height between layers

	Returns:
		list: set of points for block
	"""

	between_layers_height.append(0)  # no idea why, but it crashes without this
	skip_next_half_block = False

	min_width = [50, 50, 60, 28, 28, 50]

	width = max(width, min_width[shape_id])
	if shape_id == 0:  # regular block, allows both top and bottom connections
		start_x = 0
		start_y = 0
		bulge_x = 10
		res = []
		snappable_points = []
		for idx, h in enumerate(height):
			# top half block
			if not skip_next_half_block:
				res = res + [
					QPointF(start_x, start_y),
					QPointF(start_x+bulge_x, start_y),
					QPointF(start_x+bulge_x, start_y+5),
					QPointF(start_x+bulge_x+30, start_y+5),
					QPointF(start_x+bulge_x+30, start_y),
					QPointF(width, start_y)]
			else:
				skip_next_half_block = False

			res.append(QPointF(width, start_y+h))

			# decide on where to put the bulge
			start_x = 20 if idx != len(height) - 1 else 0

			if between_layers_height[idx] == 0:
				skip_next_half_block = 1

			# bottom half of the block
			if not skip_next_half_block:
				res = res + [
					QPointF(start_x+bulge_x+30, start_y+h),
					QPointF(start_x+bulge_x+30, start_y+h+5),
					QPointF(start_x+bulge_x, start_y+h+5),
					QPointF(start_x+bulge_x, start_y+h),
					QPointF(start_x, start_y+h)
				]
			snappable_points.append(QPointF(start_x, start_y+h))
			start_y += between_layers_height[idx] + height[idx]
		between_layers_height.pop()
		return res, snappable_points
	elif shape_id == 1:  # no bottom connections block
		start_x = 0
		start_y = 0
		bulge_x = 10
		snappable_points = []
		res = []
		for idx, h in enumerate(height):
			if not skip_next_half_block:
				res = res + [
					QPointF(start_x, start_y),
					QPointF(start_x+bulge_x, start_y),
					QPointF(start_x+bulge_x, start_y+5),
					QPointF(start_x+bulge_x+30, start_y+5),
					QPointF(start_x+bulge_x+30, start_y),
					QPointF(width, start_y)]
			else:
				skip_next_half_block = False

			res.append(QPointF(width, start_y+h))

			if between_layers_height[idx] == 0:
				skip_next_half_block = 1

			if idx != len(height) - 1:
				start_x = 20
				snappable_points.append(QPointF(start_x, start_y+h))
				if not skip_next_half_block:
					res = res + [
						QPointF(start_x + bulge_x + 30, start_y + h),
						QPointF(start_x + bulge_x + 30, start_y + h + 5),
						QPointF(start_x + bulge_x, start_y + h + 5),
						QPointF(start_x + bulge_x, start_y + h),
						QPointF(start_x, start_y + h)
					]
			else:
				start_x = 0
				res.append(QPointF(start_x, start_y + h))
			start_y += between_layers_height[idx] + height[idx]
		between_layers_height.pop()
		return res, snappable_points
	elif shape_id == 2:  # start block, no top connections
		points = get_circle_points(15)[90:271]
		points = [QPointF((v1+15)*2, 15-v2) for v1, v2 in points]  # gets points for top half-ellipse
		res = points
		snappable_points = []
		start_x = 0
		start_y = 15
		bulge_x = 10
		for idx, h in enumerate(height):
			if not skip_next_half_block:
				if idx != 0:
					res = res + [
						QPointF(start_x, start_y),
						QPointF(start_x+bulge_x, start_y),
						QPointF(start_x+bulge_x, start_y+5),
						QPointF(start_x+bulge_x+30, start_y+5),
						QPointF(start_x+bulge_x+30, start_y)]
				else:
					res.append(QPointF(60, start_y))
			else:
				skip_next_half_block = False
			res.extend([QPointF(width, start_y), QPointF(width, start_y+h)])

			if between_layers_height[idx] == 0:
				skip_next_half_block = True

			if not idx == len(height) - 1:
				start_x = 20
			else:
				start_x = 0
			snappable_points.append(QPointF(start_x, start_y+h))
			if not skip_next_half_block:
				res = res + [
					QPointF(start_x+bulge_x+30, start_y+h),
					QPointF(start_x+bulge_x+30, start_y+h+5),
					QPointF(start_x+bulge_x, start_y+h+5),
					QPointF(start_x+bulge_x, start_y+h),
					QPointF(start_x, start_y+h)
				]
			start_y += between_layers_height[idx] + height[idx]
		between_layers_height.pop()
		return res, snappable_points
	elif shape_id == 3:  # operator block, snaps inside other blocks
		between_layers_height.pop()
		new_height = sum(height)
		return [
			QPointF(new_height/2, 0),
			QPointF(width-new_height/2, 0),
			QPointF(width, new_height/2),
			QPointF(width-new_height/2, new_height),
			QPointF(new_height/2, new_height),
			QPointF(0, new_height/2)
		], []
	elif shape_id == 4:  # variable block, snaps inside other blocks
		between_layers_height.pop()
		new_height = sum(height)
		points = get_circle_points(new_height/2)
		right_half_circle = [QPointF(v1 + width-new_height/2, new_height/2-v2) for v1, v2 in points[180:]]
		left_half_circle = [QPointF(v1+new_height/2, new_height/2-v2) for v1, v2 in points[:180]]
		res = ([QPointF(new_height / 2, 0), QPointF(width-new_height/2, 0)] + right_half_circle +
			   [QPointF(width-new_height/2, new_height), QPointF(new_height/2, new_height)] + left_half_circle)

		return res, []
	elif shape_id == 5:
		between_layers_height.pop()
		new_height = sum(height)
		points = get_circle_points(new_height / 2)
		right_half_circle = [QPointF(v1 + width - new_height / 2, new_height / 2 - v2) for v1, v2 in points[180:]]
		snappable_points = [QPointF(0, new_height)]

		res = [QPointF(0, 0), QPointF(10, 0), QPointF(10, 5), QPointF(40, 5), QPointF(40, 0), QPointF(width - new_height / 2, 0)]
		res.extend(right_half_circle)
		res.extend([QPointF(width - new_height / 2, new_height), QPointF(40, new_height), QPointF(40, new_height + 5),
					QPointF(10, new_height+5), QPointF(10, new_height), QPointF(0, new_height)])
		return res, snappable_points
