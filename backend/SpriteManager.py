

class SpriteManager:
	def __init__(self, wv):
		self.wv = wv
		self.current_sprite = "Main"
		self.all_sprite_code = {"vars": {}}
		self.show_sprite(self.current_sprite)

	def _check_sprite_exists(self, sprite_name):
		if sprite_name not in self.all_sprite_code:
			self.all_sprite_code[sprite_name] = {"code": {}, "vars": {}, "roots": []}


	def change_current_sprite(self, new_sprite):
		# convert new_sprite to str
		new_sprite = new_sprite.text(0)
		self.save_sprite_data()
		self.show_sprite(new_sprite)

	def show_sprite(self, sprite):
		self._check_sprite_exists(sprite)
		sprite_json = self.all_sprite_code[sprite]
		self.current_sprite = sprite

		for block in self.wv.block_list[:]:
			block.suicide(True)

		try:
			for identifier in sprite_json["roots"]:
				self.wv.load_block(identifier, sprite_json)
		except KeyError:
			pass
		self.wv.on_new_category(self.wv.block_manager.current_category)


	def save_sprite_data(self):
		code = {}
		roots = []
		for block in self.wv.block_list:
			block_json, identifier = block.get_content()
			code[identifier] = block_json
			if not block.snap:
				roots.append(block.input_json["identifier"])

		self.all_sprite_code[self.current_sprite]["code"] = code
		self.all_sprite_code[self.current_sprite]["roots"] = roots