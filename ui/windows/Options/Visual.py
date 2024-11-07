from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class VisualOptions(QVBoxLayout):
	def __init__(self):
		super().__init__()
		self.setAlignment(Qt.AlignTop)
		self.addWidget(QLabel("go touch grass"))