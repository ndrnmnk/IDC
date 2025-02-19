from PyQt5.QtCore import QPointF


def get_circle_points(radius, angles_to_do=360):
	"""
	Approximates a circle (or part of it) of gives radius.

	Args:
		radius (float): Radius of circle go create.
		angles_to_do (int): The part of circle to create, starts from bottom and goes clockwise.

	Returns:
		list: list of coordinates for circle points.
	"""
	points = []
	x, y = 0, -radius
	angle = 0

	for _ in range(angles_to_do):
		# Append the current point
		points.append((x, y))

		# Calculate change in x and y based on step length and angle approximation
		dx = y * 0.01745
		dy = -x * 0.01745
		x += dx
		y += dy

		# Rotate the vector by approximately 1 degree
		angle += 1

	return points


def generate_points(shape_id, width, height, between_layers_height):
	between_layers_height.append(0)
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
	if shape_id == 0:  # regular block, allows both top and bottom connections
		start_x = 0
		start_y = 0
		bulge_x = 10
		res = []
		snappable_points = []
		for idx, h in enumerate(height):
			res = res + [
				QPointF(start_x, start_y),
				QPointF(start_x+bulge_x, start_y),
				QPointF(start_x+bulge_x, start_y+5),
				QPointF(start_x+bulge_x+30, start_y+5),
				QPointF(start_x+bulge_x+30, start_y),
				QPointF(width, start_y),
				QPointF(width, start_y+h)]
			if not idx == len(height) - 1:
				start_x = 40
			else:
				start_x = 0
			res = res + [
				QPointF(start_x+bulge_x+30, start_y+h),
				QPointF(start_x+bulge_x+30, start_y+h+5),
				QPointF(start_x+bulge_x, start_y+h+5),
				QPointF(start_x+bulge_x, start_y+h),
				QPointF(start_x, start_y+h)
			]
			snappable_points.append(QPointF(start_x, start_y+h))
			start_y += between_layers_height[idx] + height[idx]
		return res, snappable_points
	elif shape_id == 1:  # no bottom connections block
		start_x = 0
		start_y = 0
		bulge_x = 10
		snappable_points = []
		res = []
		for idx, h in enumerate(height):
			res = res + [
				QPointF(start_x, start_y),
				QPointF(start_x+bulge_x, start_y),
				QPointF(start_x+bulge_x, start_y+5),
				QPointF(start_x+bulge_x+30, start_y+5),
				QPointF(start_x+bulge_x+30, start_y),
				QPointF(width, start_y),
				QPointF(width, start_y+h)]
			if not idx == len(height) - 1:
				start_x = 40
				snappable_points.append(QPointF(start_x, start_y+h))
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
			if idx != 0:
				res = res + [
					QPointF(start_x, start_y),
					QPointF(start_x+bulge_x, start_y),
					QPointF(start_x+bulge_x, start_y+5),
					QPointF(start_x+bulge_x+30, start_y+5),
					QPointF(start_x+bulge_x+30, start_y),
					QPointF(width, start_y),
					QPointF(width, start_y+h)]
			else:
				res = res + [
					QPointF(60, start_y),
					QPointF(width, start_y),
					QPointF(width, start_y+h)
				]
			if not idx == len(height) - 1:
				start_x = 40
			else:
				start_x = 0
			snappable_points.append(QPointF(start_x, start_y+h))
			res = res + [
				QPointF(start_x+bulge_x+30, start_y+h),
				QPointF(start_x+bulge_x+30, start_y+h+5),
				QPointF(start_x+bulge_x, start_y+h+5),
				QPointF(start_x+bulge_x, start_y+h),
				QPointF(start_x, start_y+h)
			]
			start_y += between_layers_height[idx] + height[idx]
		return res, snappable_points
	elif shape_id == 3:  # operator block, snaps inside other blocks
		new_height = sum(height) + sum(between_layers_height)
		return [
			QPointF(new_height/2, 0),
			QPointF(width-new_height/2, 0),
			QPointF(width, new_height/2),
			QPointF(width-new_height/2, new_height),
			QPointF(new_height/2, new_height),
			QPointF(0, new_height/2)
		], []
	elif shape_id == 4:  # variable block, snaps inside other blocks
		new_height = sum(height) + sum(between_layers_height)
		points = get_circle_points(new_height/2)
		right_half_circle = [QPointF(v1 + width-new_height/2, new_height/2-v2) for v1, v2 in points[180:]]
		left_half_circle = [QPointF(v1+new_height/2, new_height/2-v2) for v1, v2 in points[:180]]
		res = [QPointF(new_height / 2, 0), QPointF(width-new_height/2, 0)] + right_half_circle + [QPointF(width-new_height/2, new_height), QPointF(new_height/2, new_height)] + left_half_circle

		return res, []
