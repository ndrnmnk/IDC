from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFontMetrics
from backend.config_manager import ConfigManager


class ResizableDropdown(QComboBox):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItems(options)
        self.setFixedHeight(24)
        self.font_metrics = QFontMetrics(self.font())
        bg = ConfigManager().get_config("styles")["text_field_bg"]
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {bg};
                border: 2px solid #000000;
                border-radius: 2px;
            }}
            QComboBox::drop-down {{
                border: 10px solid #0000ff;
                background-color: {bg};
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

    def sizeHint(self):
        # Override sizeHint to respect the style's preferred size
        hint = super().sizeHint()
        hint.setWidth(self.width())  # Maintain calculated width an
        return hint