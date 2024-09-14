from PyQt5.QtWidgets import QLabel, QListWidget, QListWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon


def create_problems_tab():
    layout = QVBoxLayout()

    list_widget = QListWidget()
    icon = QIcon('textures/logo.png')
    item1 = QListWidgetItem(icon, 'Item 1')
    item2 = QListWidgetItem(icon, 'Item 2')
    item3 = QListWidgetItem(icon, 'Item 3')

    # Add items to the QListWidget
    list_widget.addItem(item1)
    list_widget.addItem(item2)
    list_widget.addItem(item3)

    layout.addWidget(list_widget)
    return layout
