from PyQt5.QtWidgets import QMenu, QAction
from .layer_manager import *

class BlockContextMenu(QMenu):
	def __init__(self, parent, event):
		super().__init__()
		self.parent_block = parent

		layer_id = self.get_layer_by_pos(event.pos())

		self.actions_list = []

		if not self.parent_block.spawner:
			self.generate_actions(layer_id)
			self.actions_list.append(QAction("Delete block"))
			self.addAction(self.actions_list[-1])
			self.actions_list[-1].triggered.connect(self.parent_block.suicide)
			self.actions_list.append(QAction("Unsnap + Delete block"))
			self.addAction(self.actions_list[-1])
			self.actions_list[-1].triggered.connect(lambda: self.parent_block.suicide(True))
		elif self.parent_block.input_json["meta"] == 1:
			self.actions_list.append(QAction("Delete variable"))
			self.addAction(self.actions_list[-1])
			var_name = self.parent_block.input_json["internal_name"]
			var_manager = self.parent_block.workspace_view.var_manager
			self.actions_list[-1].triggered.connect(lambda: var_manager.delete_var_by_name(var_name))

		self.exec_(event.screenPos())

	def get_layer_by_pos(self, event_pos):
		clicked_y = event_pos.y()
		for idx, layer in enumerate(self.parent_block.layers_list):
			if layer.y_to_appear_at > clicked_y: return idx-1
		return idx

	def generate_actions(self, clicked_layer_id):
		clicked_layer = self.parent_block.layers_list[clicked_layer_id]
		if clicked_layer.layer_type == -2:
			self.actions_list.append(QAction("Hide this layer"))
			self.actions_list[-1].triggered.connect(lambda _, i=clicked_layer.layer_id: hide_optional_layer(self.parent_block, i))
			self.addAction(self.actions_list[-1])

		if clicked_layer.layer_type > 0:
			if self.parent_block.nonstatic_layers[clicked_layer.copy_from] > 1:
				self.actions_list.append(QAction("Delete this layer"))
				self.actions_list[-1].triggered.connect(lambda _, i=clicked_layer.layer_id: delete_dynamic_layer(self.parent_block, i))
				self.addAction(self.actions_list[-1])
			self.actions_list.append(QAction("Copy this layer"))
			self.actions_list[-1].triggered.connect(lambda _, i=clicked_layer.layer_id: make_new_dynamic_layer(self.parent_block, i))
			self.addAction(self.actions_list[-1])

		for temp_layer in self.parent_block.layers_list:
			if temp_layer.layer_type == -2 and temp_layer.hidden:
				self.actions_list.append(QAction(f"Show layer {temp_layer.layer_id}"))
				self.actions_list[-1].triggered.connect(lambda _, i=temp_layer.layer_id: show_optional_layer(self.parent_block, i))
				self.addAction(self.actions_list[-1])