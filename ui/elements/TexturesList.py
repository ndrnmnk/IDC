from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QScrollArea, QVBoxLayout
from ui.subwidgets.ListItem import ListItem
from PyQt5.QtCore import Qt

class TexturesList(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        vbox_widget = QWidget()
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)
        self.vbox.setContentsMargins(0, 0, 0, 0)

        self.vbox.addWidget(ListItem("error", "textures/error.png", show_image_size=False))
        self.vbox.addWidget(ListItem("warning", "textures/warning.png"))
        self.vbox.addWidget(ListItem("logo", "textures/logo.png"))
        self.vbox.addWidget(ListItem("test", "textures/test.png"))

        vbox_widget.setLayout(self.vbox)
        self.setWidget(vbox_widget)
