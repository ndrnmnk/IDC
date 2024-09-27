from PyQt5.QtWidgets import QLabel, QGridLayout
from ui.widgets.CodingGraphicsScene import CodingGraphicsView


class CodeTabLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 4)

        label_blocks_to_pick = QLabel("Block to pick")
        label_blocks_to_pick.setStyleSheet('background-color: grey;')

        self.addWidget(label_blocks_to_pick, 0, 0)

        test_json = [
            {"input_json": [
                {"text": "Hello, World"},
                {"dropdown": ["hello", "bye", "this is a very long one"]},
                {"int_entry": "number typing?"},
                {"text": "test!"},
                {"text_entry": "text entry"}
            ], "color": "#888888", "shape": "block", "pos": (100, 100)},
            {"input_json": [
                {"text": "Say"},
                {"text_entry": "hello"}
            ], "color": "#0aef67", "shape": "int", "pos": (300, 300)}
        ]

        view = CodingGraphicsView(block_configs=test_json)

        self.addWidget(view, 0, 1)
