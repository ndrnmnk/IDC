from PyQt5.QtWidgets import QGraphicsProxyWidget
from PyQt5.QtGui import QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPointF
from ui.widgets.BlockBase import BlockBase
from ui.widgets.PreviewLine import PreviewLine


class DraggableBlock(QGraphicsProxyWidget):
    def __init__(self, block_data, parent_view, spawner=False):
        super().__init__()
        # save the data
        self.parent_view = parent_view
        self.block_data = block_data
        self.block_shape = block_data["shape"]
        # create a base block widget
        block = BlockBase(block_data["data"], block_data["internal_name"], block_data["color"], block_data["shape"])
        self.setWidget(block)
        self.setPos(*block_data["pos"])

        # spawner blocks are used in block menu, when clicked they spawn their copy and become regular blocks
        self.spawner = spawner

        # get initial block hitbox
        self.block_polygon = self.calculate_block_polygon(block)
        # make hitbox dynamic
        block.sizeChanged.connect(self.update_polygon)

        # dragging variables
        self.drag_offset = QPointF()

        # snapping variables
        self.allow_top_snap = False
        self.allow_bottom_snap = False
        self.top_snap = None
        self.bottom_snap = None
        self.snap_candidate = None
        self.preview_line = None
        if not self.spawner:
            self.spawn()

    def spawn(self):
        # turns spawner block into regular one by allowing it to snap to others
        self.spawner = False
        self.allow_top_snap = (self.block_shape not in [2, 3, 4])
        self.allow_bottom_snap = (self.block_shape not in [1, 3, 4])

    @staticmethod
    def calculate_block_polygon(block):
        # get new hitbox
        polygon_points = block.generate_polygon_points()
        return QPolygonF(polygon_points)

    def update_polygon(self):
        # update the hitbox
        self.block_polygon = self.calculate_block_polygon(self.widget())
        self.update()

    def get_height(self):
        return int(self.geometry().height())

    def shape(self):
        # overwrite default rectangle with an actual hitbox
        path = QPainterPath()
        path.addPolygon(self.block_polygon)
        return path

    def mousePressEvent(self, event):
        # if spawner turn to regular block and start drag
        if self.spawner:
            self.setParentItem(None)
            self.parent_view.add_block(self.block_data, self.pos(), True)
            self.spawn()
            self.parent_view.menu_blocks_array.remove(self)
            self.parent_view.regular_blocks_array.append(self)
        else:
            self.setZValue(2)
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
        # check for new snaps
        if self.allow_top_snap is True:
            self.release_top_snap()
            self.snapToOthers()
        self.update_snapped_pos()

    def mouseReleaseEvent(self, event):
        # if dragged to block menu, delete itself
        # elif can snap, snap
        # else just place onto scene
        if self.parent_view.scene().block_placed_in_menu(self):
            self.update_snapped_pos(True)
        # finalize snap
        self.setZValue(1)
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
        # check for available snaps and show preview line
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
                self.scene().addItem(self.preview_line)

        if self.snap_candidate is not None and not self.check_item_for_snap(self.snap_candidate):
            self.clear_preview_line()
            self.snap_candidate = None

    def check_item_for_snap(self, item):
        self_rect = self.sceneBoundingRect()
        other_rect = item.sceneBoundingRect()
        if abs(self_rect.top() - other_rect.bottom()) < 15 \
                and abs(self_rect.left() - other_rect.left()) < 45:
            try:
                if item.allow_bottom_snap:
                    return True
            except AttributeError:
                return False
        return False

    def update_snapped_pos(self, suicide=False):
        # chains down updating positions
        if self.top_snap is not None:
            self.setPos(self.top_snap.sceneBoundingRect().left(), self.top_snap.sceneBoundingRect().bottom()-5)
        if self.bottom_snap is not None:
            self.bottom_snap.update_snapped_pos(suicide)
        if suicide:
            self.suicide()

    def release_top_snap(self):
        if self.top_snap is not None:
            self.top_snap.bottom_snap = None
            self.top_snap = None

    def get_last_widget(self):
        # gets bottom widget in the construction
        if self.bottom_snap is not None:
            return self.bottom_snap.get_last_widget()
        return self

    def clear_preview_line(self):
        if self.preview_line is not None:
            self.scene().removeItem(self.preview_line)
            self.preview_line = None

    def suicide(self):
        # delete this block and remove from lists
        self.clear_preview_line()
        self.scene().removeItem(self)
        self.deleteLater()
        if self.spawner:
            self.parent_view.menu_blocks_array.remove(self)
        else:
            self.parent_view.regular_blocks_array.remove(self)
