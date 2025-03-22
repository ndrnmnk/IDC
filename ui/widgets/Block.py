from PyQt5.QtWidgets import QGraphicsObject, QGraphicsTextItem
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QPen, QPainterPath, QFont
from PyQt5.QtCore import QRectF, pyqtSignal

from backend.shapes import generate_points
from ui.subwidgets.EntryManager import EntryManager
from ui.subwidgets.SnapLine import SnapLine
from backend.config_manager import ConfigManager


def sum_max_elements(layer, matrix):
	"""
	Calculate the sum of the maximum elements of each row
	with row index less than the given layer.

	:param layer: int, the threshold for row indices
	:param matrix: list of lists of int, the 2D list to process
	:return: int, the sum of maximum elements
	"""
	if layer <= 0 or not matrix:
		return 0

	# Limit rows to those with index less than layer
	rows_to_consider = matrix[:layer]

	# Compute the sum of maximum elements from the considered rows
	return sum(max(row) for row in rows_to_consider if row)


class Block(QGraphicsObject):
	sizeChanged = pyqtSignal()
	"""Blocks can have different colors, shapes and layer counts.
	Shapes:
	0 - regular block, allows top and bottom snaps
	1 - no bottom connections block
	2 - starter block, bottom snaps only
	3 - operator block, can be snapped in EntryManager
	4 - variable block, can be snapped in EntryManager
	
	For shapes 0, 1 and 2 other blocks can be snapped between the layers. 
	Shapes 3 and 4 with multiple layers look weird and function like single-layer ones.
	
	Spawner blocks spawn their copy and become regular ones after user clicks/drags them.
	"""

	def __init__(self, parent, input_json, spawner=False):
		super().__init__()

		self.parent_view = parent  # crashes when parent is passed to super().__init__(), so using this

		# save data
		self.input_json = input_json
		self.spawner = spawner
		self.shape_index = input_json["shape"]

		# set flags
		self.setFlag(QGraphicsObject.ItemIsMovable)
		self.setFlag(QGraphicsObject.ItemIsSelectable)

		# width and height management variables
		self.width_list = []
		self.height_list = []
		self.between_layers_height_list = []
		# snapping variables
		self.content_list = []
		self.snappable_points = []
		self.snap_line_list = []
		self.snap_candidate = None
		self.snap = None

		self.top_margin = 2 + 15 * (self.shape_index == 2)

		# prepare for launch
		self.populate_block()
		self.path = self.create_path_from_points(self.generate_block_points())
		self.setZValue(2 * self.spawner)
		if not self.spawner:
			self.create_lines_for_snappable_points()

		# finally, show this widget
		self.show()

	def mousePressEvent(self, event):
		super().mousePressEvent(event)
		self.setZValue(2)
		self.unsnap()

	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		if self.shape_index != 2:
			self.check_for_snap()

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		self.parent_view.check_block_for_deletion(self)
		self.setZValue(0)
		self.try_to_snap()

	def populate_block(self):
		ty = self.top_margin
		for layer in range(len(self.input_json["data"])):
			self.content_list.append([])
			self.width_list.append([])
			self.height_list.append([])
			tx = 2
			for idx, json_member in enumerate(self.input_json["data"][layer]):
				if "text" in json_member:
					content = QGraphicsTextItem(json_member["text"], parent=self)
					content.setFont(QFont("Arial", 12))
					self.add_content_item(layer, idx, content, tx, ty)
				elif "text_entry" in json_member:
					self.handle_entry_item(layer, idx, 0, json_member["text_entry"], tx, ty)
				elif "int_entry" in json_member:
					self.handle_entry_item(layer, idx, 1, json_member["int_entry"], tx, ty)
				elif "bool_entry" in json_member:
					self.handle_entry_item(layer, idx, 2, json_member["bool_entry"], tx, ty)
				elif "dropdown" in json_member:
					self.handle_entry_item(layer, idx, 3, json_member["dropdown"], tx, ty)
				else:
					self.content_list[layer].append("what is this")
					self.width_list[layer].append(0)
					self.height_list[layer].append(0)
					print("what is this")
				tx += self.width_list[layer][idx]
			self.between_layers_height_list.append(18)
			ty += self.between_layers_height_list[layer] + max(
				self.height_list[layer])  # height of top layer + actual height between layers
		self.between_layers_height_list.pop()

	def create_lines_for_snappable_points(self):
		for idx, point in enumerate(self.snappable_points):
			self.snap_line_list.append(SnapLine(point, self.boundingRect().width(), self))
			self.snap_line_list[idx].sizeChanged.connect(lambda layer=idx: self.between_layer_height_changed(layer))

	def repopulate_block(self, layer, idx):
		self.prepareGeometryChange()
		if idx != -1:  # if not called because of layer repopulate
			self.width_list[layer][idx] = self.content_list[layer][idx].get_width()
			self.height_list[layer][idx] = self.content_list[layer][idx].get_height()
		else:
			idx = 0

		tx = self.content_list[layer][idx].x() + self.width_list[layer][idx] + 2
		ty = self.top_margin + sum_max_elements(layer, self.height_list) + sum(self.between_layers_height_list[:layer])
		for idxn in range(idx + 1, len(self.content_list[layer])):
			self.content_list[layer][idxn].setPos(tx, ty)
			tx += self.width_list[layer][idxn]

		tx = 2
		ty += max(self.height_list[layer])

		# Repopulate all the layers below the processed one
		for lower_layer in range(layer + 1, len(self.content_list)):
			ty += self.between_layers_height_list[lower_layer - 1]
			for idxn in range(len(self.content_list[lower_layer])):
				self.content_list[lower_layer][idxn].setPos(tx, ty)
				tx += self.width_list[lower_layer][idxn]
			tx = 2
			ty += max(self.height_list[lower_layer])

		self.path = self.create_path_from_points(self.generate_block_points())

		for item in self.snap_line_list:
			item.change_width(self.boundingRect().width() - 40)

		for line in range(layer, len(self.snap_line_list)):
			self.snap_line_list[line].setPos(self.snappable_points[line])

		self.sizeChanged.emit()

	def between_layer_height_changed(self, layer):
		self.between_layers_height_list[layer] = self.snap_line_list[layer].get_height()
		if len(self.between_layers_height_list) != 1:
			self.repopulate_block(layer, -1)
		else:
			self.sizeChanged.emit()

	def unsnap(self):
		if self.snap:
			# get current scene pos
			current_scene_pos = self.mapToScene(0, 0)
			# unparent
			self.setParentItem(None)
			# restore pos
			self.setPos(current_scene_pos)
			# update variables
			self.snap.unsnap()
			self.snap = None
		elif self.spawner:
			# convert coordinates
			scene_pos = self.mapToScene(0, 0)
			# make snappable for other blocks
			self.create_lines_for_snappable_points()
			# update pos so new widget will be in its position
			self.input_json["pos"] = [self.pos().x(), self.pos().y()]
			# update scene variables and create a new spawner block
			self.parent_view.add_block(self.input_json, True)
			self.parent_view.menu_block_list.remove(self)
			self.parent_view.block_list.append(self)
			self.spawner = False
			# unparent
			self.setParentItem(None)
			self.setPos(scene_pos)

	def try_to_snap(self):
		if self.snap_candidate is not None:
			self.snap_candidate.clear_line()
			# get top left corner of snap candidate
			rect = self.snap_candidate.sceneBoundingRect()
			self.setParentItem(self.snap_candidate)
			# calculate pos
			parent_pos = self.snap_candidate.mapToScene(0, 0)
			local_target_x = rect.left() - parent_pos.x()
			local_target_y = rect.top() - parent_pos.y()
			# update pos
			self.setPos(local_target_x - self.boundingRect().left(), local_target_y - self.boundingRect().top())
			# update snap variables
			self.snap = self.snap_candidate
			self.snap.snap_in(self)
			self.snap.sizeChanged.emit()
			self.snap_candidate = None

	def check_for_snap(self):
		for item in self.scene().items():
			# type check for snappable widgets
			if (self.shape_index in [0, 1] and (not isinstance(item, SnapLine) or item in self.snap_line_list)) \
					or (self.shape_index in [3, 4] and (not isinstance(item, EntryManager) or item in self.content_list
														or item.snapped_block or item.parentItem().spawner or not
														item.allowed_snaps[self.shape_index - 3])):
				continue

			if self.check_item_for_snap(item):
				if self.snap_candidate:
					self.snap_candidate.clear_line()
				item.show_line()
				self.snap_candidate = item

		# if dragged far enough from snap candidate, forget about it
		if self.snap_candidate is not None and not self.check_item_for_snap(self.snap_candidate):
			self.snap_candidate.clear_line()
			self.snap_candidate = None

	def check_item_for_snap(self, item):
		# if item is close enough, return True
		self_rect = self.sceneBoundingRect()
		other_rect = item.sceneBoundingRect()
		if abs(self_rect.top() - other_rect.top()) < 15 and abs(self_rect.left() - other_rect.left()) < 45:
			return True
		return False

	def generate_block_points(self):
		width = []
		height = []
		# calculate the dimensions
		for idx in range(len(self.width_list)):
			width.append((sum(self.width_list[idx])) + 2 * len(self.width_list[idx]))
			height.append(max(self.height_list[idx]))
		points, self.snappable_points = generate_points(self.shape_index, max(width), height,
														self.between_layers_height_list)
		return QPolygonF(points)

	@staticmethod
	def create_path_from_points(points: QPolygonF) -> QPainterPath:
		path = QPainterPath()
		if points:
			path.addPolygon(points)
			path.closeSubpath()
		return path

	def boundingRect(self) -> QRectF:
		return self.path.boundingRect()

	def paint(self, painter: QPainter, option, widget=None):
		painter.setBrush(QColor(ConfigManager().get_config()["block_colors"][self.input_json["category"]]))
		painter.setPen(QPen(QColor("#000000")))
		painter.drawPath(self.path)

	# draw bboxes, used for debugging
	# for child in self.childItems():
	# 	rect = child.mapToParent(child.boundingRect()).boundingRect()
	# 	painter.drawRect(rect)

	def shape(self) -> QPainterPath:
		return self.path

	def add_content_item(self, layer, idx, content, tx, ty, update_signal=None):
		self.content_list[layer].append(content)
		self.content_list[layer][idx].setPos(tx, ty)
		self.width_list[layer].append(self.content_list[layer][idx].boundingRect().width())
		self.height_list[layer].append(self.content_list[layer][idx].boundingRect().height())
		if update_signal:
			self.content_list[layer][idx].sizeChanged.connect(update_signal)

	def handle_entry_item(self, layer, idx, entry_type, entry_data, tx, ty):
		content = EntryManager(self, entry_type, entry_data)
		self.add_content_item(layer, idx, content, tx, ty,
							  lambda caller_idx=idx, caller_layer=layer: self.repopulate_block(caller_layer,
																							   caller_idx))

	def suicide(self, leave_children=False):
		self.parent_view.scene().removeItem(self)

		for line in self.snap_line_list:
			line.disconnect()
			if line.snapped_block and not leave_children:
				line.snapped_block.suicide()
				line.unsnap()

		for layer in self.content_list:
			for item in layer:
				if isinstance(item, EntryManager):
					item.disconnect()
					if item.snapped_block and not leave_children:
						item.snapped_block.suicide()
						item.unsnap()

		if self.spawner:
			self.parent_view.menu_block_list.remove(self)
		else:
			self.parent_view.block_list.remove(self)
		self.deleteLater()

	def customBoundingRect(self) -> QRectF:
		"""Returns bounding rect of this widget and child blocks (if any)"""
		combined_rect = self.boundingRect()  # start with own rect
		for child in self.childItems():
			if (isinstance(child, EntryManager) or isinstance(child, SnapLine)) and child.snapped_block:
				# if child widget is a block, get its customBoundingRect and combine with our own
				child_rect = child.mapRectToParent(child.snapped_block.customBoundingRect())
				combined_rect = combined_rect.united(child_rect)
		if self.shape_index == 1:  # without this, blocks with shape 1 go inside other blocks
			return QRectF(combined_rect.x(), combined_rect.y(), combined_rect.width(), combined_rect.height() + 5)
		return combined_rect

	def get_content(self):
		res = {"category": self.input_json["category"],
			"internal_name": self.input_json["internal_name"], "pos": [self.pos().x(), self.pos().y()]}

		content = []
		for widget in self.get_entry_list():
			if widget.snapped_block:
				content.append([[widget.get_text(), widget.entry_type], widget.snapped_block.get_content()])
			else:
				content.append([[widget.get_text(), widget.entry_type], None])
		snaps = []
		for line in self.snap_line_list:
			if line.snapped_block:
				snaps.append(line.snapped_block.get_content())
			else:
				snaps.append(None)
		res["content"] = content
		res["snaps"] = snaps
		return res

	def get_entry_list(self):
		res = []
		for layer in self.content_list:
			for widget in layer:
				if isinstance(widget, EntryManager):
					res.append(widget)
		return res
