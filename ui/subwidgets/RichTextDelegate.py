from PyQt5.QtGui import QTextDocument, QPen, QColor
from PyQt5.QtWidgets import QStyledItemDelegate, QStyle


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
        doc.setHtml(text)  # Set HTML content
        doc.setTextWidth(option.rect.width())  # Adjust width

        # Render the text document
        painter.translate(option.rect.topLeft())
        doc.drawContents(painter)
        painter.restore()

    def sizeHint(self, option, index):
        doc = QTextDocument()
        doc.setHtml(index.data())
        return doc.size().toSize()
