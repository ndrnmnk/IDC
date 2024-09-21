from PyQt5.QtWidgets import QLabel, QGridLayout
from ui.elements.TexturesList import TexturesList


def create_textures_tab():
    textures_tab_layout = QGridLayout()

    textures_list = TexturesList()

    label3 = QLabel("edit here")
    label3.setStyleSheet('background-color: lightgreen;')
    textures_tab_layout.setColumnStretch(0, 0)
    textures_tab_layout.setColumnMinimumWidth(0, 90)
    textures_tab_layout.setColumnStretch(1, 1)
    textures_tab_layout.addWidget(textures_list, 0, 0)
    textures_tab_layout.addWidget(label3, 0, 1)
    return textures_tab_layout
