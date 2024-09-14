from ui.subwidgets.ResizableLineEdit import ResizableLineEdit
from ui.subwidgets.ResizableDropdown import ResizableDropdown
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPainter, QPolygon, QBrush, QColor
from PyQt5.QtCore import QPoint
import sys


class BlockBase(QWidget):
    def __init__(self, json_input, parent=None, color="#03fcf8", shape="basic"):
        super().__init__(parent)
        self.input = json_input
        self.margin = 4

        self.color = color
        self.block_width = 200
        self.block_height = 40
        self.content_y = int(self.block_height/2) - 10

        self.content = []
        self.width_list = []
        self.height_list = []
        self.populate_block()

    def populate_block(self):
        current_x = self.margin
        for idx, json_object in enumerate(self.input):
            if "text" in json_object:
                self.content.append(QLabel(json_object["text"], self))
                self.width_list.append(self.content[idx].sizeHint().width() + 4)
                self.height_list.append(self.content[idx].sizeHint().height())
                self.content[idx].move(current_x, self.content_y+2)
            elif "text_entry" in json_object:
                self.content.append(ResizableLineEdit(parent=self, placeholder=json_object["text_entry"], int_entry=False))
                self.content[idx].move(current_x, self.content_y)
                self.content[idx].textChanged.connect(lambda _, idx=idx: self.repopulate_block(idx))
                self.width_list.append(self.content[idx].width() + 4)
                self.height_list.append(self.content[idx].height())
            elif "int_entry" in json_object:
                self.content.append(ResizableLineEdit(parent=self, placeholder=json_object["int_entry"], int_entry=True))
                self.content[idx].move(current_x, self.content_y)
                self.content[idx].textChanged.connect(lambda _, idx=idx: self.repopulate_block(idx))
                self.width_list.append(self.content[idx].width() + 4)
                self.height_list.append(self.content[idx].height())
            elif "bool_entry" in json_object:
                print("no bool entry for now")
            elif "dropdown" in json_object:
                self.content.append(ResizableDropdown(parent=self, options=json_object["dropdown"]))
                self.content[idx].move(current_x, self.content_y)
                self.content[idx].currentIndexChanged.connect(lambda _, idx=idx: self.repopulate_block(idx))
                self.width_list.append(self.content[idx].width() + 4)
                self.height_list.append(self.content[idx].height())
            current_x += self.width_list[idx]
        self.block_width = self.margin*2 + current_x
        self.resize(self.block_width + 1, self.block_height + 6)

    def repopulate_block(self, idx_caller):
        self.width_list[idx_caller] = self.content[idx_caller].width() + 4
        self.height_list[idx_caller] = self.content[idx_caller].height()

        if self.block_height != max(self.height_list):
            self.block_height = max(self.height_list) + 10
            self.content_y = int(self.block_height / 2) - 10
            idx_caller = 0

        current_x = sum(self.width_list[:idx_caller]) + self.margin
        for idx, json_object in enumerate(self.input[idx_caller:], idx_caller):
            if "text" not in json_object:
                self.content[idx].move(current_x, self.content_y)
            else:
                self.content[idx].move(current_x, self.content_y+2)
            current_x += self.width_list[idx]

        self.block_width = current_x + self.margin*2
        self.resize(self.block_width + 1, self.block_height + 6)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        x = 0
        height = self.block_height
        y = 0
        width = self.block_width

        points = [
            QPoint(x, y),  # Top-left corner
            QPoint(x + 10, y),  # Start of the pit
            QPoint(x + 10, y + 5),  # Bottom-left of pit
            QPoint(x + 40, y + 5),  # Bottom-right of pit
            QPoint(x + 40, y),  # Exit from the pit
            QPoint(x + width, y),  # Top-right corner
            QPoint(x + width, y + height),  # Bottom-right corner
            QPoint(x + 40, y + height),  # Start of bulge
            QPoint(x + 40, y + height + 5),  # Bottom-right of bulge
            QPoint(x + 10, y + height + 5),  # Bottom-left of bulge
            QPoint(x + 10, y + height),  # End of bulge
            QPoint(x, y + height)  # Bottom-left corner
        ]
        painter.setBrush(QBrush(QColor(self.color)))
        polygon = QPolygon(points)
        painter.drawPolygon(polygon)


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
