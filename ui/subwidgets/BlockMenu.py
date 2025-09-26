from PyQt5.QtGui import QBrush, QColor, QWheelEvent, QPainterPath
from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtCore import QRectF

from backend import ConfigManager


class BlockMenu(QGraphicsRectItem):
	def __init__(self, width=300, scene_height=10000):
		super().__init__(0, 0, width, scene_height)
		self.setFlag(QGraphicsRectItem.ItemClipsToShape, True)
		self.setFlag(QGraphicsRectItem.ItemClipsChildrenToShape, True)
		self.setBrush(QBrush(QColor(ConfigManager().get_config()["styles"]["block_menu_bg"])))
		self.setZValue(1)

		self.offset = 0
		self.max_offset = 0
		self.view_height = 0

	def wheelEvent(self, event: QWheelEvent):
		# Determine the scroll direction
		self.clipPath()
		self.offset += event.delta()
		self.offset = max(self.view_height-self.max_offset, self.offset)  # bottom limit
		self.offset = min(0, self.offset)  # top limit

		event.accept()  # Prevent event propagation
		self.scene().update_menu_pos()

	def shape(self):
		# make a rect to trim the rectangle
		path = QPainterPath()
		rect = QRectF(0, -self.offset, 300, self.view_height)
		path.addRect(rect)
		return path

	def paint(self, painter, option, widget = ...):
		painter.setClipping(True)
		super().paint(painter, option, widget)

	def mousePressEvent(self, event):
		# to make event not pass to blocks below
		event.accept()

	def contextMenuEvent(self, event):
		# to make event not pass to blocks below
		event.accept()