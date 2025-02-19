from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor
from ui.widgets.Block import Block


class CodingGraphicsScene(QGraphicsScene):
	def __init__(self, parent_view):
		super().__init__()
		self.view = parent_view
		self.setSceneRect(0, 0, 10000, 10000)

		self.BlockMenu = QGraphicsRectItem(0, 0, 300, 1000)
		self.BlockMenu.setBrush(QBrush(QColor("#eeeeee")))
		self.BlockMenu.setZValue(1)
		self.addItem(self.BlockMenu)


class WorkspaceView(QGraphicsView):
	def __init__(self):
		super().__init__()
		scene = CodingGraphicsScene(self)
		self.setScene(scene)
		self.centerOn(0, 0)
		self.block_list = []
		self.menu_block_list = []

	def load_block_menu(self, menu_blocks_list):
		t = 10
		for block_json in menu_blocks_list:
			block_json["pos"] = [10, t]
			t += self.add_block(block_json, True) + 20

	def add_blocks(self, all_blocks_list):
		for block_json in all_blocks_list:
			self.add_block(block_json, False)

	def add_block(self, block_json, spawner):
		if spawner:
			self.menu_block_list.append(Block(self, block_json, True))
			self.scene().addItem(self.menu_block_list[-1])
			self.menu_block_list[-1].setPos(*block_json["pos"])
			return self.menu_block_list[-1].boundingRect().height()
		else:
			self.block_list.append(Block(self, block_json, False))
			self.scene().addItem(self.block_list[-1])
			self.block_list[-1].setPos(*block_json["pos"])
			return 0

	def check_block_for_deletion(self, caller):
		if caller.pos().x() + 20 < self.scene().BlockMenu.sceneBoundingRect().right():
			caller.deleteLater()
			self.block_list.remove(caller)

	def updateRectPos(self):
		# Convert the top-left corner of the viewport (0,0) to scene coordinates
		top_left_scene = self.mapToScene(0, 0)
		# Position the rectangle at that point
		self.scene().BlockMenu.setPos(top_left_scene)

	def scrollContentsBy(self, dx, dy):
		# First, perform the default scroll behavior
		super().scrollContentsBy(dx, dy)
		# Then, reposition the rectangle so it stays in the top left of the visible area
		self.updateRectPos()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		# Also update the rectangle position when the view is resized
		self.updateRectPos()


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
