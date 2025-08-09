from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, \
	QMenu
from ui.windows.NewObjectWindow import NewObjectWindow
from PyQt5.QtCore import Qt, QPoint


class SpriteList(QTreeWidget):
	def __init__(self, ui):
		super().__init__()
		self.ui = ui
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.show_context_menu)
		self.setColumnCount(2)
		self.setHeaderLabels(['Item', 'Instance of'])
		self.item_list = []
		self.item_meta = []

	def add_item(self, item, inherits_from):
		self.item_list.append(QTreeWidgetItem([item, inherits_from]))
		self.item_meta.append([item, inherits_from])
		self.addTopLevelItem(self.item_list[-1])

	def remove_item_by_name(self, name):
		if name != "Main":
			root = self.invisibleRootItem()
			for i in range(root.childCount()):
				item = root.child(i)
				if item and item.text(0) == name:
					# set current sprite to main
					self.ui.code_tab.sprite_manager.change_current_sprite(self.item_list[0])

					root.removeChild(item)
					self.item_list.remove(item)
					self.item_meta.remove([item.text(0), item.text(1)])
					del self.ui.code_tab.all_sprites_code[item.text(0)]

	def remove_all(self):
		self.clear()
		self.item_list.clear()
		self.item_meta.clear()

	def remove_item_gui(self):
		if self.selectedItems()[0].text(0) == "Main":
			return
		if self.selectedItems():
			reply = QMessageBox.warning(self, "IDC warning", "Are you sure? This can't be undone", QMessageBox.Yes | QMessageBox.No)
			if reply == QMessageBox.Yes:
				self.remove_item_by_name(self.selectedItems()[0].text(0))
		else:
			QMessageBox.information(self, "IDC warning", "Can't delete object - No object is selected", QMessageBox.Ok)

	def show_context_menu(self, position: QPoint):
		item = self.itemAt(position)  # Get the item under the cursor

		menu = QMenu(self)
		action_add = menu.addAction("Add object")
		if item:  # If user clicked on an item
			action_rename = menu.addAction("Rename")
			action_delete = menu.addAction("Delete")

			action = menu.exec_(self.viewport().mapToGlobal(position))  # Show menu

			if action == action_rename:
				print(f"Renaming {item.text(0)}")
			elif action == action_delete:
				self.remove_item_gui()
		else:  # If user clicked on the background (empty area)
			action = menu.exec_(self.viewport().mapToGlobal(position))

		if action == action_add:
			NewObjectWindow(self)
