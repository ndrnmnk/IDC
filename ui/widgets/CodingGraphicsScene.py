from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QApplication
from ui.widgets.BlockBase import BlockBase


class DraggableProxyWidget(QGraphicsProxyWidget):
    def __init__(self, parent=None):
        super(DraggableProxyWidget, self).__init__(parent)
        self.setFlag(QGraphicsProxyWidget.ItemIsMovable, True)
        self.setFlag(QGraphicsProxyWidget.ItemIsSelectable, True)
        self.setFlag(QGraphicsProxyWidget.ItemSendsGeometryChanges, True)

        self.is_dragging = False
        self.start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.widget():
                widget_under_mouse = self.widget().childAt(event.pos().toPoint())
                if widget_under_mouse:
                    widget_under_mouse.setFocus()

            self.is_dragging = True
            self.start_pos = event.pos()
            self.setZValue(1)
            event.accept()
        else:
            super(DraggableProxyWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_dragging:
            delta = event.pos() - self.start_pos
            self.moveBy(delta.x(), delta.y())
            event.accept()
        else:
            super(DraggableProxyWidget, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.setZValue(0)
            event.accept()
        else:
            super(DraggableProxyWidget, self).mouseReleaseEvent(event)


class CodingGraphicsView(QGraphicsView):
    def __init__(self, block_configs, parent=None):
        super(CodingGraphicsView, self).__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Create and add blocks to the scene
        for config in block_configs:
            self.add_block(config)

    def add_block(self, config):
        # Create BlockBase instance with the provided configuration
        block_widget = BlockBase(config["input_json"], color=config["color"], shape=config["shape"])

        # Make the BlockBase widget's background transparent
        block_widget.setAttribute(Qt.WA_TranslucentBackground)

        # Create and configure the DraggableProxyWidget
        proxy_widget = DraggableProxyWidget()
        proxy_widget.setWidget(block_widget)

        # Add the proxy widget to the scene
        self.scene.addItem(proxy_widget)
        proxy_widget.setPos(*config["pos"])  # Position the widget


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    test_json = [
            {"input_json": [
                {"text": "Hello, World"},
                {"dropdown": ["hello", "bye", "this is a very long one"]},
                {"int_entry": "number typing?"},
                {"text": "test!"},
                {"text_entry": "text entry"}
            ], "color": "#ffff00", "shape": "block", "pos": (100, 100)},
            {"input_json": [
                {"text": "Say"},
                {"text_entry": "hello"}
            ], "color": "#0aef67", "shape": "int", "pos": (300, 300)}
        ]

    view = CodingGraphicsView(block_configs=test_json)
    view.setGeometry(100, 100, 800, 600)
    view.show()
    sys.exit(app.exec_())
