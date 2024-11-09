from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon


class ProblemsTabWidget(QListWidget):
	def __init__(self):
		super().__init__()
		self.icon_warning = QIcon("textures/images/warning.png")
		self.icon_error = QIcon("textures/images/error.png")

	def add_item(self, icon_type, text):
		if icon_type == 0:
			self.addItem(QListWidgetItem(self.icon_warning, text))
		else:
			self.addItem(QListWidgetItem(self.icon_error, text))
