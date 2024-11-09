def generate_points(shape_id, width, height):
	if shape_id == 0:  # regular block
		return [
			0, 0,
			10, 0,
			10, 5,
			40, 5,
			40, 0,
			width, 0,
			width, height,
			40, height,
			40, height + 5,
			10, height + 5,
			10, height,
			0, height
		], 5, 4, 5, 8
	elif shape_id == 1:  # no bottom connections block
		return [
			0, 0,
			10, 0,
			10, 5,
			40, 5,
			40, 0,
			width, 0,
			width, height,
			0, height
		], 5, 4, 5, 3
	elif shape_id == 2:  # start block, no top connections
		return [
			0, 14,
			2, 9,
			8, 5,
			15, 2,
			25, 0,
			35, 0,
			44, 2,
			52, 5,
			58, 9,
			60, 14,
			width, 14,
			width, height + 14,
			40, height + 14,
			40, height + 19,
			10, height + 19,
			10, height + 14,
			0, height + 14
		], 5, 18, 5, 8
