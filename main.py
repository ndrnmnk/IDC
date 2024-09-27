from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget, QAction, QPushButton, QHBoxLayout
import sys
from PyQt5.QtGui import QIcon

from ui.tabs.Code import CodeTabLayout

from ui.tabs.Sounds import SoundsTabLayout
from ui.tabs.Problems import ProblemsTabWidget
from ui.tabs.Textures import TexturesTabLayout
from ui.tabs.BuildLogs import BuildLogsTabLayout
from ui.tabs.AI import AiTabLayout

from ui.elements.Spritelist import SpriteList


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
        code_tab = QWidget()
        textures_tab = QWidget()
        sounds_tab = QWidget()
        tabs_main.addTab(code_tab, 'Code')
        tabs_main.addTab(textures_tab, 'Textures')
        tabs_main.addTab(sounds_tab, "Sounds")
        # create tab layouts
        textures_tab_layout = TexturesTabLayout()
        # use tabs layouts
        textures_tab.setLayout(textures_tab_layout)

        code_tab_layout = CodeTabLayout()
        code_tab.setLayout(code_tab_layout)

        sounds_tab_layout = SoundsTabLayout()
        sounds_tab.setLayout(sounds_tab_layout)

        # CREATE MISC TABS
        # create tab selector widget
        tabs_misc = QTabWidget()
        problems_tab = ProblemsTabWidget()
        logs_tab = QWidget()
        ai_tab = QWidget()
        tabs_misc.addTab(problems_tab, "Problems")
        tabs_misc.addTab(logs_tab, "Build logs")
        tabs_misc.addTab(ai_tab, "AI")
        # create tab layouts
        build_logs_tab_layout = BuildLogsTabLayout()
        ai_tab_layout = AiTabLayout()
        # use tab layouts
        logs_tab.setLayout(build_logs_tab_layout)
        ai_tab.setLayout(ai_tab_layout)

        # create spritelist
        spritelist = SpriteList()

        # Create Layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        # create buttons
        build_btn = QPushButton(text="build")
        run_btn = QPushButton(text="run")
        kill_btn = QPushButton(text="kill")
        # fix width
        build_btn.setMinimumWidth(20)
        run_btn.setMinimumWidth(20)
        kill_btn.setMinimumWidth(20)
        # pack inside a widget
        buttons_layout.addWidget(build_btn)
        buttons_layout.addWidget(run_btn)
        buttons_layout.addWidget(kill_btn)
        buttons_widget = QWidget()
        buttons_widget.setLayout(buttons_layout)

        # place everything
        self.grid.addWidget(buttons_widget, 0, 0)
        self.grid.addWidget(tabs_misc, 1, 0)
        self.grid.addWidget(spritelist, 2, 0)
        self.grid.addWidget(tabs_main, 1, 1, 2, 1)

        tabs_misc.setCurrentIndex(1)  # build logs tab

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
