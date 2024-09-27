from PyQt5.QtWidgets import QLabel, QGridLayout
from ui.elements.TexturesList import TexturesList


class TexturesTabLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        textures_list = TexturesList()

        placeholder_label = QLabel("edit textures here")
        placeholder_label.setStyleSheet('background-color: lightgreen;')
        self.setColumnStretch(0, 0)
        self.setColumnMinimumWidth(0, 90)

        self.setColumnStretch(1, 1)

        self.addWidget(textures_list, 0, 0)
        self.addWidget(placeholder_label, 0, 1)
