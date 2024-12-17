from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsView, QGraphicsScene, QApplication, QGraphicsItem
from PyQt5.QtGui import QBrush, QColor

from ui.widgets.DraggableBlock import DraggableBlock


class BlockMenu(QGraphicsRectItem):
	def __init__(self, height):
		super().__init__(0, 0, 300, height)
		self.width = 300
		self.setBrush(QBrush(QColor("#EEEEEE")))
		self.setFlag(QGraphicsItem.ItemIgnoresTransformations, True)
		self.setZValue(4)
		self.show()


class WorkspaceScene(QGraphicsScene):
	def __init__(self):
		super().__init__()
		self.menu = BlockMenu(10000)
		self.addItem(self.menu)

	def update_menu_pos(self, view_rect):
		self.menu.setPos(view_rect.left(), view_rect.top())

	def block_placed_in_menu(self, block):
		if block.pos().x() + 20 < self.menu.width + self.menu.pos().x():
			return True
		return False


class WorkspaceView(QGraphicsView):
	def __init__(self, menu_blocks=[]):
		super().__init__()
		self.scene_widget = WorkspaceScene()
		self.setScene(self.scene_widget)
		self.scene_widget.setSceneRect(0, 0, 10000, 10000)
		self.centerOn(0, 0)
		self.block_array = []
		self.add_blocks(menu_blocks)

	def drawForeground(self, painter, rect):
		# Use the visible rect of the view, which is stable during dragging
		view_rect = self.mapToScene(self.viewport().rect()).boundingRect()
		self.scene_widget.update_menu_pos(view_rect)

	def add_blocks(self, block_data_arr):
		for block_data in block_data_arr:
			if self.block_array:
				block_pos = (10, self.block_array[-1].sceneBoundingRect().bottom()+10)
			else:
				block_pos = 10, 10
			block_data["pos"] = list(block_pos)
			self.add_block(block_data, block_pos, menu=True)

	def add_block(self, block_data, pos=None, menu=False):
		if not pos:
			pos = block_data["pos"]

		t = DraggableBlock(block_data, self, menu)
		self.scene().addItem(t)
		if menu:
			t.setParentItem(self.scene_widget.menu)
			t.setZValue(5)
		self.block_array.append(t)


if __name__ == "__main__":
	app = QApplication([])
	window = WorkspaceView()

	test_json = [
		{
			"data": [
				{"text": "Hello, World"},
				{"dropdown": ["hello", "bye", "this is a very long one"]},
				{"int_entry": "number typing?"},
				{"text": "test!"},
				{"text_entry": "text entry"}
			],
			"shape": 0,
			"internal_name": "test",
			"color": "#00ffff",
			"pos": [10, 10]
		},
		{
			"data": [
				{"text": "Say"},
				{"text_entry": "hello"}
			],
			"shape": 3,
			"internal_name": "say_bla",
			"color": "#0aef67",
			"pos": [10, 0]
		},
		{
			"data": [
				{"text": "Hello, World"},
				{"dropdown": ["hello", "bye", "this is a very long one"]},
				{"int_entry": "number typing?"},
				{"text": "test!"},
				{"text_entry": "text entry"}
			],
			"shape": 2,
			"internal_name": "test",
			"color": "#00ffff",
			"pos": [10, 0]
		},
		{
			"data": [
				{"text": "Say"},
				{"text_entry": "hello"}
			],
			"shape": 1,
			"internal_name": "say_bla",
			"color": "#0aef67",
			"pos": [10, 0]
		}
	]

	window.add_blocks(test_json)
	window.show()
	app.exec_()
