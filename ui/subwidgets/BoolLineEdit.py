from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QRegularExpressionValidator, QPainter, QColor, QFont, QFontMetrics, QPen, QPolygonF
from PyQt5.QtCore import QRegularExpression, Qt, pyqtSignal
from backend.shapes import generate_points
from backend.config_manager import ConfigManager


class BoolLineEdit(QLineEdit):
	size_changed = pyqtSignal()

	def __init__(self, placeholder_text, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setPlaceholderText(placeholder_text)
		self.font = QFont("Arial, 12")
		self.setFont(self.font)
		self.font_metrics = QFontMetrics(self.font)
		self.border_color = "#000000"
		bg = ConfigManager().get_config()["styles"]["text_field_bg"]
		self.setStyleSheet(f"""
			QLineEdit {{
				border: none;
				color: black;
				background-color: {bg};
			}}
		""")
		self.setFixedHeight(22)
		self.setContentsMargins(10, 2, 10, 2)
		self.setTextMargins(2, 0, 0, 0)
		self.border_width = 2
		self.update_width()

		self.setMaxLength(1)
		pattern = r'^[0|1]*$'  # Only 1 or 0
		regex = QRegularExpression(pattern)
		validator = QRegularExpressionValidator(regex, self)
		self.setValidator(validator)

		self.textChanged.connect(self.update_width)

	def update_width(self):
		# Get the width of the text or placeholder text
		text_width = self.font_metrics.horizontalAdvance(self.text() or self.placeholderText())

		padding = 24 + self.border_width

		# Resize the widget to fit the text width
		self.setFixedWidth(max(text_width + padding, 36))
		self.size_changed.emit()

	def set_border_width(self, width=2, use_preview_color=False):
		self.border_width = width
		if use_preview_color:
			self.border_color = ConfigManager().get_config()["styles"]["snapline_color"]
		else:
			self.border_color = "#000000"
		self.repaint()

	def paintEvent(self, a0):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.HighQualityAntialiasing)

		pen = QPen(QColor(self.border_color))
		pen.setWidth(self.border_width)  # Outline thickness
		painter.setPen(pen)

		bg = ConfigManager().get_config()["styles"]["text_field_bg"]
		painter.setBrush(QColor(bg))
		points = generate_points(3, self.width(), [22], [0])[0]
		polygon = QPolygonF(points)
		painter.drawPolygon(polygon)
		painter.end()
		super().paintEvent(a0)


if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
	import sys
	app = QApplication(sys.argv)
	view = QGraphicsView()
	scene = QGraphicsScene()
	proxy = QGraphicsProxyWidget()
	lineedit = BoolLineEdit("hello world")

	proxy.setWidget(lineedit)
	scene.addItem(proxy)
	view.setScene(scene)
	proxy.setPos(100, 100)
	view.show()
	window = view

	sys.exit(app.exec_())

