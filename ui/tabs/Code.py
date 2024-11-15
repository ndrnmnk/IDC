from PyQt5.QtWidgets import QLabel, QGridLayout
from ui.widgets.CodingGraphicsScene import DraggableBlockView


class CodeTabLayout(QGridLayout):
	def __init__(self):
		super().__init__()
		self.setColumnStretch(0, 1)
		self.setColumnStretch(1, 4)

		label_blocks_to_pick = QLabel("Block to pick")
		label_blocks_to_pick.setStyleSheet('background-color: grey;')

		self.addWidget(label_blocks_to_pick, 0, 0)

		test_json = [
			{"data": [
				{"text": "Hello, World"},
				{"dropdown": ["hello", "bye", "this is a very long one"]},
				{"int_entry": "number typing?"},
				{"text": "test!"},
				{"text_entry": "text entry"}
			], "internal_name": "test", "color": "#00ffff", "shape": 0, "pos": (100, 100)},
			{"data": [
				{"text": "Say"},
				{"text_entry": "hello"}
			], "internal_name": "say_bla", "color": "#0aef67", "shape": 1, "pos": (100, 200)},
			{"data": [
				{"text": "Move"},
				{"int_entry": "10"},
				{"text": "steps"}
			], "internal_name": "move_x", "color": "#ff0000", "shape": 4, "pos": (100, 300)},
			{"data": [
				{"text": "Rotate"},
				{"int_entry": "angle"}
			], "internal_name": "rotate_x", "color": "#ff00ff", "shape": 3, "pos": (100, 400)},
			{"data": [
				{"text": "expand"},
				{"int_entry": "%"},
			], "internal_name": "expand_x", "color": "#0000ff", "shape": 2, "pos": (100, 500)}
		]

		# view = CodingGraphicsView(block_configs=test_json)
		view = DraggableBlockView(test_json)

		self.addWidget(view, 0, 1)
