from PyQt5.QtWidgets import QGraphicsProxyWidget
from PyQt5.QtCore import pyqtSignal


class EntryManager(QGraphicsProxyWidget):
	sizeChanged = pyqtSignal()

	def __init__(self, parent, entry_type, placeholder_text=" "):
		super().__init__(parent)
		self.snapped_block = None
		self.entry_type = entry_type
		self.allowed_snaps = [0, 0]  # bool snap, variable snap
		if entry_type < 2:
			from ui.subwidgets.ResizableLineEdit import ResizableLineEdit
			self.entry = ResizableLineEdit(placeholder_text, int_entry=entry_type)
			self.allow_variable_snap_in = True
			self.allowed_snaps = [1, 1]
		elif entry_type == 2:
			from ui.subwidgets.BoolLineEdit import BoolLineEdit
			self.entry = BoolLineEdit(placeholder_text)
			self.allowed_snaps = [1, 0]
		elif entry_type == 3:
			from ui.subwidgets.ResizableDropdown import ResizableDropdown
			self.entry = ResizableDropdown(options=placeholder_text)
			self.allowed_snaps = [0, 0]

		self.setWidget(self.entry)
		self.widget().size_changed.connect(self.sizeChanged.emit)

	def get_text(self):
		if self.entry_type == 3:
			return self.entry.currentText()
		else:
			return self.entry.text()

	def set_text(self, text):
		if self.entry_type == 3:
			self.entry.setCurrentText(text)
		else:
			self.entry.setText(text)

	def snap_in(self, widget_to_snap):
		self.snapped_block = widget_to_snap
		self.snapped_block.sizeChanged.connect(self.sizeChanged.emit)
		self.setWidget(None)
		self.sizeChanged.emit()

	def show_line(self):
		self.entry.set_border_width(4, True)

	def clear_line(self):
		self.entry.set_border_width(2, False)

	def get_width(self):
		if not self.snapped_block:
			return self.entry.width()
		return self.snapped_block.boundingRect().width()

	def get_height(self):
		if not self.snapped_block:
			return self.entry.height()
		return self.snapped_block.boundingRect().height() + 4

	def unsnap(self):
		self.snapped_block.disconnect()
		self.snapped_block = None
		self.sizeChanged.emit()
		self.setWidget(self.entry)
