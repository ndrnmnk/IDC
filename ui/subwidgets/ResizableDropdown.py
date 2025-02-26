from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import pyqtSignal
from backend.config_manager import ConfigManager


class ResizableDropdown(QComboBox):
    size_changed = pyqtSignal()

    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItems(options)
        self.setFixedHeight(24)
        self.font_metrics = QFontMetrics(self.font())
        bg = ConfigManager().get_config()["styles"]["text_field_bg"]
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {bg};
                border: 2px solid #000000;
                border-radius: 2px;
            }}
            QComboBox::drop-down {{
                background-color: "#0000ff";
            }}
        """)

        # Update the width dynamically when the selection changes
        self.currentIndexChanged.connect(self.adjust_width)

        # Adjust the width initially
        self.adjust_width()

    def adjust_width(self):
        # Get the current text of the QComboBox
        current_text = self.currentText()
        text_width = self.font_metrics.horizontalAdvance(current_text)
        self.setFixedWidth(text_width + 28)
        self.size_changed.emit()

    def set_border_width(self, width=2, use_preview_color=False):
        current_style = self.styleSheet()
        if use_preview_color:
            border_color = ConfigManager().get_config()["styles"]["snapline_color"]
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
