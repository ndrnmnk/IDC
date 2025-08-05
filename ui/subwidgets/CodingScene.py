from PyQt5.QtWidgets import QGraphicsScene, QScrollBar, QGraphicsProxyWidget
from PyQt5.QtCore import Qt

from backend.config_manager import ConfigManager
from ui.subwidgets.BlockCategorySelectionMenu import BlockCategorySelectionMenu
from ui.subwidgets.BlockMenu import BlockMenu


class CodingScene(QGraphicsScene):
	def __init__(self, parent_view):
		super().__init__()
		self.view = parent_view
		self.setSceneRect(0, 0, 10000, 10000)

		self.menu = BlockMenu()
		self.addItem(self.menu)

		self.selector = BlockCategorySelectionMenu(self.view, list(ConfigManager().get_config()["block_colors"].items()))
		self.addItem(self.selector)

		self.menu_scrollbar_proxy = QGraphicsProxyWidget()
		self.menu_scrollbar = QScrollBar(Qt.Vertical)
		self.menu_scrollbar.setStyleSheet(f"background-color: {ConfigManager().get_config()['styles']['block_menu_bg']}")
		self.menu_scrollbar.setRange(0, 0)
		self.menu_scrollbar_proxy.setWidget(self.menu_scrollbar)
		self.menu_scrollbar.valueChanged.connect(self.on_scrollbar_changed)
		self.addItem(self.menu_scrollbar_proxy)
		self.menu_scrollbar_proxy.setZValue(1)

	def on_new_category(self, offset):
		self.menu.max_offset = offset
		self.menu.offset = 0
		viewport_h =  self.view.viewport().height()
		scroll_range = max(0, offset - viewport_h)
		self.menu_scrollbar.setRange(0, scroll_range)
		self.menu_scrollbar.setPageStep(viewport_h)
		self.menu_scrollbar.setValue(0)

		self.update_menu_pos()

	def on_scrollbar_changed(self, value):
		self.menu.offset = -value
		self.update_menu_pos()

	def on_view_resize(self):
		viewport_h = self.view.viewport().height()
		self.menu.view_height = viewport_h
		self.menu_scrollbar.setFixedSize(15, viewport_h-int(self.selector.boundingRect().height()))

		# Update scrollbar range
		scroll_range = max(0, self.menu.max_offset - self.menu.view_height)
		self.menu_scrollbar.setRange(0, scroll_range)
		self.menu_scrollbar.setPageStep(self.menu.view_height)

		self.update_menu_pos()

	def update_menu_pos(self):
		try:
			# Convert the top-left corner of the viewport (0,0) to scene coordinates
			top_left_viewport = self.view.mapToScene(0, 0)
			# Position the rectangle at that point
			self.menu.setPos(top_left_viewport.x(), top_left_viewport.y()+self.menu.offset)
			self.selector.setPos(top_left_viewport)
			self.menu_scrollbar_proxy.setPos(top_left_viewport.x()+285, top_left_viewport.y()+int(self.selector.boundingRect().height()))

			# sync scrollbar and menu scroll
			self.menu_scrollbar.blockSignals(True)
			self.menu_scrollbar.setValue(-self.menu.offset)
			self.menu_scrollbar.blockSignals(False)
		except Exception as e:
			print(e)
			print("smt weird happened with menu pos, ignoring")
