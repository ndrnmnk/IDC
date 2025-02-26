from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt


class CompilerOptions(QWidget):
	def __init__(self):
		super().__init__()
		vbox = QVBoxLayout()
		vbox.setAlignment(Qt.AlignTop)
		self.setLayout(vbox)

		vbox.addWidget(QLabel("This is compiler options page"))
