from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


class SpriteList(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHeaderLabels(['Item', 'Category'])

        item1 = QTreeWidgetItem(['Cat', '2D Sprite'])
        item2 = QTreeWidgetItem(['Dialog window', 'UI'])
        item3 = QTreeWidgetItem(['Cube', '3D Sprite'])

        self.addTopLevelItem(item1)
        self.addTopLevelItem(item2)
        self.addTopLevelItem(item3)
