from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PyQt5.QtGui import QPainterPath, QPen, QPainter
from PyQt5.QtCore import Qt, QPointF
import sys


class PreviewLine(QGraphicsLineItem):
	def __init__(self, pos, width):
		super().__init__()
		self.setPos(pos)

		# Create the path with the specified points
		path = QPainterPath()
		points = [
			QPointF(0, 0),
			QPointF(10, 0),
			QPointF(10, 5),
			QPointF(40, 5),
			QPointF(40, 0),
			QPointF(width, 0)
		]

		# Move to the first point and add lines to each subsequent point
		path.moveTo(points[0])
		for point in points[1:]:
			path.lineTo(point)

		# Store the path in this item
		self.setPath(path)
		self.setPen(QPen(Qt.blue, 3))  # Set line color and thickness

	def setPath(self, path):
		"""Sets the path for the line item."""
		self.path = path  # Store for drawing

	def boundingRect(self):
		"""Bounding rectangle for the line item."""
		return self.path.boundingRect()

	def paint(self, painter, option, widget=None):
		"""Draws the path."""
		painter.setPen(self.pen())
		painter.drawPath(self.path)


# Main application window
class MainWindow(QGraphicsView):
	def __init__(self):
		super().__init__()

		# Create scene and set view
		self.scene = QGraphicsScene()
		self.setScene(self.scene)

		# Set view properties
		self.setRenderHint(QPainter.Antialiasing)

		# Create and add the custom line to the scene
		line = PreviewLine(80)  # You can change the width as needed
		self.scene.addItem(line)

		# Center the view on the line
		self.setSceneRect(line.boundingRect())


# Application execution
if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
