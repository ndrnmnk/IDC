from ui.subwidgets.ResizableLineEdit import ResizableLineEdit
from ui.subwidgets.ResizableDropdown import ResizableDropdown
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPainter, QPolygon, QBrush, QColor, QFont, QFontMetrics
from PyQt5.QtCore import QPoint, Qt, QEvent
import sys


class BlockBase(QWidget):
    def __init__(self, input_json, color="#0000FF"):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.color = color
        self.input_json = input_json
        self.font = QFont("Arial", 12)
        self.font_metrics = QFontMetrics(self.font)

        self.width_list = []
        self.content_list = []
        self.height_list = []

        self.hbox = QHBoxLayout()

        self.hbox.setContentsMargins(5, 4, 5, 8)
        self.hbox.setSpacing(5)
        self.setLayout(self.hbox)

        self.populate_block()
        self.installEventFilter(self)

    def populate_block(self):
        for idx, json_object in enumerate(self.input_json):
            if "text" in json_object:
                self.content_list.append(QLabel(json_object["text"], self))
                self.content_list[idx].setFont(self.font)
                self.width_list.append(self.font_metrics.horizontalAdvance(json_object["text"]))
                self.height_list.append(self.font_metrics.height())
            elif "text_entry" in json_object:
                self.content_list.append(ResizableLineEdit(parent=self, placeholder=json_object["text_entry"], int_entry=False))
                self.content_list[idx].textChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
                self.width_list.append(self.content_list[idx].width())
                self.height_list.append(22)
            elif "int_entry" in json_object:
                self.content_list.append(ResizableLineEdit(parent=self, placeholder=json_object["int_entry"], int_entry=True))
                self.content_list[idx].textChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
                self.width_list.append(self.content_list[idx].width())
                self.height_list.append(22)
            elif "bool_entry" in json_object:
                # TODO: replace with actual bool entry
                self.content_list.append(ResizableLineEdit(parent=self, placeholder=json_object["bool_entry"], int_entry=True))
                self.content_list[idx].textChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
                self.width_list.append(self.content_list[idx].width())
                self.height_list.append(22)
            elif "dropdown" in json_object:
                self.content_list.append(ResizableDropdown(parent=self, options=json_object["dropdown"]))
                self.content_list[idx].currentIndexChanged.connect(lambda _, caller_idx=idx: self.repopulate_block(caller_idx))
                self.width_list.append(self.content_list[idx].width())
                self.height_list.append(24)
            self.hbox.addWidget(self.content_list[idx], alignment=Qt.AlignLeft)

    def repopulate_block(self, caller_idx):
        self.width_list[caller_idx] = self.content_list[caller_idx].width()
        self.height_list[caller_idx] = self.content_list[caller_idx].height()
        self.update()
        self.adjustSize()

    def paintEvent(self, event):
        painter = QPainter(self)

        points = self.generate_polygon_points()

        painter.setBrush(QBrush(QColor(self.color)))
        polygon = QPolygon(points)
        painter.drawPolygon(polygon)

    def generate_polygon_points(self):
        width = sum(self.width_list) + 6*len(self.width_list)
        height = max(self.height_list) + 6
        return [
            QPoint(0, 0),  # Top-left corner
            QPoint(10, 0),  # Start of the pit
            QPoint(10, 5),  # Bottom-left of pit
            QPoint(40, 5),  # Bottom-right of pit
            QPoint(40, 0),  # Exit from the pit
            QPoint(width, 0),  # Top-right corner
            QPoint(width, height),  # Bottom-right corner
            QPoint(40, height),  # Start of bulge
            QPoint(40, height + 5),  # Bottom-right of bulge
            QPoint(10, height + 5),  # Bottom-left of bulge
            QPoint(10, height),  # End of bulge
            QPoint(0, height)  # Bottom-left corner
        ]


    # def polygon_contains_point(self, point):
    #     # Check if a point is within the polygon's bounding rectangle
    #     # For a more accurate check, use the actual polygon points
    #     x, y = point.x(), point.y()
    #     points = self.generate_polygon_points()
    #     return QPolygon(points).containsPoint(point, Qt.WindingFill)
    #
    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.MouseButtonPress:
    #         pos = event.pos()
    #         # Check if click is within the polygon area
    #         if self.polygon_contains_point(pos):
    #             print("Polygon area clicked!")
    #             return True  # Event handled
    #         else:
    #             print("Not polygon clicked")
    #
    #         # Check if click is on any QLabel
    #         for widget in self.content_list:
    #             if isinstance(widget, QLabel) and widget.geometry().contains(pos):
    #                 print(f"{widget.text()} clicked!")
    #                 return True  # Event handled
    #             else:
    #                 print("wrong widget")
    #
    #         # Ignore clicks on other widgets
    #         return False  # Pass the event to other widgets
    #
    #     return super().eventFilter(source, event)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    test_json = [
        {"text": "Hello, World"},
        {"dropdown": ["hello", "bye", "this is a very long one"]},
        {"int_entry": "number typing?"},
        {"text": "test!"},
        {"text_entry": "text entry"}
    ]

    window = BlockBase(test_json)
    window.show()
    app.exec_()
