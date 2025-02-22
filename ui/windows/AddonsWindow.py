from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea, QCheckBox, QLabel, QLineEdit
from ui.subwidgets.ListItem2 import ListItem
from PyQt5.QtCore import Qt


def remove_duplicates(json_list):
	result = {}
	for item in json_list:
		name = item.get('name')
		# Check if name already exists in the result dictionary
		if name in result:
			# If the existing item does not have 'installed', replace it with the one that does
			if 'installed' in item:
				result[name] = item
		else:
			result[name] = item
	# Return the list of filtered JSON objects
	return list(result.values())


class AddonsWindow(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent = parent
		self.setWindowFlags(Qt.Window)
		self.setWindowTitle("IDC: Addons")
		self.grid = QGridLayout()
		self.grid.setRowStretch(0, 0)
		self.grid.setRowStretch(2, 1)
		self.grid.setRowStretch(3, 0)

		self.top_hbox = QHBoxLayout()
		categories = ["Installed", "Customization", "Compilers", "Others"]
		for caterory in categories:
			t = QCheckBox(caterory)
			self.top_hbox.addWidget(t)

		self.search_bar = QLineEdit()
		self.search_bar.setPlaceholderText("Search")

		self.vbox = QVBoxLayout()
		self.vbox.setAlignment(Qt.AlignTop)

		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		self.scroll_area_widget = QWidget()
		self.scroll_area.setWidget(self.scroll_area_widget)
		self.scroll_area_widget.setLayout(self.vbox)

		self.grid.addWidget(self.search_bar, 0, 0)
		self.grid.addLayout(self.top_hbox, 1, 0)
		self.grid.addWidget(self.scroll_area, 2, 0)
		self.grid.addWidget(QLabel("<span style='color: red;'>WARNING:</span> you have to restart IDC right after deleting addons"), 3, 0)
		self.setLayout(self.grid)

		# show all available and installed addons, removing the duplicates
		self.populate_addons(remove_duplicates(self.parent.addons_manager.available_addons + self.parent.addons_manager.imported_addons))

		self.show()

	def populate_addons(self, addons_list):
		for item in addons_list:
			addon_widget = ListItem(
				manager=self.parent.addons_manager,
				name=item["name"],
				description=item["description"],
				img_url=item["img_url"],
				git_link=item["git_link"]
			)
			self.vbox.addWidget(addon_widget)
