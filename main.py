from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget, QAction
import sys
from PyQt5.QtGui import QIcon

from ui.tabs.Code import create_code_tab
from ui.tabs.Textures import create_textures_tab
from ui.tabs.Sounds import create_sounds_tab

from ui.tabs.Spritelist import create_spritelist
from ui.tabs.BuildLogs import create_build_logs_tab
from ui.tabs.Problems import create_problems_tab
from ui.tabs.AI import create_ai_tab


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

        # Create a central widget for the main window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout
        self.grid = QGridLayout(self.central_widget)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 2)
        self.grid.setRowStretch(0, 3)
        self.grid.setRowStretch(1, 4)

        # Create main tabs
        tabs_main = QTabWidget()
        code_tab = QWidget()
        textures_tab = QWidget()
        sounds_tab = QWidget()
        tabs_main.addTab(code_tab, 'Code')
        tabs_main.addTab(textures_tab, 'Textures')
        tabs_main.addTab(sounds_tab, "Sounds")
        code_tab.setLayout(create_code_tab())
        textures_tab.setLayout(create_textures_tab())
        sounds_tab.setLayout(create_sounds_tab())

        tabs_misc = QTabWidget()
        problems_tab = QWidget()
        logs_tab = QWidget()
        ai_tab = QWidget()
        tabs_misc.addTab(problems_tab, "Problems")
        tabs_misc.addTab(logs_tab, "Build logs")
        tabs_misc.addTab(ai_tab, "AI")

        problems_tab.setLayout(create_problems_tab())
        logs_tab.setLayout(create_build_logs_tab())
        ai_tab.setLayout(create_ai_tab())

        spritelist = create_spritelist()
        self.grid.addWidget(tabs_misc, 0, 0)
        self.grid.addWidget(spritelist, 1, 0)
        self.grid.addWidget(tabs_main, 0, 1, 2, 1)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
