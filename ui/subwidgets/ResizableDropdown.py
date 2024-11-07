from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFontMetrics


class ResizableDropdown(QComboBox):
	def __init__(self, options,  *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.addItems(options)

		# Connect signal to handle changes in selection
		self.currentIndexChanged.connect(self.adjust_width)

		# Adjust width initially for the first item
		self.adjust_width()

	def adjust_width(self):
		# Get current text of the QComboBox
		current_text = self.currentText()

		# Get font metrics for the QComboBox font
		font_metrics = QFontMetrics(self.font())

		# Calculate the width
		text_width = font_metrics.horizontalAdvance(current_text)

		padding = 32

		# Set the width of the QComboBox
		self.setFixedWidth(text_width + padding)


if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	app = QApplication(sys.argv)
	window = ResizableDropdown(["Short", "A very long option", "Medium length"])
	window.show()
	app.exec_()
