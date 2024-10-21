from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QColorDialog
from PyQt5.QtCore import Qt


class OptionsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("IDC: Options")
        layout = QVBoxLayout()

        # Add a button to close the child window
        close_button = QPushButton("Open color selector")
        close_button.clicked.connect(self.get_color)

        layout.addWidget(close_button)
        self.setLayout(layout)
        self.show()

    def get_color(self):
        color = QColorDialog.getColor()