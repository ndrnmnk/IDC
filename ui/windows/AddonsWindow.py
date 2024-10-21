from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea, QCheckBox, QLabel
from ui.subwidgets.ListItem2 import ListItem
from PyQt5.QtCore import Qt


class AddonsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("IDC: Addons")
        self.grid = QGridLayout()
        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(1, 1)
        self.grid.setRowStretch(2, 0)

        self.top_hbox = QHBoxLayout()
        self.top_hbox.addWidget(QCheckBox("Installed"))
        self.top_hbox.addWidget(QCheckBox("Customization"))
        self.top_hbox.addWidget(QCheckBox("Compilers"))
        self.top_hbox.addWidget(QCheckBox("Custom"))

        self.vbox = QVBoxLayout()

        test_addons_list = [
            {"name": "rude_addon", "description": "|1 0uy cn@ d3r@ т3h|, u u3тp|b", "image_url": "https://static.vecteezy.com/system/resources/previews/021/608/790/non_2x/chatgpt-logo-chat-gpt-icon-on-black-background-free-vector.jpg", "git_link": None},
            {"name": "useless_addon", "description": "I AM NOT A MORON", "image_url": "https://cdn2.hubspot.net/hubfs/53/image8-2.jpg", "git_link": "https://github.com/ndrnmnk/mh_infrared"}
        ]

        for item in test_addons_list:
            self.vbox.addWidget(ListItem(parent, item["name"], item["description"], item["image_url"], item["git_link"]))

        self.vbox_widget = QWidget()
        self.vbox_widget.setLayout(self.vbox)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.vbox_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.grid.addLayout(self.top_hbox, 0, 0)
        self.grid.addWidget(self.scroll_area, 1, 0)
        self.grid.addWidget(QLabel("Warning: you have to restart IDC after deleting addons"), 2, 0)
        self.setLayout(self.grid)
        self.show()
