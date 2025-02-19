from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from ui.widgets.Block import Block


class CodingGraphicsScene(QGraphicsScene):
	def __init__(self, parent_view):
		super().__init__()
		self.view = parent_view
		self.setSceneRect(0, 0, 10000, 10000)


class WorkspaceView(QGraphicsView):
	def __init__(self):
		super().__init__()
		scene = CodingGraphicsScene(self)
		self.setScene(scene)
		self.centerOn(0, 0)
		self.block_list = []
		self.load_block_menu()

	def load_block_menu(self):
		pass

	def add_blocks(self, all_blocks_list):
		for block_json in all_blocks_list:
			self.add_block(block_json, True)

	def add_block(self, block_json, spawner=False):
		self.block_list.append(Block(self, block_json, spawner))
		self.scene().addItem(self.block_list[-1])
		self.block_list[-1].setPos(*block_json["pos"])


if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	app = QApplication([])
	view = WorkspaceView()
	view.setMinimumSize(1000, 1000)
	view.show()

	json1 = {
		"shape": 0,
		"pos": [20, 20],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"dropdown": ["hgfghgfghgfghgf", "run"]},
				{"text": "whatever"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			],
			[
				{"text": "if"},
				{"bool_entry": "0"}
			],
			[
				{"text": "elif"},
				{"bool_entry": "0"}
			],
			[
				{"text": "else"}
			],
			[
				{"text": "why do you need so much layers"}
			]
		]}

	json2 = {
		"shape": 0,
		"pos": [20, 300],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "Move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			]
		]}

	json3 = {
		"shape": 0,
		"pos": [20, 600],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			],
			[
				{"text": "if"},
				{"bool_entry": "0"}
			],
			[
				{"text": "elif"},
				{"bool_entry": "0"}
			],
			[
				{"text": "else"}
			],
			[
				{"text": "why do you need so much layers"}
			]
		]}

	json4 = {
		"shape": 0,
		"pos": [20, 900],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "Move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			]
		]}

	json5 = {
		"shape": 2,
		"pos": [20, 1200],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			],
			[
				{"text": "if"},
				{"bool_entry": "0"}
			],
			[
				{"text": "elif"},
				{"bool_entry": "0"}
			],
			[
				{"text": "else"}
			],
			[
				{"text": "why do you need so much layers"}
			]
		]}

	json6 = {
		"shape": 2,
		"pos": [20, 1500],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "Move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			]
		]}

	json7 = {
		"shape": 3,
		"pos": [20, 1800],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			],
			[
				{"text": "икщ ащкпще ещ срфтпу еру лунищфкв дфнщге *ісгдд*"}
			]
		]}

	json8 = {
		"shape": 3,
		"pos": [20, 2100],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "Move"},
				{"int_entry": "10"},
				{"text": "steps to"},
				{"text_entry": "WW3"},
				{"text": "that will begin in"},
				{"bool_entry": "0"}
			]
		]}

	json9 = {
		"shape": 1,
		"pos": [20, 2400],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text": "hhhhhhhhhhhhhhhhhhhhhhhhh"}
			]
		]}

	json10 = {
		"shape": 0,
		"pos": [20, 2700],
		"internal_name": "move_n_steps",
		"color": "#888888",
		"data": [
			[
				{"text_entry": "text entry only?"}
			],
			[
				{"text": "no, there is a second layer."}
			]
		]}

	view.add_blocks([json1, json2, json3, json4, json5, json6, json7, json8, json9, json10])
	# view.add_blocks([json9, json10])

	window = view
	app.exec_()
