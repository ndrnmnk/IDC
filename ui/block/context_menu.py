from PyQt5.QtWidgets import QMenu, QAction

class BlockContextMenu(QMenu):
	def __init__(self, parent, pos):
		super().__init__()
		self.parent_block = parent

		for idx, layer in enumerate(parent.layers_list):
			# TODO: implement a list of QActions
			if layer.layer_type == -2:
				if layer.hidden:
					temp_action = QAction(f"Show layer {layer.layer_id}")
					temp_action.triggered.connect(lambda _, i=layer.layer_id: self.on_show_optional(i))
				else:
					temp_action = QAction(f"Hide layer {layer.layer_id}")
					temp_action.triggered.connect(lambda _, i=layer.layer_id: self.on_hide_optional(i))
				self.addAction(temp_action)
			elif layer.layer_type >= 0:
				templ_action = QAction(f"Add 1 more {layer.layer_id} layer")
				templ_action.triggered.connect(lambda _, i=layer.layer_id: self.on_new_dynamic(i))
				self.addAction(templ_action)
				templl_action = QAction(f"Delete {layer.layer_id} layer")
				templl_action.triggered.connect(lambda _, i=layer.layer_id: self.on_delete_dynamic(i))
				self.addAction(templl_action)

		self.exec_(pos)

	def on_show_optional(self, layer_id):
		target_layer = self.parent_block.layers_list[layer_id]
		target_layer.hidden = False
		target_layer.populate()
		self.parent_block.repopulate(layer_id)

		target_layer.add_snap_line(self.parent_block.snappable_points[layer_id], max(self.parent_block.width_list)-20)

	def on_hide_optional(self, layer_id):
		self.parent_block.layers_list[layer_id].depopulate()
		self.parent_block.repopulate(layer_id)

	def on_new_dynamic(self, layer_id):
		# get y pos
		y_new = self.parent_block.layers_list[layer_id+1].y_to_appear_at
		# make a new layer
		temp_layer = self.parent_block.layers_list[layer_id].generate_copy()
		self.parent_block.layers_list.insert(layer_id + 1, temp_layer)
		temp_layer.populate(y_new)
		# edit block variables
		self.parent_block.width_list.insert(layer_id+1, 0)
		self.parent_block.height_list.insert(layer_id+1, 0)
		self.parent_block.between_layers_height_list.insert(layer_id+1, 0)
		# change ids of other layers
		for layer in self.parent_block.layers_list[layer_id+2:]:
			layer.layer_id += 1
		# adjust layout
		self.parent_block.repopulate(layer_id+1)

		temp_layer.add_snap_line(self.parent_block.snappable_points[layer_id+1], max(self.parent_block.width_list)-20)

	def on_delete_dynamic(self, layer_id):
		self.parent_block.layers_list[layer_id].depopulate()
		# adjust block size
		self.parent_block.repopulate(layer_id)
		# delete variables
		self.parent_block.width_list.pop(layer_id)
		self.parent_block.height_list.pop(layer_id)
		self.parent_block.between_layers_height_list.pop(layer_id)
		self.parent_block.layers_list.pop(layer_id)
		# change ids of other layers
		for layer in self.parent_block.layers_list[layer_id:]:
			layer.layer_id -= 1