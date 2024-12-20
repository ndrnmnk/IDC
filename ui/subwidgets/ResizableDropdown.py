from PyQt5.QtWidgets import QComboBox, QStyle
from PyQt5.QtGui import QFontMetrics


class ResizableDropdown(QComboBox):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItems(options)

        # Update the width dynamically when the selection changes
        self.currentIndexChanged.connect(self.adjust_width)

        # Adjust the width initially
        self.adjust_width()

    def adjust_width(self):
        # Get the current text of the QComboBox
        current_text = self.currentText()

        # Calculate the text width using font metrics
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.horizontalAdvance(current_text)

        # Get style-dependent padding
        style = self.style()
        padding = style.pixelMetric(QStyle.PM_ComboBoxFrameWidth)

        # Update the width dynamically
        self.setFixedWidth(text_width + padding + 10)  # Add an extra margin if needed

    def sizeHint(self):
        # Override sizeHint to respect the style's preferred size
        hint = super().sizeHint()
        hint.setWidth(self.width())  # Maintain calculated width
        return hint
