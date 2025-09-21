from PyQt5.QtWidgets import QGraphicsView

from backend.SpriteManager import SpriteManager
# from ui.widgets.Block import Block
from ui.block import Block
from backend.BlockMenuManager import BlockMenuManager
from backend.VariableManager import VariableManager
from ui.subwidgets.CodingScene import CodingScene
from backend.config_manager import ConfigManager


class WorkspaceView(QGraphicsView):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent
		self.setScene(CodingScene(self))
		self.centerOn(0, 0)

		self.block_list = []

		self.block_manager = BlockMenuManager(self)
		self.var_manager = VariableManager(self)
		self.sprite_manager = SpriteManager(self)

		self.scene().menu.view_height = self.viewport().height()
		self.on_new_category(self.block_manager.current_category)


	@staticmethod
	def complete_block_json(base, category, internal_name, identifier, pos, meta=None):
		if not meta:
			meta = 2 if any(item["type"] != 0 for item in base["data"]) else 0
		res = base
		res["category"] = category
		res["internal_name"] = internal_name
		if identifier:
			res["identifier"] = identifier
		res["meta"] = meta
		res["pos"] = pos
		return res

	@staticmethod
	def generate_variable_block_json(name, vtype):
		shape = 3 if vtype == "bool" else 4
		return {"shape": shape, "returns": vtype, "data": [{"type": 0, "data": [{"text": name}]}]}

	def add_block(self, block_json, spawner):
		block = Block(self, block_json, spawner)
		self.scene().addItem(block)
		block.setPos(*block_json["pos"])
		if spawner:
			self.block_manager.block_list.append(block)
			block.setParentItem(self.scene().menu)
			return block.boundingRect().height()
		else:
			self.block_list.append(block)
			return block

	def check_block_for_deletion(self, caller):
		if caller.pos().x() + 20 < self.scene().menu.sceneBoundingRect().right():
			caller.suicide()

	def on_new_category(self, category):
		self.block_manager.clear_menu()
		# load new category and resize scrollbar
		y_offset = self.block_manager.load_menu(category)
		self.scene().on_new_category(int(y_offset))

	def scrollContentsBy(self, dx, dy):
		# Default scroll behaviour + reposition menu so it remains visible
		super().scrollContentsBy(dx, dy)
		self.scene().update_menu_pos()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self.scene().on_view_resize()

	def get_project_data(self):
		self.sprite_manager.save_sprite_data()
		res = self.sprite_manager.all_sprite_code
		return res

	def load_sprite(self, sprite_name):
		self.sprite_manager.show_sprite(sprite_name)

	def load_block(self, identifier, sprite_json, parent_block=None, parent_idx=None, to=0):
		block_json = sprite_json["code"][identifier]
		meta = 1 if block_json["internal_name"].startswith(" ") else None
		if meta == 1:
			vname = block_json["internal_name"][5:]
			vtype = self.sprite_manager.all_sprite_code["vars"][vname] if block_json["internal_name"].startswith(" V") else sprite_json["vars"][vname]
			new_block_json = self.generate_variable_block_json(vname, vtype)
		else:
			new_block_json = ConfigManager().get_blocks()[block_json["category"]][block_json["internal_name"]]

		new_block_json = self.complete_block_json(new_block_json, block_json["category"], block_json["internal_name"], identifier, block_json["pos"], meta)
		block = self.add_block(new_block_json, False)

		# add nonstatic layers
		nonstatic_json = block_json.get("nonstatic") or []
		block.nonstatic_layers = nonstatic_json
		for idx, layer in enumerate(nonstatic_json):
			if not layer: continue
			for i in range(layer["amount"]):
				block.copy_layer(idx, True)

		# load children
		for idx, child_block_id in enumerate(block_json["snaps"]):
			self.try_loading_block(child_block_id, sprite_json, block, idx, 0)
		for idx, item in enumerate(block_json["content"]):
			self.try_loading_block(item[1], sprite_json, block, idx, 1)
		if parent_block:
			block.snap_candidate = parent_block.snap_line_list[parent_idx] if to == 0 else parent_block.get_entry_list()[parent_idx]
			block.try_to_snap()

		# fill text fields
		entry_list = block.get_entry_list()
		for i, var in enumerate(block_json["content"]):
			entry_list[i].set_text(var[0])

	def try_loading_block(self, child_block_id, sprite_json, block, idx, to):
		# if to == 0, snap to a SnapLine, else - to EntryManager
		if child_block_id:
			try:
				self.load_block(child_block_id, sprite_json, block, idx, to)
			except Exception as e: print(f"Couldn't load block: {e}")
