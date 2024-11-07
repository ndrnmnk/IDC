from PyQt5.QtWidgets import QLabel, QGridLayout
from ui.elements.TexturesList import TexturesList


class SoundsTabLayout(QGridLayout):
	def __init__(self):
		super().__init__()

		self.sounds_list = TexturesList()

		placeholder_label = QLabel("edit here")
		placeholder_label.setStyleSheet('background-color: purple;')

		self.setColumnStretch(0, 0)
		self.setColumnStretch(1, 1)
		self.setColumnMinimumWidth(0, 90)

		self.addWidget(self.sounds_list, 0, 0)
		self.addWidget(placeholder_label, 0, 1)

	def add_sound(self, name, sound_path):
		self.sounds_list.add_item(name, "textures/sound.png", False)
