from PyQt5.QtWidgets import QGraphicsProxyWidget
from PyQt5.QtCore import pyqtSignal


class EntryManager(QGraphicsProxyWidget):
	sizeChanged = pyqtSignal()

	def __init__(self, parent, entry_type, placeholder_text):
		super().__init__(parent)
		self.snapped_block = None
		self.entry_type = entry_type
		self.allow_variable_snap_in = False
		self.allow_operator_snap_in = False
		self.allow_bottom_snap = False
		if entry_type < 2:
			from ui.subwidgets.ResizableLineEdit import ResizableLineEdit
			self.entry = ResizableLineEdit(placeholder_text, int_entry=entry_type)
			self.allow_variable_snap_in = True
		elif entry_type == 2:
			from ui.subwidgets.BoolLineEdit import BoolLineEdit
			self.entry = BoolLineEdit(placeholder_text)
			self.allow_operator_snap_in = True
		elif entry_type == 3:
			from ui.subwidgets.ResizableDropdown import ResizableDropdown
			self.entry = ResizableDropdown(options=placeholder_text)
			self.allow_variable_snap_in = True

		self.setWidget(self.entry)
		self.widget().size_changed.connect(self.sizeChanged.emit)

	def snap_in(self, widget_to_snap):
		self.snapped_block = widget_to_snap
		self.sizeChanged.emit()
		self.setWidget(None)
		# hide self.entry without making snapped_block invisible

	def show_line(self):
		self.entry.set_border_width(4, True)

	def clear_line(self):
		self.entry.set_border_width(2, False)

	def get_width(self):
		if not self.snapped_block:
			return self.boundingRect().width()
		return self.snapped_block.boundingRect().width()

	def get_height(self):
		if not self.snapped_block:
			return self.boundingRect().height()
		return self.snapped_block.boundingRect().height()

	def unsnap(self):
		self.snapped_block = None
		self.sizeChanged.emit()
		self.setWidget(self.entry)
