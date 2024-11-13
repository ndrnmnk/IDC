from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsProxyWidget
from PyQt5.QtGui import QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPointF
import sys

from ui.widgets.BlockBase import BlockBase
from ui.widgets.PreviewLine import PreviewLine


class DraggableBlockView(QGraphicsView):
    def __init__(self, block_data):
        super().__init__()

        # create a scene
        self.scene = QGraphicsScene(self)
        self.setSceneRect(0, 0, 10000, 10000)
        self.setScene(self.scene)
        self.centerOn(0, 0)

        # variables
        self.all_array = []
        self.starter_array = []

        # Add blocks
        self.add_blocks(block_data)

    def add_blocks(self, block_data):
        for idx, block_info in enumerate(block_data):
            self.all_array.append(DraggableBlock(block_info))
            self.scene.addItem(self.all_array[idx])
            if block_info["shape"] == 2:
                self.starter_array.append(idx)


class DraggableBlock(QGraphicsProxyWidget):
    def __init__(self, block_data):
        super().__init__()
        block = BlockBase(block_data["data"], block_data["internal_name"], block_data["color"], block_data["shape"])
        self.setWidget(block)
        self.setPos(*block_data["pos"])

        # get initial block hitbox
        self.block_polygon = self.calculate_block_polygon(block)
        # make hitbox dynamic
        block.sizeChanged.connect(self.update_polygon)

        # dragging variables
        self.drag_offset = QPointF()

        # snapping variables
        self.allow_top_snap = (block_data["shape"] not in [2, 3, 4])
        self.allow_bottom_snap = (block_data["shape"] not in [1, 3, 4])
        self.top_snap = None
        self.bottom_snap = None
        self.snap_candidate = None
        self.preview_line = None

    @staticmethod
    def calculate_block_polygon(block):
        # get new hitbox
        polygon_points = block.generate_polygon_points()
        return QPolygonF(polygon_points)

    def update_polygon(self):
        # update the hitbox
        self.block_polygon = self.calculate_block_polygon(self.widget())
        self.update()

    def shape(self):
        # overwrite default rectangle with new hitbox
        path = QPainterPath()
        path.addPolygon(self.block_polygon)
        return path

    def mousePressEvent(self, event):
        # start drag and checking for snap
        if event.button() == Qt.LeftButton:
            if self.allow_top_snap is True:
                self.release_top_snap()
                self.snapToOthers()
            self.update_snapped_pos()
            self.drag_offset = event.pos() - self.rect().topLeft()

    def mouseMoveEvent(self, event):
        # drag
        new_pos = self.mapToScene(event.pos() - self.drag_offset)
        self.setPos(new_pos)
        # snap
        if self.allow_top_snap is True:
            self.release_top_snap()
            self.snapToOthers()
        self.update_snapped_pos()

    def mouseReleaseEvent(self, event):
        # finalize snap
        self.clear_preview_line()
        if self.snap_candidate is not None:
            if self.snap_candidate.bottom_snap is not None:
                if self.allow_bottom_snap:
                    self.snap_candidate.bottom_snap.top_snap = self.get_last_widget()
                    self.get_last_widget().bottom_snap = self.snap_candidate.bottom_snap
                else:
                    self.snap_candidate.bottom_snap.top_snap = None
            self.setPos(self.snap_candidate.sceneBoundingRect().left(), self.snap_candidate.sceneBoundingRect().bottom() - 5)
            self.update_snapped_pos()
            self.top_snap = self.snap_candidate
            self.snap_candidate.bottom_snap = self
            self.snap_candidate = None

    def snapToOthers(self):
        for item in self.scene().items():
            if item in [self, self.preview_line, self.snap_candidate]:
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
                self.scene().addItem(self.preview_line)

        if self.snap_candidate is not None and not self.check_item_for_snap(self.snap_candidate):
            self.clear_preview_line()
            self.snap_candidate = None

    def check_item_for_snap(self, item):
        self_rect = self.sceneBoundingRect()
        other_rect = item.sceneBoundingRect()
        if abs(self_rect.top() - other_rect.bottom()) < 15 \
                and abs(self_rect.left() - other_rect.left()) < 45:
            if item.allow_bottom_snap:
                return True
        return False

    def update_snapped_pos(self):
        # chains down updating positions
        if self.top_snap is not None:
            self.setPos(self.top_snap.sceneBoundingRect().left(), self.top_snap.sceneBoundingRect().bottom()-5)
        if self.bottom_snap is not None:
            self.bottom_snap.update_snapped_pos()

    def release_top_snap(self):
        if self.top_snap is not None:
            self.top_snap.bottom_snap = None
            self.top_snap = None

    def get_last_widget(self):
        if self.bottom_snap is not None:
            return self.bottom_snap.get_last_widget()
        return self

    def clear_preview_line(self):
        if self.preview_line is not None:
            self.scene().removeItem(self.preview_line)
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
