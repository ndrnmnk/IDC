from PyQt5.QtGui import QBrush, QColor, QWheelEvent
from PyQt5.QtWidgets import QGraphicsRectItem

from backend import ConfigManager


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
		self.scene().update_menu_pos()