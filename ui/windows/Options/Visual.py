from PyQt5.QtWidgets import QGridLayout, QLabel, QColorDialog, QPushButton, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend import ConfigManager


class VisualOptions(QWidget):

	def __init__(self):
		super().__init__()
		self.grid = QGridLayout()
		self.grid.setAlignment(Qt.AlignTop)
		self.setLayout(self.grid)

		label = QLabel("Category colors:")
		font = QFont("Arial", 12)
		font.setBold(True)
		label.setFont(font)

		self.grid.addWidget(QLabel("Text color"), 0, 0)
		self.grid.addWidget(QLabel("Background color"), 1, 0)
		self.grid.addWidget(QLabel("Block menu BG color"), 2, 0)
		self.grid.addWidget(QLabel("Category menu BG color"), 3, 0)
		self.grid.addWidget(QLabel("Text field BG color"), 4, 0)
		self.grid.addWidget(QLabel("Snap preview color"), 5, 0)
		self.grid.addWidget(label, 6, 0)

		# add options for built-in styles
		for idx, item in enumerate(ConfigManager().get_config()["styles"].keys()):
			button = QPushButton('Edit')
			button.clicked.connect(lambda _, cat=item: self.open_color_dialog(cat, True))
			self.grid.addWidget(button, idx, 1)

		# add options for categories
		for idx, category in enumerate(ConfigManager().get_blocks().keys(), 7):
			self.grid.addWidget(QLabel(category), idx, 0)
			button = QPushButton('Edit')
			button.clicked.connect(lambda _, cat=category: self.open_color_dialog(cat))
			self.grid.addWidget(button, idx, 1)

	@staticmethod
	def open_color_dialog(category, styles=False):
		# open the QColorDialog
		color = QColorDialog.getColor()
		# if user selected a color, save it
		if color.isValid():
			if not styles:
				ConfigManager().set(["block_colors", category], color.name())
			else:
				ConfigManager().set(["styles", category], color.name())
