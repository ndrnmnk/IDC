from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget
from PyQt5.QtCore import Qt
from ui.windows.Options.Visual import VisualOptions
from ui.windows.Options.Compilers import CompilerOptions
from ui.windows.Options.General import GeneralOptions


class AddonsOptionsWidget(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		layout = self.options_display = self.parent().parent().addons_manager.get_options()
		self.setLayout(layout)


class OptionsWindow(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("IDC: Options")
		self.setMinimumSize(360, 360)

		self.main_hbox = QHBoxLayout(self)
		self.setLayout(self.main_hbox)

		# Create navigation list
		self.menu = QListWidget()
		self.menu.setFixedWidth(100)
		self.menu.addItem(QListWidgetItem("General"))
		self.menu.addItem(QListWidgetItem("Visual"))
		self.menu.addItem(QListWidgetItem("Compilation"))
		self.menu.addItem(QListWidgetItem("Addons"))
		self.main_hbox.addWidget(self.menu)

		self.stacked_widget = QStackedWidget()
		self.main_hbox.addWidget(self.stacked_widget)

		# Connect signal to change displayed page
		self.menu.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

		# Create and add the different option pages
		self.general_page = GeneralOptions()
		self.visual_page = VisualOptions()
		self.compiler_page = CompilerOptions()
		self.addons_page = AddonsOptionsWidget(self)

		self.stacked_widget.addWidget(self.general_page)
		self.stacked_widget.addWidget(self.visual_page)
		self.stacked_widget.addWidget(self.compiler_page)
		self.stacked_widget.addWidget(self.addons_page)

		self.stacked_widget.setCurrentIndex(0)

		self.show()
