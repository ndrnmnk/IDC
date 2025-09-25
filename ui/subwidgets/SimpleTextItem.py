from PyQt5.QtWidgets import QGraphicsSimpleTextItem

class SimpleTextItem(QGraphicsSimpleTextItem):
	def __init__(self, text, parent):
		super().__init__(text, parent=parent)

	def deleteLater(self):
		self.scene().removeItem(self)
		del self