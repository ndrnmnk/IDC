from PyQt5.QtCore import QPoint


def generate_points(shape_id, width, height):
	if shape_id == 0:  # regular block
		return [
			QPoint(0, 0),
			QPoint(10, 0),
			QPoint(10, 5),
			QPoint(40, 5),
			QPoint(40, 0),
			QPoint(width, 0),
			QPoint(width, height),
			QPoint(40, height),
			QPoint(40, height + 5),
			QPoint(10, height + 5),
			QPoint(10, height),
			QPoint(0, height)
		], 5, 4, 5, 8
	elif shape_id == 1:  # no bottom connections block
		return [
			QPoint(0, 0),
			QPoint(10, 0),
			QPoint(10, 5),
			QPoint(40, 5),
			QPoint(40, 0),
			QPoint(width, 0),
			QPoint(width, height),
			QPoint(0, height)
		], 5, 4, 5, 3
	elif shape_id == 2:  # start block, no top connections
		return [
			QPoint(0, 14),
			QPoint(2, 9),
			QPoint(8, 5),
			QPoint(15, 2),
			QPoint(25, 0),
			QPoint(35, 0),
			QPoint(44, 2),
			QPoint(52, 5),
			QPoint(58, 9),
			QPoint(60, 14),
			QPoint(width, 14),
			QPoint(width, height + 14),
			QPoint(40, height + 14),
			QPoint(40, height + 19),
			QPoint(10, height + 19),
			QPoint(10, height + 14),
			QPoint(0, height + 14)
		], 5, 18, 5, 8
	elif shape_id == 3:
		return [
			QPoint(10, 0),
			QPoint(width, 0),
			QPoint(width+10, int(height/2)),
			QPoint(width, height),
			QPoint(10, height),
			QPoint(0, int(height/2))
		], 10, 4, 10, 3
	elif shape_id == 4:
		return [
			QPoint(10, 0),
			QPoint(width, 0),
			QPoint(width+10, int(height/4)),
			QPoint(width + 10, int(height / 4)*3),
			QPoint(width, height),
			QPoint(10, height),
			QPoint(0, int(height/4)*3),
			QPoint(0, int(height / 4))
		], 10, 4, 10, 3
