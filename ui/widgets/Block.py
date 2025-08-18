from copy import deepcopy
from uuid import uuid4

from PyQt5.QtWidgets import QGraphicsObject, QGraphicsTextItem, QMenu, QAction
from PyQt5.QtGui import QPainter, QColor, QPolygonF, QPen, QPainterPath, QFont
from PyQt5.QtCore import QRectF, pyqtSignal, Qt

from backend.shapes import generate_points
from ui.subwidgets.EntryManager import EntryManager
from ui.subwidgets.SnapLine import SnapLine
from backend.config_manager import ConfigManager

LAYER_STATIC = 0
LAYER_OPTIONAl = 1
LAYER_DYNAMIC = 2


def sum_max_elements(layer, matrix):
	""" Calculates the sum of the maximum elements of each row with row index less than the given layer. """
	if layer <= 0 or not matrix:
		return 0

	rows_to_consider = matrix[:layer]
	return sum(max(row) for row in rows_to_consider if row)


class Block(QGraphicsObject):
	sizeChanged = pyqtSignal()
	"""Blocks can have different colors, shapes and layer counts.
	Possible options:
	0 - regular block, allows top and bottom snaps
	1 - no bottom connections block
	2 - starter block, bottom snaps only
	3 - operator block, can be snapped in EntryManager
	4 - variable block, can be snapped in EntryManager
	
	For shapes 0, 1 and 2 other blocks can be snapped between the layers. 
	Shapes 3 and 4 with multiple layers look weird and function like single-layer ones.
	
	Spawner blocks spawn their copy and become regular ones after user clicks/drags them.
	
	'meta' describes the block:
	0 - regular block
	1 - variable block
	2 - dynamic block (has optional or dynamic layers)
	3 - custom function block (not implemented yet)
	"""

	def __init__(self, parent, input_json, spawner=False):
		super().__init__()
		# print(input_json)

		self.parent_view = parent

		if input_json.get("tooltip"): self.setToolTip(input_json.get("tooltip"))

		# save data
		self.spawner = spawner
		self.meta = input_json["meta"]
		self.shape_index = input_json["shape"]

		# handle dynamic blocks
		self.nonstatic_layers = []
		self.input_json = deepcopy(input_json) if self.meta == 2 else input_json
		# variable blocks
		if self.meta == 1 and not self.spawner: self.parent_view.var_manager.register_usage(self)

		# set flags
		self.setFlag(QGraphicsObject.ItemIsMovable)
		self.setFlag(QGraphicsObject.ItemIsSelectable)

		# width and height management variables
		self.width_list = []
		self.height_list = []
		self.between_layers_height_list = []
		# snapping variables
		self.snap_lock = False
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
		if event.button() == Qt.RightButton and (not self.spawner or (self.spawner and self.meta == 1)):
			self.showContextMenu(event)
		else:
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
		blh = 18 if self.shape_index in (0, 1, 2) else 0
		output_layer_id = 0
		for layer in range(len(self.input_json["data"])):
			ltype = self.input_json["data"][layer]["type"]
			if ltype is not LAYER_STATIC:
				self.nonstatic_layers.append({"copy_from": layer, "amount": 0, "type": ltype, "name": self.input_json["data"][layer]["name"]})
				if ltype == LAYER_OPTIONAl: continue
			else:
				self.nonstatic_layers.append(None)
			self.content_list.append([])
			self.width_list.append([])
			self.height_list.append([])
			tx = 2
			for idx, json_member in enumerate(self.input_json["data"][layer]["data"]):
				self.process_content_json_item(json_member, output_layer_id, idx, tx, ty)
				tx += self.width_list[output_layer_id][idx]
			self.between_layers_height_list.append(blh)
			ty += self.between_layers_height_list[output_layer_id] + max(self.height_list[output_layer_id])  # height of top layer + actual height between layers
			output_layer_id += 1
		self.between_layers_height_list.pop()

	def process_content_json_item(self, json_member, layer, idx, tx, ty):
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
		elif "block_entry" in json_member:
			self.handle_entry_item(layer, idx, 4, json_member["block_entry"], tx, ty)

	def create_lines_for_snappable_points(self):
		for idx, point in enumerate(self.snappable_points):
			self.snap_line_list.append(SnapLine(point, self.boundingRect().width(), self))
			self.snap_line_list[-1].sizeChanged.connect(lambda t=idx: self.between_layer_height_changed(t))

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
		if layer < len(self.between_layers_height_list):
			self.between_layers_height_list[layer] = self.snap_line_list[layer].get_height()
		if len(self.between_layers_height_list) > 0:
			self.repopulate_block(layer, -1)
		else:
			self.sizeChanged.emit()

	def unsnap(self):
		self.snap_lock = False
		if self.snap:
			# unparent and restore pos
			current_scene_pos = self.mapToScene(0, 0)
			self.setParentItem(None)
			self.setPos(current_scene_pos)
			# update variables
			self.snap.unsnap()
			self.snap = None
		elif self.spawner:
			if self.meta == 1:
				self.parent_view.var_manager.register_usage(self)
			# convert coordinates
			scene_pos = self.mapToScene(0, 0)
			# make snappable for other blocks
			self.create_lines_for_snappable_points()
			# update pos so new widget will be in its position
			self.input_json["pos"] = [self.pos().x(), self.pos().y()]
			# update scene variables and create a new spawner block
			j = deepcopy(self.input_json)
			j["identifier"] = str(uuid4())
			self.parent_view.add_block(j, True)
			self.parent_view.block_manager.block_list.remove(self)
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

			if self.shape_index in (0, 1) and isinstance(self.snap, EntryManager):
				self.snap_lock = True

	def check_for_snap(self):
		for item in self.scene().items():
			if not self.check_widget_for_snappable(item):
				continue

			if self.check_item_for_snap_distance(item):
				if self.snap_candidate:
					self.snap_candidate.clear_line()
				item.show_line()
				self.snap_candidate = item

		# if dragged far enough from snap candidate, forget about it
		if self.snap_candidate is not None and not self.check_item_for_snap_distance(self.snap_candidate):
			self.snap_candidate.clear_line()
			self.snap_lock = False
			self.snap_candidate = None

	def check_widget_for_snappable(self, widget):
		if self.shape_index in [0, 1]:
			if isinstance(widget, SnapLine) and widget not in self.snap_line_list and not widget.parentItem().snap_lock:
				return True
			if (isinstance(widget, EntryManager) and widget.allowed_snaps[2] and not any(widget in sublist for sublist in self.content_list)
				and len(self.snap_line_list) == 1 and not self.snap_line_list[0].snapped_block):
					return True
			return False
		elif self.shape_index in [3, 4]:
			if isinstance(widget, EntryManager) and widget.allowed_snaps[self.shape_index - 3] \
				and widget not in self.content_list and not widget.snapped_block and not widget.parentItem().spawner:
					return True
			return False
		return False

	def check_item_for_snap_distance(self, item):
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
		points, self.snappable_points = generate_points(self.shape_index, max(width), height, self.between_layers_height_list)
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
							  lambda caller_idx=idx, caller_layer=layer: self.repopulate_block(caller_layer, caller_idx))

	def suicide(self, leave_children=False):
		if self.snap:
			self.unsnap()

		if leave_children:
			for line in self.snap_line_list:
				line.disconnect()
				if line.snapped_block:
						line.snapped_block.unsnap()

			for item in self.get_entry_list():
				if isinstance(item, EntryManager):
					item.disconnect()
					if item.snapped_block:
						item.snapped_block.unsnap()

		else:
			for line in self.snap_line_list:
				line.disconnect()
				if line.snapped_block:
						line.snapped_block.suicide()

			for item in self.get_entry_list():
				if isinstance(item, EntryManager):
					item.disconnect()
					if item.snapped_block:
						item.snapped_block.suicide()

		self.parent_view.scene().removeItem(self)

		if self.spawner: self.parent_view.block_manager.block_list.remove(self)
		else: self.parent_view.block_list.remove(self)

		if self.meta == 1:
			try:
				vname = self.input_json["internal_name"][5:]
				var_id = self.input_json["identifier"]
				self.parent_view.var_manager.unreg_usage(vname, var_id, self.parent_view.sprite_manager.current_sprite)
			except (ValueError, KeyError):
				pass

		self.deleteLater()

	def showContextMenu(self, event):
		position = event.screenPos()
		menu = QMenu()

		if self.spawner and self.meta == 1:
			action_del_var = QAction("Delete variable")
			internal_name = self.input_json["internal_name"]
			action_del_var.triggered.connect(lambda checked, n=internal_name: self.parent_view.var_manager.delete_var_by_name(n))
			menu.addAction(action_del_var)
			menu.exec_(position)
			return

		clicked_layer = self.get_layer_by_mouse_pos(event.pos())
		if self.input_json["data"][clicked_layer]["type"] is not LAYER_STATIC:
			action_del3 = QAction(f"Delete layer №{clicked_layer+1}", menu)
			action_del3.triggered.connect(lambda checked, i=clicked_layer: self.delete_layer(i))
			menu.addAction(action_del3)

		for idx, layer in enumerate(self.nonstatic_layers):
			if not layer or (layer["type"] == LAYER_OPTIONAl and layer["amount"] > 0):
				continue
			action_add_layer = QAction(f"Add «{layer["name"]}» layer", menu)
			action_add_layer.triggered.connect(lambda checked, i=idx: self.copy_layer(i))
			menu.addAction(action_add_layer)

		# Regular delete actions
		action_del1 = QAction("Delete", menu)
		action_del2 = QAction("Unsnap + delete", menu)
		action_del1.triggered.connect(lambda: self.suicide(False))
		action_del2.triggered.connect(lambda: self.suicide(True))
		menu.addAction(action_del1)
		menu.addAction(action_del2)

		menu.exec_(position)

	def copy_layer(self, og_copy_from, on_block_creation=False):
		copy_from = self.nonstatic_layers[og_copy_from]["copy_from"]
		is_optional = self.nonstatic_layers[og_copy_from]["type"] == LAYER_OPTIONAl
		if is_optional: insert_at = copy_from
		elif on_block_creation: insert_at = copy_from + 1
		else: insert_at = copy_from + 1 + self.nonstatic_layers[og_copy_from]["amount"]

		# add a layer in json
		layer = self.input_json["data"][copy_from]
		if not is_optional: self.input_json["data"].insert(insert_at, layer)

		# add other variables
		self.content_list.insert(insert_at, [])
		blh = 18 if self.shape_index in (0, 1, 2) else 0
		self.between_layers_height_list.insert(insert_at, blh)
		self.width_list.insert(insert_at, [])
		self.height_list.insert(insert_at, [])

		# add new widgets
		ty = self.top_margin + sum_max_elements(insert_at, self.height_list) + sum(self.between_layers_height_list[:insert_at])
		tx = 2
		for idx, json_member in enumerate(layer["data"]):
			self.process_content_json_item(json_member, insert_at, idx, tx, ty)
			tx += self.width_list[insert_at][idx]

		# add a snap line
		if self.shape_index not in (3, 4):
			self.path = self.create_path_from_points(self.generate_block_points())
			self.snap_line_list.insert(insert_at, SnapLine(self.snappable_points[insert_at], self.boundingRect().width(), self))
			self.snap_line_list[insert_at].sizeChanged.connect(lambda t=insert_at: self.between_layer_height_changed(t))

		self.rewire_snapline_signals(insert_at+1)
		self.rewire_entry_signals(insert_at)
		if not on_block_creation:
			self.nonstatic_layers[og_copy_from]["amount"] += 1
			self.rewire_nonstatic_ids(og_copy_from, 1)

		self.repopulate_block(insert_at, -1)

	def rewire_entry_signals(self, start_at):
		for layer_idx, _ in enumerate(self.height_list[start_at:], start_at):
			for idx, widget in enumerate(self.content_list[layer_idx]):
				if isinstance(widget, EntryManager):
					widget.sizeChanged.disconnect()
					widget.sizeChanged.connect(lambda layer=layer_idx, t=idx: self.repopulate_block(layer, t))

	def rewire_snapline_signals(self, start_at):
		for idx, snapline in enumerate(self.snap_line_list[start_at:], start_at):
			snapline.sizeChanged.disconnect()
			snapline.sizeChanged.connect(lambda t=idx: self.between_layer_height_changed(t))

	def rewire_nonstatic_ids(self, inserted_layer_id, change_by):
		for item in self.nonstatic_layers[inserted_layer_id+1:]:
			if item: item["copy_from"] += change_by

	def get_layer_by_mouse_pos(self, pos):
		y = pos.y()
		ty = self.top_margin
		res = None
		for layer_idx in range(len(self.height_list)):
			layer_height = max(self.height_list[layer_idx])
			if y <= ty + layer_height:
				res = layer_idx
				break
			ty += layer_height
			if layer_idx < len(self.between_layers_height_list):
				ty += self.between_layers_height_list[layer_idx]

		# account for skipped layers
		l = self.regular_to_nonstatic_id(res) + 1
		for layer in self.nonstatic_layers[:l]:
			if not layer: continue
			if layer["amount"] == 0 and layer["type"] == 1: res += 1
		return res

	def delete_layer(self, layer_idx):
		idx = self.regular_to_nonstatic_id(layer_idx)
		if self.input_json["data"][layer_idx]["type"] == LAYER_DYNAMIC:
			if self.nonstatic_layers[idx]["amount"] == 0: return
			del self.input_json["data"][layer_idx]
		self.nonstatic_layers[idx]["amount"] -= 1
		for widget in self.content_list[layer_idx]: widget.deleteLater()
		del self.content_list[layer_idx]
		del self.width_list[layer_idx]
		del self.height_list[layer_idx]
		try: del self.between_layers_height_list[layer_idx]
		except IndexError: pass

		self.snap_line_list[layer_idx].deleteLater()
		del self.snap_line_list[layer_idx]

		if layer_idx != len(self.height_list):
			self.rewire_entry_signals(layer_idx)
			self.rewire_snapline_signals(layer_idx)
		self.rewire_nonstatic_ids(idx, -1)

		self.repopulate_block(layer_idx-1, -1)

	def regular_to_nonstatic_id(self, regular_layer_id):
		current_regular_index = -1

		for i, nonstatic in enumerate(self.nonstatic_layers):
			if nonstatic is None: current_regular_index += 1
			else:
				current_regular_index += nonstatic["amount"] + 1
				if current_regular_index >= regular_layer_id:
					return i
		return None

	def customBoundingRect(self):
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

	def get_entry_list(self):
		res = []
		for layer in self.content_list:
			for widget in layer:
				if isinstance(widget, EntryManager):
					res.append(widget)
		return res

	def get_content(self):
		res = {"category": self.input_json["category"], "internal_name": self.input_json["internal_name"],
			   "pos": [self.pos().x(), self.pos().y()]}

		content = []
		for widget in self.get_entry_list():
			if widget.snapped_block:
				content.append([[widget.get_text(), widget.entry_type], widget.snapped_block.input_json["identifier"]])
			else:
				content.append([[widget.get_text(), widget.entry_type], None])
		snaps = []
		for line in self.snap_line_list:
			if line.snapped_block:
				snaps.append(line.snapped_block.input_json["identifier"])
			else:
				snaps.append(None)
		res["content"] = content
		res["snaps"] = snaps
		res["nonstatic"] = self.nonstatic_layers
		return res, self.input_json["identifier"]