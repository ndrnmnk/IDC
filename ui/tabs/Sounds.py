from PyQt5.QtWidgets import QLabel, QGridLayout


class SoundsTabLayout(QGridLayout):
    def __init__(self):
        super().__init__()

        placeholde_label = QLabel("Sounds list")
        placeholder_label = QLabel("edit here")

        placeholder_label.setStyleSheet('background-color: purple;')

        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 4)
        self.addWidget(placeholde_label, 0, 0)
        self.addWidget(placeholder_label, 0, 1)
