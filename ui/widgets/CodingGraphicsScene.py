from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem, QScrollBar, QGraphicsProxyWidget
from PyQt5.QtGui import QBrush, QColor, QWheelEvent
from PyQt5.QtCore import Qt
from ui.widgets.Block import Block
from ui.widgets.BlockSelectionMenu import BlockSelectionMenu
from backend.config_manager import ConfigManager


class BlockMenu(QGraphicsRectItem):
	def __init__(self, width=300, scene_height=10000):
		super().__init__(0, 0, width, scene_height)
		self.setBrush(QBrush(QColor(ConfigManager().get_config()["styles"]["block_menu_bg"])))
		self.setZValue(1)

		self.offset = 0
		self.max_offset = 0
		self.view_height = 0

	def wheelEvent(self, event: QWheelEvent):
		# Determine the scroll direction
		self.offset += event.delta()
		self.offset = max(self.view_height-self.max_offset, self.offset)  # bottom limit
		self.offset = min(0, self.offset)  # top limit

		event.accept()  # Prevent event propagation
		self.scene().view.updateMenuPos()


class CodingGraphicsScene(QGraphicsScene):
	def __init__(self, parent_view):
		super().__init__()
		self.view = parent_view
		self.setSceneRect(0, 0, 10000, 10000)

		self.menu = BlockMenu()
		self.addItem(self.menu)

		self.selector = BlockSelectionMenu(self.view, list(ConfigManager().get_config()["block_colors"].items()))
		self.addItem(self.selector)

		self.menu_scrollbar = QGraphicsProxyWidget()
		self.scrollbar_menu = QScrollBar(Qt.Vertical)
		self.scrollbar_menu.setStyleSheet(f"background-color: {ConfigManager().get_config()['styles']['block_menu_bg']}")
		self.scrollbar_menu.setRange(0, 0)
		self.menu_scrollbar.setWidget(self.scrollbar_menu)
		self.scrollbar_menu.valueChanged.connect(self.view.on_scrollbar_changed)
		self.addItem(self.menu_scrollbar)
		self.menu_scrollbar.setZValue(1)


class WorkspaceView(QGraphicsView):
	def __init__(self):
		super().__init__()
		scene = CodingGraphicsScene(self)
		self.setScene(scene)
		self.centerOn(0, 0)
		self.block_list = []
		self.menu_block_list = []
		self.scene().menu.view_height = self.viewport().height()

	def load_block_menu(self, category):
		# load configs
		menu_blocks_list = ConfigManager().get_blocks()[category]

		# get a starting position
		t = int(self.scene().selector.boundingRect().height()) + 10
		# populate
		for key in menu_blocks_list:  # for key in json
			block_json = self.compile_block_json(menu_blocks_list[key], category, key, [10, t])
			t += self.add_block(block_json, True) + 20
		self.scene().menu.max_offset = int(t)
		self.scene().menu.offset = 0
		# update scrollbar range
		scroll_range = max(0, int(t) - self.viewport().height())
		self.scene().scrollbar_menu.setRange(0, scroll_range)
		self.scene().scrollbar_menu.setPageStep(self.viewport().height())
		self.scene().scrollbar_menu.setValue(0)

		self.updateMenuPos()

	@staticmethod
	def compile_block_json(base, category, internal_name, pos):
		res = base
		res["category"] = category
		res["internal_name"] = internal_name
		res["pos"] = pos
		return res

	def add_block(self, block_json, spawner):
		if spawner:
			self.menu_block_list.append(Block(self, block_json, True))
			self.scene().addItem(self.menu_block_list[-1])
			self.menu_block_list[-1].setPos(*block_json["pos"])
			self.menu_block_list[-1].setParentItem(self.scene().menu)
			return self.menu_block_list[-1].boundingRect().height()
		else:
			self.block_list.append(Block(self, block_json, False))
			self.scene().addItem(self.block_list[-1])
			self.block_list[-1].setPos(*block_json["pos"])
			return self.block_list[-1]

	def check_block_for_deletion(self, caller):
		if caller.pos().x() + 20 < self.scene().menu.sceneBoundingRect().right():
			caller.suicide()

	def on_new_category(self, category):
		self.clear_menu()
		self.load_block_menu(category)

	def on_scrollbar_changed(self, value):
		# Invert the scrollbar value so that 0 means offset=0 (menu at top)
		self.scene().menu.offset = -value
		self.updateMenuPos()

	def clear_menu(self):
		for block in self.menu_block_list[:]:
			block.suicide()

	def updateMenuPos(self):
		try:
			# Convert the top-left corner of the viewport (0,0) to scene coordinates
			top_left_scene = self.mapToScene(0, 0)
			# Position the rectangle at that point
			self.scene().menu.setPos(top_left_scene.x(), top_left_scene.y()+self.scene().menu.offset)
			self.scene().selector.setPos(top_left_scene)
			self.scene().menu_scrollbar.setPos(top_left_scene.x()+285, top_left_scene.y()+int(self.scene().selector.boundingRect().height()))

			# sync scrollbar and menu scroll
			self.scene().scrollbar_menu.blockSignals(True)
			self.scene().scrollbar_menu.setValue(-self.scene().menu.offset)
			self.scene().scrollbar_menu.blockSignals(False)
		except Exception as e:
			print(e)
			print("smt weird happened with menu pos, ignoring")

	def scrollContentsBy(self, dx, dy):
		# First, perform the default scroll behavior
		super().scrollContentsBy(dx, dy)
		# Then, reposition the rectangle so it stays in the top left of the visible area
		self.updateMenuPos()

	def resizeEvent(self, event):
		# Also update position when the view is resized
		super().resizeEvent(event)
		self.scene().menu.view_height = self.viewport().height()
		self.scene().scrollbar_menu.setFixedSize(15, self.viewport().height()-int(self.scene().selector.boundingRect().height()))

		# Update scrollbar range
		scroll_range = max(0, self.scene().menu.max_offset - self.scene().menu.view_height)
		self.scene().scrollbar_menu.setRange(0, scroll_range)
		self.scene().scrollbar_menu.setPageStep(self.scene().menu.view_height)

		self.updateMenuPos()

	def get_data(self, return_all=False):
		"""Returns block data for saving(return_all=1) or compiling(return_all=0)"""
		res = []
		if not return_all:
			for block in self.block_list:
				if block.shape_index == 2:
					res.append(block.get_content())
		else:
			for block in self.block_list:
				if not block.snap:
					res.append(block.get_content())
		return res

	def load_project(self, project_json, parent_block=None):
		for idx, json_item in enumerate(project_json):
			if isinstance(json_item, dict):
				# create a new json for a block
				new_json = ConfigManager().get_blocks()[json_item["category"]][json_item["internal_name"]]
				new_json = self.compile_block_json(new_json, json_item["category"], json_item["internal_name"], json_item["pos"])
				# create new block
				block = self.add_block(new_json, False)
				if parent_block:
					if new_json["shape"] in (0, 1):
						block.snap_candidate = parent_block.snap_line_list[idx]
					if new_json["shape"] in (3, 4):
						block.snap_candidate = parent_block.get_entry_list()[idx]
						print(block.snap_candidate)
					block.try_to_snap()
				entry_list = block.get_entry_list()
				for i, var in enumerate(json_item["content"]):
					entry_list[i].set_text(var[0][0])
				self.load_project([x[1] for x in json_item["content"]], block)
				self.load_project(json_item["snaps"], block)
