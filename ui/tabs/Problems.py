from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QApplication
from PyQt5.QtGui import QIcon


class ProblemsTabWidget(QListWidget):
	def __init__(self):
		super().__init__()
		self.icon_warning = self.style().standardIcon(QApplication.style().SP_MessageBoxWarning)
		self.icon_error = self.style().standardIcon(QApplication.style().SP_MessageBoxCritical)

	def add_item(self, icon_type, text):
		if icon_type == 0:
			self.addItem(QListWidgetItem(self.icon_warning, text))
		else:
			self.addItem(QListWidgetItem(self.icon_error, text))
