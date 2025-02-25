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

        # Top controls
        self.top_hbox = QHBoxLayout()
        categories = ["Installed", "Customization", "Compilers", "Others"]
        for category in categories:
            cb = QCheckBox(category)
            self.top_hbox.addWidget(cb)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search")

        # Main vertical layout for addons
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)

        # Scroll area to hold addons
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.vbox)
        self.scroll_area.setWidget(self.scroll_area_widget)

        # Add widgets to grid layout
        self.grid.addWidget(self.search_bar, 0, 0)
        self.grid.addLayout(self.top_hbox, 1, 0)
        self.grid.addWidget(self.scroll_area, 2, 0)
        self.grid.addWidget(QLabel("<span style='color: red;'>WARNING:</span> you have to restart IDC right after deleting addons"), 3, 0)
        self.setLayout(self.grid)

        # Prepare dynamic loading variables
        self.batch_size = 10
        self.current_index = 0
        self.all_addons = remove_duplicates(
            self.parent.addons_manager.available_addons + self.parent.addons_manager.imported_addons
        )

        # Load initial batch of addons
        self.load_more_addons()

        # Connect the scroll bar to check when to load more addons
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.show()

    def load_more_addons(self):
        for i in range(self.current_index, min(self.current_index + self.batch_size, len(self.all_addons))):
            item = self.all_addons[i]
            addon_widget = ListItem(
                manager=self.parent.addons_manager,
                name=item["name"],
                description=item["description"],
                img_url=item["img_url"],
                git_link=item["git_link"]
            )
            self.vbox.addWidget(addon_widget)
        self.current_index += self.batch_size

    def on_scroll(self, value):
        # Check if user has scrolled near the bottom
        scrollbar = self.scroll_area.verticalScrollBar()
        if value > scrollbar.maximum() - 50:
            # Only load more if there are still addons remaining
            if self.current_index < len(self.all_addons):
                self.load_more_addons()
