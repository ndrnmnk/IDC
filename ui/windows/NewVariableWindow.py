from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt


class NewVariableWindow(QWidget):
	def __init__(self, parent):
		super().__init__(parent.parent)
		self.grid = QGridLayout()
		self.parent = parent
		self.setLayout(self.grid)

		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("IDC: New variable")
		self.setMinimumSize(180, 100)

		self.grid.addWidget(QLabel("Variable name:"), 0, 0)
		self.grid.addWidget(QLabel("Type:"), 1, 0)
		self.grid.addWidget(QLabel("Is global"), 2, 0)

		self.entry = QLineEdit()
		self.entry.setPlaceholderText("Name")
		self.grid.addWidget(self.entry, 0, 1)

		self.dropdown = QComboBox()
		self.dropdown.addItems(["Integer", "String", "Boolean"])
		self.grid.addWidget(self.dropdown, 1, 1)

		self.global_checkbox = QCheckBox()
		self.grid.addWidget(self.global_checkbox, 2, 1)

		self.add_btn = QPushButton("Add")
		self.cancel_btn = QPushButton("Cancel")

		self.add_btn.pressed.connect(self.add)
		self.cancel_btn.pressed.connect(self.deleteLater)
		self.grid.addWidget(self.add_btn, 3, 1)
		self.grid.addWidget(self.cancel_btn, 3, 0)

		self.show()

	def add(self):
		sprite = None if self.global_checkbox.isChecked() else self.parent.sprite_manager.current_sprite
		self.parent.var_manager.add_var(self.entry.text(), self.dropdown.currentText(), sprite)
		self.parent.on_new_category("Variables")
		self.deleteLater()
