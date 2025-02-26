from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea, QCheckBox, QLabel, QLineEdit
from ui.subwidgets.ListItem2 import ListItem
from PyQt5.QtCore import Qt
from backend.config_manager import ConfigManager


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
        self.categories = ["Installed", "Customization", "Compilers", "Others"]
        self.cb_list = []
        for idx, category in enumerate(self.categories):
            cb = QCheckBox(category)
            cb.stateChanged.connect(lambda state, i=idx: self.update_cb_list(i, state))
            self.top_hbox.addWidget(cb)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search (press Enter to display results)")
        if ConfigManager().get_config()["dynamic_addons_updating"]:
            self.search_bar.textEdited.connect(self.apply_filter)
        else:
            self.search_bar.editingFinished.connect(self.apply_filter)

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
                categories=item["categories"],
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

    def filtered_addons(self):
        res = []
        query = self.search_bar.text().lower().replace(" ", "_")
        for item in self.all_addons:
            if item["name"].lower().startswith(query) and set(self.cb_list).issubset(item["categories"]):
                res.append(item)
        return res

    def apply_filter(self):
        # Get the filtered list of addons
        filtered = self.filtered_addons()

        # Remove all existing ListItems from the vertical layout
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()  # Schedule the widget for deletion

        # Populate the layout with the filtered addons
        for addon in filtered:
            addon_widget = ListItem(
                manager=self.parent.addons_manager,
                name=addon["name"],
                description=addon["description"],
                categories=addon["categories"],
                img_url=addon["img_url"],
                git_link=addon["git_link"]
            )
            self.vbox.addWidget(addon_widget)

    def update_cb_list(self, index, state):
        if state:
            self.cb_list.append(self.categories[index])
        else:
            self.cb_list.remove(self.categories[index])
        self.apply_filter()
