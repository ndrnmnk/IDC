from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea,
    QCheckBox, QLabel, QLineEdit
)
from ui.subwidgets.ListItem2 import ListItem
from PyQt5.QtCore import Qt
from backend.config_manager import ConfigManager


def remove_duplicates(json_list):
    """
    Remove duplicate addon entries based on the 'name' key.
    If two entries share the same name, prefer the one with the 'installed' key.
    """
    result = {}
    for item in json_list:
        name = item.get('name')
        # If name exists and the new item has 'installed', replace it
        if name in result:
            if 'installed' in item:
                result[name] = item
        else:
            result[name] = item
    return list(result.values())


class AddonsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # It’s not necessary to store parent in self.parent since QWidget.parent() exists.
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("IDC: Addons")

        # Use a set for active categories for cleaner membership testing.
        self.categories = ["Installed", "Customization", "Compilers", "Others"]
        self.active_categories = set()

        # Prepare dynamic loading variables
        self.batch_size = 10
        self.current_index = 0

        # Combine available and imported addons and remove duplicates
        self.all_addons = remove_duplicates(
            parent.addons_manager.available_addons + parent.addons_manager.imported_addons
        )

        # Build UI and connect signals
        self._init_ui()

        # Load the initial batch of addons
        self.load_more_addons()

        # Monitor scrolling for lazy loading
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.on_scroll)

        self.show()

    def _init_ui(self):
        """Initialize and layout all UI components."""
        # Create the main grid layout for the window
        self.grid = QGridLayout()
        self.grid.setRowStretch(0, 0)
        self.grid.setRowStretch(2, 1)
        self.grid.setRowStretch(3, 0)

        # Top controls: checkboxes for categories
        self.top_hbox = QHBoxLayout()
        for idx, category in enumerate(self.categories):
            cb = QCheckBox(category)
            # Use default argument to capture current idx
            cb.stateChanged.connect(lambda state, i=idx: self.update_active_categories(i, state))
            self.top_hbox.addWidget(cb)

        # Search bar setup based on configuration
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search (press Enter to display results)")
        if ConfigManager().get_config().get("dynamic_addons_updating"):
            self.search_bar.textEdited.connect(self.apply_filter)
        else:
            self.search_bar.editingFinished.connect(self.apply_filter)

        # Vertical layout to hold addon items
        self.vbox = QVBoxLayout()
        self.vbox.setAlignment(Qt.AlignTop)

        # Scroll area to contain the vbox
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # Use a dedicated widget to hold the vbox layout
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.vbox)
        self.scroll_area.setWidget(self.scroll_area_widget)

        # A warning label at the bottom
        warning_label = QLabel("<span style='color: red;'>WARNING:</span> you have to restart IDC right after deleting addons")

        # Arrange everything in the grid layout
        self.grid.addWidget(self.search_bar, 0, 0)
        self.grid.addLayout(self.top_hbox, 1, 0)
        self.grid.addWidget(self.scroll_area, 2, 0)
        self.grid.addWidget(warning_label, 3, 0)
        self.setLayout(self.grid)

    def create_list_item(self, item):
        """Helper method to create a ListItem widget from an addon dictionary."""
        return ListItem(
            manager=self.parent().addons_manager,
            name=item["name"],
            description=item["description"],
            categories=item["categories"],
            img_url=item["img_url"],
            git_link=item["git_link"]
        )

    def load_more_addons(self):
        """Load a batch of addons into the scroll area."""
        end_index = min(self.current_index + self.batch_size, len(self.all_addons))
        for i in range(self.current_index, end_index):
            addon_widget = self.create_list_item(self.all_addons[i])
            self.vbox.addWidget(addon_widget)
        self.current_index = end_index

    def on_scroll(self, value):
        """Check if the scroll bar is near the bottom to load more addons."""
        scrollbar = self.scroll_area.verticalScrollBar()
        if value > scrollbar.maximum() - 50:
            if self.current_index < len(self.all_addons):
                self.load_more_addons()

    def filtered_addons(self):
        """Return the list of addons filtered by the search query and active categories."""
        query = self.search_bar.text().lower().replace(" ", "_")
        return [
            item for item in self.all_addons
            if item["name"].lower().startswith(query) and self.active_categories.issubset(item["categories"])
        ]

    def apply_filter(self):
        """Clear the current list and repopulate it with addons that match the filter criteria."""
        filtered = self.filtered_addons()
        # Remove all current widgets from the vbox layout
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # Reset index so that lazy loading starts fresh on the filtered list
        self.current_index = 0
        # Instead of batch loading, here we add all filtered addons at once
        for addon in filtered:
            addon_widget = self.create_list_item(addon)
            self.vbox.addWidget(addon_widget)

    def update_active_categories(self, index, state):
        """Update the set of active categories based on checkbox state and reapply the filter."""
        category = self.categories[index]
        if state:
            self.active_categories.add(category)
        else:
            self.active_categories.discard(category)
        self.apply_filter()
