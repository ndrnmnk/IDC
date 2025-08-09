from ui.windows.VariableDelWindow import VariableDelWindow

class VariableManager:
	def __init__(self, workspace_view):
		self.wv = workspace_view
		self.meta_dict = {}
		self.global_vars = {}
		self.local_vars = {}

	def add_var(self, vname, vtype, sprite):
		self.meta_dict[vname] = {}
		self.meta_dict[vname]["type"] = vtype
		self.meta_dict[vname]["at"] = sprite
		if sprite is not None:
			if sprite not in self.local_vars:
				self.local_vars[sprite] = {}
			self.local_vars[sprite][vname] = set()
			self.wv.sprite_manager.all_sprite_code[sprite]["vars"][vname] = vtype
		else:
			self.global_vars[vname] = {}
			self.wv.sprite_manager.all_sprite_code["vars"][vname] = vtype

	def delete_var(self, vname, sprite):
		if sprite is not None:
			# if no usages, delete
			if not self.local_vars[sprite][vname]:
				del self.local_vars[sprite][vname]
				del self.meta_dict[vname]
				del self.wv.sprite_manager.all_sprite_code[sprite]["vars"][vname]
			else:
				VariableDelWindow(self, vname, [0, 1, vname, sprite])
		else:
			if not self.global_vars[vname]:
				del self.global_vars[vname]
				del self.meta_dict[vname]
				del self.wv.sprite_manager.all_sprite_code["vars"][vname]
			else:
				VariableDelWindow(self, vname, [0, 0, vname, sprite])

	def _delete_var_and_ref(self, vname, sprite):
		if sprite is not None:
			for item in self.local_vars[sprite][vname]:
				del self.wv.sprite_manager.all_sprite_code[sprite]["code"][item]

			del self.local_vars[sprite][vname]
			del self.meta_dict[vname]
			del self.wv.sprite_manager.all_sprite_code[sprite]["vars"][vname]
		else:
			for sprite in self.global_vars[vname]:
				for item in self.global_vars[vname][sprite]:
					del self.wv.sprite_manager.all_sprite_code[sprite]["code"][item]

			del self.global_vars[vname]
			del self.meta_dict[vname]
			del self.wv.sprite_manager.all_sprite_code["vars"][vname]

		self.wv.sprite_manager.save_sprite_data()
		self.wv.sprite_manager.show_sprite(self.wv.sprite_manager.current_sprite)
		self.wv.on_new_category("Variables")

	def register_usage(self, caller):
		name = caller.input_json["internal_name"]
		uuid = caller.input_json["identifier"]
		is_global = name.startswith(" V")
		name = name[5:]
		sprite = self.wv.sprite_manager.current_sprite

		if not is_global:
			self.local_vars[sprite][name].add(uuid)
		else:
			if sprite not in self.global_vars[name]:
				self.global_vars[name][sprite] = set()
			self.global_vars[name][sprite].add(uuid)

	def unreg_usage(self, name, uuid, sprite):
		if name in self.global_vars:
			self.global_vars[name][sprite].remove(uuid)
		else:
			self.local_vars[sprite][name].remove(uuid)

	def delete_var_by_name(self, internal_name):
		self.wv.sprite_manager.save_sprite_data()
		vname = internal_name[5:]
		sprite = self.wv.sprite_manager.current_sprite if internal_name.startswith(" v") else None
		self.delete_var(vname, sprite)
		self.wv.on_new_category("Variables")

	def on_load_project(self):
		# pull data from sprite manager
		all_sprite_code = self.wv.sprite_manager.all_sprite_code
		for vname in all_sprite_code["vars"]:
			self.global_vars[vname] = {}
			self.meta_dict[vname] = {"type": all_sprite_code["vars"][vname], "at": None}

		for sprite in all_sprite_code:
			self.local_vars[sprite] = {}
			if sprite == "vars": continue
			for vname in all_sprite_code[sprite]["vars"]:
				self.local_vars[sprite][vname] = set()
				self.meta_dict[vname] = {"type": all_sprite_code[sprite]["vars"][vname], "at": sprite}

		print(self.local_vars)

