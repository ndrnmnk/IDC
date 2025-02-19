from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression, Qt, pyqtSignal
from backend.config_manager import ConfigManager


class ResizableLineEdit(QLineEdit):
    size_changed = pyqtSignal()

    def __init__(self, placeholder="", int_entry=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(22)
        self.setPlaceholderText(placeholder)
        self.setTextMargins(2, 0, 0, 0)
        self.border_width = 2
        self.setAttribute(Qt.WA_TranslucentBackground)
        bg = ConfigManager().get_config("styles")["text_field_bg"]
        # bg = "#ffffff"
        self.setStyleSheet(f"""
            QToolTip {{ border-radius: 0px; }}
            QLineEdit {{
                background-color: {bg};
                border: 2px solid #000000;
            }}
        """)
        if int_entry:
            self.setToolTip("Number entry")
            self.setStyleSheet(self.styleSheet() + """border-radius: 10px;""")
            pattern = r'^[0-9.-]*$'  # Only digits, hyphen, and dot
            regex = QRegularExpression(pattern)
            validator = QRegularExpressionValidator(regex, self)
            self.setValidator(validator)
        else:
            self.setToolTip("String entry")

        # Adjust size based on placeholder text immediately
        self.adjust_width()

        # Connect the textChanged signal to the resize function
        self.textChanged.connect(self.adjust_width)

    def adjust_width(self):
        # Get the width of the text or placeholder text
        text_width = self.fontMetrics().width(self.text() or self.placeholderText())

        padding = 10 + self.border_width

        # Resize the widget to fit the text width
        self.setFixedWidth(max(text_width + padding, 24))
        self.size_changed.emit()

    def set_border_width(self, width=2, use_preview_color=False):
        self.border_width = width
        current_style = self.styleSheet()
        if use_preview_color:
            border_color = ConfigManager().get_config("styles")["preview_line_color"]
        else:
            border_color = "#000000"
        updated_style = f"border: {width}px solid {border_color};"
        # Replace existing border style or append the new one
        if "border:" in current_style:
            new_style = "\n".join([
                line if not line.strip().startswith("border:") else updated_style
                for line in current_style.splitlines()
            ])
        else:
            new_style = current_style + updated_style
        self.setStyleSheet(new_style)
