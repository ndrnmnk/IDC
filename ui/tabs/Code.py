from PyQt5.QtWidgets import QLabel, QGridLayout
from ui.widgets.CodingGraphicsScene import CodingGraphicsView


def create_code_tab():
    code_tab_layout = QGridLayout()
    label0 = QLabel("Block to pick")
    label0.setStyleSheet('background-color: grey;')
    code_tab_layout.setColumnStretch(0, 1)
    code_tab_layout.setColumnStretch(1, 4)
    code_tab_layout.addWidget(label0, 0, 0)

    test_json = [
            {"input_json": [
                {"text": "Hello, World"},
                {"dropdown": ["hello", "bye", "this is a very long one"]},
                {"int_entry": "number typing?"},
                {"text": "test!"},
                {"text_entry": "text entry"}
            ], "color": "#ffff00", "shape": "block", "pos": (100, 100)},
            {"input_json": [
                {"text": "Say"},
                {"text_entry": "hello"}
            ], "color": "#0aef67", "shape": "int", "pos": (300, 300)}
        ]
    view = CodingGraphicsView(block_configs=test_json)

    code_tab_layout.addWidget(view, 0, 1)
    return code_tab_layout
