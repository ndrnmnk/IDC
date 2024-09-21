from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon


def create_problems_tab():
    layout = QVBoxLayout()

    list_widget = QListWidget()
    icon_warning = QIcon('textures/warning.png')
    icon_error = QIcon(QIcon('textures/error.png'))
    item1 = QListWidgetItem(icon_warning, 'warning')
    item2 = QListWidgetItem(icon_warning, 'warning')
    item3 = QListWidgetItem(icon_error, 'error')

    # Add items to the QListWidget
    list_widget.addItem(item1)
    list_widget.addItem(item2)
    list_widget.addItem(item3)

    layout.addWidget(list_widget)
    return layout
