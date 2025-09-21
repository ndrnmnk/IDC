from PyQt5.QtWidgets import QGraphicsProxyWidget
from PyQt5.QtCore import pyqtSignal


class EntryManager(QGraphicsProxyWidget):
	sizeChanged = pyqtSignal()

	def __init__(self, parent, allowed_types, placeholder_text=" "):
		super().__init__(parent)
		self.snapped_block = None
		self.allowed_types = allowed_types
		self.entry_type = 0
		if allowed_types == ["bool"]:
			from ui.subwidgets.BoolLineEdit import BoolLineEdit
			self.entry = BoolLineEdit(placeholder_text)
		elif allowed_types == [" dropdown"]:
			self.entry_type = 1
			from ui.subwidgets.ResizableDropdown import ResizableDropdown
			self.entry = ResizableDropdown(options=placeholder_text)
		elif allowed_types == [" block"]:
			self.entry_type = 2
			from ui.subwidgets.BlockEntry import BlockEntry
			self.entry = BlockEntry()
		else:
			from ui.subwidgets.ResizableLineEdit import ResizableLineEdit
			if "str" in allowed_types or "all" in allowed_types: shape = "str"
			elif "int" in allowed_types or "float" in allowed_types: shape = "int"
			else: shape = "custom"
			self.entry = ResizableLineEdit(placeholder_text, shape)

			if " notype" in allowed_types:  # causes block shape 5 to get stuck
				self.entry.setReadOnly(True)
		tt = ", ".join(self.allowed_types)
		self.entry.setToolTip("Accepts " + tt)

		self.setWidget(self.entry)
		self.widget().size_changed.connect(self.sizeChanged.emit)

	def get_text(self):
		if self.entry_type == 2: return ""
		if self.entry_type == 1: return self.entry.currentText()
		else: return self.entry.text()

	def set_text(self, text):
		if self.entry_type == 3:
			self.entry.setCurrentText(text)
		elif self.entry_type == 4:
			return
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

	def check_block(self, block):
		shape_id = block.shape_id
		if self.snapped_block: return False

		if shape_id in (0, 1, 5):
			if len(block.snap_line_list) < 2:
				if not block.snap_line_list: pass
				elif not block.snap_line_list[0].snapped_block: pass
				else: return False
			else: return False

		if shape_id in (0, 1):
			return " block" in self.allowed_types
		else:
			if block.return_type in self.allowed_types or "all" in self.allowed_types \
					or (shape_id == 5 and " block" in self.allowed_types):
				return True
			return False
