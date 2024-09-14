import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsPolygonItem, QGraphicsProxyWidget, QLineEdit
from PyQt5.QtGui import QPolygonF, QBrush
from PyQt5.QtCore import QPointF, Qt
from ui.subwidgets.ResizableLineEdit import ResizableLineEdit

class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Create the scene
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        x = 10
        y = 10
        width = 100
        height = 40
        # Define the polygon
        points = [
            QPointF(x, y),  # Top-left corner
            QPointF(x + 10, y),  # Start of the pit
            QPointF(x + 10, y + 10),  # Bottom-left of pit
            QPointF(x + 40, y + 10),  # Bottom-right of pit
            QPointF(x + 40, y),  # Exit from the pit
            QPointF(x + width, y),  # Top-right corner
            QPointF(x + width, y + height),  # Bottom-right corner
            QPointF(x + 40, y + height),  # Start of bulge
            QPointF(x + 40, y + height + 10),  # Bottom-right of bulge
            QPointF(x + 10, y + height + 10),  # Bottom-left of bulge
            QPointF(x + 10, y + height),  # End of bulge
            QPointF(x, y + height)  # Bottom-left corner
        ]
        polygon = QPolygonF(points)

        # Create a polygon item
        self.polygon_item = QGraphicsPolygonItem(polygon)
        self.polygon_item.setBrush(QBrush(Qt.yellow))
        self.polygon_item.setFlags(QGraphicsPolygonItem.ItemIsMovable | QGraphicsPolygonItem.ItemIsSelectable)
        self.scene.addItem(self.polygon_item)

        # Create a QLineEdit and embed it into the scene
        self.line_edit = ResizableLineEdit()
        self.line_edit.setPlaceholderText("10")
        proxy_widget = QGraphicsProxyWidget(self.polygon_item)
        proxy_widget.setWidget(self.line_edit)
        proxy_widget.setPos(x+5, height/2+y-5)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = GraphicsView()
    view.show()
    sys.exit(app.exec_())
