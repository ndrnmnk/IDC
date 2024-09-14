from PyQt5.QtWidgets import QLabel, QGridLayout


def create_sounds_tab():
    sounds_tab_layout = QGridLayout()
    label4 = QLabel("Sounds list")
    label5 = QLabel("edit here")
    label4.setStyleSheet('background-color: lightblue;')
    label5.setStyleSheet('background-color: purple;')
    sounds_tab_layout.setColumnStretch(0, 1)
    sounds_tab_layout.setColumnStretch(1, 4)
    sounds_tab_layout.addWidget(label4, 0, 0)
    sounds_tab_layout.addWidget(label5, 0, 1)
    return sounds_tab_layout
