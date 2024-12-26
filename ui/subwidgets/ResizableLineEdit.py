import sys
from PyQt5.QtWidgets import QApplication, QLineEdit
from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression
from backend.config_manager import ConfigManager


class ResizableLineEdit(QLineEdit):
	def __init__(self, placeholder="", int_entry=False, bool_entry=False, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setFixedHeight(22)
		self.setPlaceholderText(placeholder)
		self.setTextMargins(2, 0, 0, 0)
		bg = ConfigManager().get_config("styles")["text_field_bg"]
		self.setStyleSheet(f"""
			QToolTip {{ border-radius: 0px; }}
				background-color: {bg};
				border: 2px solid #000000;
		""")
		if int_entry:
			self.setToolTip("Number entry")
			self.setStyleSheet(self.styleSheet() + """border-radius: 10px;""")
			pattern = r'^[0-9.-]*$'  # Only digits, hyphen, and dot
			regex = QRegularExpression(pattern)
			validator = QRegularExpressionValidator(regex, self)
			self.setValidator(validator)
		elif bool_entry:
			self.setToolTip("Bool entry (1 or 0)")
			self.setStyleSheet(self.styleSheet() + """border-radius: 5px;""")
			self.setMaxLength(1)
			pattern = r'^[0|1]*$'  # Only 1 or 0
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
