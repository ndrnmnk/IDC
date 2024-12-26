from PyQt5.QtGui import QTextDocument, QPen, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle
from backend.config_manager import ConfigManager


class RichTextDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if option.state & QStyle.State_Selected:
            pen = QPen(QColor("black"), 2)
            painter.setPen(pen)
            rect = option.rect
            painter.drawRect(rect)

        painter.save()
        text = index.data()
        doc = QTextDocument()
        doc.setDefaultStyleSheet(f"body {{ color: {ConfigManager().get_config('styles')['text_color']}; }}")  # Set default text color
        doc.setHtml(f"<body>{text}</body>")  # Wrap content in <body>
        doc.setTextWidth(option.rect.width())  # Adjust width

        # Render the text document
        painter.translate(option.rect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        doc = QTextDocument()
        # doc.setDefaultStyleSheet("body { color: #888888; }")
        # doc.setHtml(f"<body>{index.data()}</body>")
        return doc.size().toSize()
