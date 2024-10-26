from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
from ui.windows.Options.Visual import VisualOptions
from ui.windows.Options.Compilers import CompilerOptions


class OptionsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("IDC: Options")
        self.setMinimumSize(360, 360)
        self.main_hbox = QHBoxLayout()
        self.setLayout(self.main_hbox)

        self.menu = QListWidget()
        self.menu.setFixedWidth(100)
        self.menu.itemClicked.connect(self.menu_option_selected)
        self.main_hbox.addWidget(self.menu)

        self.menu.addItem(QListWidgetItem("Visual"))
        self.menu.addItem(QListWidgetItem("Compilation"))
        self.menu.addItem(QListWidgetItem("Addons"))

        self.options_display = VisualOptions()
        self.main_hbox.addLayout(self.options_display)

        self.show()

    def menu_option_selected(self, item):
        self.options_display.deleteLater()
        del self.options_display

        if item.text() == "Visual":
            self.options_display = VisualOptions()

        elif item.text() == "Compilation":
            self.options_display = CompilerOptions()
        elif item.text() == "Addons":
            self.options_display = self.parent.addons_manager.get_options()

        self.main_hbox.addLayout(self.options_display)
