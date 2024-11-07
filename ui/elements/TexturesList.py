from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QScrollArea, QVBoxLayout
from ui.subwidgets.ListItem import ListItem
from PyQt5.QtCore import Qt

class TexturesList(QScrollArea):
	def __init__(self):
		super().__init__()
		self.setWidgetResizable(True)
		self.vbox = QVBoxLayout()
		self.vbox.setAlignment(Qt.AlignTop)
		self.vbox.setContentsMargins(0, 0, 0, 0)

		self.setLayout(self.vbox)

	def add_item(self, name, image_path, show_image_size):
		self.vbox.addWidget(ListItem(name, image_path, show_image_size))
