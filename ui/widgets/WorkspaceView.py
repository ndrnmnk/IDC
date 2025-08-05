from PyQt5.QtWidgets import QGraphicsView

from ui.widgets.Block import Block
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

		self.current_sprite = "Main"
		self.all_sprites_code = {"vars": {}}

		self.block_manager = BlockMenuManager(self)
		self.var_manager = VariableManager(self)

		self.block_list = []

		self.scene().menu.view_height = self.viewport().height()
		self.on_new_category(self.block_manager.current_category)


	@staticmethod
	def complete_block_json(base, category, internal_name, identifier, pos, meta=None):
		if not meta:
			meta = 2 if "dynamic_layer" in base else 0
		res = base
		res["category"] = category
		res["internal_name"] = internal_name
		res["identifier"] = identifier
		res["meta"] = meta
		res["pos"] = pos
		return res

	@staticmethod
	def generate_variable_block_json(name, vtype):
		shape = 3 if vtype == "Boolean" else 4
		return {"shape": shape, "tooltip": vtype, "data": [[{"text": name}]]}

	def add_block(self, block_json, spawner):
		if spawner:
			block = Block(self, block_json, True)
			self.block_manager.block_list.append(block)
			self.scene().addItem(block)
			block.setPos(*block_json["pos"])
			block.setParentItem(self.scene().menu)
			return block.boundingRect().height()
		else:
			self.block_list.append(Block(self, block_json, False))
			self.scene().addItem(self.block_list[-1])
			self.block_list[-1].setPos(*block_json["pos"])
			return self.block_list[-1]

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

	def get_sprite_data(self):
		code = {}
		roots = []
		for block in self.block_list:
			block_json, identifier = block.get_content()
			code[identifier] = block_json
			if not block.snap:
				roots.append(block.input_json["identifier"])

		return code, roots

	def get_project_data(self):
		res = self.all_sprites_code
		res[self.current_sprite]["code"], res[self.current_sprite]["roots"] = self.get_sprite_data()
		return res

	def load_sprite(self, sprite_json):
		try:
			for identifier in sprite_json["roots"]:
				self.load_block(identifier, sprite_json)
		except KeyError:
			return
		self.on_new_category(self.block_manager.current_category)

	def load_block(self, identifier, sprite_json, parent_block=None, parent_idx=None):
		json_item = sprite_json["code"][identifier]
		# create a new json for a block
		if json_item["internal_name"].startswith(" "):
			vname = json_item["internal_name"][5:]
			if json_item["internal_name"].startswith(" V"):  # " VAR_" for global variables, " var_" for local
				vtype = self.all_sprites_code["vars"][vname]
			else:
				vtype = sprite_json["vars"][vname]
			new_json = self.generate_variable_block_json(vname, vtype)
			meta = 1
		else:
			new_json = ConfigManager().get_blocks()[json_item["category"]][json_item["internal_name"]]
			meta = None
		new_json = self.complete_block_json(new_json, json_item["category"], json_item["internal_name"], identifier, json_item["pos"], meta)
		# create new block
		block = self.add_block(new_json, False)

		# add dynamic layers
		t = json_item.get("dynamic") or 0
		for i in range(t):
			block.copy_dynamic_layer()

		# load children
		for idx, child_block_id in enumerate(json_item["snaps"]):
			if child_block_id:
				try:
					self.load_block(child_block_id, sprite_json, block, idx)
				except:
					pass
		for idx, item in enumerate(json_item["content"]):
			if item[1]:
				try:
					self.load_block(item[1], sprite_json, block, idx)
				except:
					pass
		if parent_block:
			if new_json["shape"] in (0, 1):
				block.snap_candidate = parent_block.snap_line_list[parent_idx]
			if new_json["shape"] in (3, 4):
				block.snap_candidate = parent_block.get_entry_list()[parent_idx]
			block.try_to_snap()
		entry_list = block.get_entry_list()
		for i, var in enumerate(json_item["content"]):
			entry_list[i].set_text(var[0][0])

	def set_sprite(self, sl_item):
		sprite_name = sl_item.text(0)
		# save current code to self.all_sprites_code
		self.all_sprites_code[self.current_sprite]["code"], self.all_sprites_code[self.current_sprite]["roots"] = self.get_sprite_data()
		self.current_sprite = sprite_name
		# delete all previous block widgets
		for block in self.block_list[:]:
			block.suicide(True)
		# load new code into blocks
		self.load_sprite(self.all_sprites_code[sprite_name])
