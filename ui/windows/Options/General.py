from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from backend import ConfigManager


class GeneralOptions(QWidget):
	def __init__(self):
		super().__init__()
		self.vbox = QVBoxLayout()
		self.vbox.setAlignment(Qt.AlignTop)
		self.setLayout(self.vbox)

		self.dynamic_addon_checkbox = QCheckBox("Update addons search results dynamically")
		self.dynamic_addon_checkbox.setCheckState(ConfigManager().get_config()["dynamic_addons_updating"])
		self.dynamic_addon_checkbox.stateChanged.connect(self.update_dynamic_addon_config)
		self.vbox.addWidget(self.dynamic_addon_checkbox)

		self.auto_update_addons_checkbox = QCheckBox("Automatically update addons")
		self.auto_update_addons_checkbox.setCheckState(ConfigManager().get_config()["autoupdate_addons"])
		self.auto_update_addons_checkbox.stateChanged.connect(self.update_autoupdate_addon_config)
		self.vbox.addWidget(self.auto_update_addons_checkbox)

	def update_dynamic_addon_config(self):
		ConfigManager().set("dynamic_addons_updating", self.dynamic_addon_checkbox.checkState())

	def update_autoupdate_addon_config(self):
		ConfigManager().set("autoupdate_addons", self.auto_update_addons_checkbox.checkState())