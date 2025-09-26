from uuid import uuid4

from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPainterPath, QPolygonF, QPen, QColor, QPainter
from PyQt5.QtCore import pyqtSignal, QRectF, Qt

from backend import ConfigManager, generate_points
from .layer import BlockLayer
from .context_menu import BlockContextMenu

from ui.subwidgets.EntryManager import EntryManager
from ui.subwidgets.SnapLine import SnapLine

class Block(QGraphicsObject):
	sizeChanged = pyqtSignal()

	def __init__(self, wv, input_json, spawner=False):
		super().__init__()
		self.path = None
		self.setFlag(QGraphicsObject.ItemIsMovable)
		self.setFlag(QGraphicsObject.ItemIsSelectable)

		# save input json
		self.spawner = spawner
		self.workspace_view = wv
		self.shape_id = input_json["shape"]
		self.return_type = input_json.get("returns", None)

		self.input_json = input_json

		if not self.input_json.get("identifier", None):
			self.input_json["identifier"] = str(uuid4())

		self.layers_list = []
		self.layer_info = []
		self.snap_line_list = []  # populated by BlockLayer class
		self.nonstatic_layers = {}

		self.width_list = []
		self.height_list = []
		self.between_layers_height_list = []

		self.snap_candidate = None
		self.snapped_to = None
		self.snappable_points = []

		self.populate()

		points = self.generate_block_points()
		self.create_path(points)

		if not self.spawner:
			self.create_snap_lines()
			self.snap_lock = False
			if self.input_json["meta"] == 1: self.workspace_view.var_manager.register_usage(self)
		else:
			self.snap_lock = True

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			super().mousePressEvent(event)
			if self.spawner:
				self.despawnerize()
			self.setZValue(10)
			self.unsnap()

	def contextMenuEvent(self, event):
		if self.spawner and self.input_json["meta"] != 1:
			# exiting because there won't be any actions in the menu
			event.accept()
			return
		BlockContextMenu(self, event)

	def mouseMoveEvent(self, event):
		super().mouseMoveEvent(event)
		if self.shape_id != 2: self.check_for_snap()

	def mouseReleaseEvent(self, event):
		super().mouseReleaseEvent(event)
		if event.button() == Qt.LeftButton:
			self.workspace_view.check_block_for_deletion(self)
			self.setZValue(0)
			self.snap_to_candidate()

	def check_for_snap(self):
		for item in self.scene().items():
			if item in self.childItems() or item is self.snap_candidate:
				continue
			if not self.snap_distance_check(item): continue
			if not self.snap_widget_check(item): continue

			if self.snap_candidate:
				self.snap_candidate.clear_line()
			self.snap_candidate = item
			item.show_line()

		if self.snap_candidate and not self.snap_distance_check(self.snap_candidate):
			self.snap_candidate.clear_line()
			self.snap_candidate = None

	def snap_to_candidate(self):
		if self.snap_candidate:
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
			self.snapped_to = self.snap_candidate
			self.snapped_to.snap_in(self)
			self.snapped_to.sizeChanged.emit()
			self.snap_candidate = None

			if isinstance(self.snapped_to, EntryManager) and self.shape_id in (0, 1, 5):
				self.snap_lock = True

	def unsnap(self):
		if self.snapped_to:
			self.snap_lock = False
			# unparent and restore pos
			current_scene_pos = self.mapToScene(0, 0)
			self.setParentItem(None)
			self.setPos(current_scene_pos)
			# update variables
			self.snapped_to.unsnap()
			self.snapped_to = None

	def populate(self):
		ty = 0 if self.shape_id != 2 else 16
		for idx, json_member in enumerate(self.input_json["data"]):
			temp_layer = BlockLayer(self, idx, json_member["type"])
			self.layers_list.append(temp_layer)
			temp_layer.populate(ty)
			self.width_list.append(self.layers_list[-1].get_width())
			self.height_list.append(self.layers_list[-1].get_height())
			self.between_layers_height_list.append(self.layers_list[-1].get_snapped_block_height())
			ty += self.height_list[-1] + self.between_layers_height_list[-1]

	def repopulate(self, caller_id):
		self.prepareGeometryChange()
		old_w = max(self.width_list)
		old_h = self.height_list[caller_id]
		old_blh = self.between_layers_height_list[caller_id]
		self.width_list[caller_id] = self.layers_list[caller_id].get_width()
		self.height_list[caller_id] = self.layers_list[caller_id].get_height()
		self.between_layers_height_list[caller_id] = self.layers_list[caller_id].get_snapped_block_height()

		if old_w < self.width_list[caller_id]:
			for sl in self.snap_line_list:
				sl.change_width(self.width_list[caller_id]-20)

		# if height changed, move layers below caller
		if old_h != self.height_list[caller_id] or old_blh != self.between_layers_height_list[caller_id]:
			dy = self.height_list[caller_id] - old_h
			if dy: self.layers_list[caller_id].move_by(dy, True)
			dy += self.between_layers_height_list[caller_id] - old_blh

			for layer in self.layers_list[caller_id+1:]:
				layer.move_by(dy)

		points = self.generate_block_points()
		self.create_path(points)
		self.update()
		self.sizeChanged.emit()

	def suicide(self, leave_children=False):
		self.unsnap()

		if leave_children:
			for item in self.get_entry_list() + self.snap_line_list:
				item.try_to_disconnect()
				if item.snapped_block: item.snapped_block.unsnap()
		else:
			for item in self.get_entry_list() + self.snap_line_list:
				item.try_to_disconnect()
				if item.snapped_block: item.snapped_block.suicide()

		self.workspace_view.scene().removeItem(self)
		if self.spawner: self.workspace_view.block_manager.block_list.remove(self)
		else: self.workspace_view.block_list.remove(self)

		if self.input_json["meta"] == 1:
			try:
				vname = self.input_json["internal_name"][5:]
				var_id = self.input_json["identifier"]
				self.workspace_view.var_manager.unreg_usage(vname, var_id, self.workspace_view.sprite_manager.current_sprite)
			except (ValueError, KeyError): pass

		self.deleteLater()

	def create_snap_lines(self):
		for idx, point in enumerate(self.snappable_points):
			self.layers_list[idx].add_snap_line(point, max(self.width_list)-20)

	def snap_distance_check(self, item):
		self_rect = self.sceneBoundingRect()
		other_rect = item.sceneBoundingRect()
		return abs(self_rect.top() - other_rect.top()) < 15 and abs(self_rect.left() - other_rect.left()) < 45

	def snap_widget_check(self, item):
		if isinstance(item, EntryManager) or isinstance(item, SnapLine):
			return item.check_block(self)
		return False

	def get_content(self):
		pos_x = round(self.pos().x(), 3)
		pos_y = round(self.pos().y(), 3)

		res = {"category": self.input_json["category"], "internal_name": self.input_json["internal_name"],
			   "pos": [pos_x, pos_y]}

		content = []
		for widget in self.get_entry_list():
			if widget.snapped_block:
				content.append([widget.get_text(), widget.snapped_block.input_json["identifier"]])
			else: content.append([widget.get_text(), None])
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

	def despawnerize(self):
		self.create_snap_lines()
		# update pos
		scene_pos = self.mapToScene(0, 0)
		if self.input_json["meta"] == 1: self.workspace_view.var_manager.register_usage(self)
		self.input_json["pos"] = [self.pos().x(), self.pos().y()]
		self.setParentItem(None)
		self.setPos(scene_pos)
		# make a copy
		j = self.input_json.copy()
		j["identifier"] = str(uuid4())
		self.workspace_view.add_block(j, True)
		self.workspace_view.block_manager.block_list.remove(self)
		self.workspace_view.block_list.append(self)
		self.spawner = False
		self.snap_lock = False

	def get_entry_list(self):
		res = []
		for layer in self.layers_list:
			res.extend(layer.get_entry_list())
		return res

	def customBoundingRect(self):
		"""Returns bounding rect of this widget and child blocks (if any)"""
		combined_rect = self.boundingRect()  # start with own rect
		for child in self.childItems():
			if (isinstance(child, EntryManager) or isinstance(child, SnapLine)) and child.snapped_block:
				# if child widget is a block, get its customBoundingRect and combine with our own
				child_rect = child.mapRectToParent(child.snapped_block.customBoundingRect())
				combined_rect = combined_rect.united(child_rect)
		if self.shape_id == 1:  # without this, blocks with shape 1 go inside other blocks
			return QRectF(combined_rect.x(), combined_rect.y(), combined_rect.width(), combined_rect.height() + 5)
		return combined_rect

	def boundingRect(self):
		return self.path.boundingRect()

	def paint(self, painter, option, widget = None):
		painter.setRenderHint(QPainter.Antialiasing, True)
		# get colors
		bg_color = ConfigManager().get_config()["block_colors"][self.input_json["category"]]
		border_color = ConfigManager().get_config()["styles"]["text_color"]
		# configure painter
		painter.setBrush(QColor(bg_color))
		painter.setPen(QPen(QColor(border_color)))

		painter.drawPath(self.path)

	def create_path(self, points):
		path = QPainterPath()
		if points:
			path.addPolygon(points)
			path.closeSubpath()
		self.path = path

	def generate_block_points(self):
		points, self.snappable_points = generate_points(self.shape_id, max(self.width_list), self.height_list, self.between_layers_height_list)
		return QPolygonF(points)