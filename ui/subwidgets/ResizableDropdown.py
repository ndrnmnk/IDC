from PyQt5.QtWidgets import QComboBox, QStyleFactory
from PyQt5.QtGui import QFontMetrics


class ResizableDropdown(QComboBox):
    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyle(QStyleFactory.create("Fusion"))
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
        padding = 32

        # Update the width
        self.setFixedWidth(text_width + padding)

    def sizeHint(self):
        # Override sizeHint to respect the style's preferred size
        hint = super().sizeHint()
        hint.setWidth(self.width())  # Maintain calculated width an
        return hint