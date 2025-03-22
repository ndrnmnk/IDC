from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


class NewObjectWindow(QWidget):
	def __init__(self, parent):
		super().__init__(parent)
		self.grid = QGridLayout()
		self.setLayout(self.grid)

		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("IDC: New object")
		self.setMinimumSize(180, 100)

		self.grid.addWidget(QLabel("Object name:"), 0, 0)
		self.grid.addWidget(QLabel("Instance of:"), 1, 0)

		self.entry = QLineEdit()
		self.entry.setPlaceholderText("Name")
		self.grid.addWidget(self.entry, 0, 1)

		self.dropdown = QComboBox()
		self.dropdown.addItems(["Class", "Function"])
		self.grid.addWidget(self.dropdown, 1, 1)

		self.add_btn = QPushButton("Add")
		self.cancel_btn = QPushButton("Cancel")

		self.add_btn.pressed.connect(self.add)
		self.cancel_btn.pressed.connect(self.deleteLater)
		self.grid.addWidget(self.add_btn, 2, 1)
		self.grid.addWidget(self.cancel_btn, 2, 0)

		self.show()

	def add(self):
		self.parent().add_item(self.entry.text(), self.dropdown.currentText())
		self.parent().ui.code_tab.all_sprites_code[self.entry.text()] = {"instance_of": self.dropdown.currentText(), "code": []}
		self.deleteLater()

