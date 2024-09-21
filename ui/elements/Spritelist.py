from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


def create_spritelist():
    tree_widget = QTreeWidget()
    tree_widget.setColumnCount(2)
    # Set the headers for the columns
    tree_widget.setHeaderLabels(['Item', 'Category'])
    # Create an item with multiple columns
    item1 = QTreeWidgetItem(['Cat', '2D Sprite'])
    item2 = QTreeWidgetItem(['Dialog window', 'UI'])
    item3 = QTreeWidgetItem(['Cube', '3D Sprite'])
    # Add items to the tree widget
    tree_widget.addTopLevelItem(item1)
    tree_widget.addTopLevelItem(item2)
    tree_widget.addTopLevelItem(item3)

    return tree_widget
