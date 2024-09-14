from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget
import sys
from PyQt5.QtGui import QIcon
from ui.tabs.Code import create_code_tab
from ui.tabs.Textures import create_textures_tab
from ui.tabs.Sounds import create_sounds_tab
# temporary ones
from PyQt5.QtWidgets import QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(480, 360)
        self.setWindowTitle("IDC")
        self.setWindowIcon(QIcon("textures/logo.png"))
        self.setStyleSheet('background-color: #FFFFFF')

        # Create a central widget for the main window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a layout
        self.grid = QGridLayout(self.central_widget)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 2)
        self.grid.setRowStretch(0, 3)
        self.grid.setRowStretch(1, 4)

        tabs_main = QTabWidget()
        code_tab = QWidget()
        textures_tab = QWidget()
        sounds_tab = QWidget()
        tabs_main.addTab(code_tab, 'Code')
        tabs_main.addTab(textures_tab, 'Textures')
        tabs_main.addTab(sounds_tab, "Sounds")

        # Code tab
        code_tab.setLayout(create_code_tab())

        # Textures tab
        textures_tab.setLayout(create_textures_tab())

        # Sounds tab
        sounds_tab.setLayout(create_sounds_tab())


        label_logs = QLabel("logs, ai and more here")
        label_logs.setStyleSheet('background-color: red;')
        label_spritelist = QLabel("sprite list here")
        label_spritelist.setStyleSheet('background-color: blue;')
        self.grid.addWidget(label_logs, 0, 0)
        self.grid.addWidget(label_spritelist, 1, 0)
        self.grid.addWidget(tabs_main, 0, 1, 2, 1)

        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
