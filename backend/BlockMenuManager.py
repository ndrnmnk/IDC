from backend.config_manager import ConfigManager
from ui.subwidgets.NewVariableBtn import NewVariableBtn
from ui.subwidgets.NewFunctionBtn import NewFunctionBtn


class BlockMenuManager:
	def __init__(self, workspace_view):
		self.current_category = "Basic"
		self.block_list = []
		self.wv = workspace_view

	def load_menu(self, category):
		self.current_category = category
		# get blocks to load
		menu_blocks_list = ConfigManager().get_blocks()[category]

		# get a starting position
		y_offset = int(self.wv.scene().selector.boundingRect().height()) + 10
		# populate
		for key in menu_blocks_list:
			block_json = self.wv.complete_block_json(menu_blocks_list[key], category, key, None, [10, y_offset])
			y_offset += self.wv.add_block(block_json, True) + 20

		if category == "Variables":
			y_offset = self._load_variables(self.wv.sprite_manager.all_sprite_code["vars"], y_offset, True)
			y_offset = self._load_variables(self.wv.sprite_manager.all_sprite_code[self.wv.sprite_manager.current_sprite]["vars"], y_offset)
			y_offset = self._add_new_variable_btn(y_offset)
		elif category == "Functions":
			y_offset = self._add_new_function_btn(y_offset)

		return y_offset

	def _load_variables(self, input_json, y_offset, is_global=False):
		for vname in input_json:
			vtype = input_json[vname]
			block_json = self.wv.generate_variable_block_json(vname, vtype)
			vname = f" VAR_{vname}" if is_global else f" var_{vname}"
			block_json = self.wv.complete_block_json(block_json, "Variables", vname, None, [10, y_offset], 1)
			y_offset += self.wv.add_block(block_json, True) + 20

		return y_offset

	def _add_new_variable_btn(self, y_offset):
		btn = NewVariableBtn(self.wv)
		btn.setPos(10, y_offset)
		y_offset += btn.boundingRect().height() + 10
		self.block_list.append(btn)
		return y_offset

	def _add_new_function_btn(self, y_offset):
		btn = NewFunctionBtn(self.wv)
		btn.setPos(10, y_offset)
		y_offset += btn.boundingRect().height() + 10
		self.block_list.append(btn)
		return y_offset

	def clear_menu(self):
		for block in self.block_list[:]:
			block.suicide()