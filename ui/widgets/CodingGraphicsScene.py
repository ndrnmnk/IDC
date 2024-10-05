from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QPointF
import sys

# Import BlockBase from the previous code
from ui.widgets.BlockBase import BlockBase


class DraggableBlockView(QGraphicsView):
    def __init__(self, block_data):
        super().__init__()

        # Create a scene to hold items
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Variables for tracking drag state and offsets
        self.dragging = False
        self.drag_offset = QPointF()
        self.dragged_item = None

        # Add multiple blocks to the scene based on block_data
        self.add_blocks(block_data)

        # Enable smoother dragging visuals
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def add_blocks(self, block_data):
        """
        Adds multiple BlockBase widgets to the scene, based on block_data.
        Each block will have its own position, content, and color.
        """
        for block_info in block_data:
            input_json = block_info.get("input_json", [])
            color = block_info.get("color", "#000000")  # Default color if not specified
            pos = block_info.get("pos", (0, 0))  # Default position if not specified

            # Create a BlockBase widget with input_json and color
            block_widget = BlockBase(input_json, color=color)

            # Add the BlockBase widget to the scene via QGraphicsProxyWidget
            block_proxy = QGraphicsProxyWidget()
            block_proxy.setWidget(block_widget)
            block_proxy.setPos(*pos)  # Set the initial position of the block

            # Add the block_proxy to the scene
            self.scene.addItem(block_proxy)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Check if the click is inside any block proxy's area
            clicked_item = self.itemAt(event.pos())
            if isinstance(clicked_item, QGraphicsProxyWidget):
                self.dragging = True
                self.dragged_item = clicked_item
                # Calculate offset to keep relative position while dragging
                self.drag_offset = self.dragged_item.pos() - self.mapToScene(event.pos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging and self.dragged_item:
            # Update block position based on mouse movement
            new_pos = self.mapToScene(event.pos()) + self.drag_offset
            self.dragged_item.setPos(new_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Stop dragging
            self.dragging = False
            self.dragged_item = None
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example JSON for multiple blocks
    block_data = [
        {
            "input_json": [
                {"text": "Hello, World"},
                {"dropdown": ["hello", "bye", "this is a very long one"]},
                {"int_entry": "number typing?"},
                {"text": "test!"},
                {"text_entry": "text entry"}
            ],
            "color": "#888888",
            "pos": (100, 100)
        },
        {
            "input_json": [
                {"text": "Say"},
                {"text_entry": "hello"}
            ],
            "color": "#0aef67",
            "pos": (300, 300)
        }
    ]

    # Create and display the DraggableBlockView window with block_data
    view = DraggableBlockView(block_data)
    view.setWindowTitle("Draggable Multiple BlockBase on QGraphicsView")
    view.resize(800, 600)
    view.show()

    sys.exit(app.exec_())
