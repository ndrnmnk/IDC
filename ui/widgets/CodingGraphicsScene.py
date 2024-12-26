from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsItem, QScrollBar, QGraphicsProxyWidget
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt

from ui.widgets.DraggableBlock import DraggableBlock
from ui.widgets.BlockSelectionMenu import BlockSelectionMenu
from backend.config_manager import ConfigManager


class BlockMenu(QGraphicsRectItem):
	def __init__(self, height, parent):
		super().__init__(0, 0, 300, height)
		self.parent = parent
		self.width = 300
		self.y_offset = 0
		self.lowest_block_pos = 0
		self.bottom_limit = 0
		self.smh = self.parent.get_selector_menu_height()
		self.setBrush(QBrush(QColor(ConfigManager().get_config('styles')['block_menu_bg'])))
		self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
		self.setZValue(4)
		self.show()

		# Create a scrollbar
		self.scrollbar = QScrollBar(Qt.Vertical)
		self.scrollbar.setStyleSheet(f"background-color: {ConfigManager().get_config('styles')['block_menu_bg']}; ")
		self.scrollbar.setSingleStep(20)  # Adjust step size
		self.scrollbar.setMinimum(0)
		self.scrollbar.setPageStep(100)
		self.scrollbar.setVisible(True)
		self.scrollbar.valueChanged.connect(self.on_scrollbar_moved)
		self.scrollbar.setFixedHeight(300)

		# Embed the scrollbar into the scene
		self.scrollbar_proxy = QGraphicsProxyWidget(self)
		self.scrollbar_proxy.setWidget(self.scrollbar)
		self.scrollbar_proxy.setZValue(100)
		self.scrollbar_proxy.show()
		self.update_scrollbar_position()

	def update_scrollbar_position(self):
		"""Adjust the scrollbar's position to match the BlockMenu's visible area."""
		self.scrollbar_proxy.setPos(int(self.pos().x() + self.width - 15), int(self.pos().y() + self.smh - self.y_offset))

	def update_range(self):
		"""Update the range based on the content."""
		self.bottom_limit = self.parent.get_selector_menu_height() - self.lowest_block_pos
		self.scrollbar.setMaximum(int(-self.bottom_limit))

	def on_scrollbar_moved(self, value):
		"""Move the menu content when the scrollbar is moved."""
		new_y_offset = -value
		self.moveBy(0, new_y_offset - self.y_offset)
		self.y_offset = new_y_offset

	def wheelEvent(self, event):
		"""Scroll using mouse wheel"""
		delta = event.delta()
		if delta > 0:
			if self.bottom_limit == 0:
				self.update_range()
			if self.y_offset > self.bottom_limit:
				self.y_offset -= 20
				self.moveBy(0, -20)
		else:
			if self.y_offset < 0:
				self.y_offset += 20
				self.moveBy(0, 20)
		self.scrollbar.setValue(int(-self.y_offset))

		def on_category_changed(self):
			self.bottom_limit = 0
			self.moveBy(0, -self.y_offset)
			self.y_offset = 0

	def on_category_changed(self):
		"""Reset the scrollbar and position when the category changes."""
		self.bottom_limit = 0
		self.moveBy(0, -self.y_offset)
		self.y_offset = 0
		self.scrollbar.setValue(0)


class WorkspaceScene(QGraphicsScene):
	def __init__(self, parent_view):
		super().__init__()
		self.parent_view = parent_view
		self.category_selector = BlockSelectionMenu(parent_view, self.generate_categories())
		self.addItem(self.category_selector)
		self.category_selector.setPos(0, 0)
		self.menu = BlockMenu(10000, self)
		self.addItem(self.menu.scrollbar_proxy)
		self.addItem(self.menu)

	def generate_categories(self):
		res = []
		keys = list(self.parent_view.json.keys())
		for category in keys:
			try:
				res.append([category, self.parent_view.color_json[category]])
			except KeyError:
				res.append([category, "#ffffff"])
		return res

	def get_selector_menu_height(self):
		return self.category_selector.size().height()

	def update_menu_pos(self, view_rect):
		self.menu.setPos(view_rect.left(), view_rect.top() + self.menu.y_offset)
		self.category_selector.setPos(view_rect.left(), view_rect.top())
		self.menu.update_scrollbar_position()

	def block_placed_in_menu(self, block):
		if block.pos().x() + 20 < self.menu.width + self.menu.pos().x():
			return True
		return False


class WorkspaceView(QGraphicsView):
	def __init__(self):
		super().__init__()
		self.json = ConfigManager().get_blocks(0)
		self.color_json = ConfigManager().get_config("block_colors")
		self.scene_widget = WorkspaceScene(self)
		self.setScene(self.scene_widget)
		self.scene_widget.setSceneRect(0, 0, 10000, 10000)
		self.centerOn(0, 0)
		self.regular_blocks_array = []
		self.menu_blocks_array = []
		self.add_blocks(list(self.json.keys())[0])

	def drawForeground(self, painter, rect):
		# Use the visible rect of the view, which is stable during dragging
		view_rect = self.mapToScene(self.viewport().rect()).boundingRect()
		self.scene_widget.update_menu_pos(view_rect)

	def add_blocks(self, category):
		try:
			color = self.color_json[category]
		except KeyError:
			color = "#ffffff"
		for key in self.json[category].keys():
			if self.menu_blocks_array:
				block_pos = [10, self.menu_blocks_array[-1].sceneBoundingRect().bottom()+10]
			else:
				block_pos = [10, self.scene().get_selector_menu_height() + 10]
			block_data = self.json[category][key]
			block_data["pos"] = block_pos
			block_data["internal_name"] = key
			block_data["color"] = color
			self.add_block(block_data, block_pos, menu=True)
		self.scene().menu.lowest_block_pos = block_pos[1] - self.menu_blocks_array[-1].get_height() + 20
		self.scene().menu.update_range()

	def add_block(self, block_data, pos=None, menu=False):

		t = DraggableBlock(block_data, self, menu)
		self.scene().addItem(t)
		if menu:
			t.setParentItem(self.scene_widget.menu)
			t.setZValue(5)
			self.menu_blocks_array.append(t)
		else:
			self.regular_blocks_array.append(t)

	def on_new_category(self, category):
		for block in self.menu_blocks_array[:]:
			block.suicide()
		self.menu_blocks_array.clear()
		self.scene().menu.on_category_changed()
		self.add_blocks(category)
