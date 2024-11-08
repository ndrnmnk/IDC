from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget, QAction, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
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
from backend.addons_manager import AddonsManager


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setMinimumSize(480, 360)
		self.setWindowTitle("IDC")
		self.setWindowIcon(QIcon("textures/logo.png"))
		self.setStyleSheet("background-color: #FFFFFF;")

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
		exit_action.triggered.connect(self.close)

		self.options_menu.triggered.connect(self.open_options_window)
		self.addons_menu.triggered.connect(self.open_addons_window)

		# create a central widget for the main window
		self.central_widget = QWidget(self)
		self.setCentralWidget(self.central_widget)

		# create a layout
		self.grid = QGridLayout(self.central_widget)
		self.grid.setColumnStretch(0, 1)
		self.grid.setColumnStretch(1, 2)
		self.grid.setRowStretch(0, 0)
		self.grid.setRowStretch(1, 15)
		self.grid.setRowStretch(2, 20)

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
		self.target_os_dropdown = ResizableDropdown([])
		self.target_arch_dropdown = ResizableDropdown([])
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
		buttons_layout.addWidget(self.target_os_dropdown)
		buttons_layout.addWidget(self.target_arch_dropdown)
		buttons_widget = QWidget()
		buttons_widget.setLayout(buttons_layout)

		# place everything
		self.grid.addWidget(buttons_widget, 0, 0, 1, 2)
		self.grid.addWidget(tabs_misc, 1, 0)
		self.grid.addWidget(self.spritelist, 2, 0)
		self.grid.addWidget(tabs_main, 1, 1, 2, 1)

		tabs_misc.setCurrentIndex(1)  # logs tab

		# project path will be inserted into {}
		self.compilers = {
			"C++ (cmake)":
				{"command": "cd {}/build; cmake ..; make", "run": "{}/build/main", "platforms": {
					'Windows': ['x86', 'x64', 'arm64'],
					'Linux': ['x86', 'x64', 'arm32', 'arm64'],
					'macOS': ['x64', 'arm64']
				}
				},
			"Python":
				{"command": "cd {}/build; cmake ..; make", "run": "{}/build/main", "platforms": {
					'All': ['All']
				}
				}
		}

		self.compiler_dropdown.currentTextChanged.connect(self.update_os_dropdown)
		self.target_os_dropdown.currentTextChanged.connect(self.update_arch_dropdown)

		self.addons_manager = AddonsManager(self)

		for item in self.compilers:
			self.compiler_dropdown.addItem(item)
		del item

		self.backend = Backend(self)

		self.show()

	def update_os_dropdown(self):
		self.target_os_dropdown.clear()
		oss = self.compilers[self.compiler_dropdown.currentText()]["platforms"].keys()
		self.target_os_dropdown.addItems(oss)

	def update_arch_dropdown(self):
		self.target_arch_dropdown.clear()
		try:
			archs = self.compilers[self.compiler_dropdown.currentText()]["platforms"][self.target_os_dropdown.currentText()]
		except KeyError:
			# because of weird KeyError appearing after running update_os_dropdown, it uses the first available os
			a = list(self.compilers[self.compiler_dropdown.currentText()]["platforms"].keys())
			archs = self.compilers[self.compiler_dropdown.currentText()]["platforms"][a[0]]
		self.target_arch_dropdown.addItems(archs)

	def open_options_window(self):
		OptionsWindow(self)

	def open_addons_window(self):
		AddonsWindow(self)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()

	sys.exit(app.exec_())
