from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTabWidget
import sys
from PyQt5.QtGui import QIcon
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
        code_tab_layout = QGridLayout()
        label0 = QLabel("Block to pick")
        label1 = QLabel("Code here")
        label0.setStyleSheet('background-color: pink;')
        label1.setStyleSheet('background-color: grey;')
        code_tab_layout.setColumnStretch(0, 1)
        code_tab_layout.setColumnStretch(1, 4)
        code_tab_layout.addWidget(label0, 0, 0)
        code_tab_layout.addWidget(label1, 0, 1)
        code_tab.setLayout(code_tab_layout)

        # Textures tab
        textures_tab_layout = QGridLayout()
        label2 = QLabel("Skins or models list")
        label3 = QLabel("edit here")
        label2.setStyleSheet('background-color: yellow;')
        label3.setStyleSheet('background-color: lightgreen;')
        textures_tab_layout.setColumnStretch(0, 1)
        textures_tab_layout.setColumnStretch(1, 4)
        textures_tab_layout.addWidget(label2, 0, 0)
        textures_tab_layout.addWidget(label3, 0, 1)
        textures_tab.setLayout(textures_tab_layout)

        # Sounds tab
        sounds_tab_layout = QGridLayout()
        label4 = QLabel("Sounds list")
        label5 = QLabel("edit here")
        label4.setStyleSheet('background-color: lightblue;')
        label5.setStyleSheet('background-color: purple;')
        sounds_tab_layout.setColumnStretch(0, 1)
        sounds_tab_layout.setColumnStretch(1, 4)
        sounds_tab_layout.addWidget(label4, 0, 0)
        sounds_tab_layout.addWidget(label5, 0, 1)
        sounds_tab.setLayout(sounds_tab_layout)


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
