from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QBrush, QPen, QColor, QPainter, QPainterPath
from PyQt5.QtCore import Qt

class Minimap(QGraphicsView):
	def __init__(self, wv, ws):
		super().__init__(parent=wv)
		self.setScene(ws)
		self.workspace_view = wv
		self.setRenderHint(QPainter.Antialiasing, True)

		# self.fitInView(self.sceneRect()) breaks everything, so calculating scale factor manually

		self.target_size = 250
		self.scale_factor = self.target_size / 10_000  # 10_000 stands for scene size
		self.scale(self.scale_factor, self.scale_factor)

		self.setRenderHints(self.renderHints())
		self.setDragMode(QGraphicsView.NoDrag)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setInteractive(False)

	def drawForeground(self, painter, rect):
		super().drawForeground(painter, rect)
		# Get workspace visible rect in scene coordinates
		visible_rect = self.workspace_view.mapToScene(self.workspace_view.viewport().rect()).boundingRect()

		full_scene_rect = self.sceneRect()

		# Create a path that contains both rectangles
		path = QPainterPath()
		path.addRect(full_scene_rect)
		path.addRect(visible_rect)

		# Use OddEvenFill rule. This fills the area inside the first rectangle
		# but outside the second, creating a "mask with a hole".
		path.setFillRule(Qt.OddEvenFill)

		# Set the painter to fill with a semi-transparent black color
		painter.setBrush(QBrush(QColor(0, 0, 0, 50)))  # Adjust alpha (150) for more/less darkness
		painter.setPen(Qt.NoPen)  # No outline for the mask itself
		painter.drawPath(path)

		# --- Draw a bright border for the viewport for better visibility ---

		# Use a cosmetic pen so its width is in pixels, not affected by scene scaling
		pen = QPen(QColor(255, 255, 255, 220), 2)
		pen.setCosmetic(True)

		painter.setPen(pen)
		painter.setBrush(Qt.NoBrush)  # We only want the outline
		painter.drawRect(visible_rect)

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			pos_x = event.pos().x() / self.scale_factor
			pos_y = event.pos().y() / self.scale_factor
			self.workspace_view.centerOn(pos_x, pos_y)
	def update_pos(self):
		pos_x = self.workspace_view.viewport().x() + self.workspace_view.viewport().width() - self.target_size
		pos_y = self.workspace_view.viewport().y() + self.workspace_view.viewport().height() - self.target_size
		self.setGeometry(pos_x, pos_y, self.target_size, self.target_size)