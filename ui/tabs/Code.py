from PyQt5.QtWidgets import QGridLayout
from ui.widgets.CodingGraphicsScene import WorkspaceView


class CodeTabLayout(QGridLayout):
	def __init__(self):
		super().__init__()
		self.setColumnStretch(0, 4)

		self.view = WorkspaceView()

		self.addWidget(self.view, 0, 0)
