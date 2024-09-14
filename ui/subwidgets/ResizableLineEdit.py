import sys
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression


class ResizableLineEdit(QLineEdit):
    def __init__(self, placeholder="", int_entry=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setPlaceholderText(placeholder)
        self.setTextMargins(2, 0, 0, 0)  # Adds 2px padding on the left
        if int_entry:
            self.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #5c5c5c;
                    border-radius: 10px;
                }
            """)
            pattern = r'^[0-9.-]*$'  # Only digits, hyphen, and dot
            regex = QRegularExpression(pattern)
            validator = QRegularExpressionValidator(regex, self)
            self.setValidator(validator)
        else:
            self.setStyleSheet("""
                QLineEdit {
                    border: 2px solid #5c5c5c;
                }
            """)

        # Adjust size based on placeholder text immediately
        self.adjust_width()

        # Connect the textChanged signal to the resize function
        self.textChanged.connect(self.adjust_width)

    def adjust_width(self):
        # Get the width of the text or placeholder text
        text_width = self.fontMetrics().width(self.text() or self.placeholderText())

        # Add some padding (optional, to make sure text is not too close to edges)
        padding = 10 + 2

        # Resize the widget to fit the text width
        self.setFixedWidth(max(text_width + padding, 24))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the resizing QLineEdit
    line_edit = ResizableLineEdit(placeholder="Type")
    line_edit.show()

    sys.exit(app.exec_())
