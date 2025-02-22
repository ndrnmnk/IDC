from PyQt5.QtWidgets import QGraphicsWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtCore import pyqtSignal
from backend.config_manager import ConfigManager


class SnapLine(QGraphicsWidget):
	sizeChanged = pyqtSignal()

	def __init__(self, pos, width, parent=None):
		super().__init__(parent)
		self.width = width
		self.snapped_block = None
		self.setPos(pos)
		self.setZValue(3)
		self.setMaximumSize(width, 5)
		self.visible = False

	def clear_line(self):
		self.visible = False
		self.update()
		self.parentItem().update()

	def show_line(self):
		self.parentItem().update()
		self.visible = True
		self.update()

	def snap_in(self, widget):
		if self.snapped_block:
			old_widget = self.snapped_block
			self.snapped_block.unsnap()
			if widget.shape_index != 1 or widget.snap_line_list:
				old_widget.snap_candidate = widget.snap_line_list[0]
				old_widget.try_to_snap()
		self.snapped_block = widget
		self.snapped_block.sizeChanged.connect(self.sizeChanged.emit)

	def unsnap(self):
		self.snapped_block.sizeChanged.disconnect()
		self.snapped_block = None
		self.sizeChanged.emit()

	def get_height(self):
		if self.snapped_block:
			rect = self.snapped_block.customBoundingRect()
			return rect.height() - 5
		return 18

	def change_width(self, width):
		self.width = width
		self.update()

	def paint(self, painter, option, widget=None):
		if not self.visible:
			return

		color = QColor(ConfigManager().get_config()["styles"]["preview_line_color"])
		painter.setRenderHint(QPainter.HighQualityAntialiasing)
		pen = QPen(color, 3, Qt.SolidLine)
		painter.setPen(pen)

		points = [
			QPointF(0, 0),
			QPointF(10, 0),
			QPointF(10, 5),
			QPointF(40, 5),
			QPointF(40, 0),
			QPointF(self.width, 0),
		]

		painter.drawPolyline(*points)