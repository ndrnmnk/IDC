from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class SpriteList(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(['Item', 'Category'])

    def add_item(self, item, category):
        self.addTopLevelItem(QTreeWidgetItem([item, category]))
