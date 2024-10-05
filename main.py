from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget, QAction, QPushButton, QHBoxLayout
import sys
from PyQt5.QtGui import QIcon

from ui.tabs.Code import CodeTabLayout
from ui.tabs.Sounds import SoundsTabLayout
from ui.tabs.Textures import TexturesTabLayout
from ui.tabs.BuildLogs import BuildLogsTabLayout
from ui.tabs.AI import AiTabLayout
from ui.tabs.Problems import ProblemsTabWidget
from ui.elements.Spritelist import SpriteList

from backend.backend import Backend


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(480, 360)
        self.setWindowTitle("IDC")
        self.setWindowIcon(QIcon("textures/logo.png"))
        self.setStyleSheet("background-color: #FFFFFF;")

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        # Create file tab of menu bar
        open_action = QAction('Open', self)
        save_action = QAction('Save', self)
        exit_action = QAction('Exit', self)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close)

        # create a central widget for the main window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # create a layout
        self.grid = QGridLayout(self.central_widget)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 2)
        self.grid.setRowStretch(0, 1)
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
        tabs_misc.addTab(self.logs_tab, "Build logs")
        tabs_misc.addTab(self.ai_tab, "AI")
        # create tab layouts
        self.build_logs_widget = BuildLogsTabLayout()
        self.ai_tab_layout = AiTabLayout()
        # use tab layouts
        self.logs_tab.setLayout(self.build_logs_widget)
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
        # fix width
        self.build_btn.setMinimumWidth(20)
        self.run_btn.setMinimumWidth(20)
        self.kill_btn.setMinimumWidth(20)
        # pack inside a widget
        buttons_layout.addWidget(self.build_btn)
        buttons_layout.addWidget(self.run_btn)
        buttons_layout.addWidget(self.kill_btn)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        # place everything
        self.grid.addWidget(buttons_widget, 0, 0)
        self.grid.addWidget(tabs_misc, 1, 0)
        self.grid.addWidget(self.spritelist, 2, 0)
        self.grid.addWidget(tabs_main, 1, 1, 2, 1)

        tabs_misc.setCurrentIndex(1)  # build logs tab

        self.backend = Backend(self)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
