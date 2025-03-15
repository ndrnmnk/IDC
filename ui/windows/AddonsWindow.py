from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QHBoxLayout, QScrollArea,
    QCheckBox, QLabel, QLineEdit
)
from ui.subwidgets.ListItem2 import ListItem
from PyQt5.QtCore import Qt
from backend.config_manager import ConfigManager


def merge_dicts(dict1, dict2):
    merged = {}
    # Get all unique keys from both dictionaries
    all_keys = set(dict1.keys()).union(dict2.keys())
    for key in all_keys:
        if key in dict1 and key in dict2:
            # Prefer the dictionary where 'installed' is True
            if dict1[key].get("installed", False):
                merged[key] = dict1[key]
            else:
                merged[key] = dict2[key]
        else:
            # Add the existing entry from either dictionary
            merged[key] = dict1.get(key, dict2.get(key))
    return merged


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
        self.all_addons = merge_dicts(parent.addons_manager.available_addons, parent.addons_manager.addons_metadata)

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

        # Arrange everything in the grid layout
        self.grid.addWidget(self.search_bar, 0, 0)
        self.grid.addLayout(self.top_hbox, 1, 0)
        self.grid.addWidget(self.scroll_area, 2, 0)
        self.setLayout(self.grid)

    def create_list_item(self, item_name):
        """Helper method to create a ListItem widget from an addon dictionary."""
        return ListItem(
            manager=self.parent().addons_manager,
            name=item_name
        )

    def load_more_addons(self):
        """Load a batch of addons into the scroll area."""
        end_index = min(self.current_index + self.batch_size, len(self.all_addons))
        for i in range(self.current_index, end_index):
            addon_widget = self.create_list_item(list(self.all_addons.keys())[i])
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
            if item.lower().startswith(query) and self.active_categories.issubset(self.all_addons[item]["categories"])
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
