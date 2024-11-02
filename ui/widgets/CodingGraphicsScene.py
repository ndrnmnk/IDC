from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QPointF
import sys

from ui.widgets.BlockBase import BlockBase


class DraggableBlockView(QGraphicsView):
    def __init__(self, block_data):
        super().__init__()

        # Create a scene
        self.scene = QGraphicsScene(self)
        self.setSceneRect(0, 0, 10000, 10000)
        self.setScene(self.scene)

        # Add blocks
        self.add_blocks(block_data)

    def add_blocks(self, block_data):
        for block_info in block_data:
            block_proxy = DraggableBlock(block_info)
            self.scene.addItem(block_proxy)


class DraggableBlock(QGraphicsProxyWidget):
    def __init__(self, block_data):
        super().__init__()
        block = BlockBase(block_data["data"], block_data["color"])
        self.setWidget(block)
        self.setPos(*block_data["pos"])

        # Dragging variables
        self.dragging = False
        self.drag_offset = QPointF()
        self.top_snap = None
        self.bottom_snap = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.release_top_snap()
            self.update_snapped_pos()
            self.snapToOthers()
            self.dragging = True
            self.drag_offset = event.pos() - self.rect().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToScene(event.pos() - self.drag_offset)
            self.setPos(new_pos)
            self.release_top_snap()
            self.snapToOthers()
            self.update_snapped_pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
        else:
            event.ignore()

    def snapToOthers(self):
        scene = self.scene()
        for item in scene.items():
            if item is self:
                continue

            self_rect = self.sceneBoundingRect()
            other_rect = item.sceneBoundingRect()

            # Check snapping conditions
            if abs(self_rect.top() - other_rect.bottom()) < 15 \
                    and abs(self_rect.left() - other_rect.left()) < 45:
                self.setPos(other_rect.left(), other_rect.bottom()-5)
                self.update_snapped_pos()
                self.top_snap = item
                item.bottom_snap = self

    def update_snapped_pos(self):
        if self.top_snap is not None:
            self.setPos(self.top_snap.sceneBoundingRect().left(), self.top_snap.sceneBoundingRect().bottom()-5)
        if self.bottom_snap is not None:
            self.bottom_snap.update_snapped_pos()

    def release_top_snap(self):
        if self.top_snap is not None:
            self.top_snap.bottom_snap = None
            self.top_snap = None



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Example JSON for multiple blocks
    block_data = [
        {
            "data": [
                {"text": "Hello, World"},
                {"dropdown": ["hello", "bye", "this is a very long one"]},
                {"int_entry": "number typing?"},
                {"text": "test!"},
                {"text_entry": "text entry"}
            ],
            "color": "#00ffff",
            "pos": (100, 100)
        },
        {
            "data": [
                {"text": "Say"},
                {"text_entry": "hello"}
            ],
            "color": "#0aef67",
            "pos": (300, 300)
        }
    ]

    # Create and display the DraggableBlockView window with block_data
    view = DraggableBlockView(block_data)
    view.setWindowTitle("Draggable Blocks")
    view.resize(800, 600)
    view.show()

    sys.exit(app.exec_())
