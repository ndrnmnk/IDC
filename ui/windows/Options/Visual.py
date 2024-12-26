from PyQt5.QtWidgets import QGridLayout, QLabel, QColorDialog, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend.config_manager import ConfigManager


class VisualOptions(QGridLayout):

	def __init__(self):
		super().__init__()
		self.setAlignment(Qt.AlignTop)

		label = QLabel("Category colors:")
		font = QFont("Arial", 12)
		font.setBold(True)
		label.setFont(font)

		self.addWidget(QLabel("Text color"), 0, 0)
		self.addWidget(QLabel("Background color"), 1, 0)
		self.addWidget(QLabel("Block menu BG color"), 2, 0)
		self.addWidget(QLabel("Category menu BG color"), 3, 0)
		self.addWidget(QLabel("Text field BG color"), 4, 0)
		self.addWidget(label, 5, 0)

		# add options for built-in styles
		for idx, item in enumerate(ConfigManager().get_config("styles").keys()):
			button = QPushButton('Edit')
			button.clicked.connect(lambda _, cat=item: self.open_color_dialog(cat, True))
			self.addWidget(button, idx, 1)

		# add options for categories
		for idx, category in enumerate(ConfigManager().get_blocks(0).keys(), 6):
			self.addWidget(QLabel(category), idx, 0)
			button = QPushButton('Edit')
			button.clicked.connect(lambda _, cat=category: self.open_color_dialog(cat))
			self.addWidget(button, idx, 1)

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
