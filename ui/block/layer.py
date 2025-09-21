from PyQt5.QtWidgets import QGraphicsTextItem as QTextItem
from PyQt5.QtGui import QFont

from ui.subwidgets.SnapLine import SnapLine
from ui.subwidgets.EntryManager import EntryManager

LTYPE_STATIC = -1    # regular layer
LTYPE_OPTIONAL = -2  # hidden by default, can be shown using right-click
LTYPE_STICKY = -3    # sticks to the layer below it; doesn't have a SnapLine
# every non-negative number means a layer is dynamic
# that number points to from which layer to copy input json

class BlockLayer:
	def __init__(self, pb, idx, ltype):
		self.parent_block = pb
		self.layer_id = idx
		self.layer_type = ltype

		self.content_list = []
		self.width_list = []
		self.height_list = []
		self.snapped_block_h = 0
		self.snap_line = None

		self.copy_from = self.layer_id if self.layer_type < 0 else self.layer_type

		self.hidden = ltype == LTYPE_OPTIONAL
		self.y_to_appear_at = 0

	def populate(self, ty=None):
		if ty is not None: self.y_to_appear_at = ty + 1
		if self.hidden: return

		input_json = self.parent_block.input_json["data"][self.copy_from]["data"]
		tx = 2
		for idx, json_member in enumerate(input_json):
			if "text" in json_member:
				temp = QTextItem(json_member["text"], parent=self.parent_block)
				temp.setFont(QFont("Arial", 12))
				self.add_content_item(temp, tx, self.y_to_appear_at)
			elif "entry" in json_member:
				self.handle_entry_item(idx, json_member["types"], json_member["entry"], tx, self.y_to_appear_at+2)

			tx += self.width_list[idx]

	def depopulate(self):
		# is used ONLY when the user deletes an optional layer
		self.hidden = True

		self.width_list = []
		self.height_list = []

		for widget in self.content_list: widget.deleteLater()
		if self.snap_line:
			if self.snap_line.snapped_block: self.snap_line.snapped_block.unsnap()
			self.snap_line.deleteLater()
			self.snap_line = None
		self.content_list = []
		self.snapped_block_h = 0

	def repopulate(self, caller_id):
		self.width_list[caller_id] = self.content_list[caller_id].get_width()
		self.height_list[caller_id] = self.content_list[caller_id].get_height()
		tx = 2 + sum(self.width_list[:caller_id+1])
		for item in self.content_list[caller_id+1:]:
			item.setX(tx)
			tx += item.boundingRect().width()

		self.parent_block.repopulate(self.layer_id)

	def on_snapline_size_changed(self):
		self.snapped_block_h = self.snap_line.get_height()
		self.parent_block.repopulate(self.layer_id)

	def add_snap_line(self, pos, width):
		if self.layer_type is LTYPE_STICKY or self.hidden: return
		self.snap_line = SnapLine(pos, width, self.parent_block)
		self.snap_line.sizeChanged.connect(self.on_snapline_size_changed)
		self.parent_block.snap_line_list.append(self.snap_line)

	def move_by(self, ty, only_snapline=False):
		if not only_snapline: self.y_to_appear_at += ty
		if self.hidden: return
		if not only_snapline:
			for widget in self.content_list:
				widget.moveBy(0, ty)
		if self.snap_line:
			self.snap_line.moveBy(0, ty)

	def generate_copy(self):
		return BlockLayer(self.parent_block, self.layer_id+1, self.layer_type)

	def add_content_item(self, content, tx, ty, update_signal=None):
		self.content_list.append(content)
		content.setPos(tx, ty)
		self.width_list.append(content.boundingRect().width())
		self.height_list.append(content.boundingRect().height())
		if update_signal:
			content.sizeChanged.connect(update_signal)

	def handle_entry_item(self, idx, entry_type, entry_data, tx, ty):
		content = EntryManager(self.parent_block, entry_type, entry_data)
		self.add_content_item(content, tx, ty, lambda caller_idx=idx: self.repopulate(caller_idx))

	def get_width(self):
		if self.hidden: return 0
		return sum(self.width_list) + 2*len(self.width_list)

	def get_height(self):
		if self.hidden: return 0
		return max(self.height_list)

	def get_snapped_block_height(self):
		fake_h = 0 if (self.layer_type is LTYPE_STICKY) or self.hidden else 18
		return self.snapped_block_h or fake_h

	def get_entry_list(self):
		return [item for item in self.content_list if isinstance(item, EntryManager)]
