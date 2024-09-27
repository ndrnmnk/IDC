from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon


class ProblemsTabWidget(QListWidget):
    def __init__(self):
        super().__init__()
        icon_warning = QIcon("textures/warning.png")
        icon_error = QIcon("textures/error.png")

        item1 = QListWidgetItem(icon_warning, 'warning')
        item2 = QListWidgetItem(icon_warning, 'warning')
        item3 = QListWidgetItem(icon_error, 'error')

        self.addItem(item1)
        self.addItem(item2)
        self.addItem(item3)
