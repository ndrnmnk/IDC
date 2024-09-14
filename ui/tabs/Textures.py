from PyQt5.QtWidgets import QLabel, QGridLayout


def create_textures_tab():
    textures_tab_layout = QGridLayout()
    label2 = QLabel("Skins or models list")
    label3 = QLabel("edit here")
    label2.setStyleSheet('background-color: yellow;')
    label3.setStyleSheet('background-color: lightgreen;')
    textures_tab_layout.setColumnStretch(0, 1)
    textures_tab_layout.setColumnStretch(1, 4)
    textures_tab_layout.addWidget(label2, 0, 0)
    textures_tab_layout.addWidget(label3, 0, 1)
    return textures_tab_layout
