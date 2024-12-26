from PyQt5.QtWidgets import QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class CompilerOptions(QVBoxLayout):
	def __init__(self, ui):
		super().__init__()
		self.setAlignment(Qt.AlignTop)
		self.addWidget(QLabel("why does it lag"))
