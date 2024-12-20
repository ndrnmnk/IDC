from ui.subwidgets.ResizableLineEdit import ResizableLineEdit
from ui.subwidgets.ResizableDropdown import ResizableDropdown
from textures.blocks.shapes import generate_points
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QPolygon, QBrush, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, pyqtSignal
import sys


class BlockBase(QWidget):
	sizeChanged = pyqtSignal()

	def __init__(self, input_json, internal_name, color="#0000FF", shape=0):
		super().__init__()
		# save the data
		self.color = color
		self.shape = shape
		self.input_json = input_json
		self.internal_name = internal_name
		# fix visuals
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.font = QFont("Arial", 12)
		self.font_metrics = QFontMetrics(self.font)

		self.points, x1, y1, x2, y2 = generate_points(shape, 10,  24)

		self.width_list = []
		self.content_list = []
		self.height_list = []

		self.hbox = QHBoxLayout()

		self.hbox.setContentsMargins(x1, y1, x2, y2)
		self.hbox.setSpacing(5)
		self.setLayout(self.hbox)

		self.populate_block()

	def populate_block(self):
		for idx, json_object in enumerate(self.input_json):
			if "text" in json_object:
				self.content_list.append(QLabel(json_object["text"], self))
				self.content_list[idx].setFont(self.font)
				self.width_list.append(self.font_metrics.horizontalAdvance(json_object["text"]))
				self.height_list.append(self.font_metrics.height())
			elif "text_entry" in json_object:
				self.content_list.append(ResizableLineEdit(parent=self, placeholder=json_object["text_entry"], int_entry=False))
				self.content_list[idx].textChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
				self.width_list.append(self.content_list[idx].width())
				self.height_list.append(22)
			elif "int_entry" in json_object:
				self.content_list.append(ResizableLineEdit(parent=self, placeholder=json_object["int_entry"], int_entry=True))
				self.content_list[idx].textChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
				self.width_list.append(self.content_list[idx].width())
				self.height_list.append(22)
			elif "bool_entry" in json_object:
				# TODO: replace with actual bool entry
				self.content_list.append(ResizableLineEdit(parent=self, placeholder=json_object["bool_entry"], int_entry=True))
				self.content_list[idx].textChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
				self.width_list.append(self.content_list[idx].width())
				self.height_list.append(22)
			elif "dropdown" in json_object:
				self.content_list.append(ResizableDropdown(parent=self, options=json_object["dropdown"]))
				self.content_list[idx].currentIndexChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
				self.width_list.append(self.content_list[idx].width())
				self.height_list.append(24)
			self.hbox.addWidget(self.content_list[idx], alignment=Qt.AlignLeft)

	def repopulate_block(self, caller_idx):
		self.width_list[caller_idx] = self.content_list[caller_idx].width()
		self.height_list[caller_idx] = self.content_list[caller_idx].height()
		self.update()
		self.adjustSize()
		self.sizeChanged.emit()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.sizeChanged.emit()  # Emit signal on resize event

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.HighQualityAntialiasing)

		points = self.generate_polygon_points()

		painter.setBrush(QBrush(QColor(self.color)))
		polygon = QPolygon(points)
		painter.drawPolygon(polygon)

	def generate_polygon_points(self):
		width = sum(self.width_list) + 6*len(self.width_list)
		height = max(self.height_list) + 6
		return generate_points(self.shape, width, height)[0]

	def get_internal_name(self):
		return self.internal_name


if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication(sys.argv)

	test_json = [
		{"text": "Hello, World"},
		{"dropdown": ["hello", "bye", "this is a very long one"]},
		{"int_entry": "number typing?"},
		{"text": "test!"},
		{"text_entry": "text entry"}
	]

	window = BlockBase(test_json, "test", "#00ff00", 1)
	window.show()
	app.exec_()
