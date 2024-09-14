from PyQt5.QtWidgets import QLabel, QGridLayout


def create_code_tab():
    code_tab_layout = QGridLayout()
    label0 = QLabel("Block to pick")
    label1 = QLabel("Code here")
    label0.setStyleSheet('background-color: pink;')
    label1.setStyleSheet('background-color: grey;')
    code_tab_layout.setColumnStretch(0, 1)
    code_tab_layout.setColumnStretch(1, 4)
    code_tab_layout.addWidget(label0, 0, 0)
    code_tab_layout.addWidget(label1, 0, 1)
    return code_tab_layout
