from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtCore import Qt, QPointF
import sys

from ui.widgets.BlockBase import BlockBase
from ui.widgets.PreviewLine import PreviewLine


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
            block_proxy = DraggableBlock(self.scene, block_info)
            self.scene.addItem(block_proxy)


class DraggableBlock(QGraphicsProxyWidget):
    def __init__(self, parent_scene, block_data):
        super().__init__()
        self.parent_scene = parent_scene
        block = BlockBase(block_data["data"], block_data["internal_name"], block_data["color"], block_data["shape"])
        self.setWidget(block)
        self.setPos(*block_data["pos"])

        # Dragging variables
        self.dragging = False
        self.drag_offset = QPointF()

        # Snapping variables
        if block_data["shape"] == 2:
            self.allow_top_snap = False
        else:
            self.allow_top_snap = True
        self.top_snap = None
        if block_data["shape"] == 1:
            self.bottom_snap = False
        else:
            self.bottom_snap = None
        self.snap_candidate = None
        self.preview_line = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.allow_top_snap is True:
                self.release_top_snap()
                self.snapToOthers()
            self.update_snapped_pos()
            self.dragging = True
            self.drag_offset = event.pos() - self.rect().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = self.mapToScene(event.pos() - self.drag_offset)
            self.setPos(new_pos)
            if self.allow_top_snap is True:
                self.release_top_snap()
                self.snapToOthers()
            self.update_snapped_pos()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.clear_preview_line()
        if self.snap_candidate is not None:
            if self.snap_candidate.bottom_snap is not None:
                if self.bottom_snap is not False:
                    self.snap_candidate.bottom_snap.top_snap = self.get_last_widget()
                    self.get_last_widget().bottom_snap = self.snap_candidate.bottom_snap
                else:
                    self.snap_candidate.bottom_snap.top_snap = None
            self.setPos(self.snap_candidate.sceneBoundingRect().left(), self.snap_candidate.sceneBoundingRect().bottom() - 5)
            self.update_snapped_pos()
            self.top_snap = self.snap_candidate
            self.snap_candidate.bottom_snap = self
            self.snap_candidate = None
        # print(self.widget().get_internal_name())

    def snapToOthers(self):
        scene = self.scene()
        for item in scene.items():
            if item is self or item is self.preview_line or item is self.snap_candidate:
                continue

            if self.check_item_for_snap(item):
                self.snap_candidate = item
                self.clear_preview_line()
                try:
                    line_width = min(item.widget().width(), item.bottom_snap.widget().width()) - 5
                except AttributeError:
                    line_width = item.widget().width() - 5
                self.preview_line = PreviewLine(QPointF(item.sceneBoundingRect().left(), item.sceneBoundingRect().bottom()-5), line_width)
                self.preview_line.setZValue(1)
                self.parent_scene.addItem(self.preview_line)

        if self.snap_candidate is not None and not self.check_item_for_snap(self.snap_candidate):
            self.clear_preview_line()
            self.snap_candidate = None

    def check_item_for_snap(self, item):
        self_rect = self.sceneBoundingRect()
        other_rect = item.sceneBoundingRect()
        if abs(self_rect.top() - other_rect.bottom()) < 15 \
                and abs(self_rect.left() - other_rect.left()) < 45:
            if item.bottom_snap is not False:
                return True
        return False

    def update_snapped_pos(self):
        if self.top_snap is not None:
            self.setPos(self.top_snap.sceneBoundingRect().left(), self.top_snap.sceneBoundingRect().bottom()-5)
        if self.bottom_snap is not None and self.bottom_snap is not False:
            self.bottom_snap.update_snapped_pos()

    def release_top_snap(self):
        if self.top_snap is not None:
            self.top_snap.bottom_snap = None
            self.top_snap = None

    def get_last_widget(self):
        if self.bottom_snap is not None and self.bottom_snap is not False:
            return self.bottom_snap.get_last_widget()
        return self

    def clear_preview_line(self):
        if self.preview_line is not None:
            self.parent_scene.removeItem(self.preview_line)
            self.preview_line = None


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
            "shape": 0,
            "internal_name": "test",
            "color": "#00ffff",
            "pos": (100, 100)
        },
        {
            "data": [
                {"text": "Say"},
                {"text_entry": "hello"}
            ],
            "shape": 0,
            "internal_name": "say_bla",
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
