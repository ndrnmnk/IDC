from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QBrush, QColor, QWheelEvent
from ui.widgets.Block import Block


class BlockMenu(QGraphicsRectItem):
	def __init__(self):
		super().__init__(0, 0, 300, 10000)
		self.setBrush(QBrush(QColor("#eeeeee")))
		self.setZValue(1)

		self.offset = 0
		self.max_offset = 0
		self.view_height = 0

	def wheelEvent(self, event: QWheelEvent):
		# Determine the scroll direction
		self.offset += event.delta()
		self.offset = min(0, self.offset)
		self.offset = max(self.view_height-self.max_offset, self.offset)

		event.accept()  # Prevent event propagation
		self.scene().view.updateMenuPos()


class CodingGraphicsScene(QGraphicsScene):
	def __init__(self, parent_view):
		super().__init__()
		self.view = parent_view
		self.setSceneRect(0, 0, 10000, 10000)

		self.menu = BlockMenu()
		self.addItem(self.menu)


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
		self.scene().menu.max_offset = int(t)
		self.scene().menu.view_height = self.viewport().height()

	def add_blocks(self, all_blocks_list):
		for block_json in all_blocks_list:
			self.add_block(block_json, False)

	def add_block(self, block_json, spawner):
		if spawner:
			self.menu_block_list.append(Block(self, block_json, True))
			self.scene().addItem(self.menu_block_list[-1])
			self.menu_block_list[-1].setPos(*block_json["pos"])
			self.menu_block_list[-1].setParentItem(self.scene().menu)
			return self.menu_block_list[-1].boundingRect().height()
		else:
			self.block_list.append(Block(self, block_json, False))
			self.scene().addItem(self.block_list[-1])
			self.block_list[-1].setPos(*block_json["pos"])
			return 0

	def check_block_for_deletion(self, caller):
		if caller.pos().x() + 20 < self.scene().menu.sceneBoundingRect().right():
			caller.suicide()

	def updateMenuPos(self):
		try:
			# Convert the top-left corner of the viewport (0,0) to scene coordinates
			top_left_scene = self.mapToScene(0, self.scene().menu.offset)
			# Position the rectangle at that point
			self.scene().menu.setPos(top_left_scene)
		except:
			print("smt weird happened with menu pos, ignoring")

	def scrollContentsBy(self, dx, dy):
		# First, perform the default scroll behavior
		super().scrollContentsBy(dx, dy)
		# Then, reposition the rectangle so it stays in the top left of the visible area
		self.updateMenuPos()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.scene().menu.view_height = self.viewport().height()
		# Also update the rectangle position when the view is resized
		self.updateMenuPos()
