def show_optional_layer(block, layer_id):
	target_layer = block.layers_list[layer_id]
	target_layer.hidden = False
	target_layer.populate()
	block.repopulate(layer_id)

	target_layer.add_snap_line(block.snappable_points[layer_id], max(block.width_list)-20, layer_id)

def hide_optional_layer(block, layer_id):
	block.layers_list[layer_id].depopulate()
	block.repopulate(layer_id)

def make_new_dynamic_layer(block, layer_id):
	"""Makes a new layer and inserts it below the layer_id one"""
	# get y pos for future layer
	y_new = block.layers_list[layer_id+1].y_to_appear_at
	# make a new layer
	temp_layer = block.layers_list[layer_id].generate_copy()
	block.layers_list.insert(layer_id + 1, temp_layer)
	temp_layer.populate(y_new)
	# edit block variables
	block.width_list.insert(layer_id+1, 0)
	block.height_list.insert(layer_id+1, 0)
	block.between_layers_height_list.insert(layer_id+1, 0)
	# change ids of other layers
	for layer in block.layers_list[layer_id+2:]:
		layer.layer_id += 1
	# adjust layout
	block.repopulate(layer_id+1)

	temp_layer.add_snap_line(block.snappable_points[layer_id+1], max(block.width_list)-20, layer_id+1)

def delete_dynamic_layer(block, layer_id):
	block.layers_list[layer_id].depopulate()
	# adjust block size
	block.repopulate(layer_id)
	# delete variables
	block.width_list.pop(layer_id)
	block.height_list.pop(layer_id)
	block.between_layers_height_list.pop(layer_id)
	block.layers_list.pop(layer_id)
	# change ids of other layers
	for layer in block.layers_list[layer_id:]:
		layer.layer_id -= 1

def find_layer_by_copy_from(block, target_copy_from, start_at=0):
	for layer in block.layers_list[start_at:]:
		if layer.copy_from == target_copy_from:
			return layer.layer_id


def load_nonstatic_json(block, nonstatic_json):
	last_processed_layer = 0  # to speed up search process
	for key in nonstatic_json:
		ikey = int(key)
		if block.input_json["data"][ikey]["type"] == -2:
			if nonstatic_json[key] == 1:
				layer_id = find_layer_by_copy_from(block, ikey, last_processed_layer)
				show_optional_layer(block, layer_id)
				last_processed_layer = layer_id
		else:
			if nonstatic_json[key] > 1:
				layer_id = find_layer_by_copy_from(block, ikey, last_processed_layer)
				for i in range(nonstatic_json[key]-1):
					make_new_dynamic_layer(block, layer_id)
				last_processed_layer = layer_id
