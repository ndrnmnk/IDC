from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt


class NewFunctionWindow(QWidget):
	def __init__(self, parent):
		super().__init__(parent.parent)
		self.grid = QGridLayout()
		self.parent = parent
		self.setLayout(self.grid)

		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("IDC: New function")
		self.setMinimumSize(180, 100)

		self.grid.addWidget(QLabel("Function name:"), 0, 0)
		self.grid.addWidget(QLabel("Is static:"), 1, 0)

		self.entry = QLineEdit()
		self.entry.setPlaceholderText("Name")
		self.grid.addWidget(self.entry, 0, 1)

		self.static_cb = QCheckBox()
		self.grid.addWidget(self.static_cb, 1, 1)

		self.add_btn = QPushButton("Add")
		self.cancel_btn = QPushButton("Cancel")

		self.add_btn.pressed.connect(self.add)
		self.cancel_btn.pressed.connect(self.deleteLater)
		self.grid.addWidget(self.add_btn, 2, 1)
		self.grid.addWidget(self.cancel_btn, 2, 0)

		self.show()

	def add(self):
		self.parent.on_new_category("Functions")
		self.deleteLater()
