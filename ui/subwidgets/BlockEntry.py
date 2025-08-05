from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygonF
from PyQt5.QtCore import pyqtSignal, QPointF, Qt
from backend.shapes import generate_points
from backend.config_manager import ConfigManager


class BlockEntry(QWidget):
	size_changed = pyqtSignal()

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setFixedWidth(56)
		self.setFixedHeight(22)
		self.border_color = "#000000"
		self.border_width = 2

	def set_border_width(self, width=2, use_preview_color=False):
		self.border_width = width
		if use_preview_color:
			self.border_color = ConfigManager().get_config()["styles"]["snapline_color"]
		else:
			self.border_color = "#000000"
		self.update()

	def paintEvent(self, a0):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.HighQualityAntialiasing)

		pen = QPen(QColor(self.border_color))
		pen.setWidth(self.border_width)  # Outline thickness
		painter.setPen(pen)

		bg = ConfigManager().get_config()["styles"]["text_field_bg"]
		painter.setBrush(QColor(bg))
		points = generate_points(0, self.width(), [16], [0])[0]
		points = [QPointF(p.x()*0.95+1, p.y()*0.95+1) for p in points]
		polygon = QPolygonF(points)
		painter.drawPolygon(polygon)
		painter.end()
		super().paintEvent(a0)