import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget, QAction, QPushButton, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys
from ui.tabs.Code import CodeTabLayout
from ui.tabs.Sounds import SoundsTabLayout
from ui.tabs.Textures import TexturesTabLayout
from ui.tabs.Logs import LogsTabLayout
from ui.tabs.AI import AiTabLayout
from ui.tabs.Problems import ProblemsTabWidget
from ui.elements.Spritelist import SpriteList
from ui.windows.OptionsWindow import OptionsWindow
from ui.windows.AddonsWindow import AddonsWindow
from ui.subwidgets.ResizableDropdown import ResizableDropdown
from backend.backend import Backend
from backend.config_manager import ConfigManager
from backend.addons_manager import AddonsManager


class MainWindow(QMainWindow):
	def __init__(self, config):
		super().__init__()
		# Load data
		self.setStyleSheet(f"background-color: {config.get_config()['styles']['bg_color']};")
		# Apply data
		self.setWindowTitle("IDC")
		self.setFont(QFont(config.get_config()["font_family"], config.get_config()["font_size"]))
		self.setWindowIcon(QIcon(config.get_config()["icon_path"]))
		self.setMinimumSize(480, 360)

		# Create top bar
		menu_bar = self.menuBar()
		file_menu = menu_bar.addMenu('File')
		self.options_menu = menu_bar.addAction('Options')
		self.addons_menu = menu_bar.addAction('Addons')
		# Create file tab of menu bar
		open_action = QAction('Open', self)
		save_action = QAction('Save', self)
		exit_action = QAction('Exit', self)
		file_menu.addAction(open_action)
		file_menu.addAction(save_action)
		file_menu.addAction(exit_action)
		open_action.triggered.connect(self.open_project)
		exit_action.triggered.connect(self.close)
		self.options_menu.triggered.connect(self.open_options_window)
		self.addons_menu.triggered.connect(self.open_addons_window)

		# create a central widget for the main window
		self.central_widget = QWidget(self)
		self.setCentralWidget(self.central_widget)

		# create a layout
		self.grid = QGridLayout(self.central_widget)
		self.grid.setColumnStretch(0, 1)
		self.grid.setColumnStretch(1, 4)
		self.grid.setRowStretch(0, 0)
		self.grid.setRowStretch(1, 1)
		self.grid.setRowStretch(2, 1)

		# CREATE MAIN TABS
		# create tab selector widget
		tabs_main = QTabWidget()
		self.code_tab = QWidget()
		self.textures_tab = QWidget()
		self.sounds_tab = QWidget()
		tabs_main.addTab(self.code_tab, 'Code')
		tabs_main.addTab(self.textures_tab, 'Textures')
		tabs_main.addTab(self.sounds_tab, "Sounds")
		# create tab layouts
		self.textures_tab_layout = TexturesTabLayout()
		# use tabs layouts
		self.textures_tab.setLayout(self.textures_tab_layout)

		self.code_tab_layout = CodeTabLayout()
		self.code_tab.setLayout(self.code_tab_layout)

		self.sounds_tab_layout = SoundsTabLayout()
		self.sounds_tab.setLayout(self.sounds_tab_layout)

		# CREATE MISC TABS
		# create tab selector widget
		tabs_misc = QTabWidget()
		self.problems_tab = ProblemsTabWidget()
		self.logs_tab = QWidget()
		self.ai_tab = QWidget()
		tabs_misc.addTab(self.problems_tab, "Problems")
		tabs_misc.addTab(self.logs_tab, "Logs")
		tabs_misc.addTab(self.ai_tab, "AI")
		# create tab layouts
		self.logs_widget = LogsTabLayout()
		self.ai_tab_layout = AiTabLayout()
		# use tab layouts
		self.logs_tab.setLayout(self.logs_widget)
		self.ai_tab.setLayout(self.ai_tab_layout)

		# create sprite list
		self.spritelist = SpriteList()

		# Create Layout for buttons
		buttons_layout = QHBoxLayout()
		buttons_layout.setContentsMargins(0, 0, 0, 0)
		# create buttons
		self.build_btn = QPushButton(text="build")
		self.run_btn = QPushButton(text="run")
		self.kill_btn = QPushButton(text="kill")
		self.compiler_dropdown = ResizableDropdown([])
		self.compiler_options_btn = QPushButton("Compiler Options")
		# fix width
		self.build_btn.setFixedWidth(40)
		self.run_btn.setFixedWidth(40)
		self.kill_btn.setFixedWidth(40)
		# pack inside a widget
		buttons_layout.setAlignment(Qt.AlignLeft)
		buttons_layout.addWidget(self.build_btn)
		buttons_layout.addWidget(self.run_btn)
		buttons_layout.addWidget(self.kill_btn)
		buttons_layout.addWidget(self.compiler_dropdown)
		buttons_layout.addWidget(self.compiler_options_btn)
		buttons_widget = QWidget()
		buttons_widget.setLayout(buttons_layout)

		# place everything
		self.grid.addWidget(buttons_widget, 0, 0, 1, 2)
		self.grid.addWidget(tabs_misc, 1, 0)
		self.grid.addWidget(self.spritelist, 2, 0)
		self.grid.addWidget(tabs_main, 1, 1, 2, 1)

		tabs_misc.setCurrentIndex(1)  # logs tab

		self.opened_project_path = None

		# project path will be inserted into {}
		self.compilers = {}
		self.current_compiler = None

		self.backend = Backend(self)
		self.addons_manager = AddonsManager(self)

		self.show()

	def add_compiler(self, name, module):
		self.compilers[name] = module
		self.compiler_dropdown.addItem(name)

	def on_new_compiler(self):
		self.current_compiler = self.compilers[self.compiler_dropdown.currentText()]
		self.compiler_options_btn.disconnect()
		self.compiler_options_btn.pressed.connect(self.current_compiler.on_compiler_options)

	def open_options_window(self):
		OptionsWindow(self)

	def open_addons_window(self):
		AddonsWindow(self)

	def open_project(self):
		file_path, _ = QFileDialog.getOpenFileName(None, "Select a File", "", "IDC Project (*.idcp)")
		if not self.opened_project_path:
			self.opened_project_path = os.path.dirname(file_path)
			print(self.opened_project_path)
		else:
			print("save the project? [Y/n]")

	def closeEvent(self, event):
		ConfigManager().save_config()
		for addon in self.addons_manager.addons_names:
			self.addons_manager.addons[addon].on_idc_close()
		super().closeEvent(event)


if __name__ == "__main__":
	config = ConfigManager()
	config.load_config("options.json")
	config.load_blocks("block_info/categories.json")
	app = QApplication(sys.argv)
	app.setStyle("Fusion")
	app.setStyleSheet(f"QWidget {{ color: {config.get_config()['styles']['text_color']}; }}")
	window = MainWindow(config)

	sys.exit(app.exec_())
